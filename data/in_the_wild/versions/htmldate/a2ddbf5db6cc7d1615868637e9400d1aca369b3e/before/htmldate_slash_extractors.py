# pylint:disable-msg=E0611,I1101
"""
Custom parsers and XPath expressions for date extraction
"""
## This file is available from https://github.com/adbar/htmldate
## under GNU GPL v3 license

# standard
import datetime
import logging
import re

from functools import lru_cache

# conditional imports with fallbacks for compatibility
# coverage for date parsing
#try:
import dateparser  # third-party, slow
EXTERNAL_PARSER = dateparser.DateDataParser(settings={
    'PREFER_DAY_OF_MONTH': 'first', 'PREFER_DATES_FROM': 'past',
    'DATE_ORDER': 'DMY',
})

# potential regex speedup
#try:
import regex
#except ImportError:
#    regex = re

# allow_redetect_language=False, languages=['de', 'en'],
#EXTERNAL_PARSER_CONFIG = {
#    'PREFER_DAY_OF_MONTH': 'first', 'PREFER_DATES_FROM': 'past',
#    'DATE_ORDER': 'DMY'
#}
#except ImportError:
#    # try dateutil parser
#    from dateutil.parser import parse as FULL_PARSE
#    EXTERNAL_PARSER = None
#    DEFAULT_PARSER_PARAMS = {'dayfirst': True, 'fuzzy': False}
#else:
#FULL_PARSE = DEFAULT_PARSER_PARAMS = None
# iso date parsing speedup
try:
    from ciso8601 import parse_datetime, parse_datetime_as_naive
except ImportError:
    #if not FULL_PARSE:
    from dateutil.parser import parse as FULL_PARSE
    parse_datetime = parse_datetime_as_naive = FULL_PARSE  # shortcut

# own
from .validators import convert_date, date_validator

LOGGER = logging.getLogger(__name__)

DATE_EXPRESSIONS = [
    """.//*[contains(@id, 'date') or contains(@id, 'Date') or
    contains(@id, 'datum') or contains(@id, 'Datum') or contains(@id, 'time')
    or contains(@class, 'post-meta-time')]""",
    """.//*[contains(@class, 'date') or contains(@class, 'Date')
    or contains(@class, 'datum') or contains(@class, 'Datum')]""",
    """.//*[contains(@class, 'postmeta') or contains(@class, 'post-meta')
    or contains(@class, 'entry-meta') or contains(@class, 'entry-date') or contains(@class, 'postMeta')
    or contains(@class, 'post_meta') or contains(@class, 'post__meta') or
    contains(@class, 'article__date') or contains(@class, 'post_detail') or @class='meta'
    or @class='meta-before' or @class='asset-meta' or
    contains(@id, 'article-metadata') or contains(@class, 'article-metadata')
    or contains(@class, 'block-content') or contains(@class, 'byline') or
    contains(@class, 'dateline') or contains(@class, 'subline')
    or contains(@class, 'published') or contains(@class, 'posted') or
    contains(@class, 'submitted') or contains(@class, 'updated') or contains(@class, 'created-post')
    or contains(@id, 'post-timestamp') or contains(@class, 'post-timestamp')]""",
    """.//*[contains(@id, 'lastmod') or contains(@itemprop, 'date') or
    contains(@class, 'time') or contains(@id, 'metadata') or contains(@id, 'publish')]""",
    ".//footer|.//*[@class='post-footer' or @class='footer' or @id='footer']",
    ".//small",
    """.//*[contains(@class, 'author') or contains(@class, 'autor') or
    contains(@class, 'field-content') or @class='meta' or
    contains(@class, 'info') or contains(@class, 'fa-clock-o') or contains(@class, 'fa-calendar') or
    contains(@class, 'publication')]""",
]

# supply more expressions for more languages
ADDITIONAL_EXPRESSIONS = [
    ".//*[contains(@class, 'fecha') or contains(@class, 'parution')]",
]

# discard parts of the webpage
DISCARD_EXPRESSIONS = [
    './/footer',
    './/*[(self::div or self::section)][@id="footer" or @class="footer"]',
]

