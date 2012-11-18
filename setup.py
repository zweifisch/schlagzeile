from distutils.core import setup

setup(
	name='schlagzeile',
	url='https://github.com/zweifisch/schlagzeile',
	version='0.0.1',
	description='headlines on commandline',
	author='Feng Zhou',
	author_email='zf.pascal@gmail.com',
	packages=['schlagzeile'],
	package_data={'schlagzeile': ['schlagzeile.json']},
	install_requires=['PyQuery', 'beaker', 'blessings', 'pyfiglet'],
	scripts=['bin/schlagzeile']
)
