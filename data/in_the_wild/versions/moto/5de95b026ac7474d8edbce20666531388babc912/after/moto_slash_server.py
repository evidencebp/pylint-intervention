from __future__ import unicode_literals

import argparse
import json
import re
import sys
from threading import Lock

import six
from flask import Flask
from flask.testing import FlaskClient

from six.moves.urllib.parse import urlencode
from werkzeug.routing import BaseConverter
from werkzeug.serving import run_simple

from moto.backends import BACKENDS
from moto.core.utils import convert_flask_to_httpretty_response


HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"]


DEFAULT_SERVICE_REGION = ('s3', 'us-east-1')

# Map of unsigned calls to service-region as per AWS API docs
# https://docs.aws.amazon.com/cognito/latest/developerguide/resource-permissions.html#amazon-cognito-signed-versus-unsigned-apis
UNSIGNED_REQUESTS = {
    'AWSCognitoIdentityService': ('cognito-identity', 'us-east-1'),
    'AWSCognitoIdentityProviderService': ('cognito-idp', 'us-east-1'),
}


class DomainDispatcherApplication(object):
    """
    Dispatch requests to different applications based on the "Host:" header
    value. We'll match the host header value with the url_bases of each backend.
    """

    def __init__(self, create_app, service=None):
        self.create_app = create_app
        self.lock = Lock()
        self.app_instances = {}
        self.service = service

    def get_backend_for_host(self, host):
        if host == 'moto_api':
            return host

        if self.service:
            return self.service

        if host in BACKENDS:
            return host

        for backend_name, backend in BACKENDS.items():
            for url_base in list(backend.values())[0].url_bases:
                if re.match(url_base, 'http://%s' % host):
                    return backend_name

    def infer_service_region_host(self, environ):
        auth = environ.get('HTTP_AUTHORIZATION')
        if auth:
            # Signed request
            # Parse auth header to find service assuming a SigV4 request
            # https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
            # ['Credential=sdffdsa', '20170220', 'us-east-1', 'sns', 'aws4_request']
            try:
                credential_scope = auth.split(",")[0].split()[1]
                _, _, region, service, _ = credential_scope.split("/")
            except ValueError:
                # Signature format does not match, this is exceptional and we can't
                # infer a service-region. A reduced set of services still use
                # the deprecated SigV2, ergo prefer S3 as most likely default.
                # https://docs.aws.amazon.com/general/latest/gr/signature-version-2.html
                service, region = DEFAULT_SERVICE_REGION
        else:
            # Unsigned request
            target = environ.get('HTTP_X_AMZ_TARGET')
            if target:
                service, _ = target.split('.', 1)
                service, region = UNSIGNED_REQUESTS.get(service, DEFAULT_SERVICE_REGION)
            # S3 is the last resort when the target is also unknown
            service, region = DEFAULT_SERVICE_REGION

        if service == 'dynamodb':
            if environ['HTTP_X_AMZ_TARGET'].startswith('DynamoDBStreams'):
                host = 'dynamodbstreams'
            else:
                dynamo_api_version = environ['HTTP_X_AMZ_TARGET'].split("_")[1].split(".")[0]
                # If Newer API version, use dynamodb2
                if dynamo_api_version > "20111205":
                    host = "dynamodb2"
        else:
            host = "{service}.{region}.amazonaws.com".format(
                service=service, region=region)

        return host

    def get_application(self, environ):
        path_info = environ.get('PATH_INFO', '')

        # The URL path might contain non-ASCII text, for instance unicode S3 bucket names
        if six.PY2 and isinstance(path_info, str):
            path_info = six.u(path_info)
        if six.PY3 and isinstance(path_info, six.binary_type):
            path_info = path_info.decode('utf-8')

        if path_info.startswith("/moto-api") or path_info == "/favicon.ico":
            host = "moto_api"
        elif path_info.startswith("/latest/meta-data/"):
            host = "instance_metadata"
        else:
            host = environ['HTTP_HOST'].split(':')[0]

        with self.lock:
            backend = self.get_backend_for_host(host)
            if not backend:
                # No regular backend found; try parsing other headers
                host = self.infer_service_region_host(environ)
                backend = self.get_backend_for_host(host)

            app = self.app_instances.get(backend, None)
            if app is None:
                app = self.create_app(backend)
                self.app_instances[backend] = app
            return app

    def __call__(self, environ, start_response):
        backend_app = self.get_application(environ)
        return backend_app(environ, start_response)


