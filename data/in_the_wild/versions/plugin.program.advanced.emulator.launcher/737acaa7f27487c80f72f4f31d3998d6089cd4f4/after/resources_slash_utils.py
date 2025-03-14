# -*- coding: utf-8 -*-
# Advanced Emulator Launcher miscellaneous functions
#

# Copyright (c) 2016 Wintermute0110 <wintermute0110@gmail.com>
# Portions (c) 2010-2015 Angelscry and others
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

#
# Utility functions which does not depend on Kodi modules (except log_* functions)
#

# --- Python standard library ---
from __future__ import unicode_literals
import sys, os, shutil, time, random, hashlib, urlparse, re, string, fnmatch

# --- AEL modules ---
# >> utils.py and utils_kodi.py must not depend on any other AEL module to avoid circular dependencies.

# -------------------------------------------------------------------------------------------------
# Strings and text
# -------------------------------------------------------------------------------------------------
#
# If max_length == -1 do nothing (no length limit).
#
def text_limit_string(string, max_length):
  if max_length > 5 and len(string) > max_length:
    string = string[0:max_length-3] + '...'

  return string

# Some XML encoding of special characters:
#   {'\n': '&#10;', '\r': '&#13;', '\t':'&#9;'}
#
# See http://stackoverflow.com/questions/1091945/what-characters-do-i-need-to-escape-in-xml-documents
# See https://wiki.python.org/moin/EscapingXml
# See https://github.com/python/cpython/blob/master/Lib/xml/sax/saxutils.py
# See http://stackoverflow.com/questions/2265966/xml-carriage-return-encoding
#
def text_escape_XML(data_str):
    # Ampersand MUST BE replaced FIRST
    data_str = data_str.replace('&', '&amp;')
    data_str = data_str.replace('>', '&gt;')
    data_str = data_str.replace('<', '&lt;')

    data_str = data_str.replace("'", '&apos;')
    data_str = data_str.replace('"', '&quot;')
    
    # --- Unprintable characters ---
    data_str = data_str.replace('\n', '&#10;')
    data_str = data_str.replace('\r', '&#13;')
    data_str = data_str.replace('\t', '&#9;')

    return data_str

def text_unescape_XML(data_str):
    data_str = data_str.replace('&quot;', '"')
    data_str = data_str.replace('&apos;', "'")

    data_str = data_str.replace('&lt;', '<')
    data_str = data_str.replace('&gt;', '>')
    # Ampersand MUST BE replaced LAST
    data_str = data_str.replace('&amp;', '&')
    
    # --- Unprintable characters ---
    data_str = data_str.replace('&#10;', '\n')
    data_str = data_str.replace('&#13;', '\r')
    data_str = data_str.replace('&#9;', '\t')
    
    return data_str

def text_unescape_HTML(s):
    # >> Replace single HTML characters by their Unicode equivalent
    s = s.replace('<br>',   ' ')
    s = s.replace('<br />', ' ')
    s = s.replace('&lt;',   '<')
    s = s.replace('&gt;',   '>')
    s = s.replace('&quot;', '"')
    s = s.replace('&nbsp;', ' ')
    s = s.replace('&amp;',  '&') # Must be done last
    
    # >> Complex HTML entities. Single HTML chars must be already replaced.
    s = s.replace('&#039;', "'")
    s = s.replace('&#x26;', '&')
    s = s.replace('&#x27;', "'")

    # >> Remove HTML tags
    p = re.compile(r'<.*?>')
    s = p.sub('', s)

    return s

def text_dump_str_to_file(filename, full_string):
    file_obj = open(filename, 'w')
    file_obj.write(full_string.encode('utf-8'))
    file_obj.close()

