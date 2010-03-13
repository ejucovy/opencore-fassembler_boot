#!/usr/bin/env python

from optparse import OptionParser
import os
import pwd
import re
import string
import subprocess
import sys
import shutil

import tempita
from pkg_resources import resource_filename

script_dir = os.path.dirname(__file__)

parser = OptionParser(
    usage="%prog [OPTIONS] SITE_FQDN BASE_PORT",
    description='Creates a new OpenCore site layout for Fassembler builds',
    )

parser.add_option(
    '', '--force',
    dest='force',
    action='store_true',
    help='Ignore existing directories?',
    )

parser.add_option(
    '-b', '--basedir',
    dest='base_dir',
    action='store',
    default=None,
    help='Base directory to put site layout in. Defaults to current directory if none provided.',
    )

parser.add_option(
    '', '--etc_svn_repo',
    dest='etc_svn_repo',
    action='store',
    default=None,
    help='URL of SVN repo to store etc files (e.g. file:///srv/svn/opencore_etc/)',
    )

_var_re = re.compile(r'^(?:\[(\w+)\])?\s*(\w+)=(.*)$')
_dot_var_re = re.compile(r'^(\w+)\.(\w+)=([^=>].*)$')
def parse_positional(args):
    """
    Parses out the positional arguments into fassembler projects and
    variable assignments.
    """
    nonvar_args = []
    variables = []
    for arg in args:
        match = _var_re.search(arg)
        if match:
            variables.append(('general', match.group(2), match.group(3)))
        else:
            match = _dot_var_re.search(arg)
            if match:
                variables.append((match.group(1), match.group(2), match.group(3)))
            else:
                nonvar_args.append(arg)
    return nonvar_args, variables

def assert_svn_repo_exists(url):
    command = subprocess.Popen(['svn', 'ls', url],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = command.communicate()
    errcode = command.wait()
    if errcode:
        sys.stderr.write(stdout)
        return False
    return True

def main():
    """
    Implements the command-line new site script.
    """
    # validation and initialization
    options, args = parser.parse_args()
    args, variables = parse_positional(args)
    if len(args) < 2:
        parser.error("You must provide both SITE_FQDN and BASE_PORT")

    site_fqdn = args[0]
    base_port = args[1]

    # make sure we have an etc_svn_repo URL before we get any further
    etc_svn_repo = options.etc_svn_repo
    while not etc_svn_repo:
        # this one is so important we prompt the user interactively
        prompt = '\n'.join(("Please enter a URL for your configuration svn repository",
                            "(i.e. the 'etc_svn_repo'). Because this will contain",
                            "possibly sensitive configuration information, it is",
                            "recommended that this repository NOT be readable by",
                            "untrusted users.:\n"))
        etc_svn_repo = raw_input(prompt).strip()

    if not assert_svn_repo_exists(etc_svn_repo):
        sys.stderr.write("Warning: couldn't verify subversion at %r!\n"
                         % etc_svn_repo)

    # calculate install directory name (either fqdn or port number)
    base_dir = options.base_dir or os.getcwd()
    install_dir = os.path.join(base_dir, site_fqdn)

    # create directory structure
    subs = {'dir': install_dir}
    print 'Making directories "%(dir)s" "%(dir)s/builds" "%(dir)s/var"' \
          % subs
    builds = "%(dir)s/builds" % subs
    vars = "%(dir)s/var" % subs
    for newdir in (builds, vars):
        if os.path.isdir(newdir):
            if not options.force:
                sys.stderr.write("Directory %s already exists, bailing out\n"
                                 % newdir)
                sys.exit(1)
        else: 
            os.makedirs(newdir)


    conf_template = resource_filename('fassembler_boot', 'opencore.conf')
    conf_template = tempita.Template.from_filename(conf_template)
    conf = conf_template.substitute(locals())

    # create configuration
    outfile = open(os.path.join(install_dir, 'opencore.conf'), 'w')
    outfile.write(conf)
    outfile.close()

    # for now, just copy over extras.txt 
    shutil.copy(resource_filename('fassembler_boot', 
                                  'extra-fassembler-projects.txt'),
                install_dir)
    
    print "\nSuccess; site layout set up in %(dir)s\n" \
        "Run `rebuild-opencore -b %(dir)s` to continue" % subs

def config():
    conf_template = resource_filename('fassembler_boot', 'opencore.conf')
    fp = open(conf_template)
    print fp.read()
    fp.close()

if __name__ == '__main__':
    main()