# Regex cache
MDY_PATTERN = re.compile(r'''(
January|February|March|April|May|June|July|August|September|October|November|December|
Januari|Februari|Maret|Mei|Juni|Juli|Agustus|Oktober|Desember|
Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
Januar|Jänner|Februar|Feber|März|Mai|Dezember|
janvier|février|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|décembre|
Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık|
Oca|Şub|Mar|Nis|Haz|Tem|Ağu|Eyl|Eki|Kas|Ara
) ([0-9]{1,2})(st|nd|rd|th)?,? ([0-9]{4})'''.replace('\n', ''))
DMY_PATTERN = re.compile(r'''([0-9]{1,2})(st|nd|rd|th)? (of )?(
January|February|March|April|May|June|July|August|September|October|November|December|
Januari|Februari|Maret|Mei|Juni|Juli|Agustus|Oktober|Desember|
Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
Januar|Jänner|Februar|Feber|März|Mai|Dezember|
janvier|février|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|décembre|
Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık|
Oca|Şub|Mar|Nis|Haz|Tem|Ağu|Eyl|Eki|Kas|Ara
),? ([0-9]{4})'''.replace('\n', ''))
ENGLISH_DATE = re.compile(r'([0-9]{1,2})/([0-9]{1,2})/([0-9]{2,4})')
COMPLETE_URL = re.compile(r'([0-9]{4})[/-]([0-9]{1,2})[/-]([0-9]{1,2})')
PARTIAL_URL = re.compile(r'/([0-9]{4})/([0-9]{1,2})/')
YMD_PATTERN = re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2})')
DATESTUB_PATTERN = re.compile(r'([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{2,4})')
GERMAN_TEXTSEARCH = re.compile(r'''([0-9]{1,2})\.? (Januar|Jänner|Februar|Feber|März|April|
Mai|Juni|Juli|August|September|Oktober|November|Dezember) ([0-9]{4})'''.replace('\n', ''))
GENERAL_TEXTSEARCH = re.compile(r'''
January|February|March|April|May|June|July|August|September|October|November|December|
Januari|Februari|Maret|Mei|Juni|Juli|Agustus|Oktober|Desember|
Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
Januar|Jänner|Februar|Feber|März|Mai|Dezember|
janvier|février|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|décembre|
Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık|
Oca|Şub|Mar|Nis|Haz|Tem|Ağu|Eyl|Eki|Kas|Ara'''.replace('\n', ''))
JSON_PATTERN_MODIFIED = \
  re.compile(r'"dateModified": ?"([0-9]{4}-[0-9]{2}-[0-9]{2})')
JSON_PATTERN_PUBLISHED = \
  re.compile(r'"datePublished": ?"([0-9]{4}-[0-9]{2}-[0-9]{2})')
TIMESTAMP_PATTERN = regex.compile(r'([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{2}\.[0-9]{2}\.[0-9]{4}).[0-9]{2}:[0-9]{2}:[0-9]{2}')

# English + German + Turkish dates cache
TEXT_MONTHS = {
    # January
    'Januar': '01', 'Jänner': '01', 'January': '01', 'Januari': '01', 'Jan': '01',
    'Ocak': '01', 'Oca': '01', 'janvier': '01',
    # February
    'Februar': '02', 'Feber': '02', 'February': '02', 'Februari': '02', 'Feb': '02',
    'Şubat': '02', 'Şub': '02', 'février': '02',
    # March
    'März': '03', 'March': '03', 'Maret': '03', 'Mar': '03', 'Mart': '03', 'mars': '03',
    # April
    'April': '04', 'Apr': '04', 'Nisan': '04', 'Nis': '04', 'avril': '04',
    # May
    'Mai': '05', 'May': '05', 'Mei': '05', 'Mayıs': '05', 'mai': '05',
    # June
    'Juni': '06', 'June': '06', 'Jun': '06', 'Haziran': '06', 'Haz': '06', 'juin': '06',
    # July
    'Juli': '07', 'July': '07', 'Jul': '07', 'Temmuz': '07', 'Tem': '07', 'juillet': '07',
    # August
    'August': '08', 'Agustus': '08', 'Aug': '08', 'Ağustos': '08', 'Ağu': '08', 'aout': '08',
    # September
    'September': '09', 'Sep': '09', 'Eylül': '09', 'Eyl': '09', 'septembre': '09',
    # October
    'Oktober': '10', 'October': '10', 'Oct': '10', 'Ekim': '10', 'Eki': '10', 'octobre': '10',
    # November
    'November': '11', 'Nov': '11', 'Kasım': '11', 'Kas': '11', 'novembre': '11',
    # December
    'Dezember': '12', 'December': '12', 'Desember': '12', 'Dec': '12', 'Aralık': '12',
    'Ara': '12', 'décembre': '12'
}

