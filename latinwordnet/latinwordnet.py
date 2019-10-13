"""A light-weight wrapper for the Latin WordNet API"""

import requests


class Semfields:
    def __init__(self, host, code=None, english=None, username=None, password=None):
        self.host = host
        self.code = code
        self.english = english
        self.json = None
        self.username = username
        self.password = password

    def get(self):
        auth = (self.username, self.password) if self.username and self.password else None
        if self.json is None:
            self.json = requests.get(
                f"{self.host}/api/semfields/{self.code}/?format=json", auth=auth,
                timeout=(10.0, 60.0)
            ).json()
        return self.json

    def search(self):
        auth = (self.username, self.password) if self.username and self.password else None

        if self.english:
            return requests.get(
                f"{self.host}/api/semfields?search={self.english}", auth=auth,
                timeout=(10.0, 60.0)
            ).json()["results"]
        else:
            return None

    def __iter__(self):
        return iter(self.get())

    @property
    def lemmas(self):
        auth = (self.username, self.password) if self.username and self.password else None

        return iter(
            requests.get(
                f"{self.host}/api/semfields/{self.code}/lemmas/?format=json", auth=auth,
                timeout=(10.0, 60.0)
            ).json()
        )

    @property
    def synsets(self):
        auth = (self.username, self.password) if self.username and self.password else None

        return iter(
            requests.get(
                f"{self.host}/api/semfields/{self.code}/synsets/?format=json", auth=auth,
                timeout=(10.0, 60.0)
            ).json()
        )


class Synsets:
    def __init__(self, host, pos=None, offset=None, gloss=None, username=None, password=None):
        self.host = host
        self.offset = f"{offset}/" if offset else ""
        self.pos = f"{pos}/" if pos else ""
        self.gloss = gloss
        self.json = None
        self.username = username
        self.password = password

    def get(self):
        auth = (self.username, self.password) if self.username and self.password else None

        if self.json is None:
            self.json = []

            results = requests.get(
                f"{self.host}/api/synsets/{self.pos}{self.offset}?format=json", auth=auth,
                timeout=(10.0, 60.0)
            ).json()
            if 'results' in results:
                self.json.extend(results["results"])

                while results["next"]:
                    results = requests.get(results["next"], auth=auth, timeout=(10.0, 60.0)).json()
                    self.json.extend(results["results"])
            else:
                self.json = [results,]
            return self.json

    def search(self):
        auth = (self.username, self.password) if self.username and self.password else None

        if self.gloss:
            return requests.get(
                f"{self.host}/api/synsets?search={self.gloss}", auth=auth,
                timeout=(10.0, 60.0)
            ).json()["results"]
        else:
            return None

    def __iter__(self):
        yield from self.get()

    @property
    def lemmas(self):
        auth = (self.username, self.password) if self.username and self.password else None

        return requests.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}lemmas/?format=json", auth=auth,
            timeout=(10.0, 60.0)
        ).json()

    @property
    def relations(self):
        auth = (self.username, self.password) if self.username and self.password else None

        return requests.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}relations/?format=json",
            auth=auth,
            timeout=(10.0, 60.0)
        ).json()["relations"]

    @property
    def sentiment(self):
        auth = (self.username, self.password) if self.username and self.password else None

        return requests.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}sentiment/?format=json",
            auth=auth,
            timeout=(10.0, 60.0)
        ).json()["sentiment"]


