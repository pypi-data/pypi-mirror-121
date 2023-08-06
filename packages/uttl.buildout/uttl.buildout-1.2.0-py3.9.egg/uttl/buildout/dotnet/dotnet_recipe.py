from uttl.buildout.command_recipe import CommandRecipe
from zc.buildout import UserError

class DotnetRecipe(CommandRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='dotnet')

		# inputs

		if not 'inputs' in self.options:
			raise UserError('Missing mandatory "inputs" option.')

		self.inputs = self.options['inputs'].splitlines()

	def install(self):
		for a in self.artefacts:
			self.options.created(a)

		self.runCommand(self.args)

		return self.options.created()

def uninstall(name, options):
	pass