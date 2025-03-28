# -*- coding: utf-8 -*-
##  Photini - a simple photo metadata editor.
##  http://github.com/jim-easterbrook/Photini
##  Copyright (C) 2012-17  Jim Easterbrook  jim@jim-easterbrook.me.uk
##
##  This program is free software: you can redistribute it and/or
##  modify it under the terms of the GNU General Public License as
##  published by the Free Software Foundation, either version 3 of the
##  License, or (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##  General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see
##  <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import codecs
from datetime import datetime
from fractions import Fraction
import locale
import logging
import math
import os
import re

try:
    import pgi
    pgi.install_as_gi()
    using_pgi = True
except ImportError:
    using_pgi = False
import gi
for gexiv2_vsn in ('0.10', '0.4'):
    try:
        gi.require_version('GExiv2', gexiv2_vsn)
        break
    except ValueError:
        pass
from gi.repository import GLib, GObject, GExiv2
import six

from photini import __version__
from photini.pyqt import QtCore, QtGui

logger = logging.getLogger(__name__)

gexiv2_version = '{} {}, GExiv2 {}.{}.{}, GObject {}'.format(
    ('PyGI', 'pgi')[using_pgi], gi.__version__, GExiv2.MAJOR_VERSION,
    GExiv2.MINOR_VERSION, GExiv2.MICRO_VERSION, GObject._version)

# pydoc gi.repository.GExiv2.Metadata is useful to see methods available

GExiv2.initialize()

# we can't reroute GExiv2 messages to Python logging, so mute them...
GExiv2.log_set_level(GExiv2.LogLevel.MUTE)

# ...unless in test mode
def debug_metadata():
    GExiv2.log_set_level(GExiv2.LogLevel.INFO)

# recent versions of Exiv2 have these namespaces defined, but older versions
# may not recognise them
for prefix, name in (
        ('video',   'http://www.video/'),
        ('xmpGImg', 'http://ns.adobe.com/xap/1.0/g/img/')):
    GExiv2.Metadata.register_xmp_namespace(name, prefix)

def safe_fraction(value):
    # Avoid ZeroDivisionError when '0/0' used for zero values in Exif
    if isinstance(value, six.string_types):
        numerator, sep, denominator = value.partition('/')
        if denominator and int(denominator) == 0:
            return Fraction(0.0)
    return Fraction(value).limit_denominator(1000000)

def decode_UCS2(value):
    value = bytearray(map(int, value.split()))
    return value.decode('utf_16').strip('\x00')

class MD_Value(object):
    # mixin for "metadata objects" - Python types with additional functionality
    def __nonzero__(self):
        # reinterpret as "has a value"
        return True

    def log_merged(self, info, tag, value):
        logger.info('%s: merged %s', info, tag)

    def log_replaced(self, info, tag, value):
        logger.warning(
            '%s: "%s" replaced by %s "%s"', info, str(self), tag, str(value))

    def log_ignored(self, info, tag, value):
        logger.warning('%s: ignored %s "%s"', info, tag, str(value))


class MD_Dict(dict, MD_Value):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(
            "{} has no attribute {}".format(self.__class__, name))

    def __setattr__(self, name, value):
        if name in self:
            self[name] = value
            return
        super(MD_Dict, self).__setattr__(name, value)

    def __nonzero__(self):
        return any(self.values())

    def merge(self, info, tag, other):
        if other == self:
            return self
        ignored = False
        for key in self:
            if not other[key]:
                continue
            if not self[key]:
                self[key] = other[key]
            elif other[key] != self[key]:
                ignored = True
        if ignored:
            self.log_ignored(info, tag, other)
        else:
            self.log_merged(info, tag, other)
        return self


class FocalLength(MD_Dict):
    # store actual focal length and 35mm film equivalent
    def __init__(self, value):
        fl, fl_35 = value
        if fl in (None, ''):
            fl = None
        else:
            fl = safe_fraction(fl)
        if fl_35 in (None, ''):
            fl_35 = None
        else:
            fl_35 = int(fl_35)
        super(FocalLength, self).__init__({'fl': fl, 'fl_35': fl_35})

    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if not any(file_value):
            return None
        focal_length = file_value[0]
        if len(file_value) > 1:
            focal_length_35mm = file_value[1]
        else:
            focal_length_35mm = None
        return cls((focal_length, focal_length_35mm))

    def write(self, handler, tag):
        if self.fl is None:
            focal_length = None
        else:
            focal_length = '{:d}/{:d}'.format(
                self.fl.numerator, self.fl.denominator)
        if self.fl_35 is None:
            focal_length_35mm = None
        else:
            focal_length_35mm = '{:d}'.format(self.fl_35)
        handler.set_string(tag, (focal_length, focal_length_35mm))

    def to_35(self, value):
        if value and self.fl and self.fl_35:
            return int((float(value) * float(self.fl_35) / self.fl) + 0.5)
        return self.fl_35

    def from_35(self, value):
        if value and self.fl and self.fl_35:
            return round(float(value) * self.fl / float(self.fl_35), 2)
        return self.fl