class Lemmas:
    def __init__(self, host, lemma=None, pos=None, morpho=None, uri=None, username=None, password=None):
        self.host = host
        self.lemma = f"{lemma}/" if lemma else "*/"
        self.pos = f"{pos}/" if pos else "*/"
        self.morpho = f"{morpho}/" if morpho else ""
        self.uri = uri
        self.json = None
        self.username = username
        self.password = password

    def get(self):
        auth = (self.username, self.password) if self.username and self.password else None

        if self.json is None:
            if self.uri is not None:
                self.json = requests.get(
                    f"{self.host}/api/uri/{self.uri}?format=json",
                    auth=auth,
                    timeout=(10.0, 60.0)
                ).json()

            else:
                self.json = requests.get(
                    f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}?format=json",
                    auth=auth,
                    timeout=(10.0, 60.0)
                ).json()
        return self.json

    def search(self):
        auth = (self.username, self.password) if self.username and self.password else None

        if self.lemma:
            results = self.json = requests.get(
                f"{self.host}/api/lemmas/?search={self.lemma.strip('/')}",
                auth=auth,
                timeout=(10.0, 60.0)
                ).json()
            yield from results["results"]

            while results["next"]:
                results = requests.get(results["next"], auth=auth, timeout=(10.0, 60.0)).json()
                yield from results["results"]

    def __iter__(self):
        return iter(self.get())

    @property
    def synsets(self):
        auth = (self.username, self.password) if self.username and self.password else None

        if self.uri is not None:
            return requests.get(
                f"{self.host}/api/uri/{self.uri}/synsets/?format=json",
                auth=auth,
                timeout=(10.0, 60.0)
            ).json()
        else:
            return requests.get(
                f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}synsets/?format=json",
                auth=auth,
                timeout=(10.0, 60.0)
            ).json()

    @property
    def relations(self):
        auth = (self.username, self.password) if self.username and self.password else None

        if self.uri is not None:
            return requests.get(
                f"{self.host}/api/uri/{self.uri}/relations/?format=json",
                auth=auth,
                timeout=(10.0, 60.0)
            ).json()
        else:
            return requests.get(
                f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}relations/?format=json",
                auth=auth,
                timeout=(10.0, 60.0)
            ).json()

    @property
    def synsets_relations(self):
        auth = (self.username, self.password) if self.username and self.password else None

        if self.uri is not None:
            return requests.get(
                f"{self.host}/api/uri/{self.uri}/synsets/relations/?format=json",
                auth=auth,
                timeout=(10.0, 60.0)
            ).json()

        return requests.get(
            f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}synsets/relations/?format=json",
            auth=auth,
            timeout=(10.0, 60.0)
        ).json()


class LatinWordNet:
    def __init__(self, host="https://latinwordnet.exeter.ac.uk", username=None, password=None):
        self.host = host.rstrip("/")
        self.username = username
        self.password = password

    def lemmatize(self, form: str, pos: str = None):
        auth = (self.username, self.password) if self.username and self.password else None
        results = requests.get(
            f"{self.host}/lemmatize/{form}/{f'{pos}/' if pos else ''}?format=json", auth=auth,
            timeout=(10.0, 60.0)
        )
        return iter(results.json()) if results else []

    def translate(self, language: str, form: str, pos: str = "*"):
        auth = (self.username, self.password) if self.username and self.password else None
        pos = f"{pos}/" if pos else ""
        results = requests.get(
            f"{self.host}/translate/{language}/{form}/{pos}?format=json", auth=auth,
            timeout=(10.0, 60.0)
        )
        return iter(results.json()) if results else []

    def sentiment_analysis(self, text, weighting=None, excluded=None):
        """

        :param text: The string to be analyzed.
        :param weighting: 'average', 'harmonic' or 'geometric'
        :param excluded: List of 3-uples consisting of ('lemma', 'morpho', 'uri') to be excluded from analysis
        :return: List of possible analyses with scores
        """
        auth = (self.username, self.password) if self.username and self.password else None
        data = {
                'text': text,
        }
        if weighting:
            data['weighting'] = weighting
        if excluded:
            data['excluded'] = excluded
        results = requests.post(f"{self.host}/sentiment/", data=data, auth=auth, verify=True)
        return results

    def lemmas(self, lemma=None, pos=None, morpho=None):
        return Lemmas(self.host, lemma, pos, morpho)

    def lemmas_by_uri(self, uri):
        return Lemmas(self.host, uri=uri)

    def synsets(self, pos: str = None, offset: str = None, gloss: str = None):
        return Synsets(self.host, pos, offset, gloss)

    def semfields(self, code: str = None, english: str = None):
        return Semfields(self.host, code, english)

    def index(self, pos=None, morpho=None):
        auth = (self.username, self.password) if self.username and self.password else None

        pos = f"{pos}/" if pos else "*/"
        morpho = f"{morpho}/" if morpho else ""

        results = requests.get(
            f"{self.host}/api/index/{pos}{morpho}/?format=json", auth=auth,
            timeout=(10.0, 60.0)
        ).json()
        yield from results["results"]

        while results["next"]:
            results = requests.get(results["next"], auth=auth, timeout=(10.0, 60.0)).json()
            yield from results["results"]


relation_types = {
    '!': 'antonyms',
    '@': 'hypernyms',
    '~': 'hyponyms',
    '#m': 'member-of',
    '#s': 'substance-of',
    '#p': 'part-of',
    '%m': 'has-member',
    '%s': 'has-substance',
    '%p': 'has-part',
    '=': 'attribute-of',
    '|': 'nearest',
    '+r': 'has-role',
    '-r': 'is-role-of',
    '*': 'entails',
    '>': 'causes',
    '^': 'also-see',
    '$': 'verb-group',
    '&': 'similar-to',
    '<': 'participle',
    '+c': 'composed-of',
    '-c': 'composes',
    '\\': 'derived-from',
    '/': 'related-to',
    }
