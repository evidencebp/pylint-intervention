# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
import os

from oslo_config import cfg
from oslo_config import types

from kolla.common.sources import SOURCES
from kolla.common.users import USERS
from kolla.version import version_info as version


BASE_OS_DISTRO = ['centos', 'debian', 'ubuntu']
BASE_ARCH = ['x86_64', 'aarch64']
DEFAULT_BASE_TAGS = {
    'centos': {'name': 'quay.io/centos/centos', 'tag': 'stream8'},
    'debian': {'name': 'debian', 'tag': 'bullseye'},
    'ubuntu': {'name': 'ubuntu', 'tag': '20.04'},
}
# NOTE(hrw): has to match PRETTY_NAME in /etc/os-release
DISTRO_PRETTY_NAME = {
    'centos': 'CentOS Stream 8',
    'debian': 'Debian GNU/Linux 11 (bullseye)',
    'ubuntu': 'Ubuntu 20.04',
}
OPENSTACK_RELEASE = 'master'

# This is noarch repository so we will use it on all architectures
DELOREAN = "https://trunk.rdoproject.org/centos8-yoga/" \
    "consistent/delorean.repo"
DELOREAN_DEPS = "https://trunk.rdoproject.org/centos8-yoga/" \
    "delorean-deps.repo"

INSTALL_TYPE_CHOICES = ['source']

# TODO(mandre) check for file integrity instead of downloading from an HTTPS
# source
TARBALLS_BASE = "https://tarballs.opendev.org"

_PROFILE_OPTS = [
    cfg.ListOpt('infra',
                default=[
                    'cron',
                    'elasticsearch',
                    'etcd',
                    'fluentd',
                    'haproxy',
                    'hacluster',
                    'keepalived',
                    'kibana',
                    'kolla-toolbox',
                    'letsencrypt',
                    'logstash',
                    'mariadb',
                    'memcached',
                    'openvswitch',
                    'proxysql',
                    'rabbitmq',
                    'redis',
                    'skydive',
                    'storm',
                    'tgtd',
                ],
                help='Infra images'),
    cfg.ListOpt('main',
                default=[
                    'ceilometer',
                    'cinder',
                    'glance',
                    'heat',
                    'horizon',
                    'iscsi',
                    'keystone',
                    'neutron',
                    'nova-',
                    'placement',
                    'swift',
                ],
                help='Main images'),
    cfg.ListOpt('aux',
                default=[
                    'aodh',
                    'blazar',
                    'cloudkitty',
                    'designate',
                    'freezer',
                    'gnocchi',
                    'influxdb',
                    'ironic',
                    'kafka',
                    'kuryr',
                    'magnum',
                    'manila',
                    'masakari',
                    'mistral',
                    'monasca',
                    'murano',
                    'octavia',
                    'redis',
                    'sahara',
                    'senlin',
                    'solum',
                    'tacker',
                    'telegraf',
                    'trove',
                    'vitrage',
                    'zookeeper',
                    'zun',
                ],
                help='Aux Images'),
    cfg.ListOpt('default',
                default=[
                    'cron',
                    'kolla-toolbox',
                    'fluentd',
                    'glance',
                    'haproxy',
                    'heat',
                    'horizon',
                    'keepalived',
                    'keystone',
                    'mariadb',
                    'memcached',
                    'neutron',
                    'nova-',
                    'placement',
                    'proxysql',
                    'openvswitch',
                    'rabbitmq',
                ],
                help='Default images'),
]

hostarch = os.uname()[4]

