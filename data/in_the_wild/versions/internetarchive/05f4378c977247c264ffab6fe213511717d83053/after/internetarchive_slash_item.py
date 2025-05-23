try:
    import ujson as json
except ImportError:
    import json
import urllib
import os
import sys
from fnmatch import fnmatch
import logging

import requests.sessions
from requests.exceptions import HTTPError
from jsonpatch import make_patch
from clint.textui import progress

from . import s3, __version__, session, iarequest, utils


log = logging.getLogger(__name__)


# Item class
#_________________________________________________________________________________________
class Item(object):
    """This class represents an archive.org item. You can use this
    class to access item metadata::

        >>> import internetarchive
        >>> item = internetarchive.Item('stairs')
        >>> print item.metadata

    Or to modify the metadata for an item::

        >>> metadata = dict(title='The Stairs')
        >>> item.modify(metadata)
        >>> print item.metadata['title']
        u'The Stairs'

    This class also uses IA's S3-like interface to upload files to an
    item. You need to supply your IAS3 credentials in environment
    variables in order to upload::

        >>> item.upload('myfile.tar', access_key='Y6oUrAcCEs4sK8ey',
        ...                           secret_key='youRSECRETKEYzZzZ')
        True

    You can retrieve S3 keys here: `https://archive.org/account/s3.php
    <https://archive.org/account/s3.php>`__

    """
    # init()
    #_____________________________________________________________________________________
    def __init__(self, identifier, metadata_timeout=None, config=None):
        """
        :type identifier: str
        :param identifier: The globally unique Archive.org identifier
                           for a given item.

        :type metadata_timeout: int
        :param metadata_timeout: (optional) Set a timeout for retrieving
                                 an item's metadata.

        :type secure: bool
        :param secure: (optional) If secure is True, use HTTPS protocol,
                       otherwise use HTTP.

        """
        self.session = session.ArchiveSession(config)
        self.protocol = 'https:' if self.session.secure else 'http:'
        self.http_session = requests.sessions.Session()
        self.http_session.cookies = self.session.cookies
        self.identifier = identifier
        self._json = self.get_metadata(metadata_timeout)
        self.exists = False if self._json == {} else True

    # __repr__()
    #_____________________________________________________________________________________
    def __repr__(self):
        return ('Item(identifier={identifier!r}, '
                'exists={exists!r})'.format(**self.__dict__))

    # get_metadata()
    #_____________________________________________________________________________________
    def get_metadata(self, metadata_timeout=None):
        """Get an item's metadata from the `Metadata API
        <http://blog.archive.org/2013/07/04/metadata-api/>`__

        :type identifier: str
        :param identifier: Globally unique Archive.org identifier.

        :rtype: dict
        :returns: Metadat API response.

        """
        url = '{protocol}//archive.org/metadata/{identifier}'.format(**self.__dict__)
        try:
            resp = self.http_session.get(url, timeout=metadata_timeout)
            resp.raise_for_status()
        except HTTPError as e:
            error_msg = 'Error retrieving metadata from {0}, {1}'.format(resp.url, e)
            log.error(error_msg)
            raise HTTPError(error_msg)
        metadata = resp.json()
        for key in metadata:
                setattr(self, key, metadata[key])
        return metadata

    # iter_files()
    #_____________________________________________________________________________________
    def iter_files(self):
        """Generator for iterating over files in an item.

        :rtype: generator
        :returns: A generator that yields :class:`internetarchive.File
                  <File>` objects.

        """
        for file_dict in self.files:
            file = File(self, file_dict.get('name'))
            yield file

    # file()
    #_____________________________________________________________________________________
    def get_file(self, file_name):
        """Get a :class:`File <File>` object for the named file.

        :rtype: :class:`internetarchive.File <File>`
        :returns: An :class:`internetarchive.File <File>` object.

        """
        for f in self.iter_files():
            if f.name == file_name:
                return f

    # get_files()
    #_____________________________________________________________________________________
    def get_files(self, files=None, source=None, formats=None, glob_pattern=None):
        files = [] if not files else files
        source = [] if not source else source

        if not isinstance(files, (list, tuple, set)):
            files = [files]
        if not isinstance(source, (list, tuple, set)):
            source = [source]
        if not isinstance(formats, (list, tuple, set)):
            formats = [formats]

        file_objects = []
        for f in self.iter_files():
            if f.name in files:
                file_objects.append(f)
            elif f.source in source:
                file_objects.append(f)
            elif f.format in formats:
                file_objects.append(f)
            elif glob_pattern:
                print f.name, fnmatch(f.name, glob_pattern)
                if fnmatch(f.name, glob_pattern):
                    file_objects.append(f)
        return file_objects

    # download()
    #_____________________________________________________________________________________
    def download(self, concurrent=False, source=None, formats=None, glob_pattern=None,
                 dry_run=False, verbose=False, ignore_existing=False):
        """Download the entire item into the current working directory.

        :type concurrent: bool
        :param concurrent: Download files concurrently if ``True``.

        :type source: str
        :param source: Only download files matching given source.

        :type formats: str
        :param formats: Only download files matching the given Formats.

        :type glob_pattern: str
        :param glob_pattern: Only download files matching the given glob
                             pattern

        :type ignore_existing: bool
        :param ignore_existing: Overwrite local files if they already
                                exist.

        :rtype: bool
        :returns: True if if files have been downloaded successfully.

        """
        if concurrent:
            try:
                from gevent import monkey
                monkey.patch_socket()
                from gevent.pool import Pool
                pool = Pool()
            except ImportError:
                raise ImportError(
                    """No module named gevent

                    Downloading files concurrently requires the gevent neworking library.
                    gevent and all of it's dependencies can be installed with pip:

                    \tpip install cython git+git://github.com/surfly/gevent.git@1.0rc2#egg=gevent

                    """)

        files = self.iter_files()
        if source:
            if type(source) == str:
                source = [source]
            files = [f for f in files if f.source in source]
        if formats:
            if type(formats) == str:
                formats = [formats]
            files = [f for f in files if f.format in formats]
        if glob_pattern:
            files = [f for f in files if fnmatch(f.name, glob_pattern)]

        for f in files:
            fname = f.name.encode('utf-8')
            path = os.path.join(self.identifier, fname)
            if dry_run:
                sys.stdout.write(f.url + '\n')
                continue
            if verbose:
                sys.stdout.write(' downloading: {0}\n'.format(fname))
            if concurrent:
                pool.spawn(f.download, path, ignore_existing=ignore_existing)
            else:
                f.download(path, ignore_existing=ignore_existing)
        if concurrent:
            pool.join()
        return True

    # modify_metadata()
    #_____________________________________________________________________________________
    def modify_metadata(self, metadata, target='metadata', append=False, priority=0,
                        access_key=None, secret_key=None, debug=False):
        """Modify the metadata of an existing item on Archive.org.

        Note: The Metadata Write API does not yet comply with the
        latest Json-Patch standard. It currently complies with `version 02
        <https://tools.ietf.org/html/draft-ietf-appsawg-json-patch-02>`__.

        :type metadata: dict
        :param metadata: Metadata used to update the item.

        :type target: str
        :param target: (optional) Set the metadata target to update.

        :type priority: int
        :param priority: (optional) Set task priority.

        Usage::

            >>> import internetarchive
            >>> item = internetarchive.Item('mapi_test_item1')
            >>> md = dict(new_key='new_value', foo=['bar', 'bar2'])
            >>> item.modify_metadata(md)

        :rtype: dict
        :returns: A dictionary containing the status_code and response
                  returned from the Metadata API.

        """
        access_key = self.session.access_key if not access_key else access_key
        secret_key = self.session.secret_key if not secret_key else secret_key
        src = self.metadata.get(target, {})
        dest = src.copy()
        dest.update(metadata)

        # Prepare patch to remove metadata elements with the value: "REMOVE_TAG".
        for key, val in metadata.items():
            if val == 'REMOVE_TAG' or not val:
                del dest[key]
            if append:
                dest[key] = '{0} {1}'.format(src[key], val)

        json_patch = json.dumps(make_patch(src, dest).patch)

        url = '{protocol}//archive.org/metadata/{identifier}'.format(**self.__dict__)
        request = iarequest.MetadataRequest(
            url=url,
            method='POST',
            patch=json_patch,
            target=target,
            priority=priority,
            access_key=access_key,
            secret_key=secret_key,
        )
        if debug:
            return request
        prepared_request = request.prepare()
        resp = self.http_session.send(prepared_request)
        self._json = self.get_metadata()
        return resp

    # upload_file()
    #_____________________________________________________________________________________
    def upload_file(self, body, key=None, metadata={}, headers={},
                    access_key=None, secret_key=None, queue_derive=True,
                    ignore_preexisting_bucket=False, verify=True, verbose=False,
                    debug=False, **kwargs):
        """Upload a single file to an item. The item will be created
        if it does not exist.

        :type body: Filepath or file-like object.
        :param body: File or data to be uploaded.

        :type key: str
        :param key: (optional) Remote filename.

        :type metadata: dict
        :param metadata: (optional) Metadata used to create a new item.

        :type headers: dict
        :param headers: (optional) Add additional IA-S3 headers to request.

        :type queue_derive: bool
        :param queue_derive: (optional) Set to False to prevent an item from
                             being derived after upload.

        :type ignore_preexisting_bucket: bool
        :param ignore_preexisting_bucket: (optional) Destroy and respecify the
                                          metadata for an item

        :type verbose: bool
        :param verbose: (optional) Print progress to stdout.

        :type debug: bool
        :param debug: (optional) Set to True to print headers to stdout, and
                      exit without sending the upload request.

        Usage::

            >>> import internetarchive
            >>> item = internetarchive.Item('identifier')
            >>> item.upload_file('/path/to/image.jpg',
            ...                  key='photos/image1.jpg')
            True

        """
        access_key = self.session.access_key if not access_key else access_key
        secret_key = self.session.secret_key if not secret_key else secret_key

        if not hasattr(body, 'read'):
            body = open(body, 'rb')

        if not metadata.get('scanner'):
            scanner = 'Internet Archive Python library {0}'.format(__version__)
            metadata['scanner'] = scanner

        try:
            body.seek(0, os.SEEK_END)
            size = body.tell()
            body.seek(0, os.SEEK_SET)
        except IOError:
            size = None

        if not headers.get('x-archive-size-hint'):
            headers['x-archive-size-hint'] = size

        key = body.name.split('/')[-1] if key is None else key
        base_url = '{protocol}//s3.us.archive.org/{identifier}'.format(**self.__dict__)
        url = '{base_url}/{key}'.format(base_url=base_url, key=key)
        if verify:
            headers['Content-MD5'] = utils.get_md5(body)
        if verbose:
            try:
                chunk_size = 1048576
                expected_size = size/chunk_size + 1
                chunks = utils.chunk_generator(body, chunk_size)
                progress_generator = progress.bar(chunks, expected_size=expected_size,
                                                  label=' uploading {f}: '.format(f=key))
                data = utils.IterableToFileAdapter(progress_generator, size)
            except:
                sys.stdout.write(' uploading {f}: '.format(f=key))
                data = body
        else:
            data = body

        request = iarequest.S3Request(
            method='PUT',
            url=url,
            headers=headers,
            data=data,
            metadata=metadata,
            access_key=access_key,
            secret_key=secret_key,
            **kwargs
        )

        if debug:
            return request
        else:
            prepared_request = request.prepare()
            try:
                response = self.http_session.send(prepared_request, stream=True)
                response.raise_for_status()
                log.info('uploaded {f} to {u}'.format(f=key, u=url))
                return response
            except HTTPError as e:
                error_msg = 'Error uploading {0}, {1}'.format(key, e)
                log.error(error_msg)
                return response
                #raise HTTPError(error_msg)

    # upload()
    #_____________________________________________________________________________________
    def upload(self, files, **kwargs):
        """Upload files to an item. The item will be created if it
        does not exist.

        :type files: list
        :param files: The filepaths or file-like objects to upload.

        :type kwargs: dict
        :param kwargs: The keyword arguments from the call to
                       upload_file().

        Usage::

            >>> import internetarchive
            >>> item = internetarchive.Item('identifier')
            >>> md = dict(mediatype='image', creator='Jake Johnson')
            >>> item.upload('/path/to/image.jpg', metadata=md, queue_derive=False)
            True

        :rtype: bool
        :returns: True if the request was successful and all files were
                  uploaded, False otherwise.

        """
        def iter_directory(directory):
            for path, dir, files in os.walk(directory):
                for f in files:
                    filepath = os.path.join(path, f)
                    key = os.path.relpath(filepath, directory)
                    yield (filepath, key)

        if not isinstance(files, (list, tuple)):
            files = [files]

        responses = []
        for f in files:
            key = None
            if isinstance(f, basestring) and os.path.isdir(f):
                for filepath, key in iter_directory(f):
                    resp = self.upload_file(filepath, key=key, **kwargs)
                    responses.append(resp)
            else:
                resp = self.upload_file(f, **kwargs)
                responses.append(resp)
        return responses