# -------------------------------------------------------------------------------------------------
# ROM name cleaning and formatting
# -------------------------------------------------------------------------------------------------
#
# This function is used to clean the ROM name to be used as search string for the scraper.
#
# 1) Cleans ROM tags: [BIOS], (Europe), (Rev A), ...
# 2) Substitutes some characters by spaces
#
def text_format_ROM_name_for_scraping(title):
    title = re.sub('\[.*?\]', '', title)
    title = re.sub('\(.*?\)', '', title)
    title = re.sub('\{.*?\}', '', title)
    
    title = title.replace('_', '')
    title = title.replace('-', '')
    title = title.replace(':', '')
    title = title.replace('.', '')
    title = title.strip()

    return title

# def text_ROM_base_filename(filename):
#     filename = re.sub('(\[.*?\]|\(.*?\)|\{.*?\})', '', filename)
#     filename = re.sub('(\.|-| |_)cd\d+$', '', filename)
#
#     return filename.rstrip()

#
# Format ROM file name when scraping is disabled.
# 1) Remove No-Intro/TOSEC tags (), [], {} at the end of the file
#
def text_format_ROM_title(title, clean_tags):
    #
    # Regexp to decompose a string in tokens
    #
    reg_exp = '\[.+?\]\s?|\(.+?\)\s?|\{.+?\}|[^\[\(\{]+'
    if clean_tags:
        tokens = re.findall(reg_exp, title)
        str_list = []
        for token in tokens:
            stripped_token = token.strip()
            if (stripped_token[0] == '[' or stripped_token[0] == '(' or stripped_token[0] == '{') and \
               stripped_token != '[BIOS]':
                continue
            str_list.append(stripped_token)
        cleaned_title = ' '.join(str_list)
    else:
        cleaned_title = title

    # if format_title:
    #     if (title.startswith("The ")): new_title = title.replace("The ","", 1)+", The"
    #     if (title.startswith("A ")): new_title = title.replace("A ","", 1)+", A"
    #     if (title.startswith("An ")): new_title = title.replace("An ","", 1)+", An"
    # else:
    #     if (title.endswith(", The")): new_title = "The "+"".join(title.rsplit(", The", 1))
    #     if (title.endswith(", A")): new_title = "A "+"".join(title.rsplit(", A", 1))
    #     if (title.endswith(", An")): new_title = "An "+"".join(title.rsplit(", An", 1))

    return cleaned_title

# -------------------------------------------------------------------------------------------------
# URLs
# -------------------------------------------------------------------------------------------------
#
# Get extension of URL. Returns '' if not found.
#
def text_get_URL_extension(url):
    path = urlparse.urlparse(url).path
    ext = os.path.splitext(path)[1]
    
    return ext

#
# Defaults to .jpg if URL extension cannot be determined
#
def text_get_image_URL_extension(url):
    path = urlparse.urlparse(url).path
    ext = os.path.splitext(path)[1]
    ret = '.jpg' if ext == '' else ext

    return ret

# -------------------------------------------------------------------------------------------------
# Misc stuff
# -------------------------------------------------------------------------------------------------
#
# Given the image path, image filename with no extension and a list of file extensions search for a file.
#
# rootPath       -> FileName object
# filename_noext -> Unicode string
# file_exts      -> list of extenstions with no dot [ 'zip', 'rar' ]
#
# Returns a FileName object.
#
def misc_look_for_file(rootPath, filename_noext, file_exts):
    for ext in file_exts:
        file_path = rootPath + filename_noext + '.' + ext
        if file_path.exists():
            return file_path

    return None

#
# Generates a random an unique MD5 hash and returns a string with the hash
#
def misc_generate_random_SID():
    t1 = time.time()
    t2 = t1 + random.getrandbits(32)
    base = hashlib.md5( str(t1 + t2) )
    sid = base.hexdigest()

    return sid