TEXT_DATE_PATTERN = re.compile(r'[.:,_/ -]|^[0-9]+$')
NO_TEXT_DATE_PATTERN = re.compile(r'[0-9]{3,}\D+[0-9]{3,}|[0-9]{2}:[0-9]{2}(:| )|\D*[0-9]{4}\D*$')

# use of regex module for speed
EN_PATTERNS = regex.compile(r'(?:[Dd]ate[^0-9"]{,20}|updated|published) *?(?:in)? *?:? *?([0-9]{1,4})[./]([0-9]{1,2})[./]([0-9]{2,4})', re.I)
DE_PATTERNS = regex.compile(r'(?:Datum|Stand): ?([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{2,4})')
TR_PATTERNS = regex.compile(r'''(?:güncellen?me|yayı(?:m|n)lan?ma) *?(?:tarihi)? *?:? *?([0-9]{1,2})[./]([0-9]{1,2})[./]([0-9]{2,4})|
([0-9]{1,2})[./]([0-9]{1,2})[./]([0-9]{2,4}) *?(?:'de|'da|'te|'ta|’de|’da|’te|’ta|tarihinde) *(?:güncellendi|yayı(?:m|n)landı)'''.replace('\n', ''), re.I)

# extensive search patterns
YEAR_PATTERN = re.compile(r'^\D?(199[0-9]|20[0-9]{2})')
COPYRIGHT_PATTERN = re.compile(r'(?:©|\&copy;|Copyright|\(c\))\D*(?:[12][0-9]{3}-)?([12][0-9]{3})\D')
THREE_PATTERN = re.compile(r'/([0-9]{4}/[0-9]{2}/[0-9]{2})[01/]')
THREE_CATCH = re.compile(r'([0-9]{4})/([0-9]{2})/([0-9]{2})')
THREE_LOOSE_PATTERN = re.compile(r'\D([0-9]{4}[/.-][0-9]{2}[/.-][0-9]{2})\D')
THREE_LOOSE_CATCH = re.compile(r'([0-9]{4})[/.-]([0-9]{2})[/.-]([0-9]{2})')
SELECT_YMD_PATTERN = re.compile(r'\D([0-3]?[0-9][/.-][01]?[0-9][/.-][0-9]{4})\D')
SELECT_YMD_YEAR = re.compile(r'(19[0-9]{2}|20[0-9]{2})\D?$')
YMD_YEAR = re.compile(r'^([0-9]{4})')
DATESTRINGS_PATTERN = re.compile(r'(\D19[0-9]{2}[01][0-9][0-3][0-9]\D|\D20[0-9]{2}[01][0-9][0-3][0-9]\D)')
DATESTRINGS_CATCH = re.compile(r'([12][0-9]{3})([01][0-9])([0-3][0-9])')
SLASHES_PATTERN = re.compile(r'\D([0-3]?[0-9][/.][01]?[0-9][/.][0129][0-9])\D')
SLASHES_YEAR = re.compile(r'([0-9]{2})$')
YYYYMM_PATTERN = re.compile(r'\D([12][0-9]{3}[/.-][01][0-9])\D')
YYYYMM_CATCH = re.compile(r'([12][0-9]{3})[/.-]([01][0-9])')
MMYYYY_PATTERN = re.compile(r'\D([01]?[0-9][/.-][12][0-9]{3})\D')
MMYYYY_YEAR = re.compile(r'([12][0-9]{3})\D?$')
SIMPLE_PATTERN = re.compile(r'\D(199[0-9]|20[0-9]{2})\D')


