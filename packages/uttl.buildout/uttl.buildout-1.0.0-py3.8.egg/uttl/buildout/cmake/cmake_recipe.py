import logging
import os
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class CmakeRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='cmake')

		self.args = [ ]

		# generator

		if 'generator' in self.options:
			self.args.extend([ '-G', self.options['generator'] ])

		# configure or build

		if 'configure_path' in self.options:
			if not 'generator' in self.options:
				raise UserError('Missing mandatory "generator" parameter.')

			self.args.append(os.path.abspath(self.options['configure_path']))
		else:
			if not 'build_path' in self.options:
				raise UserError('Missing mandatory "build_path" parameter.')

			if 'build_path' in self.options:
				build_path = os.path.abspath(self.options['build_path'])
				self.args.extend([ '--build', build_path ])

			if 'target' in self.options:
				targets = self.options['target'].splitlines()
				self.args.extend([ '--target', ' '.join(str(t) for t in targets) ])

			if 'config' in self.options:
				self.args.extend([ '--config', self.options['config'] ])

		self.options['args'] = ' '.join(str(e) for e in self.args)

		# variables

		self.var_args = []

		if 'install_path' in self.options:
			install_path = os.path.abspath(self.options['install_path'])
			self.options['var_CMAKE_INSTALL_PREFIX'] = os.path.abspath(install_path) + ':PATH'

		split_name = re.compile(r'var_(.+)')
		split_type = re.compile(r'(.+):(\w*)$')

		for var in [var for var in list(self.options.keys()) if var.startswith('var_')]:
			# get name

			match = split_name.match(var)
			if not match:
				raise UserError('Failed to split variable name for "%s".' % (var))

			var_name = match.group(1)

			# get type and value

			var_value = self.options[var]

			match = split_type.match(var_value)
			if match:
				var_value = match.group(1)
				var_type = match.group(2)
			else:
				var_value = var_value
				var_type = 'STRING'

			if not any(var_type in t for t in ['BOOL', 'FILEPATH', 'PATH', 'STRING', 'INTERNAL']):
				raise UserError('Invalid variable type "%s" for "%s".' % (var_type, var))

			arg = '-D%s:%s=%s' % (var_name, var_type, var_value)
			self.var_args.append(arg)

			self.log.debug(arg)

		if len(self.var_args) > 0:
			if not 'generator' in self.options:
				raise UserError('Missing mandatory "generator" parameter.')

			self.var_args += [ '-G', self.options['generator'] ]

			if not 'configure_path' in self.options:
				raise UserError('Missing mandatory "configure_path" parameter.')

			if not 'install_path' in self.options:
				raise UserError('Missing mandatory "install_path" parameter.')

			self.var_args.append(os.path.abspath(self.options['configure_path']))

	def install(self):
		self.working_dir = os.getcwd()
		configure_path = None

		# change to configure path

		if 'configure_path' in self.options:
			configure_path = os.path.abspath(self.options['configure_path'])

			if not os.path.exists(configure_path):
				os.makedirs(configure_path, 0o777, True)

			os.chdir(configure_path)

		# set variables

		if len(self.var_args) > 0:
			self.runCommand(self.var_args, parseLine=self.parseLine, quiet=True)

		# run command

		self.runCommand(self.args, parseLine=self.parseLine)

		# back to working directory

		if configure_path:
			os.chdir(self.working_dir)

		# add manual artefact (e.g. generated solution)

		if 'artefact_path' in self.options:
			self.options.created(os.path.abspath(self.options['artefact_path']))

		return self.options.created()

	check_errors = re.compile(r'.*Error: (.*)')
	check_failed = re.compile(r'.*(Build FAILED|CMake Error|MSBUILD : error).*')
	check_artefacts = re.compile(r'.*(.+?) -> (.+)')
	check_installed = re.compile(r'.*-- (.+?): (.+)')

	def parseLine(self, line):
		# check for errors

		if self.check_errors.match(line) or self.check_failed.match(line):
			return False

		# add artefacts to options

		match = self.check_artefacts.match(line)
		if match:
			path = match.group(2)
			self.options.created(os.path.abspath(path))

		# add installed files to options

		match = self.check_installed.match(line)
		if match:
			what = match.group(1)
			path = match.group(2)

			if any(what in s for s in ['Installing', 'Up-to-date']):
				self.options.created(os.path.abspath(path))

		return True

def uninstall(name, options):
	pass