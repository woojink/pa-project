import rdflib

BASE_URL = 'http://dbpedia.org/resource/'

class DBpediaExtractor(object):
	"""
	Extractor for DBPedia

	Attributes:
		entity (str): URL friendly name for the entity
		url (str): The main resource URL
		g (rdflib graph): DBPedia RDF graph object
	"""

	def __init__(self, url):
		"""
		Args:
			url (str): Raw DBPedia URL
		"""
		self.entity = url.split('/')[-1]
		self.url = BASE_URL + self.entity
		self.g = self.get_rdf()
		
	def get_rdf(self):
		g = rdflib.Graph()
		g.load(self.url)
		return g

	def get_ontology(self, endpoint):
		"""
		Returns ontology information for the given endpoint

		Args:
			endpoint (url): Endpoint for the desired ontology
		"""
		r_list = []
		for stmt in self.g.subject_objects(rdflib.URIRef("http://dbpedia.org/ontology/" + endpoint)):
			r_list.append(str(stmt[1]))
		return r_list

	def get_properties(self, endpoint):
		"""
		Returns properties for the given endpoint

		Args:
			endpoint (str): Endpoint for the desired properties
		"""
		r_list = []
		for stmt in self.g.subject_objects(rdflib.URIRef("http://dbpedia.org/property/" + endpoint)):
			r_list.append(str(stmt[1]))
		return r_list

	def get_name(self):
		return self.get_properties("name")

	def get_birthDate(self):
		return self.get_ontology("birthDate")

	def get_deathDate(self):
		return self.get_ontology("deathDate")

	def get_birthPlace_uri(self):
		return self.get_ontology("birthPlace")

	def get_deathPlace_uri(self):
		return self.get_ontology("deathPlace")

	def get_residence(self):
		return self.get_ontology("residence")

	def get_knownFor(self):
		return self.get_ontology("knownFor")

	def get_almaMater(self):
		return self.get_properties("almaMater")

	def get_spouse(self):
		r_list = []
		for stmt in self.g.subject_objects(rdflib.URIRef("http://dbpedia.org/ontology/" + "spouse")):
			# Filters through to exclude symmetrical (repeated) information
			if str(stmt[1]) != self.url:
				r_list.append(str(stmt[1]))
		return r_list