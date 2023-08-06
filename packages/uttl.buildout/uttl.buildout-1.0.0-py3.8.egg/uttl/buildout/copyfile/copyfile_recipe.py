import logging
import os
import shutil

class CopyFileRecipe(object):
	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		self.log = logging.getLogger(self.name)

		self.options.setdefault('destination', os.getcwd())
		self.options.setdefault('source-path', '')

		self.files = options['files'].splitlines()

	def install(self):
		dstPath = os.path.abspath(self.options['destination'])
		if not os.path.exists(dstPath):
			os.makedirs(dstPath, 0o777, True)

		srcPath = os.path.abspath(self.options['source-path'])

		for file in self.files:
			filename = os.path.basename(file)

			src = os.path.abspath(file)
			srcExists = os.path.exists(src)
			if not srcExists:
				src = os.path.abspath(os.path.join(srcPath, filename))
				srcExists = os.path.exists(src)

			self.log.debug('src: %s (exists: %r)' % (src, srcExists))

			if not srcExists:
				raise FileNotFoundError(src)

			dst = os.path.abspath(os.path.join(dstPath, filename))
			dstExists = os.path.exists(dst)

			self.log.debug('dst: %s (exists: %r)' % (dst, dstExists))

			self.options.created(dst)

			if not dstExists:
				self.log.info('Copying "' + filename + "'...")
				shutil.copy(src, dst)

		return self.options.created()

	update = install

def uninstall(name, options):
	pass