"""
Objects used with ProofreadPage Extension.

This module includes objects:

* ProofreadPage(Page)
* FullHeader
* IndexPage(Page)


OCR support of page scans via:
- https://phetools.toolforge.org/hocr_cgi.py
- https://phetools.toolforge.org/ocr.php
- inspired by https://en.wikisource.org/wiki/MediaWiki:Gadget-ocr.js

- Wikimedia OCR
- see: https://www.mediawiki.org/wiki/Help:Extension:Wikisource/Wikimedia_OCR

- https://ws-google-ocr.toolforge.org/
- inspired by https://wikisource.org/wiki/MediaWiki:GoogleOCR.js
- see also: https://wikisource.org/wiki/Wikisource:Google_OCR

"""
#
# (C) Pywikibot team, 2015-2021
#
# Distributed under the terms of the MIT license.
#
import json
import re
import time
from functools import partial
from http import HTTPStatus
from typing import Any, Optional, Union

from requests.exceptions import ReadTimeout  # type: ignore[import]

import pywikibot
from pywikibot import textlib
from pywikibot.backports import (
    Callable,
    Dict,
    Iterable,
    List,
    Sequence,
    Set,
    Tuple,
)
from pywikibot.comms import http
from pywikibot.data.api import Request
from pywikibot.exceptions import Error, OtherPageSaveError

PAGES_FROM_LABEL_TYPE = Dict[str, Set['pywikibot.page.Page']]

# TODO: replace these after T286867

OPT_INDEX_PAGE_TYPE = Any  # Optional['IndexPage']
OPT_INDEX_PAGE_LIST_TYPE = Any  # Optional[List['IndexPage']]

INDEX_TYPE = Optional[Tuple[OPT_INDEX_PAGE_TYPE,
                            OPT_INDEX_PAGE_LIST_TYPE]]

try:
    from bs4 import BeautifulSoup
except ImportError as e:
    BeautifulSoup = e

    def _bs4_soup(*args: Any, **kwargs: Any) -> None:
        """Raise BeautifulSoup when called, if bs4 is not available."""
        raise BeautifulSoup
else:
    from bs4 import FeatureNotFound
    try:
        BeautifulSoup('', 'lxml')
    except FeatureNotFound:
        _bs4_soup = partial(BeautifulSoup, features='html.parser')
    else:
        _bs4_soup = partial(BeautifulSoup, features='lxml')


_logger = 'proofreadpage'


def decompose(fn: Callable) -> Callable:  # type: ignore # noqa: N805
    """Decorator for ProofreadPage.

    Decompose text if needed and recompose text.
    """
    def wrapper(self: 'ProofreadPage', *args: Any, **kwargs: Any) -> Any:
        if not hasattr(self, '_full_header'):
            self._decompose_page()
        _res = fn(self, *args, **kwargs)
        self._compose_page()
        return _res

    return wrapper


def check_if_cached(fn: Callable) -> Callable:  # type: ignore # noqa: N805
    """Decorator for IndexPage to ensure data is cached."""
    def wrapper(self: 'IndexPage', *args: Any, **kwargs: Any) -> Any:
        if self._cached is False:
            self._get_page_mappings()
        return fn(self, *args, **kwargs)

    return wrapper


class FullHeader:

    """Header of a ProofreadPage object."""

    p_header = re.compile(
        r'<pagequality level="(?P<ql>\d)" user="(?P<user>.*?)" />'
        r'(?P<has_div><div class="pagetext">)?(?P<header>.*)',
        re.DOTALL)

    TEMPLATE_V1 = ('<pagequality level="{0.ql}" user="{0.user}" />'
                   '<div class="pagetext">{0.header}\n\n\n')
    TEMPLATE_V2 = ('<pagequality level="{0.ql}" user="{0.user}" />'
                   '{0.header}')

    def __init__(self, text: Optional[str] = None) -> None:
        """Initializer."""
        self._text = text or ''
        self._has_div = True

        m = self.p_header.search(self._text)
        if m:
            self.ql = int(m.group('ql'))
            self.user = m.group('user')
            self.header = m.group('header')
            if not m.group('has_div'):
                self._has_div = False
        else:
            self.ql = ProofreadPage.NOT_PROOFREAD
            self.user = ''
            self.header = ''

    def __str__(self) -> str:
        """Return a string representation."""
        if self._has_div:
            return FullHeader.TEMPLATE_V1.format(self)
        return FullHeader.TEMPLATE_V2.format(self)


