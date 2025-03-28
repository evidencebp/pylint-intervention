import json
from dataclasses import dataclass
from importlib_metadata import entry_points
from invisibleroads_macros_disk import is_path_in_folder
from invisibleroads_macros_log import format_path
from logging import getLogger
from os.path import basename, exists, join, splitext
from string import Template

from ..constants import (
    FUNCTION_BY_NAME,
    MAXIMUM_FILE_CACHE_LENGTH,
    VARIABLE_ID_PATTERN)
from ..exceptions import (
    CrossComputeConfigurationError,
    CrossComputeDataError)
from ..macros.disk import FileCache
from ..macros.package import import_attribute
from ..macros.web import get_html_from_markdown


@dataclass(repr=False, eq=False, order=False, frozen=True)
class VariableElement():

    id: str
    mode_name: str
    function_names: list[str]
    uri: str
    for_print: bool


class VariableView():

    view_name = 'variable'

    def __init__(self, variable_definition):
        self.variable_definition = variable_definition
        self.variable_id = variable_definition['id']
        self.variable_path = variable_definition['path']
        self.mode_name = variable_definition['mode']

    @classmethod
    def get_from(Class, variable_definition):
        view_name = variable_definition['view']
        try:
            View = VIEW_BY_NAME[view_name]
        except KeyError:
            L.error('%s view not installed', view_name)
            View = Class
        return View(variable_definition)

    def load(self, absolute_batch_folder):
        self.data = self._get_data(absolute_batch_folder)
        self.configuration = self._get_configuration(absolute_batch_folder)
        return self

    def parse(self, data):
        return data

    def render(self, x: VariableElement):
        if x.mode_name == 'input':
            render = self.render_input
        else:
            render = self.render_output
        return render(x)

    def render_input(self, x: VariableElement):
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': '',
            'js_texts': [],
        }

    def render_output(self, x: VariableElement):
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': '',
            'js_texts': [],
        }

    def _get_data(self, absolute_batch_folder):
        variable_path = self.variable_path
        if variable_path == 'ENVIRONMENT':
            return
        try:
            variable_data = load_variable_data_from_folder(
                absolute_batch_folder, self.mode_name, variable_path,
                self.variable_id)
        except CrossComputeDataError:
            return
        return variable_data

    def _get_configuration(self, absolute_batch_folder):
        variable_configuration = self.variable_definition.get(
            'configuration', {})
        configuration_path = variable_configuration.get('path')
        if configuration_path:
            path = join(
                absolute_batch_folder, self.mode_name, configuration_path)
            try:
                variable_configuration.update(json.load(open(path, 'rt')))
            except OSError:
                L.error('path not found %s', format_path(path))
            except json.JSONDecodeError:
                L.error('must be json %s', format_path(path))
            except TypeError:
                L.error('must contain a dictionary %s', format_path(path))
        return variable_configuration


class LinkView(VariableView):

    view_name = 'link'

    def render_output(self, x: VariableElement):
        variable_id = self.variable_id
        c = self.configuration
        name = c.get('name', basename(self.variable_path))
        text = c.get('text', name)
        body_text = (
            f'<a id="{x.id}" href="{x.uri}" '
            f'class="{self.view_name} {variable_id}" download="{name}">'
            f'{text}</a>')
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': body_text,
            'js_texts': [],
        }


class StringView(VariableView):

    view_name = 'string'
    input_type = 'text'
    function_by_name = FUNCTION_BY_NAME

    def render_input(self, x: VariableElement):
        variable_id = self.variable_id
        value = '' if self.data is None else self.data
        body_text = (
            f'<input id="{x.id}" name="{variable_id}" '
            f'class="{self.view_name} {variable_id}" '
            f'value="{value}" type="{self.input_type}">')
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': body_text,
            'js_texts': [],
        }

    def render_output(self, x: VariableElement):
        try:
            data = apply_functions(
                self.data, x.function_names, self.function_by_name)
        except KeyError as e:
            L.error('%s function not supported for string', e)
            data = self.data
        body_text = (
            f'<span id="{x.id}" '
            f'class="{self.view_name} {self.variable_id}">'
            f'{data}</span>')
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': body_text,
            'js_texts': [],
        }


