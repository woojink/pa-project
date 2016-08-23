from alchemyapi import AlchemyAPI

alchemyapi = AlchemyAPI()

class extract_entities(object):

    def __init__(self, myText):
        self.response = alchemyapi.entities("text", myText)

    def get_names(self):
        names = []
        for ent in self.response['entities']:
            if 'disambiguated' in ent:
                if ent['type']=='Person':
                    names.append([ent['text'], ent['disambiguated']['dbpedia']])
        return names

    def get_places(self):
        places = []
        tags = ['Country','Continent','City','StateOrCounty','Region']
        for ent in self.response['entities']:
            if ent['type'] in tags:
                places.append([ent['text'], ent['disambiguated']['dbpedia']])
        return places