class ProofreadPage(pywikibot.Page):

    """ProofreadPage page used in Mediawiki ProofreadPage extension."""

    WITHOUT_TEXT = 0
    NOT_PROOFREAD = 1
    PROBLEMATIC = 2
    PROOFREAD = 3
    VALIDATED = 4

    PROOFREAD_LEVELS = [
        WITHOUT_TEXT,
        NOT_PROOFREAD,
        PROBLEMATIC,
        PROOFREAD,
        VALIDATED,
    ]

    _FMT = ('{0.open_tag}{0._full_header}{0.close_tag}'
            '{0._body}'
            '{0.open_tag}{0._footer}%s{0.close_tag}')

    open_tag = '<noinclude>'
    close_tag = '</noinclude>'
    p_open = re.compile(r'<noinclude>')
    p_close = re.compile(r'(</div>|\n\n\n)?</noinclude>')
    p_close_no_div = re.compile('</noinclude>')  # V2 page format.

    # phetools ocr utility
    _HOCR_CMD = ('https://phetools.toolforge.org/hocr_cgi.py?'
                 'cmd=hocr&book={book}&lang={lang}&user={user}')

    _OCR_CMD = ('https://phetools.toolforge.org/ocr.php?'
                'cmd=ocr&url={url_image}&lang={lang}&user={user}')

    # Wikimedia OCR utility
    _WMFOCR_CMD = ('https://ocr.wmcloud.org/api.php?engine=tesseract&'
                   'langs[]={lang}&image={url_image}&uselang={lang}')

    # googleOCR ocr utility
    _GOCR_CMD = ('https://ws-google-ocr.toolforge.org/api.php?'
                 'image={url_image}&lang={lang}')

    _MULTI_PAGE_EXT = ['djvu', 'pdf']

    _PHETOOLS = 'phetools'
    _WMFOCR = 'wmfOCR'
    _GOOGLE_OCR = 'googleOCR'
    _OCR_CMDS = {_PHETOOLS: _OCR_CMD,
                 _WMFOCR: _WMFOCR_CMD,
                 _GOOGLE_OCR: _GOCR_CMD,
                 }
    _OCR_METHODS = list(_OCR_CMDS.keys())

    def __init__(self, source, title: str = '') -> None:
        """Instantiate a ProofreadPage object.

        :raise UnknownExtensionError: source Site has no ProofreadPage
            Extension.
        """
        if not isinstance(source, pywikibot.site.BaseSite):
            site = source.site
        else:
            site = source
        super().__init__(source, title)
        if self.namespace() != site.proofread_page_ns:
            raise ValueError('Page {} must belong to {} namespace'
                             .format(self.title(), site.proofread_page_ns))
        # Ensure that constants are in line with Extension values.
        if list(self.site.proofread_levels.keys()) != self.PROOFREAD_LEVELS:
            raise ValueError('QLs do not match site values: {} != {}'
                             .format(self.site.proofread_levels.keys(),
                                     self.PROOFREAD_LEVELS))

        self._base, self._base_ext, self._num = self._parse_title()
        self._multi_page = self._base_ext in self._MULTI_PAGE_EXT

    @property
    def _fmt(self) -> str:
        return self._FMT % ('</div>' if self._full_header._has_div else '')

    def _parse_title(self) -> Tuple[str, str, Optional[int]]:
        """Get ProofreadPage base title, base extension and page number.

        Base title is the part of title before the last '/', if any,
        or the whole title if no '/' is present.

        Extension is the extension of the base title.

        Page number is the part of title after the last '/', if any,
        or None if no '/' is present.

        E.g. for title 'Page:Popular Science Monthly Volume 1.djvu/12':
        - base = 'Popular Science Monthly Volume 1.djvu'
        - extension = 'djvu'
        - number = 12

        E.g. for title 'Page:Original Waltzing Matilda manuscript.jpg':
        - base = 'Original Waltzing Matilda manuscript.jpg'
        - extension = 'jpg'
        - number = None

        :return: (base, ext, num).
        """
        left, sep, right = self.title(with_ns=False).rpartition('/')
        num = None  # type: Optional[int]

        if sep:
            base = left
            num = int(right)
        else:
            base = right

        left, sep, right = base.rpartition('.')
        ext = right if sep else ''

        return base, ext, num

    @property
    def index(self) -> OPT_INDEX_PAGE_TYPE:
        """Get the Index page which contains ProofreadPage.

        If there are many Index pages link to this ProofreadPage, and
        the ProofreadPage is titled Page:<index title>/<page number>,
        the Index page with the same title will be returned.
        Otherwise None is returned in the case of multiple linked Index pages.

        To force reload, delete index and call it again.

        :return: the Index page for this ProofreadPage
        """
        if not hasattr(self, '_index'):
            index_ns = self.site.proofread_index_ns
            what_links_here = [IndexPage(page) for page in
                               set(self.getReferences(namespaces=index_ns))]

            if not what_links_here:
                self._index = (None, [])
            elif len(what_links_here) == 1:
                self._index = (what_links_here.pop(), [])
            else:
                self._index = (None, what_links_here)
                # Try to infer names from page titles.
                if self._num is not None:
                    for page in what_links_here:
                        if page.title(with_ns=False) == self._base:
                            what_links_here.remove(page)
                            self._index = (page, what_links_here)
                            break

        page, others = self._index
        if others:
            pywikibot.warning('{} linked to several Index pages.'.format(self))
            pywikibot.output('{}{!s}'.format(' ' * 9, [page] + others))

            if page:
                pywikibot.output(
                    '{}Selected Index: {}'.format(' ' * 9, page))
                pywikibot.output('{}remaining: {!s}'.format(' ' * 9, others))

        if not page:
            pywikibot.warning('Page {} is not linked to any Index page.'
                              .format(self))

        return page

    @index.setter
    def index(self, value: 'IndexPage') -> None:
        if not isinstance(value, IndexPage):
            raise TypeError('value {} must be an IndexPage object.'
                            .format(value))
        self._index = (value, None)

    @index.deleter
    def index(self) -> None:
        if hasattr(self, '_index'):
            del self._index

    @property
    def quality_level(self) -> int:
        """Return the quality level of this page when it is retrieved from API.

        This is only applicable if contentmodel equals 'proofread-page'.
        None is returned otherwise.

        This property is read-only and is applicable only when page is loaded.
        If quality level is overwritten during page processing, this property
        is no longer necessarily aligned with the new value.

        In this way, no text parsing is necessary to check quality level when
        fetching a page.
        """
        # TODO: align this value with ProofreadPage.ql

        if (self.content_model == 'proofread-page'
                and hasattr(self, '_quality')):
            return int(self._quality)  # type: ignore[attr-defined]
        return self.ql

    @property  # type: ignore[misc]
    @decompose
    def ql(self) -> int:
        """Return page quality level."""
        return self._full_header.ql

    @ql.setter  # type: ignore[misc]
    @decompose
    def ql(self, value: int) -> None:
        if value not in self.site.proofread_levels:
            raise ValueError('Not valid QL value: {} (legal values: {})'
                             .format(value, self.site.proofread_levels))
        # TODO: add logic to validate ql value change, considering
        # site.proofread_levels.
        self._full_header.ql = value

    @property  # type: ignore[misc]
    @decompose
    def user(self) -> str:
        """Return user in page header."""
        return self._full_header.user

    @user.setter  # type: ignore[misc]
    @decompose
    def user(self, value: str) -> None:
        self._full_header.user = value

    @property  # type: ignore[misc]
    @decompose
    def status(self) -> Optional[str]:
        """Return Proofread Page status."""
        try:
            return self.site.proofread_levels[self.ql]
        except KeyError:
            pywikibot.warning('Not valid status set for {}: quality level = {}'
                              .format(self.title(as_link=True), self.ql))
            return None

    def without_text(self) -> None:
        """Set Page QL to "Without text"."""
        self.ql = self.WITHOUT_TEXT  # type: ignore[misc]

    def problematic(self) -> None:
        """Set Page QL to "Problematic"."""
        self.ql = self.PROBLEMATIC  # type: ignore[misc]

    def not_proofread(self) -> None:
        """Set Page QL to "Not Proofread"."""
        self.ql = self.NOT_PROOFREAD  # type: ignore[misc]

    def proofread(self) -> None:
        """Set Page QL to "Proofread"."""
        # TODO: check should be made to be consistent with Proofread Extension
        self.ql = self.PROOFREAD  # type: ignore[misc]

    def validate(self) -> None:
        """Set Page QL to "Validated"."""
        # TODO: check should be made to be consistent with Proofread Extension
        self.ql = self.VALIDATED  # type: ignore[misc]

    @property  # type: ignore[misc]
    @decompose
    def header(self) -> str:
        """Return editable part of Page header."""
        return self._full_header.header

    @header.setter  # type: ignore[misc]
    @decompose
    def header(self, value: str) -> None:
        self._full_header.header = value

    @property  # type: ignore[misc]
    @decompose
    def body(self) -> str:
        """Return Page body."""
        return self._body

    @body.setter  # type: ignore[misc]
    @decompose
    def body(self, value: str) -> None:
        self._body = value

    @property  # type: ignore[misc]
    @decompose
    def footer(self) -> str:
        """Return Page footer."""
        return self._footer

    @footer.setter  # type: ignore[misc]
    @decompose
    def footer(self, value: str) -> None:
        self._footer = value

    def _create_empty_page(self) -> None:
        """Create empty page."""
        self._full_header = FullHeader()
        self._body = ''
        self._footer = ''
        self.user = self.site.username()  # type: ignore[misc]
        self._compose_page()

    @property
    def text(self) -> str:
        """Override text property.

        Preload text returned by EditFormPreloadText to preload non-existing
        pages.
        """
        # Text is already cached.
        if getattr(self, '_text', None) is not None:
            return self._text

        if self.exists():
            # If page exists, load it.
            return super().text

        # If page does not exist, preload it.
        self._text = self.preloadText()
        self.user = self.site.username()  # type: ignore[misc]
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Update current text.

        Mainly for use within the class, called by other methods.
        Use self.header, self.body and self.footer to set page content,

        :param value: New value or None

        :raise Error: the page is not formatted according to ProofreadPage
            extension.
        """
        self._text = value
        if self._text:
            self._decompose_page()
        else:
            self._create_empty_page()

    @text.deleter
    def text(self) -> None:
        if hasattr(self, '_text'):
            del self._text

    def _decompose_page(self) -> None:
        """Split Proofread Page text in header, body and footer.

        :raise Error: the page is not formatted according to ProofreadPage
            extension.
        """
        def _assert_len(len_oq: int, len_cq: int, title: str) -> None:
            if (len_oq != len_cq) or (len_oq < 2 or len_cq < 2):
                raise Error('ProofreadPage {}: invalid format'.format(title))

        # Property force page text loading.
        text = self.text
        if not text:
            self._create_empty_page()
            return

        _title = self.title(as_link=True)

        open_queue = list(self.p_open.finditer(text))
        close_queue = list(self.p_close.finditer(text))
        _assert_len(len(open_queue), len(close_queue), _title)

        f_open, f_close = open_queue[0], close_queue[0]
        self._full_header = FullHeader(text[f_open.end():f_close.start()])

        # check version of page format and in case recompute last match,
        # in order not to include </div>.
        if not self._full_header._has_div:
            close_queue = list(self.p_close_no_div.finditer(text))
            _assert_len(len(open_queue), len(close_queue), _title)

        l_open, l_close = open_queue[-1], close_queue[-1]
        self._footer = text[l_open.end():l_close.start()]

        self._body = text[f_close.end():l_open.start()]

    def _compose_page(self) -> str:
        """Compose Proofread Page text from header, body and footer."""
        self._text = self._fmt.format(self)
        return self._text

    def _page_to_json(self) -> str:
        """Convert page text to json format.

        This is the format accepted by action=edit specifying
        contentformat=application/json. This format is recommended to save the
        page, as it is not subject to possible errors done in composing the
        wikitext header and footer of the page or changes in the ProofreadPage
        extension format.
        """
        page_dict = {'header': self.header,
                     'body': self.body,
                     'footer': self.footer,
                     'level': {'level': self.ql, 'user': self.user},
                     }
        # Ensure_ascii=False returns a unicode.
        return json.dumps(page_dict, ensure_ascii=False)

    def save(self, *args: Any, **kwargs: Any) -> None:  # See Page.save().
        """Save page content after recomposing the page."""
        summary = kwargs.pop('summary', '')
        summary = self.pre_summary + summary
        # Save using contentformat='application/json'.
        kwargs['contentformat'] = 'application/json'
        kwargs['contentmodel'] = 'proofread-page'
        text = self._page_to_json()
        super().save(*args, text=text, summary=summary, **kwargs)

    @property
    def pre_summary(self) -> str:
        """Return trailing part of edit summary.

        The edit summary shall be appended to pre_summary to highlight
        Status in the edit summary on wiki.
        """
        return '/* {0.status} */ '.format(self)

    @property
    def url_image(self) -> str:
        """Get the file url of the scan of ProofreadPage.

        :return: file url of the scan ProofreadPage or None.

        :raises Exception: in case of http errors
        :raises ImportError: if bs4 is not installed, _bs4_soup() will raise
        :raises ValueError: in case of no prp_page_image src found for scan
        """
        # wrong link fails with various possible Exceptions.
        if not hasattr(self, '_url_image'):

            if self.exists():
                url = self.full_url()
            else:
                path = 'w/index.php?title={}&action=edit&redlink=1'
                url = self.site.base_url(path.format(self.title(as_url=True)))

            try:
                response = http.fetch(url, charset='utf-8')
            except Exception:
                pywikibot.error('Error fetching HTML for {}.'.format(self))
                raise

            soup = _bs4_soup(response.text)  # type: ignore

            try:
                self._url_image = soup.find(class_='prp-page-image')
                # if None raises AttributeError
                self._url_image = self._url_image.find('img')
                # if None raises TypeError.
                self._url_image = self._url_image['src']
            except (TypeError, AttributeError):
                raise ValueError('No prp-page-image src found for {}.'
                                 .format(self))
            else:
                self._url_image = 'https:' + self._url_image

        return self._url_image

    def _ocr_callback(self, cmd_uri: str,
                      parser_func: Optional[Callable[[str], str]] = None,
                      ocr_tool: Optional[str] = None
                      ) -> Tuple[bool, Union[str, Exception]]:
        """OCR callback function.

        :return: tuple (error, text [error description in case of error]).
        """
        def identity(x: Any) -> Any:
            return x

        if not cmd_uri:
            raise ValueError('Parameter cmd_uri is mandatory.')

        if parser_func is None:
            parser_func = identity

        if not callable(parser_func):
            raise TypeError('Keyword parser_func must be callable.')

        if ocr_tool not in self._OCR_METHODS:
            raise TypeError(
                "ocr_tool must be in {}, not '{}'."
                .format(self._OCR_METHODS, ocr_tool))

        # wrong link fail with Exceptions
        for retry in range(5, 30, 5):
            pywikibot.debug('{}: get URI {!r}'.format(ocr_tool, cmd_uri),
                            _logger)
            try:
                response = http.fetch(cmd_uri)
            except ReadTimeout as e:
                pywikibot.warning('ReadTimeout {}: {}'.format(cmd_uri, e))
            except Exception as e:
                pywikibot.error('"{}": {}'.format(cmd_uri, e))
                return True, e
            else:
                pywikibot.debug('{}: {}'.format(ocr_tool, response.text),
                                _logger)
                break

            pywikibot.warning('retrying in {} seconds ...'.format(retry))
            time.sleep(retry)
        else:
            return True, ReadTimeout

        if HTTPStatus.BAD_REQUEST <= response.status_code < 600:
            return True, 'Http response status {}'.format(response.status_code)

        data = json.loads(response.text)

        if ocr_tool == self._PHETOOLS:  # phetools
            assert 'error' in data, 'Error from phetools: {}'.format(data)
            assert data['error'] in [0, 1, 2, 3], \
                'Error from phetools: {}'.format(data)
            error, _text = bool(data['error']), data['text']
        else:  # googleOCR
            if 'error' in data:
                error, _text = True, data['error']
            else:
                error, _text = False, data['text']

        if error:
            pywikibot.error('OCR query {}: {}'.format(cmd_uri, _text))
            return error, _text
        return error, parser_func(_text)

    def _do_hocr(self) -> Tuple[bool, Union[str, Exception]]:
        """Do hocr using https://phetools.toolforge.org/hocr_cgi.py?cmd=hocr.

        This is the main method for 'phetools'.
        Fallback method is ocr.

        :raise ImportError: if bs4 is not installed, _bs4_soup() will raise
        """
        def parse_hocr_text(txt: str) -> str:
            """Parse hocr text."""
            soup = _bs4_soup(txt)  # type: ignore

            res = []
            for ocr_page in soup.find_all(class_='ocr_page'):
                for area in soup.find_all(class_='ocr_carea'):
                    for par in area.find_all(class_='ocr_par'):
                        for line in par.find_all(class_='ocr_line'):
                            res.append(line.get_text())
                        res.append('\n')
            return ''.join(res)

        params = {
            'book': self.title(as_url=True, with_ns=False),
            'lang': self.site.lang,
            'user': self.site.user(),
        }
        cmd_uri = self._HOCR_CMD.format_map(params)

        return self._ocr_callback(cmd_uri,
                                  parser_func=parse_hocr_text,
                                  ocr_tool=self._PHETOOLS)

    def _do_ocr(self, ocr_tool: Optional[str] = None
                ) -> Tuple[bool, Union[str, Exception]]:
        """Do ocr using specified ocr_tool method."""
        try:
            url_image = self.url_image
        except ValueError:
            error_text = 'No prp-page-image src found for {}.'.format(self)
            pywikibot.error(error_text)
            return True, error_text

        if ocr_tool is None:
            msg = 'ocr_tool required, must be among {}'
            raise TypeError(msg.format(self._OCR_METHODS))

        try:
            cmd_fmt = self._OCR_CMDS[ocr_tool]
        except KeyError:
            raise TypeError(
                "ocr_tool must be in {}, not '{}'."
                .format(self._OCR_METHODS, ocr_tool))

        params = {
            'url_image': url_image,
            'lang': self.site.lang,
            'user': self.site.user(),
        }
        cmd_uri = cmd_fmt.format_map(params)

        return self._ocr_callback(cmd_uri, ocr_tool=ocr_tool)

    def ocr(self, ocr_tool: Optional[str] = None) -> str:
        """Do OCR of ProofreadPage scan.

        The text returned by this function shall be assigned to self.body,
        otherwise the ProofreadPage format will not be maintained.

        It is the user's responsibility to reset quality level accordingly.

        :param ocr_tool: 'phetools' or 'googleOCR', default is 'phetools'

        :return: OCR text for the page.

        :raise TypeError: wrong ocr_tool keyword arg.
        :raise ValueError: something went wrong with OCR process.
        """
        if ocr_tool is None:  # default value
            ocr_tool = self._PHETOOLS

        if ocr_tool not in self._OCR_METHODS:
            raise TypeError(
                "ocr_tool must be in {}, not '{}'."
                .format(self._OCR_METHODS, ocr_tool))

        if ocr_tool == self._PHETOOLS:
            # if _multi_page, try _do_hocr() first and fall back to _do_ocr()
            if self._multi_page:
                error, text = self._do_hocr()
                if not error and isinstance(text, str):
                    return text
                pywikibot.warning('{}: phetools hocr failed, '
                                  'falling back to ocr.'.format(self))

        error, text = self._do_ocr(ocr_tool=ocr_tool)

        if not error and isinstance(text, str):
            return text
        raise ValueError(
            '{}: not possible to perform OCR. {}'.format(self, text))


class PurgeRequest(Request):

    """Subclass of Request which skips the check on write rights.

    Workaround for T128994.
    # TODO: remove once bug is fixed.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Monkeypatch action in Request initializer."""
        action = kwargs['parameters']['action']
        kwargs['parameters']['action'] = 'dummy'
        super().__init__(**kwargs)
        self.action = action
        self.update({'action': action})


