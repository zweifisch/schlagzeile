# TODO
# * view teaser by entering number, implement by history, using beaker
# * read full article by entering number
# * enable number as cmd
# * shell mode?

import sys
import os
import json
from pyquery import PyQuery as pq

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from blessings import Terminal

from pyfiglet import figlet_format

from . import Mappers
from . import Scrapers


def determine_path():
	try:
		root = __file__
		if os.path.islink(root):
			root = os.path.realpath(root)
		return os.path.dirname(os.path.abspath(root))
	except:
		print("can't locate configuration")
		return False


class Schlagzeile():

	def init_cache(self):
		cache_opts = {
				'cache.type': 'file',
				'cache.data_dir': '/tmp/cache/data',
				'cache.lock_dir': '/tmp/cache/lock'}
		cm = CacheManager(**parse_cache_config_options(cache_opts))
		return cm.get_cache('schlagzeile', expire=600)

	def get_config(self):
		user_config_file = os.path.expanduser('~') + os.path.sep + '.schlagzeile.json'
		site_files = [
				os.path.dirname(os.path.realpath(sys.argv[0])) + os.path.sep + '.schlagzeile.json',
				os.path.dirname(os.path.realpath(sys.argv[0])) + os.path.sep + 'schlagzeile.json',
				user_config_file]
		while len(site_files) > 0:
			site_file = site_files.pop()
			if(os.path.exists(site_file)):
				return site_file
		else:
			path = determine_path()
			if path:
				with open(user_config_file, 'w') as f:
					with open(path + os.path.sep + 'schlagzeile.json') as config_example:
						f.write(config_example.read())
				return user_config_file
		return False

	def process_site(self, site_name, site):
		url = site.get('url')
		scraper = getattr(self.scrapers, str(site.get('type')), None)
		pattern = site.get('pattern')
		if scraper is None:
			return

		print(figlet_format(site_name, font='slant'))

		def get_raw_html():
			return str(pq(url))

		markup = self.cache.get(key=url, createfunc=get_raw_html)
		pattern.update({'markup': markup})

		items = scraper(**pattern)

		if site.get('mapper'):
			for key, mappers_list in site.get('mapper').items():
				for mapper_type, arg in mappers_list:
					mapper_factory = getattr(self.mappers, str(mapper_type) + '_mapper', None)
					if mapper_factory:
						items = map(mapper_factory(key, arg), items)

		for index, item in enumerate(items):
			# import pprint
			# pprint.pprint(item)
			if not item['link']:
				item['link'] = ''
			else:
				if(item['link'][0:4] != 'http'): item['link'] = url + item['link']
			if not item['title']:
				item['title'] = ''
			item['title'] = self.term.cyan(item['title'])
			item.update({
				'index': index + 1,
				'indent': ' ' * (len(str(index + 1)) + 2)})
			if(item.get('supertitle')):
				print "%(index)d. %(supertitle)s - %(title)s\n%(indent)s%(link)s" % item
			else:
				print "%(index)d. %(title)s\n%(indent)s%(link)s" % item

	def init(self):
		site_file = self.get_config()
		if(not site_file):
			print "schlagzeile.json not found"
			sys.exit(1)

		with open(site_file) as fp:
			self.sites = json.load(fp)

		self.cache = self.init_cache()

		self.mappers = Mappers()
		self.scrapers = Scrapers()
		self.term = Terminal()

	def output(self, items, **kargs):
		if(kargs.get('number')):
			for index, item in enumerate(items):
				print "%d. %s" % (index + 1, item)

	def cmd_all(self):
		for site_name, site in self.sites.items():
			self.process_site(site_name, site)

	def cmd_list(self, *args):
		if(len(args) == 0):
			self.output(self.sites.keys(), number=True)
		else:
			for site_name, site in self.sites.items():
				if site_name in args:
					self.process_site(site_name, site)

	def execute(self, cmd, *args):
		self.init()
		commands = {
				'all': self.cmd_all,
				'ls': self.cmd_list,
				'list': self.cmd_list}
		command = commands.get(cmd)
		if command:
			command(*args)
		else:
			sys.exit(1)


def run():
	if(len(sys.argv) > 1):
		argv = sys.argv[1:]
	else:
		argv = ['ls']
	schlagzeile = Schlagzeile()
	schlagzeile.execute(*argv)

if __name__ == '__main__':
	run()
