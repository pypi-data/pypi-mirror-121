import os
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class DotnetRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='dotnet')

		# inputs

		if not 'inputs' in self.options:
			raise UserError('Missing mandatory "inputs" parameter.')

		self.inputs = self.options['inputs'].splitlines()

		# artefacts

		if not 'artefacts' in self.options:
			raise UserError('Missing mandatory "artefacts" parameter.')

		self.artefacts = self.options['artefacts'].splitlines()

		self.args = []

		# restore

		if 'restore' in self.options:
			# dotnet restore [<ROOT>] [--configfile <FILE>] [--disable-parallel]
			#	[-f|--force] [--force-evaluate] [--ignore-failed-sources]
			#	[--interactive] [--lock-file-path <LOCK_FILE_PATH>] [--locked-mode]
			#	[--no-cache] [--no-dependencies] [--packages <PACKAGES_DIRECTORY>]
			#	[-r|--runtime <RUNTIME_IDENTIFIER>] [-s|--source <SOURCE>]
			#	[--use-lock-file] [-v|--verbosity <LEVEL>]

			self.args.append('restore')

			for i in self.inputs:
				self.args.append(os.path.abspath(i))

			if 'config-file' in self.options:
				self.args += [ '--configfile', os.path.abspath(self.options['config-file']) ]

			if 'parallel' in self.options and self.options['parallel'] == '0':
				self.args += [ '--disable-parallel' ]

			if 'force' in self.options:
				self.args += [ '--force' ]

			if 'force-evaluate' in self.options:
				self.args += [ '--force-evaluate' ]

			if 'ignore-failed-sources' in self.options:
				self.args += [ '--ignore-failed-sources' ]

			if 'interactive' in self.options:
				self.args += [ '--interactive' ]

			if 'locked-mode' in self.options:
				self.args += [ '--locked-mode' ]

			if 'no-cache' in self.options:
				self.args += [ '--no-cache' ]

			if 'no-dependencies' in self.options:
				self.args += [ '--no-dependencies' ]

			if 'packages-path' in self.options:
				self.args += [ '--packages', os.path.abspath(self.options['packages-path']) ]

			if 'runtime' in self.options:
				self.args += [ '--runtime', self.options['runtime'] ]

			if 'source' in self.options:
				self.args += [ '--source', self.options['source'] ]

			if 'use-lock-file' in self.options:
				self.args += [ '--use-lock-file' ]

			if 'verbosity' in self.options:
				self.args += [ '--verbosity', self.options['verbosity'] ]

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		for a in self.artefacts:
			self.options.created(os.path.abspath(a))

		self.runCommand(self.args)

		return self.options.created()

def uninstall(name, options):
	pass