_CLI_OPTS = [
    cfg.StrOpt('base', short='b', default='centos',
               choices=BASE_OS_DISTRO,
               help='The distro type of the base image.'),
    cfg.StrOpt('base-tag', default='latest',
               help='The base distro image tag'),
    cfg.StrOpt('base-image',
               help='The base image name. Default is the same with base.'),
    cfg.StrOpt('base-arch', default=hostarch,
               choices=BASE_ARCH,
               help='The base architecture. Default is same as host.'),
    cfg.BoolOpt('use-dumb-init', default=True,
                help='Use dumb-init as init system in containers'),
    cfg.BoolOpt('debug', short='d', default=False,
                help='Turn on debugging log level'),
    cfg.BoolOpt('skip-parents', default=False,
                help='Do not rebuild parents of matched images'),
    cfg.BoolOpt('skip-existing', default=False,
                help='Do not rebuild images present in the docker cache'),
    cfg.DictOpt('build-args',
                help='Set docker build time variables'),
    cfg.BoolOpt('keep', default=False,
                help='Keep failed intermediate containers'),
    cfg.BoolOpt('list-dependencies', short='l',
                help='Show image dependencies (filtering supported)'),
    cfg.BoolOpt('list-images',
                help='Show all available images (filtering supported)'),
    cfg.StrOpt('namespace', short='n', default='kolla',
               help='The Docker namespace name'),
    cfg.StrOpt('network_mode', default='host',
               help='The network mode for Docker build. Example: host'),
    cfg.BoolOpt('cache', default=True,
                help='Use the Docker cache when building'),
    cfg.MultiOpt('profile', types.String(), short='p',
                 help=('Build a pre-defined set of images, see [profiles]'
                       ' section in config. The default profiles are:'
                       ' {}'.format(', '.join(
                           [opt.name for opt in _PROFILE_OPTS])
                       ))),
    cfg.BoolOpt('push', default=False,
                help='Push images after building'),
    cfg.IntOpt('push-threads', default=1, min=1,
               help=('The number of threads to use while pushing images.'
                     ' Note: Docker cannot handle threaded pushing properly')),
    cfg.IntOpt('retries', short='r', default=3, min=0,
               help='The number of times to retry while building'),
    cfg.MultiOpt('regex', types.String(), positional=True, required=False,
                 help=('Build only images matching regex and its'
                       ' dependencies')),
    cfg.StrOpt('registry',
               help=('The docker registry host. The default registry host'
                     ' is Docker Hub')),
    cfg.StrOpt('save-dependency',
               help=('Path to the file to store the docker image'
                     ' dependency in Graphviz dot format')),
    cfg.StrOpt('format', short='f', default='json',
               choices=['json', 'none'],
               help='Format to write the final results in'),
    cfg.StrOpt('tarballs-base', default=TARBALLS_BASE,
               help='Base url to OpenStack tarballs'),
    # NOTE(hrw): deprecate argument in Zed, remove in A-cycle
    cfg.StrOpt('type', short='t', default='source',
               choices=INSTALL_TYPE_CHOICES,
               dest='install_type',
               help=('Ignored, kept for script compatibility.')),
    cfg.IntOpt('threads', short='T', default=8, min=1,
               help=('The number of threads to use while building.'
                     ' (Note: setting to one will allow real time'
                     ' logging)')),
    cfg.StrOpt('tag', default=version.cached_version_string(),
               help='The Docker tag'),
    cfg.BoolOpt('template-only', default=False,
                help="Don't build images. Generate Dockerfile only"),
    cfg.IntOpt('timeout', default=120,
               help='Time in seconds after which any operation times out'),
    cfg.MultiOpt('template-override', types.String(),
                 help='Path to template override file'),
    cfg.MultiOpt('docker-dir', types.String(),
                 help=('Path to additional docker file template directory,'
                       ' can be specified multiple times'),
                 short='D', default=[]),
    cfg.StrOpt('logs-dir', help='Path to logs directory'),
    cfg.BoolOpt('pull', default=True,
                help='Attempt to pull a newer version of the base image'),
    cfg.StrOpt('work-dir', help=('Path to be used as working directory.'
                                 ' By default, a temporary dir is created')),
    cfg.BoolOpt('squash', default=False,
                help=('Squash the image layers. WARNING: it will consume lots'
                      ' of disk IO. "docker-squash" tool is required, install'
                      ' it by "pip install docker-squash"')),
    cfg.StrOpt('openstack-release', default=OPENSTACK_RELEASE,
               help='OpenStack release for building kolla source images and '
                    'kolla-toolbox image'),
    cfg.StrOpt('openstack-branch',
               help='Branch for source images (internal; with a dash; '
                    'please set openstack-release instead)'),
    cfg.StrOpt('openstack-branch-slashed',
               help='Branch for source images (internal; with a slash; '
                    'please set openstack-release instead)'),
    cfg.BoolOpt('docker-healthchecks', default=True,
                help='Add Kolla docker healthcheck scripts in the image'),
    cfg.BoolOpt('quiet', short='q', default=False,
                help='Do not print image logs'),
    cfg.BoolOpt('enable-unbuildable', default=False,
                help='Enable images marked as unbuildable'),
    cfg.BoolOpt('summary', default=True,
                help='Show summary at the end of build'),
    cfg.StrOpt('image-name-prefix', default='',
               help='Prefix prepended to image names'),
    cfg.StrOpt('repos-yaml', default='',
               help='Path to alternative repos.yaml file'),
]

