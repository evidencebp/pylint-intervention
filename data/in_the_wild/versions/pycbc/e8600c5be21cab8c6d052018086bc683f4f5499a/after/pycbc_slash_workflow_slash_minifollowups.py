# Copyright (C) 2015 Christopher M. Biwer
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging
from pycbc.workflow.core import Executable, FileList, Node
from pycbc.workflow.plotting import PlotExecutable

def setup_minifollowups(workflow, coinc_file, 
                                  single_triggers,
                                  tmpltbank_file, 
                             out_dir, tags=None):
    """ This performs a series of followup jobs on the num_events-th loudest
    events.
    """
    logging.info('Entering minifollowups module')

    # check if minifollowups section exists
    # if not then do not do add minifollowup jobs to the workflow
    if not workflow.cp.has_section('workflow-minifollowups'):
        logging.info('There is no [workflow-minifollowups] section in configuration file')
        logging.info('Leaving minifollowups')
        return output_filelist
    
    
    tags = [] if tags is None else tags
    makedir(out_dir)

    # create a FileList that will contain all output files
    output_filelist = FileList([])

    # loop over number of loudest events to be followed up
    num_events = int(workflow.cp.get_opt_tags('workflow-minifollowups', 'num-events', ''))
    for num_event in range(num_events):
        num_event += 1
        
        

    logging.info('Leaving minifollowups module')

    return output_filelist



