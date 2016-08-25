from SPARQLWrapper import SPARQLWrapper, JSON

class DBpediaExtractor(object):
    """
    Extractor for DBPedia

    Attributes:
        entity (str): URL friendly name for the entity
        url (str): The main resource URL
    """

    def __init__(self, url):
        """
        Args:
            url (str): Raw DBPedia URL
        """
        self.url = url
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    
    # Internal functions
    def get_ontology(self, endpoint, subject=False):
        """
        Returns ontology information for the given endpoint

        Args:
            endpoint (url): Endpoint for the desired ontology
        """
        r_list = []
        if subject:
            self.sparql.setQuery("""
                PREFIX ont: <http://dbpedia.org/ontology/>
                SELECT ?x
                WHERE {{ ?x ont:{endpoint} <{url}> }}
            """.format(url=self.url, endpoint=endpoint))
        else:
            self.sparql.setQuery("""
                PREFIX ont: <http://dbpedia.org/ontology/>
                SELECT ?x
                WHERE {{ <{url}> ont:{endpoint} ?x }}
            """.format(url=self.url, endpoint=endpoint))

        self.sparql.setReturnFormat(JSON)

        results = self.sparql.query().convert()
        for result in results["results"]["bindings"]:
            r_list.append(result["x"]["value"])

        return r_list

    def get_properties(self, endpoint, subject=False):
        """
        Returns properties for the given endpoint

        Args:
            endpoint (str): Endpoint for the desired properties
        """
        r_list = []
        if subject:
            self.sparql.setQuery("""
                PREFIX prop: <http://dbpedia.org/property/>
                SELECT ?x
                WHERE {{ ?x prop:{endpoint} <{url}> }}
            """.format(url=self.url, endpoint=endpoint))
        else:
            self.sparql.setQuery("""
                PREFIX prop: <http://dbpedia.org/property/>
                SELECT ?x
                WHERE {{ <{url}> prop:{endpoint} ?x }}
            """.format(url=self.url, endpoint=endpoint))

        self.sparql.setReturnFormat(JSON)

        results = self.sparql.query().convert()
        for result in results["results"]["bindings"]:
            r_list.append(result["x"]["value"])

        return r_list

    def get_geo(self, endpoint):
        r_list = []
        self.sparql.setQuery("""
            PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            SELECT ?x
            WHERE {{ <{url}> geo:{endpoint} ?x }}
        """.format(url=self.url, endpoint=endpoint))

        self.sparql.setReturnFormat(JSON)

        results = self.sparql.query().convert()
        for result in results["results"]["bindings"]:
            r_list.append(float(result["x"]["value"]))

        return r_list

    def get_misc(self, prefix, endpoint, lang=None):
        r_list = []

        if lang:
            self.sparql.setQuery("""
                PREFIX pf: <{prefix}>
                SELECT ?x
                WHERE {{
                    <{url}> pf:{endpoint} ?x
                    FILTER (lang(?x) = '{lang}')
                }}
            """.format(url=self.url, prefix=prefix, endpoint=endpoint, lang=lang))
        else:
            self.sparql.setQuery("""
                PREFIX pf: <{prefix}>
                SELECT ?x
                WHERE {{
                    <{url}> pf:{endpoint} ?x
                }}
            """.format(url=self.url, prefix=prefix, endpoint=endpoint))

        self.sparql.setReturnFormat(JSON)

        results = self.sparql.query().convert()
        for result in results["results"]["bindings"]:
            r_list.append(result["x"]["value"])

        return r_list

    # General
    def get_name(self):
        return self.get_properties("name")

    def get_label(self):
        # return str(self.g.preferredLabel(rdflib.term.URIRef(self.url), lang="en")[0][1])
        return self.get_misc("http://www.w3.org/2000/01/rdf-schema#", "label", lang="en")

    def get_comment(self):
        return self.get_misc("http://www.w3.org/2000/01/rdf-schema#", "comment", lang="en")

    # People
    def get_birthDate(self):
        return self.get_ontology("birthDate")

    def get_deathDate(self):
        return self.get_ontology("deathDate")

    def get_birthPlace(self):
        return self.get_ontology("birthPlace")

    def get_deathPlace(self):
        return self.get_ontology("deathPlace")

    def get_residence(self):
        return self.get_ontology("residence")

    def get_knownFor(self):
        return self.get_ontology("knownFor")

    def get_almaMater(self):
        return self.get_ontology("almaMater")

    def get_spouse(self):
        r_list = []
        spouse_list = self.get_ontology("spouse") + self.get_ontology("spouse", subject=True)
        for spouse_uri in spouse_list:
            # Filters through to exclude symmetrical (repeated) information
            if spouse_uri != self.url:
                r_list.append(spouse_uri)
        return r_list

    def get_description(self):
        return self.get_misc("http://purl.org/dc/elements/1.1/", "description", lang="en")

    def get_mp(self):
        return self.get_properties("mp", subject=True)

    # Locations
    def get_coordinates(self):
        """
        Returns:
            (lat, lng): Tuple of latitude, longitude coordinates
        """
        lat = self.get_geo('lat')
        lng = self.get_geo('long')
        return list(zip(lat, lng))

    def get_latitude(self):
        return self.get_geo('lat')

    def get_longitude(self):
        return self.get_geo('long')
