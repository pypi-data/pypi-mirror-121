from __future__ import print_function
from __future__ import unicode_literals

import errno
import glob
import logging
import os
import re
import stat
import subprocess

import six.moves.urllib as urllib

from zc.buildout import UserError
from zc.buildout.easy_install import allow_picked_versions
from slapos.recipe import rmtree
from slapos.recipe.downloadunpacked import Recipe as Download

strip = lambda x:x.strip()  # noqa

is_true = ('false', 'true').index

RUBYGEMS_URL_BASE = 'https://rubygems.org/rubygems/rubygems'
VERSION_ZIP_RE = '-([0-9.]+).zip'


class Recipe(object):
    """zc.buildout recipe for compiling and installing software"""

    def __init__(self, buildout, name, options):
        self.options = options
        self.buildout = buildout
        self.name = name
        self.log = logging.getLogger(name)

        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name,
        )

        self.gems = options.get('gems')
        if self.gems:
            self.gems = self.gems.split()
        else:
            raise UserError("Configuration error, 'gems' option is missing")

        self.url = options.get('url')
        if(self.url and options.get('version')):
            raise UserError("Configuration error, "
                            "'url' and 'version' options are mutually exclusive")

        # Allow to define specific ruby executable. If not, take just 'ruby'
        self.ruby_executable = options.get('ruby-executable', 'ruby')

        deployment = options.get('deployment')
        self.deployment = is_true(deployment) if deployment else not allow_picked_versions()
        self.gem_regex = re.compile(r'\s+([\w\-_.]+) \((<|~>|>=|!=) '
                                    r'((\d+\.)*\d+)(, (<|~>|>=|!=) ((\d+\.)*\d+))?\)')

    def run(self, cmd, environ=None):
        """Run the given ``cmd`` in a child process."""
        env = os.environ.copy()
        if environ:
            env.update(environ)

        try:
            return subprocess.check_output(cmd, env=env, universal_newlines=True)
        except OSError as e:
            raise UserError('System error, command failed: %s: %s' % (e, cmd))
        except subprocess.CalledProcessError as e:
            self.log.error(e.output)
            if e.returncode < 0:
                raise UserError('System error, command received signal %s: %s'
                                 % (-e.returncode, e.cmd))
            elif e.returncode > 0:
                raise UserError(
                    'System error, command failed with exit code %s: %s' 
                    % (e.returncode, e.cmd)
                )

    def update(self):
        pass

    def _check_dependency_constraint(self, cons_dict, dep_dict, gemname):
        if not cons_dict['symbol']:
            return

        dep_version_list = list(map(int, dep_dict['version'].split('.')))
        cons_version_list = list(map(int, cons_dict['version'].split('.')))

        if cons_dict['symbol'] == '~>':
            self._check_dependency_constraint(
                { 'symbol': '>=', 'version': cons_dict['version'],},
                dep_dict, gemname
            )

            if len(cons_version_list) > 1:
                cons_version_list = cons_version_list[:-1]
            cons_version_list[-1] += 1
            self._check_dependency_constraint(
                {
                    'symbol': '<',
                    'version': '.'.join(map(str, cons_version_list)),
                },
                dep_dict, gemname
            )
            return        
        elif cons_dict['symbol'] == '<':
            if dep_version_list < cons_version_list:
                return
        elif cons_dict['symbol'] == '>=':
            if dep_version_list >= cons_version_list:
                return
        elif cons_dict['symbol'] == '!=':
            if dep_version_list != cons_version_list:
                return
        else:
            raise ValueError(
                'Unhandled symbol in constraint %s for dependecy %s of gem %s'
                % (' '.join(cons_dict.values()), dep_dict['gemname'],  gemname)
            )

        raise UserError(
            'Configuration error, version %s for gem %s '
            'does not satisfy dependency constraint %s of gem %s' 
            % (dep_dict['version'], dep_dict['gemname'],
               ' '.join(cons_dict.values()), gemname)
        )

    def _join_paths(self, *paths):
        return ':'.join(filter(None, paths))

    def _get_env_override(self, env):
        env = filter(None, map(strip, env.splitlines()))
        try:
            env = list([(key, val) for key, val in [
                map(strip, line.split('=', 1)) for line in env
            ]])
        except ValueError:  # Unpacking impossible
            raise UserError('Configuration error, '
                            'every environment line should contain a "=" sign')
        return env

    def _get_env(self):
        s = {
            'PATH': os.environ.get('PATH', ''),
            'PREFIX': self.options['location'],
            'RUBYLIB': os.environ.get('RUBYLIB', ''),
        }
        env = {
            'GEM_HOME': '%(PREFIX)s/lib/ruby/gems' % s,
            'RUBYLIB': self._join_paths(
                '%(RUBYLIB)s',
                '%(PREFIX)s/lib',
                '%(PREFIX)s/lib/ruby',
                '%(PREFIX)s/lib/site_ruby',
            ) % s,
            'PATH': self._join_paths(
                '%(PATH)s',
                '%(PREFIX)s/bin',
            ) % s,
        }
        env_override = self.options.get('environment', '')
        env_override = self._get_env_override(env_override)
        env.update({k: (v % env) for k, v in env_override})
        return env

    def get_gem_dict(self, gem_str):
        parsed_gem = gem_str.split('==', 1)
        gem_dict = {'gemname': parsed_gem[0].strip()}
        if len(parsed_gem) > 1:
            gem_dict['version'] = parsed_gem[1].strip()
        return gem_dict

    def _get_rubygems_url_and_version(self):
        version = self.options.get('version')
        if version:
            return '%s-%s.zip' % (RUBYGEMS_URL_BASE, version), version

        url = self.url
        if url:
            r = re.search(VERSION_ZIP_RE + '$', url)
        else:
            f = urllib.request.urlopen('https://rubygems.org/pages/download')
            try:
                r = re.search(RUBYGEMS_URL_BASE + VERSION_ZIP_RE,
                              f.read().decode('utf-8'))
            finally:
                f.close()
        if r:
            return url or r.group(0), r.group(1)
        raise UserError("Can't find rubygems version.")

    def _install_rubygems(self, url, version):
        srcdir = os.path.join(self.buildout['buildout']['parts-directory'],
                              'rubygems-' + version)
        options = {
            'url': url,
            'destination': srcdir,
        }
        Download(self.buildout, self.name, options).install()

        current_dir = os.getcwd()
        os.chdir(srcdir)

        env = self._get_env()
        env['PREFIX'] = self.options['location']

        cmd = [
            self.ruby_executable,
            'setup.rb',
            'all',
            '--prefix=' + self.options['location'],
            '--no-rdoc',
            '--no-ri',
        ]

        try:
            self.run(cmd, env)
        finally:
            rmtree(srcdir)
            os.chdir(current_dir)

    def _install_executable(self, path):
        content = ['#!/bin/sh']
        for key, val in self._get_env().items():
            content.append("export %s='%s'" % (key, val))
        content.append('%s "$@"' % path)
        name = os.path.basename(path)
        bindir = self.buildout['buildout']['bin-directory']
        executable = os.path.join(bindir, name)
        f = open(executable, 'w')
        f.write('\n'.join(content) + '\n\n')
        f.close()
        os.chmod(executable, (
            # rwx rw- rw-
            stat.S_IRWXU |
            stat.S_IRGRP | stat.S_IWGRP |
            stat.S_IROTH | stat.S_IWOTH
        ))

        return executable

    def _install_gem(self, gem_dict, gem_executable, bindir):
        cmd = [
            self.ruby_executable,
            gem_executable,
            'install',
            '--no-document',
            '--bindir=' + bindir,
        ]

        if self.deployment:
            cmd.append('--ignore-dependencies')

        cmd.append(gem_dict['gemname'])
        if 'version' in gem_dict:
            cmd.append('--version=' + gem_dict['version'])

        extra = self.options.get('gem-options', '')
        extra = filter(None, map(strip, extra.splitlines()))

        cmd.append('--')
        cmd.extend(extra)

        self.run(cmd, self._get_env())

    def get_dependency_list(self, gem_dict, gem_executable, version):
        gem_search_pattern = '^' + gem_dict['gemname'].replace('.',r'\.') + '$'
        if int(version.split(".")[0]) < 3:
            gem_search_pattern = '/' + gem_search_pattern + '/'

        cmd = [
            self.ruby_executable,
            gem_executable,
            'dependency',
            '-rv',
            gem_dict['version'],
            gem_search_pattern,
        ]
        cmd_result = self.run(cmd, self._get_env())

        return [{
            'gemname': match[0],
            'constraint_list': [
                {
                    'symbol': match[1],
                    'version': match[2],
                },
                {
                    'symbol': match[5],
                    'version': match[6],
                },
            ],
        } for match in self.gem_regex.findall(cmd_result)]

    def install(self):
        location = self.options['location']

        bindir = os.path.join(self.options['location'], 'bin')
        if os.path.lexists(location):
            rmtree(location)
        try:
            os.makedirs(location)
            parts = [location]

            url, version = self._get_rubygems_url_and_version()
            if int(version.split(".")[0]) < 2:
                raise UserError("Rubygems version must be >= 2.0.0")

            self._install_rubygems(url, version)
            gem_executable = glob.glob(os.path.join(bindir, 'gem*'))[0]

            gem_dict_list = list(map(self.get_gem_dict, self.gems))
            for gem_dict in gem_dict_list:
                if self.deployment:
                    if 'version' not in gem_dict:
                        raise UserError(
                            'Configuration error, '
                            'version for gem %s is missing' % gem_dict['gemname']
                        )

                    for dep_dict in self.get_dependency_list(gem_dict,
                                                             gem_executable,
                                                             version):
                        match = [gem_d for gem_d in gem_dict_list
                                  if dep_dict['gemname'] == gem_d['gemname']]
                        if not match:
                            raise UserError(
                                'Configuration error, '
                                'version for dependency %s is missing'
                                % dep_dict['gemname']
                            )

                        for constraint in dep_dict['constraint_list']:
                            self._check_dependency_constraint(
                                constraint, match[0], gem_dict['gemname'])

                self.log.info('installing ruby gem "%s"', gem_dict['gemname'])
                self._install_gem(gem_dict, gem_executable, bindir)
        except:
            if os.path.lexists(location):
                rmtree(location)
            raise

        for executable in os.listdir(bindir):
            installed_path = self._install_executable(
                os.path.join(bindir, executable)
            )
            parts.append(installed_path)

        return parts
