
class Mappers():
	def prepend_mapper(self,key,prefix):
		def mapper(d):
			d[key] = prefix+d.get(key)
			return d
		return mapper