# -------------------------------------------------------------------------------------------------
# Filesystem helper class
# This class always takes and returns Unicode string paths. Decoding to UTF-8 must be done in
# caller code.
# A) Transform paths like smb://server/directory/ into \\server\directory\
# B) Use xbmc.translatePath() for paths starting with special://
# -------------------------------------------------------------------------------------------------
class FileName:
    # pathString must be a Unicode string object
    def __init__(self, pathString):
        self.originalPath = pathString
        self.path         = pathString
        
        # --- Path transformation ---
        if self.originalPath.lower().startswith('smb:'):
            self.path = self.path.replace('smb:', '')
            self.path = self.path.replace('SMB:', '')
            self.path = self.path.replace('//', '\\\\')
            self.path = self.path.replace('/', '\\')

        elif self.originalPath.lower().startswith('special:'):
            self.path = xbmc.translatePath(self.path)

    def _join_raw(self, arg):
        self.path         = os.path.join(self.path, arg)
        self.originalPath = os.path.join(self.originalPath, arg)

        return self

    # Appends a string to path. Returns self FileName object
    def append(self, arg):
        self.path         = self.path + arg
        self.originalPath = self.originalPath + arg

        return self

    # Behaves like os.path.join(). Returns a FileName object
    def join(self, *args):
        child = FileName(self.originalPath)
        for arg in args:
            child._join_raw(arg)

        return child

    # Behaves like os.path.join()
    #
    # See http://blog.teamtreehouse.com/operator-overloading-python
    # other is a FileName object. other originalPath is expected to be a subdirectory (path
    # transformation not required)
    def __add__(self, other):
        current_path = self.originalPath
        if type(other) is FileName:  other_path = other.originalPath
        elif type(other) is unicode: other_path = other
        elif type(other) is str:     other_path = other.decode('utf-8')
        else: raise NameError('Unknown type for overloaded + in FileName object')
        new_path = os.path.join(current_path, other_path)
        child    = FileName(new_path)

        return child

    def escapeQuotes(self):
        self.path = self.path.replace("'", "\\'")
        self.path = self.path.replace('"', '\\"')

    # ---------------------------------------------------------------------------------------------
    # Decomposes a file name path or directory into its constituents
    #   FileName.getPath()            Full path                                     /home/Wintermute/Sonic.zip
    #   FileName.getPath_noext()      Full path with no extension                   /home/Wintermute/Sonic
    #   FileName.getDirname()         Directory name of file. Does not end in '/'   /home/Wintermute/
    #   FileName.getBasename()        File name with no path                        Sonic.zip
    #   FileName.getBasename_noext()  File name with no path and no extension       Sonic
    #   FileName.getExt()             File extension                                .zip
    # ---------------------------------------------------------------------------------------------
    def getPath(self):
        return self.path

    def getOriginalPath(self):
        return self.originalPath

    def getPath_noext(self):
        root, ext = os.path.splitext(self.path)

        return root

    def getDirname(self):
        return os.path.dirname(self.path)

    def getBasename(self):
        return os.path.basename(self.path)

    def getBasename_noext(self):
        basename  = os.path.basename(self.path)
        root, ext = os.path.splitext(basename)
        
        return root

    def getExt(self):
        root, ext = os.path.splitext(self.path)
        
        return ext

    # ---------------------------------------------------------------------------------------------
    # Scanner functions
    # ---------------------------------------------------------------------------------------------
    def scanFilesInPath(self, mask):
        files = []
        filenames = os.listdir(self.path)
        for filename in fnmatch.filter(filenames, mask):
            files.append(os.path.join(self.path, filename))

        return files

    def scanFilesInPathAsPaths(self, mask):
        files = []
        filenames = os.listdir(self.path)
        for filename in fnmatch.filter(filenames, mask):
            files.append(FileName(os.path.join(self.path, filename)))

        return files

    def recursiveScanFilesInPath(self, mask):
        files = []
        for root, dirs, foundfiles in os.walk(self.path):
            for filename in fnmatch.filter(foundfiles, mask):
                files.append(os.path.join(root, filename))

        return files

    # ---------------------------------------------------------------------------------------------
    # Filesystem functions
    # ---------------------------------------------------------------------------------------------
    def stat(self):
        return os.stat(self.path)

    def exists(self):
        return os.path.exists(self.path)

    def isdir(self):
        return os.path.isdir(self.path)
        
    def isfile(self):
        return os.path.isfile(self.path)

    def makedirs(self):
        if not os.path.exists(self.path): 
            os.makedirs(self.path)

    # os.remove() and os.unlink() are exactly the same.
    def unlink(self):
        os.unlink(self.path)

    def rename(self, to):
        os.rename(self.path, to.getPath())

