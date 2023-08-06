import logging
import os
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class QmakeRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='qmake')

		self.args = [ ]

		if 'template' in self.options:
			self.args.extend([ '-t', self.options['template'] ])

		if 'template_prefix' in self.options:
			self.args.extend([ '-tp', self.options['template_prefix'] ])

		if 'recursive' in self.options:
			self.args.append('-r')

		if 'artefact_path' in self.options:
			self.args.extend([ '-o', self.options['artefact_path'] ])

		# add file list

		if 'files' in self.options:
			raise UserError('Missing mandatory "files" parameter.')

		self.args.extend(self.options['files'].splitlines())

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		self.options.created(self.options['artefact_path'])

		# build argument list

		if 'vcvars' in self.options:
			prefix_args = [ self.options['vcvars'], 'amd64', '&&' ]
		else:
			prefix_args = []

		self.runCommand(self.args, prefixArgs=prefix_args, parseLine=self.parseLine)

		return self.options.created()

	check_errors = re.compile(r'.*ERROR:\s*(.*)')

	def parseLine(self, line):
		# check for errors

		return not self.check_errors.match(line)

def uninstall(name, options):
	pass