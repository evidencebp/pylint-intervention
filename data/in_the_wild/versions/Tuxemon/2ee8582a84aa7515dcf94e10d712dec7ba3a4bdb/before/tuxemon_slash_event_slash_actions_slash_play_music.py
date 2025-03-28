#
# Tuxemon
# Copyright (c) 2014-2017 William Edwards <shadowapex@gmail.com>,
#                         Benjamin Bean <superman2k5@gmail.com>
#
# This file is part of Tuxemon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import annotations

import logging
from typing import NamedTuple, final

from tuxemon import prepare
from tuxemon.db import db
from tuxemon.event.eventaction import EventAction
from tuxemon.platform import mixer

logger = logging.getLogger(__name__)


class PlayMusicActionParameters(NamedTuple):
    filename: str


@final
class PlayMusicAction(EventAction[PlayMusicActionParameters]):
    """
    Play a music file from "resources/music/".

    Script usage:
        .. code-block::

            play_music <filename>

    Script parameters:
        filename: Music file to load.

    """

    name = "play_music"
    param_class = PlayMusicActionParameters

    def start(self) -> None:
        filename = self.parameters.filename

        try:
            path = prepare.fetch("music", db.lookup_file("music", filename))
            mixer.music.load(path)
            mixer.music.set_volume(prepare.CONFIG.music_volume)
            mixer.music.play(-1)
        except Exception as e:
            logger.error(e)
            logger.error("unable to play music")

        # Keep track of what song we're currently playing
        if self.session.client.current_music["song"]:
            self.session.client.current_music["previoussong"] = self.session.client.current_music["song"]
        self.session.client.current_music["status"] = "playing"
        self.session.client.current_music["song"] = filename