def discard_unwanted(tree):
    '''Delete unwanted sections of an HTML document and return them as a list'''
    my_discarded = []
    for expr in DISCARD_EXPRESSIONS:
        for subtree in tree.xpath(expr):
            my_discarded.append(subtree)
            subtree.getparent().remove(subtree)
    return tree, my_discarded


def extract_url_date(testurl, outputformat):
    """Extract the date out of an URL string complying with the Y-M-D format"""
    match = COMPLETE_URL.search(testurl)
    if match:
        dateresult = match.group(0)
        LOGGER.debug('found date in URL: %s', dateresult)
        try:
            dateobject = datetime.datetime(int(match.group(1)),
                                           int(match.group(2)),
                                           int(match.group(3)))
            if date_validator(dateobject, outputformat) is True:
                return dateobject.strftime(outputformat)
        except ValueError as err:
            LOGGER.debug('conversion error: %s %s', dateresult, err)
    return None


def extract_partial_url_date(testurl, outputformat):
    """Extract an approximate date out of an URL string in Y-M format"""
    match = PARTIAL_URL.search(testurl)
    if match:
        dateresult = match.group(0) + '/01'
        LOGGER.debug('found partial date in URL: %s', dateresult)
        try:
            dateobject = datetime.datetime(int(match.group(1)),
                                           int(match.group(2)),
                                           1)
            if date_validator(dateobject, outputformat) is True:
                return dateobject.strftime(outputformat)
        except ValueError as err:
            LOGGER.debug('conversion error: %s %s', dateresult, err)
    return None


def regex_parse(string):
    """Full-text parse using a series of regular expressions"""
    dateobject = None
    dateobject = regex_parse_de(string)
    if dateobject is None:
        dateobject = regex_parse_multilingual(string)
    return dateobject


def regex_parse_de(string):
    """Try full-text parse for German date elements"""
    # text match
    match = GERMAN_TEXTSEARCH.search(string)
    if not match:
        return None
    # second element
    secondelem = TEXT_MONTHS[match.group(2)]
    # process and return
    try:
        dateobject = datetime.date(int(match.group(3)),
                                   int(secondelem),
                                   int(match.group(1)))
    except ValueError:
        return None
    LOGGER.debug('German text parse: %s', dateobject)
    return dateobject


def regex_parse_multilingual(string):
    """Try full-text parse for English date elements"""
    # https://github.com/vi3k6i5/flashtext ?
    # numbers
    match = ENGLISH_DATE.search(string)
    if match:
        day, month, year = match.group(2), match.group(1), match.group(3)
    else:
        # general search
        if not GENERAL_TEXTSEARCH.search(string):
            return None
        # American English
        match = MDY_PATTERN.search(string)
        if match:
            day, month, year = match.group(2), TEXT_MONTHS[match.group(1)], \
                               match.group(4)
        # multilingual day-month-year pattern
        else:
            match = DMY_PATTERN.search(string)
            if match:
                day, month, year = match.group(1), TEXT_MONTHS[match.group(4)], \
                                   match.group(5)
            else:
                return None
    # process and return
    if len(year) == 2:
        year = '20' + year
    try:
        dateobject = datetime.date(int(year), int(month), int(day))
    except ValueError:
        return None
    LOGGER.debug('English text parse: %s', dateobject)
    return dateobject