# File class
#_________________________________________________________________________________________
class File(object):
    """:todo: document ``internetarchive.File`` class."""
    # init()
    #_____________________________________________________________________________________
    def __init__(self, item, name):
        _file = {}
        for f in item.files:
            if f.get('name') == name:
                _file = f
                break
    
        self._item = item
        self.identifier = item.identifier
        self.name = None
        self.size = None
        self.source = None
        self.format = None
        for key in _file:
            setattr(self, key, _file[key])
        base_url = '{protocol}//archive.org/download/{identifier}'.format(**item.__dict__)
        self.url = '{base_url}/{name}'.format(base_url=base_url, name=name)

    # __repr__()
    #_____________________________________________________________________________________
    def __repr__(self):
        return ('File(identifier={identifier!r}, '
                'filename={name!r}, '
                'size={size!r}, '
                'source={source!r}, '
                'format={format!r})'.format(**self.__dict__))

    # download()
    #_____________________________________________________________________________________
    def download(self, file_path=None, ignore_existing=False):
        """:todo: document ``internetarchive.File.download()`` method"""
        file_path = self.name if not file_path else file_path
        if os.path.exists(file_path) and not ignore_existing:
            raise IOError('File already exists: {0}'.format(file_path))

        parent_dir = os.path.dirname(file_path)
        if parent_dir != '' and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        try:
            response = self._item.http_session.get(self.url, stream=True)
            response.raise_for_status()
        except HTTPError as e:
            raise HTTPError('Error downloading {0}, {1}'.format(self.url, e))
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    # delete()
    #_____________________________________________________________________________________
    def delete(self, debug=False, verbose=False, cascade_delete=False):
        headers = s3.build_headers(cascade_delete=cascade_delete)
        url = 'http://s3.us.archive.org/{0}/{1}'.format(self.identifier, self.fname)
        access_key, secret_key = config.get_s3_keys()
        request = iarequest.S3Request(
            method='DELETE',
            url=url,
            headers=headers,
            access_key=access_key,
            secret_key=secret_key
        )
        if debug:
            return request
        else:
            if verbose:
                sys.stdout.write(' deleting file: {0}\n'.format(self.name))
            prepared_request = request.prepare()
            return self._item.http_session.send(prepared_request)
