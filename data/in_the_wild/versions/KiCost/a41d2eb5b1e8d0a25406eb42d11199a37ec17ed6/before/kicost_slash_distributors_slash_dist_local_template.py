# MIT license
#
# Copyright (C) 2018 by XESS Corporation / Hildo Guillardi Junior / Max Maisel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Libraries.
import re
import sys
import hashlib

from ..global_vars import SEPRTR, DEBUG_OVERVIEW, DEBUG_OBSESSIVE
# Distributors definitions.
from .distributor import distributor_class

__all__ = ['dist_local_template']

if sys.version_info[0] < 3:
    from urlparse import urlsplit, urlunsplit

    def to_bytes(val):
        return val
else:
    from urllib.parse import urlsplit, urlunsplit

    def to_bytes(val):
        return val.encode('utf-8')


class dist_local_template(distributor_class):
    name = 'Local'
    type = 'local'
    enabled = True
    url = None

    @staticmethod
    def init_dist_dict():
        # We don't add distributors here, they are collected in query_part_info
        pass

    @staticmethod
    def query_part_info(parts, distributors, currency):
        """ Fill-in part information for locally-sourced parts not handled by Octopart.
            IMPORTANT: `distributors` can be modified. """
        # This loops through all the parts and finds any that are sourced from
        # local distributors that are not normally searched and places them into
        # the distributor disctionary.
        for part in parts:
            # Find the various distributors for this part by
            # looking for leading fields terminated by SEPRTR.
            for key in part.fields:
                try:
                    dist = key[:key.index(SEPRTR)]
                except ValueError:
                    continue

                # If the distributor is not in the list of web-scrapable distributors,
                # then it's a local distributor. Copy the local distributor template
                # and add it to the table of distributors.
                if dist not in distributors:
                    distributor_class.logger.log(DEBUG_OVERVIEW, 'Creating \'{}\' local distributor profile...'.format(dist))
                    new_dist = distributor_class.get_distributor_template('local_template')
                    new_dist['label']['name'] = dist  # Set dist name for spreadsheet header.
                    distributor_class.add_distributor(dist, new_dist)
                    distributors.append(dist)

        # Set part info to default blank values for all the distributors.
        for part in parts:  # TODO create this for just the current active distributor inside each module.
            # These bellow variable are all the data the each distributor/local API/scrap module needs to fill.
            part.part_num = {dist: '' for dist in distributors}  # Distributor catalogue number.
            part.url = {dist: '' for dist in distributors}  # Purchase distributor URL for the spefic part.
            part.price_tiers = {dist: {} for dist in distributors}  # Price break tiers; [[qty1, price1][qty2, price2]...]
            part.qty_avail = {dist: None for dist in distributors}  # Available quantity.
            part.qty_increment = {dist: None for dist in distributors}
            part.info_dist = {dist: {} for dist in distributors}
            part.currency = {dist: currency for dist in distributors}  # Default currency.
            part.moq = {dist: None for dist in distributors}  # Minimum order quantity allowd by the distributor.

        # Loop through the parts looking for those sourced by local distributors
        # that won't be found online. Place any user-added info for these parts
        # (such as pricing) into the part dictionary.
        for p in parts:
            # Find the manufacturer's part number if it exists.
            pn = p.fields.get('manf#')  # Returns None if no manf# field.

            # Now look for catalog number, price list and webpage link for this part.
            for dist in distributors:
                cat_num = p.fields.get(dist + ':cat#')
                pricing = p.fields.get(dist + ':pricing')
                link = p.fields.get(dist + ':link')
                if cat_num is None and pricing is None and link is None:
                    continue

                def make_unique_catalog_number(p):
                    FIELDS_MANFCAT = ([d + '#' for d in distributor_class.get_distributors_iter()] + ['manf#'])
                    FIELDS_NOT_HASH = (['manf#_qty', 'manf'] + FIELDS_MANFCAT + [d + '#_qty' for d in distributor_class.get_distributors_iter()])
                    # TODO unify the `FIELDS_NOT_HASH` configuration (used also in `edas/tools.py`).
                    hash_fields = {k: p.fields[k] for k in p.fields if k not in FIELDS_NOT_HASH}
                    hash_fields['dist'] = dist
                    return '#' + hashlib.md5(to_bytes(str(tuple(sorted(hash_fields.items()))))).hexdigest()

                cat_num = cat_num or pn or make_unique_catalog_number(p)
                p.fields[dist + ':cat#'] = cat_num  # Store generated cat#.
                p.part_num[dist] = cat_num

                try:
                    url_parts = list(urlsplit(link))
                    if url_parts[0] == '':
                        url_parts[0] = u'http'
                    link = urlunsplit(url_parts)
                except Exception:
                    # This happens when no part URL is found.
                    distributor_class.logger.log(DEBUG_OBSESSIVE, 'No part URL found to local \'{}\' distributor!'.format(dist))
                p.url[dist] = link

                price_tiers = {}
                try:
                    try:
                        local_currency = re.findall('[a-zA-Z]{3}', pricing)[0].upper()
                    except Exception:
                        local_currency = currency
                    pricing = re.sub('[^0-9.;:]', '', pricing)  # Keep only digits, decimals, delimiters.
                    for qty_price in pricing.split(';'):
                        qty, price = qty_price.split(SEPRTR)
                        if local_currency:
                            p.currency[dist] = local_currency
                        price_tiers[int(qty)] = float(price)
                    # p.moq[dist] = min(price_tiers.keys())
                except AttributeError:
                    # This happens when no pricing info is found.
                    distributor_class.logger.log(DEBUG_OBSESSIVE, 'No pricing information found to local \'{}\' distributor!'.format(dist))
                p.price_tiers[dist] = price_tiers


distributor_class.register(dist_local_template, 100)
