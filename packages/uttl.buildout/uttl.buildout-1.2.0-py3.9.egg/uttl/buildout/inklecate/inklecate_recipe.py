import glob
import os.path
import re

from uttl.buildout.command_recipe import CommandRecipe
from zc.buildout import UserError

class InklecateRecipe(CommandRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='inklecate.exe')

		self.options.setdefault('output-directory', '')

		self.output_directory = self.options['output-directory']

		# resolve input files

		if not 'input' in self.options:
			raise UserError('Missing mandatory "input" parameter.')

		self.input_resolved = []
		for i in self.options['input'].splitlines():
			self.input_resolved.extend([os.path.abspath(f) for f in glob.glob(i) if os.path.isfile(f)])

		self.options['input_resolved'] = ' '.join(str(e) for e in self.input_resolved)

	def install(self):
		for a in self.artefacts:
			self.options.created(a)

		# resolve output files

		for i in self.input_resolved:
			if not os.path.exists(i):
				continue

			input_path = os.path.abspath(i)
			filename = os.path.split(input_path)[1]
			artefact_path = os.path.join(self.output_directory, os.path.splitext(filename)[0] + '.json')

			self.options.created(artefact_path)

			# compile ink to json

			args = self.additional_args
			args += [ '-o', artefact_path, input_path ]
			self.runCommand(args)

			self.log.info('Compiled ink to "%s.json".' % filename)

		return self.options.created()

def uninstall(name, options):
	pass