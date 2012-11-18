from pyquery import PyQuery as pq

class Scrapers():

	def hierachical(self, **kargs):
		markup,supertitle,title,block,link = map(
				lambda x: kargs.get(x).encode('utf-8'),
				['markup','supertitle','title','block','link'])
		html = pq(markup)
		return [{
			"supertitle":pqblock(supertitle).text(),
			"title":pqblock(title).text(),
			"link":pqblock(link).attr('href')}
			for pqblock in map(pq,html(block))]

	def sibling(self, **kargs):
		markup,supertitle,title,block,link = map(
				lambda x: kargs.get(x).encode('utf-8') if kargs.get(x) else '',
				['markup','supertitle','title','block','link'])
		html = pq(markup)
		return [{
			"supertitle":pqblock(supertitle).text(),
			"title":pqblock(title).text(),
			"link":pqblock.nextAll(link).attr('href')}
			for pqblock in map(pq,html(block))]