_BASE_OPTS = [
    cfg.StrOpt('maintainer',
               default='Kolla Project (https://launchpad.net/kolla)',
               help='Content of the maintainer label'),
    cfg.StrOpt('distro_package_manager', default=None,
               help=('Use this parameter to override the default package '
                     'manager used by kolla. For example, if you want to use '
                     'yum on a system with dnf, set this to yum which will '
                     'use yum command in the build process')),
    cfg.StrOpt('base_package_type', default=None,
               help=('Set the package type of the distro. If not set then '
                     'the packaging type is set to "rpm" if a RHEL based '
                     'distro and "deb" if a Debian based distro.')),
    cfg.ListOpt('rpm_setup_config', default=[DELOREAN, DELOREAN_DEPS],
                help=('Comma separated list of .rpm or .repo file(s) '
                      'or URL(s) to install before building containers')),
    cfg.StrOpt('apt_sources_list', help=('Path to custom sources.list')),
    cfg.StrOpt('apt_preferences', help=('Path to custom apt/preferences')),
    cfg.BoolOpt('squash-cleanup', default=True,
                help='Remove source image from Docker after squashing'),
    cfg.StrOpt('squash-tmp-dir',
               help='Temporary directory to be used during squashing'),
    cfg.BoolOpt('clean_package_cache', default=True,
                help='Clean all package cache.'),
    cfg.ListOpt('allowed-to-fail', default=[],
                help='Images which are allowed to fail'),
]


def get_source_opts(type_=None, location=None, reference=None, enabled=True):
    return [cfg.StrOpt('type', choices=['local', 'git', 'url'],
                       default=type_,
                       help='Source location type'),
            cfg.StrOpt('location', default=location,
                       help='The location for source install'),
            cfg.StrOpt('reference', default=reference,
                       help=('Git reference to pull, commit sha, tag '
                             'or branch name')),
            cfg.BoolOpt('enabled', default=enabled,
                        help=('Whether the source is enabled'))]


def get_user_opts(uid, gid, group):
    return [
        cfg.IntOpt('uid', default=uid, help='The user id'),
        cfg.IntOpt('gid', default=gid, help='The group id'),
        cfg.StrOpt('group', default=group, help='The group name'),
    ]


def gen_all_user_opts():
    for name, params in USERS.items():
        uid = params['uid']
        gid = params['gid']
        try:
            group = params['group']
        except KeyError:
            group = name[:-5]
        yield name, get_user_opts(uid, gid, group)


def gen_all_source_opts():
    for name, params in SOURCES.items():
        type_ = params['type']
        location = params['location']
        reference = params.get('reference')
        enabled = params.get('enabled', True)
        yield name, get_source_opts(type_, location, reference, enabled)


def list_opts():
    return itertools.chain([(None, _CLI_OPTS),
                            (None, _BASE_OPTS),
                            ('profiles', _PROFILE_OPTS)],
                           gen_all_source_opts(),
                           gen_all_user_opts(),
                           )


def parse(conf, args, usage=None, prog=None,
          default_config_files=None):
    conf.register_cli_opts(_CLI_OPTS)
    conf.register_opts(_BASE_OPTS)
    conf.register_opts(_PROFILE_OPTS, group='profiles')
    for name, opts in gen_all_source_opts():
        conf.register_opts(opts, name)
    for name, opts in gen_all_user_opts():
        conf.register_opts(opts, name)

    conf(args=args,
         project='kolla',
         usage=usage,
         prog=prog,
         version=version.cached_version_string(),
         default_config_files=default_config_files)

    # NOTE(jeffrey4l): set the default base tag based on the
    # base option
    conf.set_default('base_tag', DEFAULT_BASE_TAGS[conf.base]['tag'])
    prefix = '' if conf.openstack_release == 'master' else 'stable-'
    openstack_branch = '{}{}'.format(prefix, conf.openstack_release)
    openstack_branch_slashed = openstack_branch.replace('-', '/')
    conf.set_default('openstack_branch', openstack_branch)
    conf.set_default('openstack_branch_slashed', openstack_branch_slashed)

    if not conf.base_image:
        conf.base_image = DEFAULT_BASE_TAGS[conf.base]['name']