def custom_parse(string, outputformat, extensive_search, min_date, max_date):
    """Try to bypass the slow dateparser"""
    LOGGER.debug('custom parse test: %s', string)
    # '201709011234' not covered by dateparser # regex was too slow
    if string[0:8].isdigit():
        try:
            candidate = datetime.date(int(string[:4]),
                                      int(string[4:6]),
                                      int(string[6:8]))
        except ValueError:
            return None
        if date_validator(candidate, '%Y-%m-%d') is True:
            LOGGER.debug('ymd match: %s', candidate)
            return convert_date(candidate, '%Y-%m-%d', outputformat)
    # much faster
    if string[0:4].isdigit():
        # try speedup with ciso8601 (if installed)
        try:
            if extensive_search is True:
                result = parse_datetime(string)
            # speed-up by ignoring time zone info if ciso8601 is installed
            else:
                result = parse_datetime_as_naive(string)
            if date_validator(result, outputformat, earliest=min_date, latest=max_date) is True:
                LOGGER.debug('parsing result: %s', result)
                return result.strftime(outputformat)
        except (OverflowError, TypeError, ValueError):
            LOGGER.debug('parsing error: %s', string)
    # %Y-%m-%d search
    match = YMD_PATTERN.search(string)
    if match:
        try:
            candidate = datetime.date(int(match.group(1)),
                                      int(match.group(2)),
                                      int(match.group(3)))
        except ValueError:
            LOGGER.debug('value error: %s', match.group(0))
        else:
            if date_validator(candidate, '%Y-%m-%d') is True:
                LOGGER.debug('ymd match: %s', candidate)
                return convert_date(candidate, '%Y-%m-%d', outputformat)
    # faster than fire dateparser at once
    datestub = DATESTUB_PATTERN.search(string)
    if datestub and len(datestub.group(3)) in (2, 4):
        try:
            if len(datestub.group(3)) == 2:
                candidate = datetime.date(int('20' + datestub.group(3)),
                                          int(datestub.group(2)),
                                          int(datestub.group(1)))
            elif len(datestub.group(3)) == 4:
                candidate = datetime.date(int(datestub.group(3)),
                                          int(datestub.group(2)),
                                          int(datestub.group(1)))
        except ValueError:
            LOGGER.debug('value error: %s', datestub.group(0))
        else:
            # test candidate
            if date_validator(candidate, '%Y-%m-%d') is True:
                LOGGER.debug('D.M.Y match: %s', candidate)
                return convert_date(candidate, '%Y-%m-%d', outputformat)
    # text match
    dateobject = regex_parse(string)
    # copyright match?
    #if dateobject is None:
    # © Janssen-Cilag GmbH 2014-2019. https://www.krebsratgeber.de/artikel/was-macht-eine-zelle-zur-krebszelle
    # examine
    if dateobject is not None:
        try:
            if date_validator(dateobject, outputformat) is True:
                LOGGER.debug('custom parse result: %s', dateobject)
                return dateobject.strftime(outputformat)
        except ValueError as err:
            LOGGER.debug('value error during conversion: %s %s', string, err)
    return None


def external_date_parser(string, outputformat):
    """Use dateutil parser or dateparser module according to system settings"""
    LOGGER.debug('send to external parser: %s', string)
    try:
        # dateparser installed or not
        #if EXTERNAL_PARSER is not None:
        target = EXTERNAL_PARSER.get_date_data(string)['date_obj']
        #else:
        #    target = FULL_PARSE(string, **DEFAULT_PARSER_PARAMS)
    # 2 types of errors possible
    except (OverflowError, ValueError):
        target = None
    # issue with data type
    if target is not None:
        return datetime.date.strftime(target, outputformat)
    return None


@lru_cache(maxsize=32)
def try_ymd_date(string, outputformat, extensive_search, min_date, max_date):
    """Use a series of heuristics and rules to parse a potential date expression"""
    # discard on formal criteria
    # list(filter(str.isdigit, string))
    if not string or len(string) < 6:
        return None
    digits_num = len([c for c in string if c.isdigit()])
    if not 4 <= digits_num <= 18:
        return None
    # just time/single year or digits, not a date
    if not TEXT_DATE_PATTERN.search(string) or NO_TEXT_DATE_PATTERN.match(string):
        return None
    # faster
    customresult = custom_parse(string, outputformat, extensive_search, min_date, max_date)
    if customresult is not None:
        return customresult
    # slow but extensive search
    if extensive_search is True:
        # send to date parser
        dateparser_result = external_date_parser(string, outputformat)
        if dateparser_result is not None:
            if date_validator(dateparser_result, outputformat, earliest=min_date, latest=max_date):
                return dateparser_result
    return None