class IndexPage(pywikibot.Page):

    """Index Page page used in Mediawiki ProofreadPage extension."""

    INDEX_TEMPLATE = ':MediaWiki:Proofreadpage_index_template'

    def __init__(self, source, title: str = '') -> None:
        """Instantiate an IndexPage object.

        In this class:
        page number is the number in the page title in the Page namespace, if
        the wikisource site adopts this convention (e.g. page_number is 12
        for Page:Popular Science Monthly Volume 1.djvu/12) or the sequential
        number of the pages linked from the index section in the Index page
        if the index is built via transclusion of a list of pages (e.g. like
        on de wikisource).
        page label is the label associated with a page in the Index page.

        This class provides methods to get pages contained in Index page,
        and relative page numbers and labels by means of several helper
        functions.

        It also provides a generator to pages contained in Index page, with
        possibility to define range, filter by quality levels and page
        existence.

        :raise UnknownExtensionError: source Site has no ProofreadPage
            Extension.
        :raise ImportError: bs4 is not installed.
        """
        # Check if BeautifulSoup is imported.
        if isinstance(BeautifulSoup, ImportError):
            raise BeautifulSoup

        if not isinstance(source, pywikibot.site.BaseSite):
            site = source.site
        else:
            site = source
        super().__init__(source, title)
        if self.namespace() != site.proofread_index_ns:
            raise ValueError('Page {} must belong to {} namespace'
                             .format(self.title(), site.proofread_index_ns))

        self._all_page_links = set(
            self.site.pagelinks(self, namespaces=site.proofread_page_ns))

        self._cached = False

    @staticmethod
    def _parse_redlink(href: str) -> Optional[str]:
        """Parse page title when link in Index is a redlink."""
        p_href = re.compile(
            r'/w/index\.php\?title=(.+?)&action=edit&redlink=1')
        title = p_href.search(href)
        if title:
            return title.group(1)
        return None

    def save(self, *args: Any, **kwargs: Any) -> None:  # See Page.save().
        """
        Save page after validating the content.

        Trying to save any other content fails silently with a parameterless
        INDEX_TEMPLATE being saved.
        """
        if not self.has_valid_content():
            raise OtherPageSaveError(
                self, 'An IndexPage must consist only of a single call to '
                '{{%s}}.' % self.INDEX_TEMPLATE)
        kwargs['contentformat'] = 'text/x-wiki'
        kwargs['contentmodel'] = 'proofread-index'
        super().save(*args, **kwargs)

    def has_valid_content(self) -> bool:
        """Test page only contains a single call to the index template."""
        if (not self.text.startswith('{{' + self.INDEX_TEMPLATE)
                or not self.text.endswith('}}')):
            return False

        # Discard all inner templates as only top-level ones matter
        templates = textlib.extract_templates_and_params_regex_simple(
            self.text)
        if len(templates) != 1 or templates[0][0] != self.INDEX_TEMPLATE:
            # Only a single call to the INDEX_TEMPLATE is allowed
            return False

        return True

    def purge(self) -> None:  # type: ignore[override]
        """Overwrite purge method.

        Instead of a proper purge action, use PurgeRequest, which
        skips the check on write rights.
        """
        # TODO: This is a workaround for T128994. Remove once bug is fixed.

        params = {'action': 'purge', 'titles': [self.title()]}
        request = PurgeRequest(site=self.site, parameters=params)
        rawdata = request.submit()
        error_message = 'Purge action failed for {}'.format(self)
        assert 'purge' in rawdata, error_message
        assert 'purged' in rawdata['purge'][0], error_message

    def _get_page_mappings(self) -> None:
        """Associate label and number for each page linked to the index."""
        # Clean cache, if any.
        self._page_from_numbers = {}
        self._numbers_from_page = {}  # type: Dict[pywikibot.page.Page, int]
        self._page_numbers_from_label = {}  # type: Dict[str, Set[int]]
        self._pages_from_label = {}  # type: PAGES_FROM_LABEL_TYPE
        self._labels_from_page_number = {}  # type: Dict[int, str]
        self._labels_from_page = {}  # type: Dict[pywikibot.page.Page, str]
        if hasattr(self, '_parsed_text'):
            del self._parsed_text

        self._parsed_text = self._get_parsed_page()
        self._soup = _bs4_soup(self._parsed_text)  # type: ignore
        # Do not search for "new" here, to avoid to skip purging if links
        # to non-existing pages are present.
        attrs = {'class': re.compile('prp-pagequality')}

        # Search for attribute "prp-pagequality" in tags:
        # Existing pages:
        # <a href="/wiki/Page:xxx.djvu/n"
        #    title="Page:xxx.djvu/n">m
        #    class="quality1 prp-pagequality-1"
        # </a>
        # Non-existing pages:
        # <a href="/w/index.php?title=xxx&amp;action=edit&amp;redlink=1"
        #    class="new"
        #    title="Page:xxx.djvu/n (page does not exist)">m
        # </a>

        # Try to purge or raise ValueError.
        found = self._soup.find_all('a', attrs=attrs)
        attrs = {'class': re.compile('prp-pagequality|new')}
        if not found:
            self.purge()
            del self._parsed_text
            self._parsed_text = self._get_parsed_page()
            self._soup = _bs4_soup(self._parsed_text)  # type: ignore
            if not self._soup.find_all('a', attrs=attrs):
                raise ValueError(
                    'Missing class="qualityN prp-pagequality-N" or '
                    'class="new" in: {}.'.format(self))

        # Search for attribute "prp-pagequality" or "new" in tags:
        page_cnt = 0
        for a_tag in self._soup.find_all('a', attrs=attrs):
            label = a_tag.text.lstrip('0')  # Label is not converted to int.
            class_ = a_tag.get('class')
            href = a_tag.get('href')

            if 'new' in class_:
                title = self._parse_redlink(href)  # non-existing page
                if title is None:  # title not conforming to required format
                    continue
            else:
                title = a_tag.get('title')   # existing page

            assert title is not None
            try:
                page = ProofreadPage(self.site, title)
                page.index = self  # set index property for page
                page_cnt += 1
            except ValueError:
                # title is not in site.proofread_page_ns; do not consider it
                continue

            if page not in self._all_page_links:
                raise Error('Page {} not recognised.'.format(page))

            # In order to avoid to fetch other Page:title links outside
            # the Pages section of the Index page; these should hopefully be
            # the first ones, so if they start repeating, we are done.
            if page in self._labels_from_page:
                break

            # Sanity check if WS site use page convention name/number.
            if page._num is not None:
                assert page_cnt == int(page._num), (
                    'Page number {} not recognised as page {}.'
                    .format(page_cnt, title))

            # Mapping: numbers <-> pages.
            self._page_from_numbers[page_cnt] = page
            self._numbers_from_page[page] = page_cnt
            # Mapping: numbers/pages as keys, labels as values.
            self._labels_from_page_number[page_cnt] = label
            self._labels_from_page[page] = label
            # Reverse mapping: labels as keys, numbers/pages as values.
            self._page_numbers_from_label.setdefault(
                label, set()).add(page_cnt)
            self._pages_from_label.setdefault(label, set()).add(page)

        # Sanity check: all links to Page: ns must have been considered.
        assert set(self._labels_from_page) == set(self._all_page_links)

        # Info cached.
        self._cached = True

    @property  # type: ignore[misc]
    @check_if_cached
    def num_pages(self) -> int:
        """Return total number of pages in Index.

        :return: total number of pages in Index
        """
        return len(self._page_from_numbers)

    def page_gen(self, start: int = 1,
                 end: Optional[int] = None,
                 filter_ql: Optional[Sequence[int]] = None,
                 only_existing: bool = False,
                 content: bool = True
                 ) -> Iterable['pywikibot.page.Page']:
        """Return a page generator which yields pages contained in Index page.

        Range is [start ... end], extremes included.

        :param start: first page, defaults to 1
        :param end: num_pages if end is None
        :param filter_ql: filters quality levels
                          if None: all but 'Without Text'.
        :param only_existing: yields only existing pages.
        :param content: preload content.
        """
        if end is None:
            end = self.num_pages

        if not (1 <= start <= end <= self.num_pages):
            raise ValueError('start={}, end={} are not in valid range (1, {})'
                             .format(start, end, self.num_pages))

        # All but 'Without Text'
        if filter_ql is None:
            filter_ql = list(self.site.proofread_levels.keys())
            filter_ql.remove(ProofreadPage.WITHOUT_TEXT)

        gen = (self.get_page(i) for i in range(start, end + 1))
        if content:
            gen = self.site.preloadpages(gen)
        # Filter by QL.
        gen = (p for p in gen if p.ql in filter_ql)
        # Yield only existing.
        if only_existing:
            gen = (p for p in gen if p.exists())
        # Decorate and sort by page number because preloadpages does not
        # guarantee order.
        # TODO: remove if preloadpages will guarantee order.
        gen = ((p, self.get_number(p)) for p in gen)
        gen = (p[0] for p in sorted(gen, key=lambda x: x[1]))

        return gen

    @check_if_cached
    def get_label_from_page(self, page: 'pywikibot.page.Page') -> str:
        """Return 'page label' for page.

        There is a 1-to-1 correspondence (each page has a label).

        :param page: Page instance
        :return: page label
        """
        try:
            return self._labels_from_page[page]
        except KeyError:
            raise KeyError('Invalid Page: {}.'.format(page))

    @check_if_cached
    def get_label_from_page_number(self, page_number: int) -> str:
        """Return page label from page number.

        There is a 1-to-1 correspondence (each page has a label).

        :return: page label
        """
        try:
            return self._labels_from_page_number[page_number]
        except KeyError:
            raise KeyError('Page number ".../{}" not in range.'
                           .format(page_number))

    @staticmethod
    def _get_from_label(mapping_dict: Dict[str, Any],
                        label: Union[int, str]) -> Any:
        """Helper function to get info from label."""
        # Convert label to string if an integer is passed.
        if isinstance(label, int):
            label = str(label)

        try:
            return mapping_dict[label]
        except KeyError:
            raise KeyError('No page has label: "{}".'.format(label))

    @check_if_cached
    def get_page_number_from_label(self, label: str = '1') -> str:
        """Return page number from page label.

        There is a 1-to-many correspondence (a label can be the same for
        several pages).

        :return: set containing page numbers corresponding to page label.
        """
        return self._get_from_label(self._page_numbers_from_label, label)

    @check_if_cached
    def get_page_from_label(self, label: str = '1') -> str:
        """Return page number from page label.

        There is a 1-to-many correspondence (a label can be the same for
        several pages).

        :return: set containing pages corresponding to page label.
        """
        return self._get_from_label(self._pages_from_label, label)

    @check_if_cached
    def get_page(self, page_number: int) -> 'pywikibot.page.Page':
        """Return a page object from page number."""
        try:
            return self._page_from_numbers[page_number]
        except KeyError:
            raise KeyError('Invalid page number: {}.'.format(page_number))

    @check_if_cached
    def pages(self) -> List['pywikibot.page.Page']:
        """Return the list of pages in Index, sorted by page number.

        :return: list of pages
        """
        return [self._page_from_numbers[i]
                for i in range(1, self.num_pages + 1)]

    @check_if_cached
    def get_number(self, page: 'pywikibot.page.Page') -> int:
        """Return a page number from page object."""
        try:
            return self._numbers_from_page[page]
        except KeyError:
            raise KeyError('Invalid page: {}.'.format(page))
