from extract_entities import extract_entities
from DBpediaExtractor import DBpediaExtractor
import json

def get_enriched_entities(text):
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

	return json.dumps(return_dict)