class RegexConverter(BaseConverter):
    # http://werkzeug.pocoo.org/docs/routing/#custom-converters

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class AWSTestHelper(FlaskClient):

    def action_data(self, action_name, **kwargs):
        """
        Method calls resource with action_name and returns data of response.
        """
        opts = {"Action": action_name}
        opts.update(kwargs)
        res = self.get("/?{0}".format(urlencode(opts)),
                       headers={"Host": "{0}.us-east-1.amazonaws.com".format(self.application.service)})
        return res.data.decode("utf-8")

    def action_json(self, action_name, **kwargs):
        """
        Method calls resource with action_name and returns object obtained via
        deserialization of output.
        """
        return json.loads(self.action_data(action_name, **kwargs))


def create_backend_app(service):
    from werkzeug.routing import Map

    # Create the backend_app
    backend_app = Flask(__name__)
    backend_app.debug = True
    backend_app.service = service

    # Reset view functions to reset the app
    backend_app.view_functions = {}
    backend_app.url_map = Map()
    backend_app.url_map.converters['regex'] = RegexConverter
    backend = list(BACKENDS[service].values())[0]
    for url_path, handler in backend.flask_paths.items():
        if handler.__name__ == 'dispatch':
            endpoint = '{0}.dispatch'.format(handler.__self__.__name__)
        else:
            endpoint = None

        original_endpoint = endpoint
        index = 2
        while endpoint in backend_app.view_functions:
            # HACK: Sometimes we map the same view to multiple url_paths. Flask
            # requries us to have different names.
            endpoint = original_endpoint + str(index)
            index += 1

        backend_app.add_url_rule(
            url_path,
            endpoint=endpoint,
            methods=HTTP_METHODS,
            view_func=convert_flask_to_httpretty_response(handler),
            strict_slashes=False,
        )

    backend_app.test_client_class = AWSTestHelper
    return backend_app


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    # Keep this for backwards compat
    parser.add_argument(
        "service",
        type=str,
        nargs='?',  # http://stackoverflow.com/a/4480202/731592
        default=None)
    parser.add_argument(
        '-H', '--host', type=str,
        help='Which host to bind',
        default='127.0.0.1')
    parser.add_argument(
        '-p', '--port', type=int,
        help='Port number to use for connection',
        default=5000)
    parser.add_argument(
        '-r', '--reload',
        action='store_true',
        help='Reload server on a file change',
        default=False
    )
    parser.add_argument(
        '-s', '--ssl',
        action='store_true',
        help='Enable SSL encrypted connection with auto-generated certificate (use https://... URL)',
        default=False
    )
    parser.add_argument(
        '-c', '--ssl-cert', type=str,
        help='Path to SSL certificate',
        default=None)
    parser.add_argument(
        '-k', '--ssl-key', type=str,
        help='Path to SSL private key',
        default=None)

    args = parser.parse_args(argv)

    # Wrap the main application
    main_app = DomainDispatcherApplication(
        create_backend_app, service=args.service)
    main_app.debug = True

    ssl_context = None
    if args.ssl_key and args.ssl_cert:
        ssl_context = (args.ssl_cert, args.ssl_key)
    elif args.ssl:
        ssl_context = 'adhoc'

    run_simple(args.host, args.port, main_app,
               threaded=True, use_reloader=args.reload,
               ssl_context=ssl_context)


if __name__ == '__main__':
    main()
