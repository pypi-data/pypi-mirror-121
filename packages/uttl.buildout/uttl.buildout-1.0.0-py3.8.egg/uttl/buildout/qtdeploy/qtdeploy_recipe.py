import os.path
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class QtDeployRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='windeployqt.exe')

		self.options.setdefault('target', 'release')

		self.args = [ ]

		# target

		if self.options['target'] == 'debug':
			self.args.append('--debug')
			self.args.append('--pdb')
		else:
			self.args.append('--release')

		# translations

		if 'translations' in self.options:
			translations = self.options['translations'].splitlines()
			self.args += [ '--translations', ','.join(str(t) for t in translations) ]
		else:
			self.args.append('--no-translations')

		# compiler runtime

		if 'compiler_runtime' in self.options:
			if self.options['compiler_runtime'] == '1':
				self.args.append('--compiler-runtime')
			else:
				self.args.append('--no-compiler-runtime')

		# webkit2

		if 'webkit2' in self.options:
			if self.options['webkit2'] == '1':
				self.args.append('--webkit2')
			else:
				self.args.append('--no-webkit2')

		# angle

		if 'angle' in self.options:
			if self.options['angle'] == '1':
				self.args.append('--angle')
			else:
				self.args.append('--no-angle')

		# software rasterizer

		if 'opengl_sw' in self.options:
			self.args.append('--no-opengl-sw')

		# virtual keyboard

		if 'virtual_keyboard' in self.options:
			self.args.append('--no-virtualkeyboard')

		# d3d

		if 'system_d3d_compiler' in self.options:
			self.args.append('--no-system-d3d-compiler')

		# target path

		if not 'target_path' in self.options:
			raise UserError('Missing mandatory "target_path" parameter.')

		self.args.append(self.options['target_path'])
		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		# build argument list

		if 'vcvars' in self.options:
			prefix_args = [ self.options['vcvars'], 'amd64', '&&' ]
		else:
			prefix_args = []

		# get list of files

		self.files = []

		args = [ '--list', 'target' ] + self.args
		self.runCommand(args, prefixArgs=prefix_args, parseLine=self.parseFileList, quiet=True)

		# copy files

		self.runCommand(self.args, prefixArgs=prefix_args)

		# check if files have been copied

		copied = [f for f in self.files if os.path.exists(f)]
		for f in copied:
			self.options.created(f)

		return self.options.created()

	def parseFileList(self, path):
		drive, tail = os.path.splitdrive(path)

		if drive != '':
			self.files.append(path)

		return True

def uninstall(name, options):
	pass