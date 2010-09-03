import subprocess
from pkg_resources import resource_filename
from fassembler_boot.config import config as get_config

def start_build(base_dir, config_path=None, profile_url=None):
    script = resource_filename('fassembler_boot', 'newbuild.sh')

    if config_path is None:
        config_path = os.path.join(base_dir, 'opencore.conf')
    assert os.path.exists(config_path), \
        "No configuration file found at %s" % config_path
    if not os.path.exists(os.path.join(base_dir, 'builds')):
        os.mkdir(os.path.join(base_dir, 'builds'))
    assert os.path.isdir(os.path.join(base_dir, 'builds'))

    config = get_config(config_path)

    profile_url = profile_url or config.get('default_build_profile')
    if not profile_url:
        raise ValueError("""
You must provide a requirements profile to build, either as
an argument to new-opencore-build, or with a `default_build_profile`
setting in your configuration file (%s)""" % config_path)

    etc_svn_repo = config['etc_svn_repo']

    if '://' not in etc_svn_repo:
        etc_svn_repo = 'file://' + etc_svn_repo

    site_fqdn = config['site_fqdn']
    base_port = config['base_port']

    extra_zopes = config.get("num_extra_zopes", "0")
    try:
        int(extra_zopes)
    except ValueError:
        raise ValueError(
            "If supplied, num_extra_zopes must be an integer")

    cmd = [script,
           profile_url, base_dir, etc_svn_repo, 
           site_fqdn, base_port, extra_zopes]
    print "using profile url: %s" % profile_url
    print cmd
    
    os.chmod(script, 0755)
    subprocess.call(cmd)

import sys

from optparse import OptionParser

parser = OptionParser(
    usage="%prog [profile_url] [-b base_dir] [-c config_path]",
    description="Runs a new build",
    )

parser.add_option(
    '-c', '--config',
    dest='config_path',
    action="store",
    default=None,
    help='Config file to load')

parser.add_option(
    '-b', '--basedir',
    dest='base_dir',
    action="store",
    default=None,
    help="Base directory of the site")

import os

if __name__ == '__main__':
    main()

def main():
    options, args = parser.parse_args()

    base_dir = options.base_dir or os.getcwd()
    config_path = options.config_path
    
    profile_url = None
    if len(args) > 0:
        profile_url = args[0]

    start_build(base_dir, config_path, profile_url)
