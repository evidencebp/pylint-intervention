# coding=utf-8
import calendar
import csv
import datetime
import logging
import os
import subprocess
from importlib import import_module
from io import StringIO

import flask_login
from dateutil.parser import parse as date_parse
from flask import Response
from flask import flash
from flask import jsonify
from flask import redirect
from flask import send_file
from flask import send_from_directory
from flask import url_for
from flask.blueprints import Blueprint
from flask_babel import gettext
from flask_limiter import Limiter
from sqlalchemy import and_

from mycodo.config import DOCKER_CONTAINER
from mycodo.config import INSTALL_DIRECTORY
from mycodo.config import LOG_PATH
from mycodo.config import PATH_CAMERAS
from mycodo.config import PATH_NOTE_ATTACHMENTS
from mycodo.databases.models import Camera
from mycodo.databases.models import Conversion
from mycodo.databases.models import DeviceMeasurements
from mycodo.databases.models import Input
from mycodo.databases.models import NoteTags
from mycodo.databases.models import Notes
from mycodo.databases.models import Output
from mycodo.databases.models import OutputChannel
from mycodo.databases.models import PID
from mycodo.mycodo_client import DaemonControl
from mycodo.mycodo_flask.routes_authentication import clear_cookie_auth
from mycodo.mycodo_flask.utils import utils_general
from mycodo.mycodo_flask.utils.utils_general import get_ip_address
from mycodo.mycodo_flask.utils.utils_output import get_all_output_states
from mycodo.utils.influx import influx_time_str_to_milliseconds
from mycodo.utils.influx import query_string
from mycodo.utils.system_pi import assure_path_exists
from mycodo.utils.system_pi import return_measurement_info
from mycodo.utils.system_pi import str_is_float

blueprint = Blueprint('routes_general',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_ip_address)


@blueprint.route('/')
def home():
    """Load the default landing page."""
    try:
        if flask_login.current_user.is_authenticated:
            if flask_login.current_user.landing_page == 'live':
                return redirect(url_for('routes_page.page_live'))
            elif flask_login.current_user.landing_page == 'dashboard':
                return redirect(url_for('routes_dashboard.page_dashboard_default'))
            elif flask_login.current_user.landing_page == 'info':
                return redirect(url_for('routes_page.page_info'))
            return redirect(url_for('routes_page.page_live'))
    except:
        logger.error("User may not be logged in. Clearing cookie auth.")
    return clear_cookie_auth()

@blueprint.route('/index_page')
def index_page():
    """Load the index page."""
    try:
        if not flask_login.current_user.index_page:
            return home()
        elif flask_login.current_user.index_page == 'landing':
            return home()
        else:
            if flask_login.current_user.is_authenticated:
                if flask_login.current_user.index_page == 'live':
                    return redirect(url_for('routes_page.page_live'))
                elif flask_login.current_user.index_page == 'dashboard':
                    return redirect(url_for('routes_dashboard.page_dashboard_default'))
                elif flask_login.current_user.index_page == 'info':
                    return redirect(url_for('routes_page.page_info'))
                return redirect(url_for('routes_page.page_live'))
    except:
        logger.error("User may not be logged in. Clearing cookie auth.")
    return clear_cookie_auth()

@blueprint.route('/settings', methods=('GET', 'POST'))
@flask_login.login_required
def page_settings():
    return redirect('settings/general')


@blueprint.route('/note_attachment/<filename>')
@flask_login.login_required
def send_note_attachment(filename):
    """Return a file from the note attachment directory."""
    file_path = os.path.join(PATH_NOTE_ATTACHMENTS, filename)
    if file_path is not None:
        try:
            if os.path.abspath(file_path).startswith(PATH_NOTE_ATTACHMENTS):
                return send_file(file_path, as_attachment=True)
        except Exception:
            logger.exception("Send note attachment")