def img_search(tree, outputformat, min_date, max_date):
    '''Skim through image elements'''
    element = tree.find('.//meta[@property="og:image"]')
    if element is not None and 'content' in element.attrib:
        result = extract_url_date(element.get('content'), outputformat)
        if result is not None and date_validator(result, outputformat, earliest=min_date, latest=max_date) is True:
            return result
    return None


def json_search(tree, outputformat, original_date, min_date, max_date):
    '''Look for JSON time patterns in JSON sections of the tree'''
    # determine pattern
    if original_date is True:
        json_pattern = JSON_PATTERN_PUBLISHED
    else:
        json_pattern = JSON_PATTERN_MODIFIED
    # look throughout the HTML tree
    for elem in tree.xpath('.//script[@type="application/ld+json"]|//script[@type="application/settings+json"]'):
        if not elem.text or not '"date' in elem.text:
            continue
        json_match = json_pattern.search(elem.text)
        if json_match and date_validator(json_match.group(1), '%Y-%m-%d', earliest=min_date, latest=max_date):
            LOGGER.debug('JSON time found: %s', json_match.group(0))
            return convert_date(json_match.group(1), '%Y-%m-%d', outputformat)
    return None


def timestamp_search(htmlstring, outputformat, min_date, max_date):
    '''Look for timestamps throughout the web page'''
    tstamp_match = TIMESTAMP_PATTERN.search(htmlstring)
    if tstamp_match and date_validator(tstamp_match.group(1), '%Y-%m-%d', earliest=min_date, latest=max_date):
        LOGGER.debug('time regex found: %s', tstamp_match.group(0))
        return convert_date(tstamp_match.group(1), '%Y-%m-%d', outputformat)
    return None


def extract_idiosyncrasy(idiosyncrasy, htmlstring, outputformat, min_date, max_date):
    '''Look for a precise pattern throughout the web page'''
    candidate = None
    match = idiosyncrasy.search(htmlstring)
    groups = [0, 1, 2, 3] if match and match.group(3) else [] #because len(None) has no len
    try:
        groups = [0, 4, 5, 6] if match and match.group(6) else groups #because len(None) has no len
    except IndexError:
        pass
    if match and groups: #because len(None) has no len
        if match.group(1) is not None and len(match.group(1)) == 4:
            candidate = datetime.date(int(match.group(groups[1])),
                                      int(match.group(groups[2])),
                                      int(match.group(groups[3])))
        elif len(match.group(groups[3])) in (2, 4):
            # switch to MM/DD/YY
            if int(match.group(groups[2])) > 12:
                tmp1, tmp2 = groups[1], groups[2]
                groups[1], groups[2] = tmp2, tmp1
            # DD/MM/YY
            try:
                if len(match.group(groups[3])) == 2:
                    candidate = datetime.date(int('20' + match.group(groups[3])),
                                              int(match.group(groups[2])),
                                              int(match.group(groups[1])))
                else:
                    candidate = datetime.date(int(match.group(groups[3])),
                                              int(match.group(groups[2])),
                                              int(match.group(groups[1])))
            except ValueError:
                LOGGER.debug('value error in idiosyncrasies: %s', match.group(0))
    if candidate is not None:
        if date_validator(candidate, '%Y-%m-%d', earliest=min_date, latest=max_date) is True:
            LOGGER.debug('idiosyncratic pattern found: %s', match.group(0))
            return convert_date(candidate, '%Y-%m-%d', outputformat)
    return None


def idiosyncrasies_search(htmlstring, outputformat, min_date, max_date):
    '''Look for author-written dates throughout the web page'''
    result = None
    # DE
    result = extract_idiosyncrasy(DE_PATTERNS, htmlstring, outputformat, min_date, max_date)
    # EN
    if result is None:
        result = extract_idiosyncrasy(EN_PATTERNS, htmlstring, outputformat, min_date, max_date)
    # TR
    if result is None:
        result = extract_idiosyncrasy(TR_PATTERNS, htmlstring, outputformat, min_date, max_date)
    return result