class LatLon(MD_Dict):
    # simple class to store latitude and longitude
    def __init__(self, value):
        if isinstance(value, six.string_types):
            value = value.split(',')
        lat, lon = value
        super(LatLon, self).__init__({
            'lat' : round(float(lat), 6),
            'lon' : round(float(lon), 6),
            })

    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if tag == 'Xmp.video.GPSCoordinates':
            if file_value:
                match = re.match(r'([-+]\d+\.\d+)([-+]\d+\.\d+)', file_value)
                if match:
                    return cls(match.group(1, 2))
            return None
        if not all(file_value):
            return None
        if handler.is_exif_tag(tag[0]):
            return cls((cls.from_exif_part(file_value[0], file_value[1]),
                        cls.from_exif_part(file_value[2], file_value[3])))
        else:
            return cls((cls.from_xmp_part(file_value[0]),
                        cls.from_xmp_part(file_value[1])))

    def write(self, handler, tag):
        if handler.is_exif_tag(tag[0]):
            lat_string, negative = self.to_exif_part(self.lat)
            lat_ref = 'NS'[negative]
            lon_string, negative = self.to_exif_part(self.lon)
            lon_ref = 'EW'[negative]
            handler.set_string(tag, (lat_string, lat_ref, lon_string, lon_ref))
        else:
            lat_string, negative = self.to_xmp_part(self.lat)
            lat_string += 'NS'[negative]
            lon_string, negative = self.to_xmp_part(self.lon)
            lon_string += 'EW'[negative]
            handler.set_string(tag, (lat_string, lon_string))

    @staticmethod
    def from_exif_part(value, ref):
        parts = [float(Fraction(x)) for x in value.split()] + [0.0, 0.0]
        result = parts[0] + (parts[1] / 60.0) + (parts[2] / 3600.0)
        if ref in ('S', 'W'):
            result = -result
        return result

    @staticmethod
    def to_exif_part(value):
        negative = value < 0.0
        if negative:
            value = -value
        degrees = int(value)
        value = (value - degrees) * 60.0
        minutes = int(value)
        seconds = (value - minutes) * 60.0
        seconds = safe_fraction(seconds)
        return '{:d}/1 {:d}/1 {:d}/{:d}'.format(
            degrees, minutes, seconds.numerator, seconds.denominator), negative

    @staticmethod
    def from_xmp_part(value):
        ref = value[-1]
        if ref in ('N', 'S', 'E', 'W'):
            value = value[:-1]
        if ',' in value:
            degrees, minutes = value.split(',')
            value = float(degrees) + (float(minutes) / 60.0)
        else:
            value = float(value)
        if ref in ('S', 'W'):
            value = -value
        return value

    @staticmethod
    def to_xmp_part(value):
        negative = value < 0.0
        if negative:
            value = -value
        degrees = int(value)
        minutes = (value - degrees) * 60.0
        return '{:d},{:.6f}'.format(degrees, minutes), negative

    def __str__(self):
        return '{:.6f}, {:.6f}'.format(self.lat, self.lon)

    def merge(self, info, tag, other):
        if max(abs(other.lat - self.lat), abs(other.lon - self.lon)) > 0.0000015:
            self.log_ignored(info, tag, other)
        return self


class Location(MD_Dict):
    # stores IPTC defined location heirarchy
    def __init__(self, value):
        if isinstance(value, dict):
            value = (value['sublocation'], value['city'],
                     value['province_state'], value['country_name'],
                     value['country_code'], value['world_region'])
        elif isinstance(value, six.string_types):
            value = value.split(',')
        value = [x or None for x in value]
        country_code = value[4]
        if country_code:
            country_code = country_code.upper()
        super(Location, self).__init__({
            'sublocation'   : value[0],
            'city'          : value[1],
            'province_state': value[2],
            'country_name'  : value[3],
            'country_code'  : country_code,
            'world_region'  : value[5]
            })

    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if not any(file_value):
            return None
        if len(file_value) == 5:
            return cls(file_value + [None])
        return cls(file_value)

    def write(self, handler, tag):
        handler.set_string(tag, (
            self.sublocation, self.city, self.province_state,
            self.country_name, self.country_code, self.world_region))

    def merge(self, info, tag, other):
        merged = False
        for key in self:
            if not other[key]:
                continue
            if not self[key]:
                self[key] = other[key]
                merged = True
            elif other[key] not in self[key]:
                self[key] += ' // ' + other[key]
                merged = True
        if merged:
            self.log_merged(info, tag, other)
        return self


class LensSpec(MD_Dict):
    # simple class to store lens "specificaton"
    def __init__(self, value):
        if isinstance(value, six.string_types):
            sep = None
            if ',' in value:
                sep = ','
            value = value.split(sep)
        min_fl, max_fl, min_fl_fn, max_fl_fn = value
        super(LensSpec, self).__init__({
            'min_fl'    : safe_fraction(min_fl),
            'max_fl'    : safe_fraction(max_fl),
            'min_fl_fn' : safe_fraction(min_fl_fn),
            'max_fl_fn' : safe_fraction(max_fl_fn),
            })

    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if not file_value:
            return None
        if tag == 'Exif.CanonCs.Lens':
            long_focal, short_focal, focal_units = file_value.split()
            return cls(('{}/{}'.format(short_focal, focal_units),
                        '{}/{}'.format(long_focal, focal_units),
                        0, 0))
        return cls(file_value)

    def write(self, handler, tag):
        handler.set_string(tag, ' '.join(
            ['{:d}/{:d}'.format(x.numerator, x.denominator) for x in (
                self.min_fl, self.max_fl, self.min_fl_fn, self.max_fl_fn)]))

    def __str__(self):
        return '{:g} {:g} {:g} {:g}'.format(
            float(self.min_fl),    float(self.max_fl),
            float(self.min_fl_fn), float(self.max_fl_fn))


class Thumbnail(MD_Dict):
    def __init__(self, value):
        data, fmt, w, h = value
        super(Thumbnail, self).__init__({
            'data' : data,
            'fmt'  : fmt,
            'w'    : w,
            'h'    : h,
            })

    @classmethod
    def read(cls, handler, tag):
        if handler.is_xmp_tag(tag):
            data, fmt, w, h = handler.get_string(tag)
            if not all((data, fmt, w, h)):
                return None
            if not six.PY2:
                data = bytes(data, 'ASCII')
            data = codecs.decode(data, 'base64_codec')
            w = int(w)
            h = int(h)
        else:
            data = handler.get_exif_thumbnail()
            if not data:
                return None
            fmt = handler.get_tag_string(tag[1])
            fmt = ('TIFF', 'JPEG')[fmt == '6']
            w, h = None, None
        return cls((data, fmt, w, h))

    def write(self, handler, tag):
        if handler.is_xmp_tag(tag):
            data = self.data
            fmt  = self.fmt
            w    = self.w
            h    = self.h
            if fmt != 'JPEG':
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                buf = QtCore.QBuffer()
                buf.open(QtCore.QIODevice.WriteOnly)
                pixmap.save(buf, 'JPEG')
                data = buf.data().data()
                w = pixmap.width()
                h = pixmap.height()
            if not w or not h:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data)
                w = pixmap.width()
                h = pixmap.height()
            data = codecs.encode(data, 'base64_codec')
            handler.set_string(tag, (data, fmt, str(w), str(h)))
        elif handler.get_supports_exif():
            handler.set_exif_thumbnail_from_buffer(self.data)

    def merge(self, info, tag, other):
        return self


