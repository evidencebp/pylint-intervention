#
# Tuxemon
# Copyright (C) 2014, William Edwards <shadowapex@gmail.com>
#
# This file is part of Tuxemon.
#
# Tuxemon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tuxemon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tuxemon.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributor(s):
#
# Adam Chevalier <chevalierAdam2@gmail.com>
# Leif Theden <leif.theden@gmail.com>
#

import logging

from tuxemon.npc import NPC

logger = logging.getLogger(__name__)

"""
[Core]
Name = Common
Module = Common

[Documentation]
Author = Adam Chevalier
Version = 1.0
Website = http://www.tuxemon.org
Description = Plugin containing utility functions common to multiple action plugins.
"""


class CommonAction:
    name = "Common"

    @staticmethod
    def set_character_attribute(
        character: NPC,
        attribute: str,
        value: str,
    ) -> None:
        """
        Set a character's (npc or player) attribute.

        Parameters:
            character: The NPC object to modify.
            attribute: The attribute to modify.
            value: The value to set the attribute to, as a string.

        """

        # check for valid inputs
        # trigger an AttributeError if the attribute doesn't already exist
        attr = None
        try:
            attr = getattr(character, attribute)
        except AttributeError:
            logger.warning("Player attribute '{0}' specified does not exist.", attribute)
            return

        try:
            val = type(attr)(value)
        except TypeError:
            logger.warning("The value given cannot be parsed into the correct type for '{0}'", attribute)
            return

        setattr(character, attribute, val)

    @staticmethod
    def modify_character_attribute(
        character: NPC,
        attribute: str,
        modifier: str,
    ) -> None:
        """
        Modify a character's (npc or player) attribute.

        Default behavior is to add the given mod to the attribute, but
        prepending a percent (%) symbol will cause the mod to be used
        as a multiplier.

        Parameters:
            character: The Player object to modify.
            attribute: The attribute to modify.
            modifier: The modifier to apply the attribute by.

        """

        # check for valid inputs
        # trigger an AttributeError if the attribute doesn't already exist
        try:
            attr = getattr(character, attribute)
        except AttributeError:
            logger.warning("Player attribute '{0}' specified does not exist.", attribute)
            return

        if "%" in modifier:
            attr *= float(modifier.replace("%", ""))
        else:
            attr += float(modifier)

        setattr(character, attribute, attr)
