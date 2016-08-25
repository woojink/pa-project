from .alchemyapi import AlchemyAPI

alchemyapi = AlchemyAPI()

class AlchemyExtractor(object):

    def __init__(self, myText):
        self.response = alchemyapi.entities("text", myText)

    def get_names(self):
        names = []
        for ent in self.response['entities']:
            if 'disambiguated' in ent:
                if ent['type']=='Person':
                    try:
                        names.append((ent['text'], ent['disambiguated']['dbpedia'], float(ent['relevance'])))
                    except:
                        pass
        return names

    def get_places(self):
        places = []
        tags = ['Country','Continent','City','GeographicFeature','StateOrCounty','Region']
        for ent in self.response['entities']:
            if ent['type'] in tags:
                try:
                    places.append((ent['text'], ent['disambiguated']['dbpedia'], float(ent['relevance'])))
                except:
                    pass
        return places
