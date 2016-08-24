from extract_entities import extract_entities
from DBpediaExtractor import DBpediaExtractor
import pprint as pp
import json

text = 'One Florida Milan in Italy, Cambridge, Ibiza, Kingston Ontario, Milan Kundera, year ago, Toscani, Middle East, United Kingdom and New York City were flooded, several hours George Bush before cities across the United States started their annual fireworks displays, a different type of fireworks were set off at the European Center for Nuclear Research (CERN) in Switzerland. At 9:00 a.m., physicists announced to the world that they had found something they had been searching for for nearly 50 years: the elusive Higgs boson. Today, on the anniversary of its discovery, are we any closer to figuring out what that particle\'s true identity is? The Higgs boson is popularly referred to as "the God particle," perhaps because of its role in giving other particles their mass. However, it\'s not the boson itself that gives mass. Back in 1964, Peter Higgs proposed a theory that described a universal field (similar to an electric or a magnetic field) that particles interacted with'

ee = extract_entities(text)
return_dict = []

place_list = ee.get_places()
for (alchemy_label, uri, rel) in place_list:
	t_dict = {}
	dbe = DBpediaExtractor(uri)

	t_dict['uri'] = uri
	t_dict['type'] = 'location'
	t_dict['label'] = dbe.get_label()
	t_dict['relevance_score'] = rel
	t_dict['alchemy_label'] = alchemy_label

	t_dict['latitude'] = dbe.get_latitude()
	t_dict['longitude'] = dbe.get_longitude()
	t_dict['comment'] = dbe.get_comment()
	t_dict['coordinates'] = dbe.get_coordinates()

	return_dict.append(t_dict)

name_list = ee.get_names()
for (alchemy_label, uri, rel) in name_list:
	t_dict = {}
	dbe = DBpediaExtractor(uri)

	t_dict['uri'] = uri
	t_dict['type'] = 'person'
	t_dict['label'] = dbe.get_label()
	t_dict['relevance_score'] = rel	
	t_dict['alchemy_label'] = alchemy_label

	t_dict['alma_mater'] = dbe.get_almaMater()
	t_dict['birth_date'] = dbe.get_birthDate()
	t_dict['birthplace_uri'] = dbe.get_birthPlace_uri()
	t_dict['death_date'] = dbe.get_deathDate()	
	t_dict['deathplace_uri'] = dbe.get_deathPlace_uri()
	t_dict['description'] = dbe.get_description()
	t_dict['known_for'] = dbe.get_knownFor()
	t_dict['residence'] = dbe.get_residence()
	t_dict['spouse'] = dbe.get_spouse()		

	return_dict.append(t_dict)

pp.pprint(return_dict)
with open('output.json', 'w') as w:
	json.dump(return_dict, w)