class NumberView(StringView):

    view_name = 'number'
    input_type = 'number'

    def parse(self, data):
        try:
            data = float(data)
        except ValueError:
            raise CrossComputeDataError(f'{data} is not a number')
        if data.is_integer():
            data = int(data)
        return data


class PasswordView(StringView):

    view_name = 'password'
    input_type = 'password'


class EmailView(StringView):

    view_name = 'email'
    input_type = 'email'


class TextView(StringView):

    view_name = 'text'

    def render_input(self, x: VariableElement):
        variable_id = self.variable_id
        value = self.data or ''
        body_text = (
            f'<textarea id="{x.id}" name="{variable_id}" '
            f'class="{self.view_name} {variable_id}">'
            f'{value}</textarea>')
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': body_text,
            'js_texts': [],
        }


class MarkdownView(TextView):

    view_name = 'markdown'

    def render_output(self, x: VariableElement):
        data = get_html_from_markdown(self.data)
        body_text = (
            f'<span id="{x.id}" '
            f'class="{self.view_name} {self.variable_id}">'
            f'{data}</span>')
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': body_text,
            'js_texts': [],
        }


class ImageView(VariableView):

    view_name = 'image'

    def render_output(self, x: VariableElement):
        variable_id = self.variable_id
        body_text = (
            f'<img id="{x.id}" '
            f'class="{self.view_name} {variable_id}" '
            f'src="{x.uri}">')
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': body_text,
            'js_texts': [],
        }


class TableView(VariableView):

    view_name = 'table'

    def render_output(self, x: VariableElement):
        variable_id = self.variable_id
        body_text = (
            f'<table id="{x.id}" '
            f'class="{self.view_name} {variable_id}">'
            '<thead/><tbody/></table>')
        js_texts = [
            TABLE_JS_TEMPLATE.substitute({
                'element_id': x.id,
                'data_uri': x.uri,
            }),
        ]
        return {
            'css_uris': [],
            'js_uris': [],
            'body_text': body_text,
            'js_texts': js_texts,
        }


def save_variables(absolute_batch_folder, variables_by_mode_name):
    variables_path = join(absolute_batch_folder, 'variables.json')
    with open(variables_path, 'wt') as f:
        json.dump(variables_by_mode_name, f)
    FILE_CACHE[variables_path] = variables_by_mode_name
    return variables_path


def save_variable_data(target_path, data_by_id, variable_definitions):
    file_extension = splitext(target_path)[1]
    variable_data_by_id = get_variable_data_by_id(
        variable_definitions, data_by_id)
    if file_extension == '.dictionary':
        with open(target_path, 'wt') as input_file:
            json.dump(variable_data_by_id, input_file)
    elif len(variable_data_by_id) > 1:
        raise CrossComputeConfigurationError(
            f'{file_extension} does not support multiple variables')
    else:
        variable_data = list(variable_data_by_id.values())[0]
        # TODO: Download variable_data['uri']
        # TODO: Copy variable_data['path']
        open(target_path, 'wt').write(variable_data)


def update_variable_data(target_path, data_by_id):
    try:
        if exists(target_path):
            f = open(target_path, 'r+t')
            d = json.load(f)
            d.update(data_by_id)
            f.seek(0)
            f.truncate()
        else:
            f = open(target_path, 'wt')
            d = data_by_id
        json.dump(d, f)
        FILE_CACHE[target_path] = d
    except (json.JSONDecodeError, OSError) as e:
        raise CrossComputeDataError(e)
    finally:
        f.close()


