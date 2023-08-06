import glob
import os
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError
from subprocess import CalledProcessError

class InklecateRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='inklecate.exe')

		self.options.setdefault('output_directory', '')

		# resolve input files

		if not 'input' in self.options:
			raise UserError('Missing mandatory "input" parameter.')

		self.input_resolved = []
		for i in self.options['input'].splitlines():
			self.input_resolved.extend([os.path.abspath(f) for f in glob.glob(i) if os.path.isfile(f)])

		self.options['input_resolved'] = ' '.join(str(e) for e in self.input_resolved)

	def install(self):
		# resolve output files

		output_directory = self.options['output_directory']

		for i in self.input_resolved:
			if not os.path.exists(i):
				continue

			input_path = os.path.abspath(i)
			filename = os.path.split(input_path)[1]
			artefact_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.json')

			self.options.created(artefact_path)

			# compile ink to json

			self.runCommand([ '-o', artefact_path, input_path ])

			self.log.info('Compiled ink to "%s.json".' % filename)

		return self.options.created()

def uninstall(name, options):
	pass