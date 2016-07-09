#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import sys
import codecs


try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


if sys.version_info < (2, 7):
	raise SystemExit("Python 2.7 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 2):
	raise SystemExit("CPython 3.3 or Pypy 3 (3.2) or later is required.")

version = description = url = author = author_email = ""  # Silence linter warnings.
exec(open(os.path.join("web", "account", "release.py")).read())  # Actually populate those values.


class PyTest(TestCommand):
	__slots__ = ('test_args', 'test_suite')
	
	def finalize_options(self):
		TestCommand.finalize_options(self)
		
		self.test_args = []
		self.test_suite = True
	
	def run_tests(self):
		import pytest
		sys.exit(pytest.main(self.test_args))


here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-spec',  # output formatting
		'web.dispatch.resource',  # dispatch tests
	]


# ## Package Metadata

setup(
	# ### Basic Metadata
	name = "web.account",
	version = version,
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	download_url = 'https://github.com/marrow/web.account/releases',
	author = author.name,
	author_email = author.email,
	license = 'MIT',
	keywords = ['marrow', 'web.app', 'web.ext', 'web.account'],
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Environment :: Console",
			"Environment :: Web Environment",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 2",
			"Programming Language :: Python :: 2.7",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.2",
			"Programming Language :: Python :: 3.3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries",
			"Topic :: Software Development :: Libraries :: Python Modules",
		],
	
	# ### Code Discovery
	
	packages = find_packages(exclude=['bench', 'docs', 'example', 'test', 'htmlcov']),
	include_package_data = True,
	namespace_packages = [
			'web',  # primary namespace
			'web.app',  # account management endpoints
			'web.ext',  # framework extensions
			'web.account',  # account providers
		],
	zip_safe = True,
	cmdclass = dict(
			test = PyTest,
		),
	
	# ### Plugin Registration
	
	entry_points = {
			# #### Re-usable applications or application components.
			'web.app': [
					'account = web.app.account:AccountCollection',
				],
			
			# #### WebCore Extensions
			'web.extension': [
					'account = web.ext.account:AccountExtension',
				],
			
			# #### WebCore Extensions
			'web.account.provider': [
					'local = web.account.local:LocalProvider',
					'facebook = web.account.facebook:FacebookProvider',
					'github = web.account.github:GithubProvider',
					'linkedin = web.account.linkedin:LinkedinProvider',
					'twitter = web.account.twitter:TwitterProvider',
					'u2f = web.account.u2f:UniversalSecondFactorProvider',
					'yubikey = web.account.yubikey:YubikeyProvider',
				],
		},
	
	# ## Installation Dependencies
	
	install_requires = [
			'marrow.package<2.0',  # dynamic execution and plugin management
		],
	tests_require = tests_require,
	
	extras_require = {
			'development': tests_require,  # An extended set of useful development tools.
		},
)

