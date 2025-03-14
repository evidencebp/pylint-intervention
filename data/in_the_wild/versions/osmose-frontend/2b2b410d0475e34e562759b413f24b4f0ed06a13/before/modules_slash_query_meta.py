#! /usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from collections import defaultdict
from .utils import i10n_select


def _items_menu(db, langs):
    sql = """
    SELECT
        item,
        menu
    FROM
        items
    ORDER BY
        item
    """
    db.execute(sql)
    items = db.fetchall()
    for item in items:
        item['menu'] = i10n_select(item['menu'], langs)
    return items


def _countries(db):
    sql = """
    SELECT DISTINCT
        country
    FROM
        sources
    ORDER BY
        country
    """
    db.execute(sql)
    return list(map(lambda x: x[0], db.fetchall()))


def _items(db, item = None, classs = None, langs = None):
    sql = """
    SELECT
        id,
        menu AS title
    FROM
        categories
    WHERE
        1 = 1 """ + \
        ("""AND id = CASE
            WHEN %(item)s < 1000 THEN 10
            ELSE (%(item)s / 1000)::int * 10
         END""" if item != None else '') + \
    """
    ORDER BY
        id
    """
    db.execute(sql, {'item': item})
    categs = db.fetchall()
    for categ in categs:
        categ['title'] = i10n_select(categ['title'], langs)

    sql = """
    SELECT
        item,
        categorie_id,
        marker_color AS color,
        marker_flag AS flag,
        menu AS title,
        levels,
        number,
        tags
    FROM
        items
    WHERE
        1 = 1""" + \
        ("AND item = %(item)s" if item != None else '') + \
    """
    ORDER BY
        item
    """
    db.execute(sql, {'item': item})
    items = db.fetchall()
    items = list(map(lambda r: dict(
        r,
        title = i10n_select(r['title'], langs),
        levels = r['number'] and list(map(lambda l_n: {'level': l_n[0], 'count': l_n[1]}, zip(r['levels'], r['number']))) or list(map(lambda i: {'level': i, 'count': 0}, [1, 2, 3])),
    ), items))
    items_categ = defaultdict(list)
    for i in items:
        items_categ[i['categorie_id']].append(i)

    sql = """
    SELECT
        item,
        class,
        title,
        level,
        tags,
        detail,
        fix,
        trap,
        example,
        source,
        resource
    FROM
        class
    WHERE
        1 = 1""" + \
        ("AND item = %(item)s" if item != None else '') + \
        ("AND class = %(classs)s" if classs != None else '') + \
    """
    ORDER BY
        item,
        class
    """
    db.execute(sql, {'item': item, 'classs': classs})
    classs = db.fetchall()
    classs = list(map(lambda c: dict(
        dict(c),
        title = i10n_select(c['title'], langs),
        detail = i10n_select(c['detail'], langs),
        fix = i10n_select(c['fix'], langs),
        trap = i10n_select(c['trap'], langs),
        example = i10n_select(c['example'], langs),
    ), classs))
    class_item = defaultdict(list)
    for c in classs:
        class_item[c['item']].append(c)

    return list(map(lambda categ:
        dict(
            categ,
            items = list(map(lambda item:
                dict(
                    item,
                    **{'class': class_item[item['item']]}
                ),
                items_categ[categ['id']]))
        ),
        categs))


def _tags(db):
    sql = """
    SELECT DISTINCT
        tag
    FROM
        (
        SELECT
            unnest(tags) AS tag
        FROM
            class
        ) AS t
    WHERE
        tag != ''
    ORDER BY
        tag
    """
    db.execute(sql)
    return list(map(lambda x: x[0], db.fetchall()))
