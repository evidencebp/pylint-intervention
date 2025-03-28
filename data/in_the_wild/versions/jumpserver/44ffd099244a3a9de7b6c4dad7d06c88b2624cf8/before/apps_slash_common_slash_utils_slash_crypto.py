import base64
import logging
from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def process_key(key):
    """
    返回32 bytes 的key
    """
    if not isinstance(key, bytes):
        key = bytes(key, encoding='utf-8')

    if len(key) >= 32:
        return key[:32]

    return pad(key, 32)


class BaseCrypto:

    def encrypt(self, text):
        return base64.urlsafe_b64encode(
            self._encrypt(bytes(text, encoding='utf8'))
        ).decode('utf8')

    def _encrypt(self, data: bytes) -> bytes:
        raise NotImplementedError

    def decrypt(self, text):
        return self._decrypt(
            base64.urlsafe_b64decode(bytes(text, encoding='utf8'))
        ).decode('utf8')

    def _decrypt(self, data: bytes) -> bytes:
        raise NotImplementedError


class GMSM4EcbCrypto(BaseCrypto):
    def __init__(self, key):
        self.key = process_key(key)
        self.sm4_encryptor = CryptSM4()
        self.sm4_encryptor.set_key(self.key, SM4_ENCRYPT)

        self.sm4_decryptor = CryptSM4()
        self.sm4_decryptor.set_key(self.key, SM4_DECRYPT)

    def _encrypt(self, data: bytes) -> bytes:
        return self.sm4_encryptor.crypt_ecb(data)

    def _decrypt(self, data: bytes) -> bytes:
        return self.sm4_decryptor.crypt_ecb(data)


class AESCrypto:
    """
    AES
    除了MODE_SIV模式key长度为：32, 48, or 64,
    其余key长度为16, 24 or 32
    详细见AES内部文档
    CBC模式传入iv参数
    本例使用常用的ECB模式
    """

    def __init__(self, key):
        if len(key) > 32:
            key = key[:32]
        self.key = self.to_16(key)

    @staticmethod
    def to_16(key):
        """
        转为16倍数的bytes数据
        :param key:
        :return:
        """
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
        return key  # 返回bytes

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB)  # 初始化加密器

    def encrypt(self, text):
        aes = self.aes()
        return str(base64.encodebytes(aes.encrypt(self.to_16(text))),
                   encoding='utf8').replace('\n', '')  # 加密

    def decrypt(self, text):
        aes = self.aes()
        return str(aes.decrypt(base64.decodebytes(bytes(text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密


class AESCryptoGCM:
    """
    使用AES GCM模式
    """

    def __init__(self, key):
        self.key = process_key(key)

    def encrypt(self, text):
        """
        加密text，并将 header, nonce, tag (3*16 bytes, base64后变为 3*24 bytes)
        附在密文前。解密时要用到。
        """
        header = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_GCM)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(bytes(text, encoding='utf-8'))

        result = []
        for byte_data in (header, cipher.nonce, tag, ciphertext):
            result.append(base64.b64encode(byte_data).decode('utf-8'))

        return ''.join(result)

    def decrypt(self, text):
        """
        提取header, nonce, tag并解密text。
        """
        metadata = text[:72]
        header = base64.b64decode(metadata[:24])
        nonce = base64.b64decode(metadata[24:48])
        tag = base64.b64decode(metadata[48:])
        ciphertext = base64.b64decode(text[72:])

        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)

        cipher.update(header)
        plain_text_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        return plain_text_bytes.decode('utf-8')


def get_aes_crypto(key=None, mode='GCM'):
    if key is None:
        key = settings.SECRET_KEY
    if mode == 'ECB':
        a = AESCrypto(key)
    elif mode == 'GCM':
        a = AESCryptoGCM(key)
    return a


def get_gm_sm4_ecb_crypto(key=None):
    key = key or settings.SECRET_KEY
    return GMSM4EcbCrypto(key)


aes_ecb_crypto = get_aes_crypto(mode='ECB')
aes_crypto = get_aes_crypto(mode='GCM')
gm_sm4_ecb_crypto = get_gm_sm4_ecb_crypto()


class Crypto:
    cryptoes = {
        'aes_ecb': aes_ecb_crypto,
        'aes_gcm': aes_crypto,
        'aes': aes_crypto,
        'gm_sm4_ecb': gm_sm4_ecb_crypto,
        'gm': gm_sm4_ecb_crypto,
    }

    def __init__(self):
        cryptoes = self.__class__.cryptoes.copy()
        crypto = cryptoes.pop(settings.SECURITY_DATA_CRYPTO_ALGO, None)
        if crypto is None:
            raise ImproperlyConfigured(
                f'Crypto method not supported {settings.SECURITY_DATA_CRYPTO_ALGO}'
            )
        self.cryptoes = [crypto, *cryptoes.values()]

    @property
    def encryptor(self):
        return self.cryptoes[0]

    def encrypt(self, text):
        return self.encryptor.encrypt(text)

    def decrypt(self, text):
        for decryptor in self.cryptoes:
            try:
                origin_text = decryptor.decrypt(text)
                if origin_text:
                    # 有时不同算法解密不报错，但是返回空字符串
                    return origin_text
            except (TypeError, ValueError, UnicodeDecodeError, IndexError):
                continue


def gen_key_pair(length=1024):
    """ 生成加密key
    用于登录页面提交用户名/密码时，对密码进行加密（前端）/解密（后端）
    """
    random_generator = Random.new().read
    rsa = RSA.generate(length, random_generator)
    rsa_private_key = rsa.exportKey().decode()
    rsa_public_key = rsa.publickey().exportKey().decode()
    return rsa_private_key, rsa_public_key


def rsa_encrypt(message, rsa_public_key):
    """ 加密登录密码 """
    key = RSA.importKey(rsa_public_key)
    cipher = PKCS1_v1_5.new(key)
    cipher_text = base64.b64encode(cipher.encrypt(message.encode())).decode()
    return cipher_text


def rsa_decrypt(cipher_text, rsa_private_key=None):
    """ 解密登录密码 """
    if rsa_private_key is None:
        # rsa_private_key 为 None，可以能是API请求认证，不需要解密
        return cipher_text

    key = RSA.importKey(rsa_private_key)
    cipher = PKCS1_v1_5.new(key)
    cipher_decoded = base64.b64decode(cipher_text.encode())
    # Todo: 弄明白为何要以下这么写，https://xbuba.com/questions/57035263
    if len(cipher_decoded) == 127:
        hex_fixed = '00' + cipher_decoded.hex()
        cipher_decoded = base64.b16decode(hex_fixed.upper())
    message = cipher.decrypt(cipher_decoded, b'error').decode()
    return message


def rsa_decrypt_by_session_pkey(value):
    from jumpserver.utils import current_request
    private_key_name = settings.SESSION_RSA_PRIVATE_KEY_NAME
    private_key = current_request.session.get(private_key_name)

    if not private_key or not value:
        return value

    try:
        value = rsa_decrypt(value, private_key)
    except Exception as e:
        logging.error('Decrypt field error: {}'.format(e))
    return value


def decrypt_password(value):
    cipher = value.split(':')
    if len(cipher) != 2:
        return value
    key_cipher, password_cipher = cipher
    aes_key = rsa_decrypt_by_session_pkey(key_cipher)
    aes = get_aes_crypto(aes_key, 'ECB')
    password = aes.decrypt(password_cipher)
    return password


crypto = Crypto()