@blueprint.route('/camera/<camera_unique_id>/<img_type>/<filename>')
@flask_login.login_required
def camera_img_return_path(camera_unique_id, img_type, filename):
    """Return an image from stills or time-lapses."""
    camera = Camera.query.filter(Camera.unique_id == camera_unique_id).first()
    camera_path = assure_path_exists(
        os.path.join(PATH_CAMERAS, camera.unique_id))
    if img_type == 'still':
        if camera.path_still:
            path = camera.path_still
        else:
            path = os.path.join(camera_path, img_type)
    elif img_type == 'timelapse':
        if camera.path_timelapse:
            path = camera.path_timelapse
        else:
            path = os.path.join(camera_path, img_type)
    else:
        return "Unknown Image Type"

    if os.path.isdir(path):
        files = (files for files in os.listdir(path)
                 if os.path.isfile(os.path.join(path, files)))
    else:
        files = []
    if filename in files:
        path_file = os.path.join(path, filename)
        if os.path.abspath(path_file).startswith(path):
            return send_file(path_file, mimetype='image/jpeg')

    return "Image not found"


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@blueprint.route('/video_feed/<unique_id>')
@flask_login.login_required
def video_feed(unique_id):
    """Video streaming route. Put this in the src attribute of an img tag."""
    camera_options = Camera.query.filter(Camera.unique_id == unique_id).first()
    camera_stream = import_module('mycodo.mycodo_flask.camera.camera_' + camera_options.library).Camera
    camera_stream.set_camera_options(camera_options)
    return Response(gen(camera_stream(unique_id=unique_id)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route('/outputstate')
@flask_login.login_required
def gpio_state():
    """Return all output states."""
    return jsonify(get_all_output_states())


@blueprint.route('/outputstate_unique_id/<unique_id>/<channel_id>')
@flask_login.login_required
def gpio_state_unique_id(unique_id, channel_id):
    """Return the GPIO state, for dashboard output."""
    channel = OutputChannel.query.filter(OutputChannel.unique_id == channel_id).first()
    daemon_control = DaemonControl()
    state = daemon_control.output_state(unique_id, channel.channel)
    return jsonify(state)


@blueprint.route('/widget_execute/<unique_id>')
@flask_login.login_required
def widget_execute(unique_id):
    """Return the response from the execution of widget code."""
    daemon_control = DaemonControl()
    return_value = daemon_control.widget_execute(unique_id)
    return jsonify(return_value)


@blueprint.route('/time')
@flask_login.login_required
def get_time():
    """Return the current time."""
    return jsonify(datetime.datetime.now().strftime('%m/%d %H:%M'))


@blueprint.route('/dl/<dl_type>/<path:filename>')
@flask_login.login_required
def download_file(dl_type, filename):
    """Serve log file to download."""
    if dl_type == 'log':
        return send_from_directory(LOG_PATH, filename, as_attachment=True)

    return '', 204


@blueprint.route('/last/<unique_id>/<measure_type>/<measurement_id>/<period>')
@flask_login.login_required
def last_data(unique_id, measure_type, measurement_id, period):
    """Return the most recent time and value from influxdb."""
    if not str_is_float(period):
        return '', 204

    if measure_type not in ['input', 'function', 'output', 'pid']:
        return '', 204

    measure = DeviceMeasurements.query.filter(
        DeviceMeasurements.unique_id == measurement_id).first()

    if measure:
        conversion = Conversion.query.filter(
            Conversion.unique_id == measure.conversion_id).first()
    else:
        conversion = None

    channel, unit, measurement = return_measurement_info(
        measure, conversion)

    if hasattr(measure, 'measurement_type') and measure.measurement_type == 'setpoint':
        setpoint_pid = PID.query.filter(PID.unique_id == measure.device_id).first()
        if setpoint_pid and ',' in setpoint_pid.measurement:
            pid_measurement = setpoint_pid.measurement.split(',')[1]
            setpoint_measurement = DeviceMeasurements.query.filter(
                DeviceMeasurements.unique_id == pid_measurement).first()
            if setpoint_measurement:
                conversion = Conversion.query.filter(
                    Conversion.unique_id == setpoint_measurement.conversion_id).first()
                _, unit, measurement = return_measurement_info(setpoint_measurement, conversion)
    try:
        if period != '0':
            data = query_string(
                unit, unique_id,
                measure=measurement, channel=channel,
                value='LAST', past_sec=period)
        else:
            data = query_string(
                unit, unique_id,
                measure=measurement, channel=channel, value='LAST')

        number = len(data)
        time_raw = data[number - 1][0]
        value = data[number - 1][1]
        value = float(value)
        # Convert date-time to epoch (potential bottleneck for data)
        dt = date_parse(time_raw)
        timestamp = calendar.timegm(dt.timetuple()) * 1000
        live_data = f'[{timestamp},{value}]'

        return Response(live_data, mimetype='text/json')
    except KeyError:
        logger.debug("No Data returned form influxdb")
        return '', 204
    except IndexError:
        logger.debug("No Data returned form influxdb")
        return '', 204
    except Exception as err:
        logger.exception(f"URL for 'last_data' raised and error: {err}")
        return '', 204


@blueprint.route('/export_data/<unique_id>/<measurement_id>/<start_seconds>/<end_seconds>')
@flask_login.login_required
def export_data(unique_id, measurement_id, start_seconds, end_seconds):
    """
    Return data from start_seconds to end_seconds from influxdb.
    Used for exporting data.
    """
    output = Output.query.filter(Output.unique_id == unique_id).first()
    input_dev = Input.query.filter(Input.unique_id == unique_id).first()

    if output:
        name = output.name
    elif input_dev:
        name = input_dev.name
    else:
        name = None

    device_measurement = DeviceMeasurements.query.filter(
        DeviceMeasurements.unique_id == measurement_id).first()
    if device_measurement:
        conversion = Conversion.query.filter(
            Conversion.unique_id == device_measurement.conversion_id).first()
    else:
        conversion = None
    channel, unit, measurement = return_measurement_info(
        device_measurement, conversion)

    utc_offset_timedelta = datetime.datetime.utcnow() - datetime.datetime.now()
    start = datetime.datetime.fromtimestamp(float(start_seconds))
    start += utc_offset_timedelta
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end = datetime.datetime.fromtimestamp(float(end_seconds))
    end += utc_offset_timedelta
    end_str = end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    data = query_string(
        unit, unique_id,
        measure=measurement, channel=channel,
        start_str=start_str, end_str=end_str)

    if not data:
        flash('No measurements to export in this time period', 'error')
        return redirect(url_for('routes_page.page_export'))

    # Generate column names
    col_1 = 'timestamp (UTC)'
    col_2 = f'{name} {measurement} ({unique_id})'
    csv_filename = f'{unique_id}_{name}_{measurement}.csv'

    def iter_csv(_data):
        """Stream CSV file to user for download."""
        line = StringIO()
        writer = csv.writer(line)
        writer.writerow([col_1, col_2])
        for csv_line in _data:
            writer.writerow([
                str(csv_line[0][:-4]).replace('T', ' '),
                csv_line[1]
            ])
            line.seek(0)
            yield line.read()
            line.truncate(0)
            line.seek(0)

    response = Response(iter_csv(data), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename="{csv_filename}"'
    return response


@blueprint.route('/async/<device_id>/<device_type>/<measurement_id>/<start_seconds>/<end_seconds>')
@flask_login.login_required
def async_data(device_id, device_type, measurement_id, start_seconds, end_seconds):
    """
    Return data from start_seconds to end_seconds from influxdb.
    Used for asynchronous graph display of many points (up to millions).
    """
    count_points = None
    first_point = None

    if device_type == 'tag':
        notes_list = []
        tag = NoteTags.query.filter(NoteTags.unique_id == device_id).first()

        start = datetime.datetime.utcfromtimestamp(float(start_seconds))
        if end_seconds == '0':
            end = datetime.datetime.utcnow()
        else:
            end = datetime.datetime.utcfromtimestamp(float(end_seconds))

        notes = Notes.query.filter(
            and_(Notes.date_time >= start, Notes.date_time <= end)).all()
        for each_note in notes:
            if tag.unique_id in each_note.tags.split(','):
                notes_list.append(
                    [each_note.date_time.strftime("%Y-%m-%dT%H:%M:%S.000000000Z"), each_note.name, each_note.note])

        if notes_list:
            return jsonify(notes_list)
        else:
            return '', 204

    if device_type in ['input', 'function', 'output', 'pid']:
        measure = DeviceMeasurements.query.filter(
            DeviceMeasurements.unique_id == measurement_id).first()
    else:
        measure = None

    if not measure:
        return "Could not find measurement"

    if measure:
        conversion = Conversion.query.filter(
            Conversion.unique_id == measure.conversion_id).first()
    else:
        conversion = None
    channel, unit, measurement = return_measurement_info(
        measure, conversion)

    # Get all data if start/end not specified
    if start_seconds == '0' and end_seconds == '0':
        # Get how many points there are
        data = query_string(
            unit, device_id,
            measure=measurement,
            channel=channel,
            value='COUNT')

        if not data:
            return '', 204

        count_points = data[0][1]

        # Get the timestamp of the first point
        data = query_string(
            unit, device_id,
            measure=measurement,
            channel=channel,
            limit=1)

        if not data:
            return '', 204

        first_point = data[0][0]

        end = datetime.datetime.utcnow()
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Set the time frame to the past start epoch to now
    elif start_seconds != '0' and end_seconds == '0':
        start = datetime.datetime.utcfromtimestamp(float(start_seconds))
        start_str = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.datetime.utcnow()
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = query_string(
            unit, device_id,
            measure=measurement,
            channel=channel,
            start_str=start_str,
            end_str=end_str,
            value='COUNT')

        if not data:
            return '', 204

        count_points = data[0][1]

        # Get the timestamp of the first point in the past year
        data = query_string(
            unit, device_id,
            measure=measurement,
            channel=channel,
            start_str=start_str,
            end_str=end_str,
            limit=1)

        if not data:
            return '', 204

        first_point = data[0][0]
    else:
        start = datetime.datetime.utcfromtimestamp(float(start_seconds))
        start_str = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.datetime.utcfromtimestamp(float(end_seconds))
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = query_string(
            unit, device_id,
            measure=measurement,
            channel=channel,
            start_str=start_str,
            end_str=end_str,
            value='COUNT')

        if not data:
            return '', 204

        count_points = data[0][1]

        # Get the timestamp of the first point in the past year
        data = query_string(
            unit, device_id,
            measure=measurement,
            channel=channel,
            start_str=start_str,
            end_str=end_str,
            limit=1)

        if not data:
            return '', 204

        first_point = data[0][0]

    if not first_point:
        logger.error("No first point")
        return '', 204

    start = datetime.datetime.strptime(
        influx_time_str_to_milliseconds(first_point),
        '%Y-%m-%dT%H:%M:%S.%f')
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    logger.debug(f'Count = {count_points}')
    logger.debug(f'Start = {start}')
    logger.debug(f'End   = {end}')

    # How many seconds between the start and end period
    time_difference_seconds = (end - start).total_seconds()
    logger.debug(f'Difference seconds = {time_difference_seconds}')

    # If there are more than 700 points in the time frame, we need to group
    # data points into 700 groups with points averaged in each group.
    if count_points > 700:
        # Average period between input reads
        seconds_per_point = time_difference_seconds / count_points
        logger.debug(f'Seconds per point = {seconds_per_point}')

        # How many seconds to group data points in
        group_seconds = int(time_difference_seconds / 700)
        logger.debug(f'Group seconds = {group_seconds}')

        try:
            data = query_string(
                unit, device_id,
                measure=measurement,
                channel=channel,
                start_str=start_str,
                end_str=end_str,
                group_sec=group_seconds,
                value='MEAN')

            if not data:
                return '', 204

            return jsonify(data)
        except Exception as err:
            logger.error(f"URL for 'async_data' raised and error: {err}")
            return '', 204
    else:
        try:
            data = query_string(
                unit, device_id,
                measure=measurement,
                channel=channel,
                start_str=start_str,
                end_str=end_str)

            if not data:
                return '', 204

            return jsonify(data)
        except Exception as err:
            logger.error(f"URL for 'async_data' raised and error: {err}")
            return '', 204


@blueprint.route('/async_usage/<device_id>/<unit>/<channel>/<start_seconds>/<end_seconds>')
@flask_login.login_required
def async_usage_data(device_id, unit, channel, start_seconds, end_seconds):
    """
    Return data from start_seconds to end_seconds from influxdb.
    Used for asynchronous energy usage display of many points (up to millions).
    """
    # Set the time frame to the past year if start/end not specified
    if start_seconds == '0' and end_seconds == '0':
        # Get how many points there are in the past year
        data = query_string(
            unit, device_id,
            channel=channel,
            value='COUNT')

        if not data:
            return '', 204

        count_points = data[0][1]

        # Get the timestamp of the first point in the past year
        data = query_string(
            unit, device_id,
            channel=channel,
            limit=1)

        if not data:
            return '', 204

        first_point = data[0][0]
        end = datetime.datetime.utcnow()
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Set the time frame to the past start epoch to now
    elif start_seconds != '0' and end_seconds == '0':
        start = datetime.datetime.utcfromtimestamp(float(start_seconds))
        start_str = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.datetime.utcnow()
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = query_string(
            unit, device_id,
            channel=channel,
            value='COUNT',
            start_str=start_str,
            end_str=end_str)

        if not data:
            return '', 204

        count_points = data[0][1]

        # Get the timestamp of the first point in the past year
        data = query_string(
            unit, device_id,
            channel=channel,
            start_str=start_str,
            end_str=end_str,
            limit=1)

        if not data:
            return '', 204

        first_point = data[0][0]
    else:
        start = datetime.datetime.utcfromtimestamp(float(start_seconds))
        start_str = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.datetime.utcfromtimestamp(float(end_seconds))
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        data = query_string(
            unit, device_id,
            channel=channel,
            value='COUNT',
            start_str=start_str,
            end_str=end_str)

        if not data:
            return '', 204

        count_points = data[0][1]

        # Get the timestamp of the first point in the past year
        data = query_string(
            unit, device_id,
            channel=channel,
            start_str=start_str,
            end_str=end_str,
            limit=1)

        if not data:
            return '', 204

        first_point = data[0][0]

    start = datetime.datetime.strptime(
        influx_time_str_to_milliseconds(first_point),
        '%Y-%m-%dT%H:%M:%S.%f')
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    logger.debug(f'Count = {count_points}')
    logger.debug(f'Start = {start}')
    logger.debug(f'End   = {end}')

    # How many seconds between the start and end period
    time_difference_seconds = (end - start).total_seconds()
    logger.debug(f'Difference seconds = {time_difference_seconds}')

    # If there are more than 700 points in the time frame, we need to group
    # data points into 700 groups with points averaged in each group.
    if count_points > 700:
        # Average period between input reads
        seconds_per_point = time_difference_seconds / count_points
        logger.debug(f'Seconds per point = {seconds_per_point}')

        # How many seconds to group data points in
        group_seconds = int(time_difference_seconds / 700)
        logger.debug(f'Group seconds = {group_seconds}')

        try:
            data = query_string(
                unit, device_id,
                channel=channel,
                value='MEAN',
                start_str=start_str,
                end_str=end_str,
                group_sec=group_seconds)

            if not data:
                return '', 204

            return jsonify(data)
        except Exception as err:
            logger.error(f"URL for 'async_data' raised and error: {err}")
            return '', 204
    else:
        try:
            data = query_string(
                unit, device_id,
                channel=channel,
                start_str=start_str,
                end_str=end_str)

            if not data:
                return '', 204

            return jsonify(data)
        except Exception as err:
            logger.error(f"URL for 'async_usage' raised and error: {err}")
            return '', 204


@blueprint.route('/daemonactive')
@flask_login.login_required
def daemon_active():
    """Return 'alive' if the daemon is running."""
    try:
        control = DaemonControl()
        return control.daemon_status()
    except Exception as err:
        logger.error(f"URL for 'daemon_active' raised and error: {err}")
        return '0'


@blueprint.route('/systemctl/<action>')
@flask_login.login_required
def computer_command(action):
    """Execute one of several commands as root."""
    if not utils_general.user_has_permission('edit_settings'):
        return redirect(url_for('routes_general.home'))

    try:
        if action not in ['restart', 'shutdown', 'daemon_restart', 'frontend_reload']:
            flash(f"Unrecognized command: {action}", "success")
            return redirect('/settings')

        if DOCKER_CONTAINER:
            if action == 'daemon_restart':
                control = DaemonControl()
                control.terminate_daemon()
            elif action == 'frontend_reload':
                subprocess.Popen('docker restart mycodo_flask 2>&1', shell=True)
        else:
            cmd = f'{INSTALL_DIRECTORY}/mycodo/scripts/mycodo_wrapper {action} 2>&1'
            subprocess.Popen(cmd, shell=True)

        if action == 'restart':
            flash(gettext("System rebooting in 10 seconds"), "success")
        elif action == 'shutdown':
            flash(gettext("System shutting down in 10 seconds"), "success")
        elif action == 'daemon_restart':
            flash(gettext("Command to restart the daemon sent"), "success")
        elif action == 'frontend_reload':
            flash(gettext("Command to reload the frontend sent"), "success")

        return redirect('/settings')

    except Exception as err:
        logger.error(f"System command '{action}' raised and error: {err}")
        flash(f"System command '{action}' raised and error: {err}", "error")
        return redirect(url_for('routes_general.home'))


# @blueprint.route('/generate_thermal_image/<unique_id>/<timestamp>')
# @flask_login.login_required
# def generate_thermal_image_from_timestamp(unique_id, timestamp):
#     """Return a file from the note attachment directory."""
#     ts_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#     camera_path = assure_path_exists(
#         os.path.join(PATH_CAMERAS, unique_id))
#     filename = f'Still-{unique_id}-{ts_now}.jpg'.replace(" ", "_")
#     save_path = assure_path_exists(os.path.join(camera_path, 'thermal'))
#     assure_path_exists(save_path)
#     path_file = os.path.join(save_path, filename)
#
#     input_dev = Input.query.filter(Input.unique_id == unique_id).first()
#     pixels = []
#     success = True
#
#     start = int(int(timestamp) / 1000.0)  # Round down
#     end = start + 1  # Round up
#
#     start_timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.000000000Z', time.gmtime(start))
#     end_timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.000000000Z', time.gmtime(end))
#
#     for each_channel in range(input_dev.channels):
#         measurement = f'channel_{each_channel}'
#         data = query_string(measurement, unique_id,
#                                  start_str=start_timestamp,
#                                  end_str=end_timestamp)
#
#         if not data:
#             logger.error('No measurements to export in this time period')
#             success = False
#         else:
#             pixels.append(data[0][1])
#
#     if success:
#         from mycodo.utils.image import generate_thermal_image_from_pixels
#         generate_thermal_image_from_pixels(pixels, 8, 8, path_file)
#         return send_file(path_file, mimetype='image/jpeg')
#     else:
#         return "Could not generate image"