def load_variable_data_from_folder(
        absolute_batch_folder, mode_name, variable_path, variable_id):
    variables_path = join(absolute_batch_folder, 'variables.json')
    try:
        variable_data = FILE_CACHE[variables_path]
    except OSError:
        folder = join(absolute_batch_folder, mode_name)
        path = join(folder, variable_path)
        if not is_path_in_folder(path, folder):
            raise CrossComputeDataError(
                f'{path} for variable {variable_id} must be inside {folder}')
        return load_variable_data(join(
            absolute_batch_folder, mode_name, variable_path), variable_id)
    try:
        variable_data = variable_data[variable_id]
    except KeyError:
        raise CrossComputeDataError(
            f'variable {variable_id} not found in {variables_path}')
    return variable_data


def load_variable_data(path, variable_id):
    try:
        variable_data = FILE_CACHE[path]
    except OSError:
        raise CrossComputeDataError(
            f'{format_path(path)} path not found for variable {variable_id}')
    if path.endswith('.dictionary'):
        try:
            variable_data = variable_data[variable_id]
        except KeyError:
            raise CrossComputeDataError(
                f'variable {variable_id} not found in {format_path(path)}')
    # TODO: {uri}
    return variable_data


def load_file_data(path):
    if path.endswith('.dictionary'):
        return json.load(open(path, 'rt'))
    if not exists(path):
        raise FileNotFoundError
    return {'path': path}


def get_variable_data_by_id(variable_definitions, data_by_id):
    variable_data_by_id = {}
    for variable_definition in variable_definitions:
        variable_id = variable_definition['id']
        if None in data_by_id:
            variable_data = data_by_id[None]
        else:
            try:
                variable_data = data_by_id[variable_id]
            except KeyError:
                raise CrossComputeConfigurationError(
                    f'{variable_id} not defined in batch configuration')
        variable_data_by_id[variable_id] = variable_data
    return variable_data_by_id


def format_text(text, data_by_id):
    if not data_by_id:
        return text
    if None in data_by_id:
        f = data_by_id[None]
    else:
        def f(match):
            matching_text = match.group(0)
            expression_text = match.group(1)
            expression_terms = expression_text.split('|')
            variable_id = expression_terms[0].strip()
            try:
                text = data_by_id[variable_id]
            except KeyError:
                L.warning('%s missing in batch configuration', variable_id)
                return matching_text
            try:
                text = apply_functions(
                    text, expression_terms[1:], FUNCTION_BY_NAME)
            except KeyError as e:
                L.error('%s function not supported for string', e)
            return str(text)
    return VARIABLE_ID_PATTERN.sub(f, text)


def redact(data_by_id, variable_definitions):
    d = {}
    for variable_definition in variable_definitions:
        variable_id = variable_definition['id']
        variable_path = variable_definition['path']
        if variable_path == 'ENVIRONMENT':
            continue
        d[variable_id] = data_by_id[variable_id]
    return d


def apply_functions(value, function_names, function_by_name):
    for function_name in function_names:
        function_name = function_name.strip()
        if not function_name:
            continue
        try:
            f = function_by_name[function_name]
        except KeyError:
            raise
        value = f(value)
    return value


VIEW_BY_NAME = {_.name: import_attribute(
    _.value) for _ in entry_points().select(group='crosscompute.views')}
L = getLogger(__name__)


TABLE_JS_TEMPLATE = Template('''\
(async function () {
  const response = await fetch('$data_uri');
  const d = await response.json();
  const columns = d['columns'], columnCount = columns.length;
  const rows = d['data'], rowCount = rows.length;
  const nodes = document.getElementById('$element_id').children;
  const thead = nodes[0], tbody = nodes[1];
  let tr = document.createElement('tr');
  for (let i = 0; i < columnCount; i++) {
    const column = columns[i];
    const th = document.createElement('th');
    th.innerText = column;
    tr.append(th);
  }
  thead.append(tr);
  for (let i = 0; i < rowCount; i++) {
    const row = rows[i];
    tr = document.createElement('tr');
    for (let j = 0; j < columnCount; j++) {
      const td = document.createElement('td');
      td.innerText = row[j];
      tr.append(td);
    }
    tbody.append(tr);
  }
})();''')


FILE_CACHE = FileCache(
    load_file_data=load_file_data,
    maximum_length=MAXIMUM_FILE_CACHE_LENGTH)
