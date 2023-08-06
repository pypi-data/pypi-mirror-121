from zc.buildout import UserError
from subprocess import CalledProcessError

import logging
import os
import re
import subprocess

class DevEnvRecipe(object):
	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		self.log = logging.getLogger(self.name)

		self.options.setdefault('executable', 'devenv.com')
		self.options.setdefault('always_build', '0')
		self.options.setdefault('restore_packages', '0')

		if not 'solution' in self.options:
			raise UserError('Missing mandatory "solution" parameter.')

		if not 'artefacts' in self.options:
			raise UserError('Missing mandatory "artefacts" parameter.')

		self.artefacts = self.options['artefacts'].splitlines()

		self.args = [ os.path.abspath(self.options['solution']) ]

		if 'project' in self.options:
			self.args.extend([ '/Project', self.options['project'] ])

		if 'build' in self.options:
			self.args.extend([ '/Build', self.options['build'] ])

		if 'command' in self.options:
			self.args.extend([ '/Command', '"%s"' % self.options['command'] ])

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		build = self.options['always_build'] != '0'

		# check if any artefact is missing

		for a in self.artefacts:
			artefact_path = os.path.abspath(a)
			self.options.created(artefact_path)
			if not build and not os.path.exists(artefact_path):
				build = True

		# build with devenv

		if build:
			if self.options['restore_packages'] != '0' and not self.runCommand([ 'dotnet', 'restore', self.options['solution'] ]):
				return CalledProcessError

			args = [ self.options['executable'] ]
			args.extend(self.args)

			if not self.runCommand(args):
				return CalledProcessError

		return self.options.created()

	update = install

	def runCommand(self, args):
		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				self.log.info(line.rstrip().decode('UTF-8'))

			proc.communicate()

			return proc.returncode == 0

def uninstall(name, options):
	pass