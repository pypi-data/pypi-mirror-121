import logging
import os
import shutil

from uttl.buildout.base_recipe import BaseRecipe
from zc.buildout import UserError

class CopyFileRecipe(BaseRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

		self.options.setdefault('source-path', os.getcwd())
		self.options.setdefault('destination-path', os.getcwd())

		# paths

		self.src_path = os.path.abspath(self.options['source-path'])

		self.dst_path = os.path.abspath(self.options['destination-path'])
		if not os.path.exists(self.dst_path):
			os.makedirs(self.dst_path, 0o777, True)

		# get files

		if not 'files' in self.options:
			raise UserError('Missing mandatory "files" option.')

		self.files = [os.path.join(self.dst_path, file) for file in self.options['files'].splitlines()]

	def install(self):
		self.log.debug(str(self.files))

		for f in self.files:
			self.options.created(f)

		for dst_path in self.files:
			filename = os.path.basename(dst_path)

			src_path = os.path.join(self.src_path, filename)

			# check if file is missing

			if not os.path.exists(dst_path):
				self.log.debug('%s does not exist at destination' % (filename))

				self.copyFile(src_path, dst_path, filename)

				continue

			# check if source was modified

			src_modified = os.path.getmtime(src_path)
			dst_modified = os.path.getmtime(dst_path)

			if src_modified > dst_modified:
				self.log.debug('%s was modified (%d > %d)' % (filename, src_modified, dst_modified))

				self.copyFile(src_path, dst_path, filename)

		return self.options.created()

	update = install

	def copyFile(self, src, dst, filename):
		if not os.path.exists(src):
			raise FileNotFoundError(src)

		self.log.info('Copying "' + filename + "'...")

		shutil.copy(src, dst)

def uninstall(name, options):
	pass