from extract_entities import extract_entities
from DBpediaExtractor import DBpediaExtractor
import json

def get_enriched_entities(text):
	ee = extract_entities(text)
	return_dict = []

	place_list = ee.get_places()
	for (alchemy_label, uri, rel) in place_list:
		return_dict.append(get_place_dict(alchemy_label, uri, rel))

	name_list = ee.get_names()
	for (alchemy_label, uri, rel) in name_list:
		return_dict.append(get_name_dict(alchemy_label, uri, rel))

	return json.dumps(return_dict, indent=2, sort_keys=True)

def get_place_dict(alchemy_label, uri, rel):
	t_dict = {}
	dbe = DBpediaExtractor(uri)

	t_dict['uri'] = uri
	t_dict['type'] = 'place'
	t_dict['label'] = dbe.get_label()
	t_dict['relevance_score'] = rel
	t_dict['alchemy_label'] = alchemy_label

	t_dict['latitude'] = dbe.get_latitude()
	t_dict['longitude'] = dbe.get_longitude()
	t_dict['comment'] = dbe.get_comment()
	t_dict['coordinates'] = dbe.get_coordinates()

	return t_dict

def get_name_dict(alchemy_label, uri, rel, expand=True):
	t_dict = {}
	dbe = DBpediaExtractor(uri)

	t_dict['uri'] = uri
	t_dict['type'] = 'person'
	t_dict['label'] = dbe.get_label()

	if rel:
		t_dict['relevance_score'] = rel
	if alchemy_label:
		t_dict['alchemy_label'] = alchemy_label

	t_dict['alma_mater'] = expand_place(dbe.get_almaMater())

	t_dict['birth_date'] = dbe.get_birthDate()
	t_dict['birthplace_uri'] = expand_place(dbe.get_birthPlace_uri())
	t_dict['death_date'] = dbe.get_deathDate()	
	t_dict['deathplace_uri'] = expand_place(dbe.get_deathPlace_uri())
	t_dict['description'] = dbe.get_description()
	t_dict['known_for'] = dbe.get_knownFor()
	t_dict['residence'] = expand_place(dbe.get_residence())
	if expand:
		t_dict['spouse'] = expand_person(dbe.get_spouse())
	else:
		t_dict['spouse'] = dbe.get_spouse()

	return t_dict

def expand_place(place_list):
	temp_list = []
	if place_list:
		for subplace in place_list:
			if "http://dbpedia.org/resource/" in subplace:
				temp_list.append(get_place_dict(None, subplace, None))
			else:
				temp_list.append({'label': subplace})
	return temp_list

def expand_person(name_list):
	temp_list = []
	if name_list:
		for subperson in name_list:
			if "http://dbpedia.org/resource/" in subperson:
				temp_list.append(get_name_dict(None, subperson, None, expand=False))
			else:
				temp_list.append({'label': subperson})
	return temp_list