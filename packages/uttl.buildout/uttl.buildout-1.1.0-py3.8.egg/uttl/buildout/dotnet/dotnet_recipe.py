import os.path

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class DotnetRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='dotnet')

		# inputs

		if not 'inputs' in self.options:
			raise UserError('Missing mandatory "inputs" option.')

		self.inputs = self.options['inputs'].splitlines()

		# artefacts

		if 'artefacts' in self.options:
			self.artefacts = self.options['artefacts'].splitlines()
		else:
			self.artefacts = []

		self.args = []

	def install(self):
		for a in self.artefacts:
			self.options.created(os.path.abspath(a))

		self.runCommand(self.args)

		return self.options.created()

def uninstall(name, options):
	pass