#!/usr/bin/env python
#
# SPDX-FileCopyrightText: 2014-2022 Fredrik Ahlberg, Angus Gratton, Espressif Systems (Shanghai) CO LTD, other contributors as noted.
#
# SPDX-License-Identifier: GPL-2.0-or-later

# This executable script is a thin wrapper around the main functionality in the esptool Python package
#
# If esptool is installed via setup.py or pip then this file is not used at all, it's compatibility
# for the older "run from source dir" esptool approach.

import esptool

if __name__ == '__main__':
    esptool._main()
