# -*- coding: utf-8 -*-
import importlib
import logging
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.path.pardir) + '/..'))

from mycodo.config import CAMERA_INFO
from mycodo.config import DEPENDENCIES_GENERAL
from mycodo.config import FUNCTION_INFO
from mycodo.config import INSTALL_DIRECTORY
from mycodo.config import DEPENDENCY_LOG_FILE
from mycodo.config import METHOD_INFO
from mycodo.databases.models import Actions
from mycodo.databases.models import Widget
from mycodo.databases.models import Camera
from mycodo.databases.models import Trigger
from mycodo.databases.models import CustomController
from mycodo.databases.models import EnergyUsage
from mycodo.databases.models import Function
from mycodo.databases.models import Input
from mycodo.databases.models import Method
from mycodo.databases.models import Output
from mycodo.mycodo_flask.utils.utils_general import return_dependencies
from mycodo.utils.functions import parse_function_information
from mycodo.utils.actions import parse_action_information
from mycodo.utils.database import db_retrieve_table_daemon
from mycodo.utils.outputs import parse_output_information
from mycodo.utils.inputs import parse_input_information
from mycodo.utils.system_pi import cmd_output

logger = logging.getLogger("mycodo.update_dependencies")


def get_installed_dependencies():
    met_deps = []

    list_dependencies = [
        parse_function_information(),
        parse_action_information(),
        parse_input_information(),
        parse_output_information(),
        CAMERA_INFO,
        FUNCTION_INFO,
        METHOD_INFO,
        DEPENDENCIES_GENERAL
    ]

    for each_section in list_dependencies:
        for device_type in each_section:
            if 'dependencies_module' in each_section[device_type]:
                dep_mod = each_section[device_type]['dependencies_module']
                for (install_type, package, install_id) in dep_mod:
                    entry = '{0} {1}'.format(install_type, install_id)
                    if install_type == 'pip-pypi':
                        try:
                            module = importlib.util.find_spec(package)
                            if module is not None and entry not in met_deps:
                                met_deps.append(entry)
                        except Exception:
                            logger.error(
                                'Exception checking python dependency: '
                                '{dep}'.format(dep=package))
                    elif install_type == 'apt':
                        start = "dpkg-query -W -f='${Status}'"
                        end = '2>/dev/null | grep -c "ok installed"'
                        cmd = "{} {} {}".format(start, package, end)
                        _, _, status = cmd_output(cmd, user='root')
                        if not status and entry not in met_deps:
                            met_deps.append(entry)

    return met_deps


if __name__ == "__main__":
    dependencies = []
    devices = []

    input_dev = db_retrieve_table_daemon(Input)
    for each_dev in input_dev:
        if each_dev.device not in devices:
            devices.append(each_dev.device)

    output = db_retrieve_table_daemon(Output)
    for each_dev in output:
        if each_dev.output_type not in devices:
            devices.append(each_dev.output_type)

    camera = db_retrieve_table_daemon(Camera)
    for each_dev in camera:
        if each_dev.library not in devices:
            devices.append(each_dev.library)

    method = db_retrieve_table_daemon(Method)
    for each_dev in method:
        if each_dev.method_type not in devices:
            devices.append(each_dev.method_type)

    function = db_retrieve_table_daemon(Function)
    for each_dev in function:
        if each_dev.function_type not in devices:
            devices.append(each_dev.function_type)

    trigger = db_retrieve_table_daemon(Trigger)
    for each_dev in trigger:
        if each_dev.trigger_type not in devices:
            devices.append(each_dev.trigger_type)

    actions = db_retrieve_table_daemon(Actions)
    for each_dev in actions:
        if each_dev.action_type not in devices:
            devices.append(each_dev.action_type)

    custom = db_retrieve_table_daemon(CustomController)
    for each_dev in custom:
        if each_dev.device not in devices:
            devices.append(each_dev.device)

    widget = db_retrieve_table_daemon(Widget)
    for each_dev in widget:
        if each_dev.graph_type not in devices:
            devices.append(each_dev.graph_type)

    energy_usage = db_retrieve_table_daemon(EnergyUsage)
    for each_dev in energy_usage:
        if 'highstock' not in devices:
            devices.append('highstock')

    print(devices)

    for each_device in devices:
        device_unmet_dependencies, _, _ = return_dependencies(each_device)
        for each_dep in device_unmet_dependencies:
            if each_dep not in dependencies:
                dependencies.append(each_dep)

    if dependencies:
        print("Unmet dependencies found: {}".format(dependencies))

        for each_dep in dependencies:
            if each_dep[1] == 'bash-commands':
                for each_command in each_dep[2]:
                    command = "{cmd} | ts '[%Y-%m-%d %H:%M:%S]' >> {log} 2>&1".format(
                        cmd=each_command,
                        log=DEPENDENCY_LOG_FILE)
                    cmd_out, cmd_err, cmd_status = cmd_output(
                        command, timeout=600, cwd="/tmp")
                    ret_list = []
                    if cmd_out != b"":
                        ret_list.append("out: {}".format(cmd_out))
                    if cmd_err != b"":
                        ret_list.append("error: {}".format(cmd_err))
                    if cmd_status is not None:
                        ret_list.append("status: {}".format(cmd_status))
                    if ret_list:
                        logger.info("Command returned: {}".format(", ".join(ret_list)))
            else:
                install_cmd = "{pth}/mycodo/scripts/dependencies.sh {dep}".format(
                    pth=INSTALL_DIRECTORY,
                    dep=each_dep[1])
                output, err, stat = cmd_output(install_cmd, user='root')
                formatted_output = output.decode("utf-8").replace('\\n', '\n')

    # Update installed dependencies
    installed_deps = get_installed_dependencies()
    apt_deps = ''
    for each_dep in installed_deps:
        if each_dep.split(' ')[0] == 'apt':
            apt_deps += ' {}'.format(each_dep.split(' ')[1])

    if apt_deps:
        update_cmd = 'apt-get install -y {dep}'.format(
            home=INSTALL_DIRECTORY, dep=apt_deps)
        output, err, stat = cmd_output(update_cmd, user='root')
        formatted_output = output.decode("utf-8").replace('\\n', '\n')
        print("{}".format(formatted_output))

    tmp_req_file = '{home}/install/requirements-generated.txt'.format(home=INSTALL_DIRECTORY)
    with open(tmp_req_file, "w") as f:
        for each_dep in installed_deps:
            if each_dep.split(' ')[0] == 'pip-pypi':
                f.write('{dep}\n'.format(dep=each_dep.split(' ')[1]))

    pip_req_update = '{home}/env/bin/python -m pip install --upgrade -r {home}/install/requirements-generated.txt'.format(
        home=INSTALL_DIRECTORY)
    output, err, stat = cmd_output(pip_req_update, user='root')
    formatted_output = output.decode("utf-8").replace('\\n', '\n')
    print("{}".format(formatted_output))
    os.remove(tmp_req_file)
