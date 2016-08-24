from extract_entities import extract_entities
from DBpediaExtractor import DBpediaExtractor

text = 'One Florida Milan in Italy, Cambridge, Ibiza, Kingston Ontario, Milan Kundera, year ago, Toscani, Middle East, United Kingdom and New York City were flooded, several hours George Bush before cities across the United States started their annual fireworks displays, a different type of fireworks were set off at the European Center for Nuclear Research (CERN) in Switzerland. At 9:00 a.m., physicists announced to the world that they had found something they had been searching for for nearly 50 years: the elusive Higgs boson. Today, on the anniversary of its discovery, are we any closer to figuring out what that particle\'s true identity is? The Higgs boson is popularly referred to as "the God particle," perhaps because of its role in giving other particles their mass. However, it\'s not the boson itself that gives mass. Back in 1964, Peter Higgs proposed a theory that described a universal field (similar to an electric or a magnetic field) that particles interacted with'

ee = extract_entities(text)
place_list = ee.get_places()
for (_, uri) in place_list:
	dbe = DBpediaExtractor(uri)
	coor = dbe.get_coordinates()
	comment = dbe.get_comment()
	label = dbe.get_label()

	print(uri)
	print(label)
	print(comment)
	print(coor)
	print()

name_list = ee.get_names()
for (_, uri) in name_list:
	dbe = DBpediaExtractor(uri)
	desc = dbe.get_description()	
	label = dbe.get_label()

	print(uri)
	print(label)
	print(desc)
	print(dbe.get_birthDate())
	print(dbe.get_deathDate())
	print(dbe.get_birthPlace_uri())
	print(dbe.get_deathPlace_uri())
	print(dbe.get_spouse())
	print(dbe.get_knownFor())
	print(dbe.get_residence())
	print(dbe.get_almaMater())
	print()