class DateTime(MD_Dict):
    # store date and time with "precision" to store how much is valid
    # tz_offset is stored in minutes
    def __init__(self, value):
        date_time, precision, tz_offset = value
        if date_time is None:
            # use a well known 'zero'
            date_time = datetime(1970, 1, 1)
        else:
            date_time = self.truncate_date_time(date_time, precision)
        if precision <= 3:
            tz_offset = None
        super(DateTime, self).__init__({
            'datetime'  : date_time,
            'precision' : precision,
            'tz_offset' : tz_offset,
            })

    @staticmethod
    def truncate_date_time(date_time, precision):
        parts = [date_time.year, date_time.month, date_time.day,
                 date_time.hour, date_time.minute, date_time.second,
                 date_time.microsecond][:precision]
        parts.extend((1, 1, 1)[len(parts):])
        return datetime(*parts)

    @classmethod
    def from_ISO_8601(cls, date_string, time_string, tz_string):
        """Sufficiently general ISO 8601 parser.

        Inputs must be in "basic" format, i.e. no '-' or ':' separators.
        See https://en.wikipedia.org/wiki/ISO_8601

        """
        # parse tz_string
        if tz_string:
            tz_offset = (int(tz_string[1:3]) * 60) + int(tz_string[3:])
            if tz_string[0] == '-':
                tz_offset = -tz_offset
        else:
            tz_offset = None
        if time_string == '000000':
            # assume no time information
            time_string = ''
            tz_offset = None
        datetime_string = date_string + time_string[:13]
        precision = min((len(datetime_string) - 2) // 2, 7)
        if precision <= 0:
            return None
        fmt = ''.join(('%Y', '%m', '%d', '%H', '%M', '%S', '.%f')[:precision])
        return cls(
            (datetime.strptime(datetime_string, fmt), precision, tz_offset))

    def to_ISO_8601(self, fmt=('%Y', '-%m', '-%d', 'T%H', ':%M', ':%S', '.%f'),
                    precision=None, time_zone=True):
        if precision is None:
            precision = self.precision
        fmt = ''.join(fmt[:precision])
        datetime_string = self.datetime.strftime(fmt)
        if precision > 3 and time_zone and self.tz_offset is not None:
            # add time zone
            minutes = self.tz_offset
            if minutes >= 0:
                datetime_string += '+'
            else:
                datetime_string += '-'
                minutes = -minutes
            datetime_string += '{:02d}:{:02d}'.format(
                minutes // 60, minutes % 60)
        return datetime_string

    # many quicktime movies use Apple's 1904 timestamp zero point
    qt_offset = (datetime(1970, 1, 1) - datetime(1904, 1, 1)).total_seconds()

    # Do something different with Xmp.video tags
    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if not file_value:
            return None
        if handler.is_exif_tag(tag):
            return cls.from_exif(file_value)
        if handler.is_iptc_tag(tag):
            return cls.from_iptc(file_value)
        if tag.startswith('Xmp.video'):
            time_stamp = int(file_value)
            if time_stamp == 0:
                return None
            # assume date should be in range 1970 to 2034
            if time_stamp > cls.qt_offset:
                time_stamp -= cls.qt_offset
            return cls((datetime.utcfromtimestamp(time_stamp), 6, None))
        return cls.from_xmp(file_value)

    def write(self, handler, tag):
        if handler.is_exif_tag(tag):
            handler.set_string(tag, self.to_exif())
        elif handler.is_iptc_tag(tag):
            handler.set_string(tag, self.to_iptc())
        else:
            handler.set_string(tag, self.to_xmp())

    # Exif datetime is always full resolution and valid. Assume a time
    # of 00:00:00 is a None value though.
    @classmethod
    def from_exif(cls, file_value):
        datetime_string = file_value[0]
        if not datetime_string:
            return None
        # separate date & time and remove separators
        date_string = datetime_string[:10].replace(':', '')
        time_string = datetime_string[11:].replace(':', '')
        # append sub seconds
        if len(file_value) > 1:
            sub_sec_string = file_value[1]
            if sub_sec_string:
                time_string += '.' + sub_sec_string
        result = cls.from_ISO_8601(date_string, time_string, '')
        # set time zone
        if result.precision > 3 and len(file_value) > 2:
            tz_string = file_value[2]
            if tz_string:
                result.tz_offset = 60 * int(tz_string)
        return result

    def to_exif(self):
        datetime_string, sep, sub_sec_string = self.to_ISO_8601(
            fmt=('%Y', ':%m', ':%d', ' %H', ':%M', ':%S', '.%f'),
            time_zone=False).partition('.')
        # pad out any missing values
        #                   YYYY mm dd HH MM SS
        datetime_string += '0000:01:01 00:00:00'[len(datetime_string):]
        if self.precision > 3 and self.tz_offset is not None:
            tz_string = str(int(round(float(self.tz_offset) / 60.0)))
        else:
            tz_string = ''
        return datetime_string, sub_sec_string, tz_string

    # IPTC date & time should have no separators and be 8 and 11 chars
    # respectively (time includes time zone offset). I suspect the exiv2
    # library is adding separators, but am not sure.

    # The date (and time?) can have missing values represented by 00
    # according to
    # https://de.wikipedia.org/wiki/IPTC-IIM-Standard#IPTC-Felder
    @classmethod
    def from_iptc(cls, file_value):
        date_string, time_string = file_value
        if not date_string:
            return None
        # remove separators (that shouldn't be there)
        date_string = date_string.replace('-', '')
        # remove missing values
        while len(date_string) > 4 and date_string[-2:] == '00':
            date_string = date_string[:-2]
        if date_string == '0000':
            return None
        # ignore time if date is not full precision
        if len(date_string) < 8:
            time_string = ''
        if time_string:
            # remove separators (that shouldn't be there)
            time_string = time_string.replace(':', '')
            # split off time zone
            tz_string = time_string[6:]
            time_string = time_string[:6]
        else:
            tz_string = ''
            time_string = ''
        return cls.from_ISO_8601(date_string, time_string, tz_string)

    def to_iptc(self):
        if self.precision <= 3:
            date_string = self.to_ISO_8601()
            #               YYYY mm dd
            date_string += '0000-00-00'[len(date_string):]
            time_string = None
        else:
            datetime_string = self.to_ISO_8601(precision=6)
            date_string = datetime_string[:10]
            time_string = datetime_string[11:]
        return date_string, time_string

    # XMP uses extended ISO 8601, but the time cannot be hours only. See
    # p75 of
    # https://partners.adobe.com/public/developer/en/xmp/sdk/XMPspecification.pdf
    # According to p71, when converting Exif values with no time zone,
    # local time zone should be assumed. However, the MWG guidelines say
    # this must not be assumed to be the time zone where the photo is
    # processed. It also says the XMP standard has been revised to make
    # time zone information optional.
    @classmethod
    def from_xmp(cls, file_value):
        date_string, sep, time_string = file_value.partition('T')
        if len(time_string) > 6 and time_string[-6] in ('+', '-'):
            tz_string = time_string[-6:]
            time_string = time_string[:-6]
        elif len(time_string) > 1 and time_string[-1] == 'Z':
            tz_string = '+00:00'
            time_string = time_string[:-1]
        else:
            tz_string = ''
        return cls.from_ISO_8601(
            date_string.replace('-', ''), time_string.replace(':', ''),
            tz_string.replace(':', ''))

    def to_xmp(self):
        precision = self.precision
        if precision == 4:
            precision = 5
        return self.to_ISO_8601(precision=precision)

    def __str__(self):
        return self.to_ISO_8601()

    def merge(self, info, tag, other):
        if other == self:
            return self
        merged = False
        if other.datetime != self.datetime:
            # if datetime values differ, choose the one with more precision
            if other.precision > self.precision:
                self.log_replaced(info, tag, other)
                return other
            if other.datetime != self.truncate_date_time(
                                    self.datetime, other.precision):
                self.log_ignored(info, tag, other)
                return self
        else:
            # some formats default to a higher precision than wanted
            if self.precision < 7 and other.precision < self.precision:
                self.precision = other.precision
                merged = True
        # don't trust IPTC time zone and Exif time zone is quantised to
        # whole hours, unlike Xmp
        if (other.tz_offset not in (None, self.tz_offset) and
                MetadataHandler.is_xmp_tag(tag)):
            self.tz_offset = other.tz_offset
            merged = True
        if merged:
            self.log_merged(info, tag, other)
        return self


class MultiString(list, MD_Value):
    def __init__(self, value):
        if isinstance(value, six.string_types):
            value = value.split(';')
        value = filter(bool, [x.strip() for x in value])
        super(MultiString, self).__init__(value)

    @classmethod
    def read(cls, handler, tag):
        if handler.get_tag_type(tag) in ('String', 'XmpBag', 'XmpSeq'):
            file_value = handler.get_multiple(tag)
        else:
            file_value = handler.get_string(tag)
        if not file_value:
            return None
        if handler.get_tag_type(tag) == 'Byte':
            file_value = decode_UCS2(file_value)
        return cls(file_value)

    def write(self, handler, tag):
        if handler.is_exif_tag(tag):
            handler.set_string(tag, ';'.join(self))
        elif handler.get_tag_type(tag) in ('String', 'XmpBag', 'XmpSeq'):
            handler.set_multiple(tag, self)
        else:
            handler.set_string(tag, self)

    def __str__(self):
        return '; '.join(self)

    def merge(self, info, tag, other):
        merged = False
        for item in other:
            if item not in self:
                self.append(item)
                merged = True
        if merged:
            self.log_merged(info, tag, other)
        return self


class MD_String(six.text_type, MD_Value):
    @classmethod
    def read(cls, handler, tag):
        if handler.get_tag_type(tag) == 'LangAlt':
            file_value = handler.get_multiple(tag)
            if file_value:
                file_value = file_value[0]
        else:
            file_value = handler.get_string(tag)
        if file_value and handler.get_tag_type(tag) == 'Byte':
            file_value = decode_UCS2(file_value)
        if file_value:
            file_value = six.text_type(file_value).strip()
        if not file_value:
            return None
        return cls(file_value)

    def write(self, handler, tag):
        handler.set_string(tag, self)

    def merge(self, info, tag, other):
        if other in self:
            return self
        self.log_merged(info, tag, other)
        return MD_String(self + ' // ' + other)


class CharacterSet(MD_String):
    known_encodings = {
        'ascii'   : '\x1b(B',
        'latin_1' : '\x1b/A',
        'latin1'  : '\x1b.A',
        'utf_8'   : '\x1b%G',
        }

    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        for charset, encoding in cls.known_encodings.items():
            if encoding == file_value:
                return cls(charset)
        if file_value:
            logger.warning('Unknown character encoding "%s"', repr(file_value))
        return None

    def write(self, handler, tag):
        handler.set_string(tag, self.known_encodings[self])


class Software(MD_String):
    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if isinstance(file_value, list):
            program, version = file_value
            if not program:
                return None
            if version:
                program += ' v' + version
            return cls(program)
        if not file_value:
            return None
        return cls(file_value)

    def write(self, handler, tag):
        if handler.is_iptc_tag(tag):
            handler.set_string(tag, self.split(' v'))
        else:
            handler.set_string(tag, self)


class MD_Int(int, MD_Value):
    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if not file_value:
            return None
        return cls(file_value)

    def write(self, handler, tag):
        handler.set_string(tag, six.text_type(self))

    def merge(self, info, tag, other):
        if self != other:
            self.log_ignored(info, tag, other)
        return self


class Timezone(MD_Int):
    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if not file_value:
            return None
        if tag == 'Exif.Image.TimeZoneOffset':
            # convert hours to minutes
            return cls(int(file_value) * 60)
        return cls(file_value)


class Aperture(Fraction, MD_Value):
    # store FNumber and APEX aperture as fractions
    # only FNumber is presented to the user, either is computed if missing
    @classmethod
    def read(cls, handler, tag):
        file_value = handler.get_string(tag)
        if not any(file_value):
            return None
        f_number, apex = file_value
        if apex:
            apex = safe_fraction(apex)
        if not f_number:
            f_number = 2.0 ** (apex / 2.0)
        f_number = safe_fraction(f_number)
        self = cls(f_number)
        if apex:
            self.apex = apex
        return self

    def write(self, handler, tag):
        apex = getattr(self, 'apex', safe_fraction(math.log(self, 2) * 2.0))
        handler.set_string(tag, (
            '{:d}/{:d}'.format(self.numerator, self.denominator),
            '{:d}/{:d}'.format(apex.numerator, apex.denominator)))

    def __str__(self):
        return six.text_type(float(self))

    def merge(self, info, tag, other):
        if (min(other, self) / max(other, self)) < 0.95:
            self.log_ignored(info, tag, other)
        return self


# maximum length of Iptc data
_max_bytes = {
    'Iptc.Application2.Byline'           :   32,
    'Iptc.Application2.Caption'          : 2000,
    'Iptc.Application2.City'             :   32,
    'Iptc.Application2.Copyright'        :  128,
    'Iptc.Application2.CountryCode'      :    3,
    'Iptc.Application2.CountryName'      :   64,
    'Iptc.Application2.Headline'         :  256,
    'Iptc.Application2.Keywords'         :   64,
    'Iptc.Application2.ObjectName'       :   64,
    'Iptc.Application2.Program'          :   32,
    'Iptc.Application2.ProgramVersion'   :   10,
    'Iptc.Application2.ProvinceState'    :   32,
    'Iptc.Application2.SubLocation'      :   32,
    'Iptc.Envelope.CharacterSet'         :   32,
    }

# extra Xmp namespaces we may need
_extra_ns = {
    'Iptc4xmpExt': 'http://iptc.org/std/Iptc4xmpExt/2008-02-29/',
    }

class MetadataHandler(GExiv2.Metadata):
    def __init__(self, path):
        super(MetadataHandler, self).__init__()
        self._path = path
        # read metadata from file
        self.open_path(self._path)
        self._xmp_only = self.get_mime_type() in (
            'application/rdf+xml', 'application/postscript')
        # remove exiv2's synthesised non-XMP tags
        if self._xmp_only:
            self.clear_exif()
            self.clear_iptc()
        # make list of possible character encodings
        self._encodings = []
        for name in ('utf_8', 'latin_1'):
            self._encodings.append(codecs.lookup(name).name)
        char_set = locale.getdefaultlocale()[1]
        if char_set:
            try:
                name = codecs.lookup(char_set).name
                if name not in self._encodings:
                    self._encodings.append(name)
            except LookupError:
                pass
        # convert IPTC data to UTF-8
        if not self.has_iptc():
            return
        current_encoding = CharacterSet.read(self, 'Iptc.Envelope.CharacterSet')
        if current_encoding:
            if current_encoding == 'utf_8':
                return
            try:
                name = codecs.lookup(current_encoding).name
                if name not in self._encodings:
                    self._encodings.insert(0, name)
            except LookupError:
                pass
        for tag in self.get_iptc_tags():
            try:
                value_list = self.get_multiple(tag)
                self.set_multiple(tag, value_list)
            except Exception as ex:
                logger.exception(ex)

    def _decode_string(self, value):
        if not value:
            return value
        for encoding in self._encodings:
            try:
                return value.decode(encoding)
            except UnicodeDecodeError:
                continue
        return value.decode('utf_8', 'replace')

    def clear_value(self, tag):
        if isinstance(tag, tuple):
            for sub_tag in tag:
                self.clear_value(sub_tag)
            return
        if not self.has_tag(tag):
            return
        self.clear_tag(tag)
        if self.is_xmp_tag(tag) and '/' in tag:
            # attempt to remove XMP structure/container
            container, subtag = tag.split('/')
            bag = container.partition('[')[0]
            for t in self.get_xmp_tags():
                if t.startswith(container + '/'):
                    # bag is not empty
                    return
            if container != bag:
                self.clear_tag(container)
            self.clear_tag(bag)

    def get_string(self, tag):
        if isinstance(tag, tuple):
            return list(map(self.get_string, tag))
        try:
            result = self.get_tag_string(tag)
            if six.PY2:
                result = self._decode_string(result)
        except UnicodeDecodeError as ex:
            logger.error(str(ex))
            return None
        return result

    def get_multiple(self, tag):
        if isinstance(tag, tuple):
            return list(map(self.get_multiple, tag))
        try:
            result = self.get_tag_multiple(tag)
            if six.PY2:
                result = list(map(self._decode_string, result))
        except UnicodeDecodeError as ex:
            logger.error(str(ex))
            return []
        return result

    def set_string(self, tag, value):
        if isinstance(tag, tuple):
            for sub_tag, sub_value in zip(tag, value):
                self.set_string(sub_tag, sub_value)
            return
        if not value:
            self.clear_value(tag)
            return
        if tag in _max_bytes:
            value = value.encode('utf_8')[:_max_bytes[tag]]
            if not six.PY2:
                value = value.decode('utf_8', errors='ignore')
        elif six.PY2:
            value = value.encode('utf_8')
        if self.is_xmp_tag(tag) and '/' in tag:
            # create XMP structure/container
            container, subtag = tag.split('/')
            bag = container.partition('[')[0]
            ns_prefix = subtag.partition(':')[0]
            no_bag = True
            ns_defined = ns_prefix not in _extra_ns
            for t in self.get_xmp_tags():
                if t.startswith(bag):
                    # file already has container
                    no_bag = False
                if ns_prefix in t:
                    # file has correct namespace defined
                    ns_defined = True
            if no_bag:
                # create empty container
                if '[' in container:
                    self.set_xmp_tag_struct(bag, GExiv2.StructureType.ALT)
                else:
                    self.set_xmp_tag_struct(bag, GExiv2.StructureType.SEQ)
            if not ns_defined:
                # create some XMP data with the correct namespace
                data = '''<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description
        xmlns:{}="{}">
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''.format(ns_prefix, _extra_ns[ns_prefix])
                if six.PY2:
                    data = data.decode('utf-8')
                # open the data to register the correct namespace
                md = GExiv2.Metadata()
                md.open_buf(data.encode('utf-8'))
        self.set_tag_string(tag, value)

    def set_multiple(self, tag, value):
        if isinstance(tag, tuple):
            for sub_tag, sub_value in zip(tag, value):
                self.set_multiple(sub_tag, sub_value)
            return
        if not value:
            self.clear_value(tag)
            return
        if self.is_iptc_tag(tag) and tag in _max_bytes:
            value = [x.encode('utf_8')[:_max_bytes[tag]] for x in value]
            if not six.PY2:
                value = [x.decode('utf_8') for x in value]
        elif six.PY2:
            value = [x.encode('utf_8') for x in value]
        self.set_tag_multiple(tag, value)

    @staticmethod
    def is_exif_tag(tag):
        if isinstance(tag, tuple):
            tag = tag[0]
        return GExiv2.Metadata.is_exif_tag(tag)

    @staticmethod
    def is_iptc_tag(tag):
        if isinstance(tag, tuple):
            tag = tag[0]
        return GExiv2.Metadata.is_iptc_tag(tag)

    @staticmethod
    def is_xmp_tag(tag):
        if isinstance(tag, tuple):
            tag = tag[0]
        return GExiv2.Metadata.is_xmp_tag(tag)

    def get_supports_exif(self):
        if self._xmp_only:
            return False
        return super(MetadataHandler, self).get_supports_exif()

    def has_iptc(self):
        if self._xmp_only:
            return False
        return super(MetadataHandler, self).has_iptc()

    def save(self, file_times):
        # don't try to save to unwritable formats
        if not (self.get_supports_xmp() or self.get_supports_exif()):
            return False
        # remove exiv2's synthesised non-XMP tags
        if self._xmp_only:
            self.clear_exif()
            self.clear_iptc()
        try:
            self.save_file(self._path)
            if file_times:
                os.utime(self._path, file_times)
        except Exception as ex:
            logger.exception(ex)
            return False
        return True

    def clone(self, other):
        # copy from other to self, ignoring thumbnails
        for tag in other.get_exif_tags():
            if tag.startswith('Exif.Thumbnail'):
                continue
            self.set_string(tag, other.get_string(tag))
        for tag in other.get_iptc_tags():
            self.set_multiple(tag, other.get_multiple(tag))
        for tag in other.get_xmp_tags():
            if tag.startswith('Xmp.xmp.Thumbnails'):
                continue
            if self.get_tag_type(tag) == 'XmpText':
                self.set_string(tag, other.get_string(tag))
            else:
                self.set_multiple(tag, other.get_multiple(tag))

    def get_all_tags(self):
        return self.get_exif_tags() + self.get_iptc_tags() + self.get_xmp_tags()

    def get_exif_thumbnail(self):
        thumb = super(MetadataHandler, self).get_exif_thumbnail()
        if using_pgi and isinstance(thumb, tuple):
            # get_exif_thumbnail returns (OK, data) tuple
            thumb = thumb[thumb[0]]
        if thumb:
            return bytearray(thumb)
        return None


class Metadata(object):
    # type of each Photini data field's data
    _data_type = {
        'aperture'       : Aperture,
        'camera_model'   : MD_String,
        'character_set'  : CharacterSet,
        'copyright'      : MD_String,
        'creator'        : MultiString,
        'date_digitised' : DateTime,
        'date_modified'  : DateTime,
        'date_taken'     : DateTime,
        'description'    : MD_String,
        'focal_length'   : FocalLength,
        'keywords'       : MultiString,
        'latlong'        : LatLon,
        'lens_make'      : MD_String,
        'lens_model'     : MD_String,
        'lens_serial'    : MD_String,
        'lens_spec'      : LensSpec,
        'location_shown' : Location,
        'location_taken' : Location,
        'orientation'    : MD_Int,
        'software'       : Software,
        'thumbnail'      : Thumbnail,
        'timezone'       : Timezone,
        'title'          : MD_String,
        }
    # Mapping of tags to Photini data fields Each field has a list of
    # (mode, tag) pairs, where tag can be a tuple of tags. The mode is a
    # string containing the read mode (RA (always), or RN (never)) and
    # write mode (WA (always), WX (if Exif not supported), W0 (clear the
    # tag), or WN (never).
    _tag_list = {
        'aperture'       : (('RA.WA', ('Exif.Photo.FNumber',
                                       'Exif.Photo.ApertureValue')),
                            ('RA.W0', ('Exif.Image.FNumber',
                                       'Exif.Image.ApertureValue')),
                            ('RA.WX', ('Xmp.exif.FNumber',
                                       'Xmp.exif.ApertureValue'))),
        'camera_model'   : (('RA.WN', 'Exif.Image.Model'),
                            ('RA.WN', 'Exif.Image.UniqueCameraModel'),
                            ('RA.WN', 'Xmp.video.Model')),
        'character_set'  : (('RA.WA', 'Iptc.Envelope.CharacterSet'),),
        'copyright'      : (('RA.WA', 'Exif.Image.Copyright'),
                            ('RA.WA', 'Xmp.dc.rights'),
                            ('RA.W0', 'Xmp.tiff.Copyright'),
                            ('RA.WA', 'Iptc.Application2.Copyright')),
        'creator'        : (('RA.WA', 'Exif.Image.Artist'),
                            ('RA.W0', 'Exif.Image.XPAuthor'),
                            ('RA.WA', 'Xmp.dc.creator'),
                            ('RA.W0', 'Xmp.tiff.Artist'),
                            ('RA.WA', 'Iptc.Application2.Byline')),
        'date_digitised' : (('RA.WA', ('Exif.Photo.DateTimeDigitized',
                                       'Exif.Photo.SubSecTimeDigitized')),
                            ('RA.WA', 'Xmp.xmp.CreateDate'),
                            ('RA.W0', 'Xmp.exif.DateTimeDigitized'),
                            ('RA.WN', 'Xmp.video.DateUTC'),
                            ('RA.WA', ('Iptc.Application2.DigitizationDate',
                                       'Iptc.Application2.DigitizationTime'))),
        'date_modified'  : (('RA.WA', ('Exif.Image.DateTime',
                                       'Exif.Photo.SubSecTime')),
                            ('RA.WA', 'Xmp.xmp.ModifyDate'),
                            ('RA.WN', 'Xmp.video.ModificationDate'),
                            ('RA.W0', 'Xmp.tiff.DateTime')),
        'date_taken'     : (('RA.WA', ('Exif.Photo.DateTimeOriginal',
                                       'Exif.Photo.SubSecTimeOriginal',
                                       'Exif.Image.TimeZoneOffset')),
                            ('RA.W0', ('Exif.Image.DateTimeOriginal',)),
                            ('RA.WA', 'Xmp.photoshop.DateCreated'),
                            ('RA.W0', 'Xmp.exif.DateTimeOriginal'),
                            ('RA.WN', 'Xmp.video.DateUTC'),
                            ('RA.WA', ('Iptc.Application2.DateCreated',
                                       'Iptc.Application2.TimeCreated'))),
        'description'    : (('RA.WA', 'Exif.Image.ImageDescription'),
                            ('RA.W0', 'Exif.Image.XPComment'),
                            ('RA.W0', 'Exif.Image.XPSubject'),
                            ('RA.WA', 'Xmp.dc.description'),
                            ('RA.W0', 'Xmp.tiff.ImageDescription'),
                            ('RA.WA', 'Iptc.Application2.Caption')),
        'focal_length'   : (('RA.WA', ('Exif.Photo.FocalLength',
                                       'Exif.Photo.FocalLengthIn35mmFilm')),
                            ('RA.W0', ('Exif.Image.FocalLength',)),
                            ('RA.WX', ('Xmp.exif.FocalLength',
                                       'Xmp.exif.FocalLengthIn35mmFilm'))),
        'keywords'       : (('RA.WA', 'Xmp.dc.subject'),
                            ('RA.WA', 'Iptc.Application2.Keywords'),
                            ('RA.W0', 'Exif.Image.XPKeywords')),
        'latlong'        : (('RA.WA', ('Exif.GPSInfo.GPSLatitude',
                                       'Exif.GPSInfo.GPSLatitudeRef',
                                       'Exif.GPSInfo.GPSLongitude',
                                       'Exif.GPSInfo.GPSLongitudeRef')),
                            ('RA.WX', ('Xmp.exif.GPSLatitude',
                                       'Xmp.exif.GPSLongitude')),
                            ('RA.WN', 'Xmp.video.GPSCoordinates')),
        'lens_make'      : (('RA.WA', 'Exif.Photo.LensMake'),
                            ('RA.WX', 'Xmp.exifEX.LensMake')),
        'lens_model'     : (('RA.WA', 'Exif.Photo.LensModel'),
                            ('RA.WX', 'Xmp.exifEX.LensModel'),
                            ('RA.W0', 'Exif.Canon.LensModel'),
                            ('RA.W0', 'Exif.OlympusEq.LensModel'),
                            ('RA.W0', 'Xmp.aux.Lens'),
                            ('RN.W0', 'Exif.CanonCs.LensType')),
        'lens_serial'    : (('RA.WA', 'Exif.Photo.LensSerialNumber'),
                            ('RA.WX', 'Xmp.exifEX.LensSerialNumber'),
                            ('RA.W0', 'Exif.OlympusEq.LensSerialNumber'),
                            ('RA.W0', 'Xmp.aux.SerialNumber')),
        'lens_spec'      : (('RA.WA', 'Exif.Photo.LensSpecification'),
                            ('RA.WX', 'Xmp.exifEX.LensSpecification'),
                            ('RA.W0', 'Exif.Image.LensInfo'),
                            ('RA.W0', 'Exif.CanonCs.Lens'),
                            ('RA.W0', 'Exif.Nikon3.Lens'),
                            ('RN.W0', 'Exif.CanonCs.ShortFocal'),
                            ('RN.W0', 'Exif.CanonCs.MaxAperture'),
                            ('RN.W0', 'Exif.CanonCs.MinAperture')),
        'location_shown' : (
            ('RA.WA', ('Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:Sublocation',
                       'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:City',
                       'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:ProvinceState',
                       'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:CountryName',
                       'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:CountryCode',
                       'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:WorldRegion')),),
        'location_taken' : (
            ('RA.WA', ('Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:Sublocation',
                       'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:City',
                       'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:ProvinceState',
                       'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:CountryName',
                       'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:CountryCode',
                       'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:WorldRegion')),
            ('RA.WA', ('Xmp.iptc.Location',
                       'Xmp.photoshop.City',
                       'Xmp.photoshop.State',
                       'Xmp.photoshop.Country',
                       'Xmp.iptc.CountryCode')),
            ('RA.WA', ('Iptc.Application2.SubLocation',
                       'Iptc.Application2.City',
                       'Iptc.Application2.ProvinceState',
                       'Iptc.Application2.CountryName',
                       'Iptc.Application2.CountryCode'))),
        'orientation'    : (('RA.WA', 'Exif.Image.Orientation'),
                            ('RA.WX', 'Xmp.tiff.Orientation')),
        'software'       : (('RA.WA', 'Exif.Image.ProcessingSoftware'),
                            ('RA.WA', ('Iptc.Application2.Program',
                                       'Iptc.Application2.ProgramVersion'))),
        'thumbnail'      : (('RA.WA', ('Exif.Thumbnail.Image',
                                       'Exif.Thumbnail.Compression')),
                            ('RA.WX', ('Xmp.xmp.Thumbnails[1]/xmpGImg:image',
                                       'Xmp.xmp.Thumbnails[1]/xmpGImg:format',
                                       'Xmp.xmp.Thumbnails[1]/xmpGImg:width',
                                       'Xmp.xmp.Thumbnails[1]/xmpGImg:height')),
                            ('RA.W0', ('Xmp.xmp.Thumbnails[1]/xapGImg:image',
                                       'Xmp.xmp.Thumbnails[1]/xapGImg:format',
                                       'Xmp.xmp.Thumbnails[1]/xapGImg:width',
                                       'Xmp.xmp.Thumbnails[1]/xapGImg:height'))),
        'timezone'       : (('RA.WN', 'Exif.Image.TimeZoneOffset'),
                            ('RA.WN', 'Exif.NikonWt.Timezone')),
        'title'          : (('RA.WA', 'Xmp.dc.title'),
                            ('RA.WA', 'Iptc.Application2.ObjectName'),
                            ('RA.W0', 'Exif.Image.XPTitle'),
                            ('RA.W0', 'Iptc.Application2.Headline')),
        }
    def __init__(self, path, new_status=None):
        super(Metadata, self).__init__()
        self._new_status = new_status
        # create metadata handlers for image file and/or sidecar
        self._path = path
        self._sc_path = self._find_side_car(path)
        self._sc = None
        if self._sc_path:
            try:
                self._sc = MetadataHandler(self._sc_path)
            except Exception as ex:
                logger.exception(ex)
        self._if = None
        try:
            self._if = MetadataHandler(path)
        except GLib.Error:
            # expected if unrecognised file format
            pass
        except Exception as ex:
            logger.exception(ex)
        self._unsaved = False

    def _find_side_car(self, path):
        for base in (os.path.splitext(path)[0], path):
            for ext in ('.xmp', '.XMP'):
                result = base + ext
                if os.path.exists(result):
                    return result
        return None

    def create_side_car(self):
        self._sc_path = self._path + '.xmp'
        with open(self._sc_path, 'w') as of:
            of.write('''<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
   xmp:CreatorTool="{}"/>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''.format('Photini editor v' + __version__))
        try:
            self._sc = MetadataHandler(self._sc_path)
        except Exception as ex:
            logger.exception(ex)

    def save(self, if_mode, sc_mode, force_iptc, file_times):
        if not self._unsaved:
            return
        if (sc_mode == 'always' or not self._if) and not self._sc:
            self.create_side_car()
        self.software = 'Photini editor v' + __version__
        self.character_set = 'utf_8'
        save_iptc = force_iptc or (self._if and self._if.has_iptc())
        if self._sc:
            # workaround for bug in exiv2 xmp timestamp altering
            for name in ('date_digitised', 'date_modified', 'date_taken'):
                for mode, tag in self._tag_list[name]:
                    if mode == 'RA.WA':
                        self._sc.clear_value(tag)
            self._sc.save(file_times)
        for name in self._tag_list:
            value = getattr(self, name)
            for mode, tag in self._tag_list[name]:
                write_mode = mode.split('.')[1]
                if write_mode == 'WN':
                    continue
                for handler in (self._sc, self._if):
                    if not handler:
                        continue
                    if ((not value) or (write_mode == 'W0') or
                        (write_mode == 'WX' and handler.get_supports_exif())):
                        handler.clear_value(tag)
                    else:
                        value.write(handler, tag)
        if self._if and sc_mode == 'delete' and self._sc:
            self._if.clone(self._sc)
        OK = False
        if self._if and if_mode:
            OK = self._if.save(file_times)
            if OK:
                # check that data really was saved
                saved_tags = MetadataHandler(self._path).get_all_tags()
                for tag in self._if.get_all_tags():
                    if tag not in saved_tags:
                        logger.warning('tag not saved: %s', tag)
                        OK = False
            if not OK and not self._sc:
                # can't write to image so create side car
                self.save(False, 'always', force_iptc, file_times)
                return
        if sc_mode == 'delete' and self._sc and OK:
            os.unlink(self._sc_path)
            self._sc = None
        if self._sc:
            OK = self._sc.save(file_times)
        self._set_unsaved(not OK)

    def get_mime_type(self):
        if self._if:
            return self._if.get_mime_type()
        return None

    def copy(self, other):
        # copy from other to self, sidecar over-rides image
        if self._sc:
            if other._if:
                self._sc.clone(other._if)
            if other._sc:
                self._sc.clone(other._sc)
        if self._if:
            if other._if:
                self._if.clone(other._if)
            if other._sc:
                self._if.clone(other._sc)
        self._set_unsaved(True)

    def __getattr__(self, name):
        if name not in self._tag_list:
            raise AttributeError(
                "%s has no attribute %s" % (self.__class__, name))
        # read data values
        values = []
        for mode, tag in self._tag_list[name]:
            if mode.split('.')[0] == 'RN':
                continue
            new_value = None
            for handler in self._sc, self._if:
                if not handler:
                    continue
                try:
                    new_value = self._data_type[name].read(handler, tag)
                except Exception as ex:
                    logger.exception(ex)
                    continue
                if new_value:
                    values.append((tag, new_value))
                    break
        # choose result and merge in non-matching data so user can review it
        result = None
        if values:
            info = '{}({})'.format(os.path.basename(self._path), name)
            tag, result = values.pop(0)
            logger.debug('%s: set from %s', info, tag)
        for tag, value in values:
            merged = result.merge(info, tag, value)
        # merge in camera timezone if needed
        if (result and name.startswith('date_') and
                            result.tz_offset is None and self.timezone):
            result.tz_offset = self.timezone
            logger.info('%s: merged camera timezone offset', info)
        # add value to object attributes so __getattr__ doesn't get
        # called again
        super(Metadata, self).__setattr__(name, result)
        return result

    def __setattr__(self, name, value):
        if name not in self._tag_list:
            return super(Metadata, self).__setattr__(name, value)
        if value in (None, '', [], {}):
            value = None
        elif not isinstance(value, self._data_type[name]):
            value = self._data_type[name](value)
            if not value:
                value = None
        if getattr(self, name) == value:
            return
        super(Metadata, self).__setattr__(name, value)
        self._set_unsaved(True)

    def _set_unsaved(self, status):
        self._unsaved = status
        if self._new_status:
            self._new_status(self._unsaved)

    def changed(self):
        return self._unsaved