# -------------------------------------------------------------------------------------------------
# Utilities to test scrapers
# -------------------------------------------------------------------------------------------------
ID_LENGTH     = 60
NAME_LENGTH   = 60
GENRE_LENGTH  = 20
YEAR_LENGTH   = 4
STUDIO_LENGTH = 20
PLOT_LENGTH   = 70
URL_LENGTH    = 62

def print_scraper_list(scraper_obj_list):
    print('Scraper name')
    print('--------------------------------')
    for scraper_obj in scraper_obj_list:
        print('{0}'.format(scraper_obj.name))
    print('')

# PUT functions to print things returned by Scraper object (which are common to all scrapers)
# into util.py, to be resused by all scraper tests.
def print_games_search(results):
    print('\nFound {0} game/s'.format(len(results)))
    print("{0} {1}".format('Display name'.ljust(NAME_LENGTH), 'Id'.ljust(ID_LENGTH)))
    print("{0} {1}".format('-'*NAME_LENGTH, '-'*ID_LENGTH))
    for game in results:
        display_name = text_limit_string(game['display_name'], NAME_LENGTH)
        id           = text_limit_string(game['id'], ID_LENGTH)
        print("{0} {1}".format(display_name.ljust(NAME_LENGTH), id.ljust(ID_LENGTH)))
    print('')

def print_game_metadata(scraperObj, results):
    # --- Get metadata of first game ---
    if results:
        metadata = scraperObj.get_metadata(results[0])

        title  = text_limit_string(metadata['title'], NAME_LENGTH)
        genre  = text_limit_string(metadata['genre'], GENRE_LENGTH)
        year   = metadata['year']
        studio = text_limit_string(metadata['studio'], STUDIO_LENGTH)
        plot   = text_limit_string(metadata['plot'], PLOT_LENGTH)
        print('\nDisplaying metadata for title "{0}"'.format(title))
        print("{0} {1} {2} {3} {4}".format('Title'.ljust(NAME_LENGTH), 'Genre'.ljust(GENRE_LENGTH), 
                                           'Year'.ljust(YEAR_LENGTH), 'Studio'.ljust(STUDIO_LENGTH),
                                           'Plot'.ljust(PLOT_LENGTH)))
        print("{0} {1} {2} {3} {4}".format('-'*NAME_LENGTH, '-'*GENRE_LENGTH, '-'*YEAR_LENGTH, 
                                           '-'*STUDIO_LENGTH, '-'*PLOT_LENGTH))
        print("{0} {1} {2} {3} {4}".format(title.ljust(NAME_LENGTH), genre.ljust(GENRE_LENGTH), 
                                           year.ljust(YEAR_LENGTH), studio.ljust(STUDIO_LENGTH),
                                           plot.ljust(PLOT_LENGTH)))

def print_game_image_list(scraperObj, results, asset_kind):
    # --- Get image list of first game ---
    if results:
        image_list = scraperObj.get_images(results[0], asset_kind)
        print('Found {0} image/s'.format(len(image_list)))
        print("{0} {1} {2}".format('Display name'.ljust(NAME_LENGTH), 
                                   'URL'.ljust(URL_LENGTH), 'Display URL'.ljust(URL_LENGTH)))
        print("{0} {1} {2}".format('-'*NAME_LENGTH, '-'*URL_LENGTH, '-'*URL_LENGTH))
        for image in image_list:
            display_name  = text_limit_string(image['name'], NAME_LENGTH)
            url           = text_limit_string(image['URL'], URL_LENGTH)
            disp_url      = text_limit_string(image['disp_URL'], URL_LENGTH)
            print("{0} {1} {2}".format(display_name.ljust(NAME_LENGTH), url.ljust(URL_LENGTH), disp_url.ljust(URL_LENGTH)))
        print('\n')
