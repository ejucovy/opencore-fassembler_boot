import subprocess
from pkg_resources import resource_filename
from fassembler_boot.config import config as get_config

def start_build(base_dir, config_path=None, profile_url=None):
    script = resource_filename('fassembler_boot', 'newbuild.sh')

    if config_path is None:
        config_path = os.path.join(base_dir, 'opencore.conf')
    assert os.path.exists(config_path), \
        "No configuration file found at %s" % config_path

    config = get_config(config_path)

    profile_url = profile_url or config.get('default_build_profile')
    if not profile_url:
        raise ValueError("""
You must provide a requirements profile to build, either as
an argument to new-opencore-build, or with a `default_build_profile`
setting in your configuration file (%s)""" % config_path)

    etc_svn_repo = config['etc_svn_repo']
    site_fqdn = config['site_fqdn']
    base_port = config['base_port']

    fassembler_extras = config.get('fassembler_projects')
    if fassembler_extras and not os.path.isabs(fassembler_extras):
        fassembler_extras = os.path.join(base_dir, fassembler_extras)

    print "using profile url: %s" % profile_url

    os.chmod(script, 0755)
    subprocess.call([script,
                     profile_url, base_dir, etc_svn_repo, 
                     site_fqdn, base_port,
                     fassembler_extras])

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
