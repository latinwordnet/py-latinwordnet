"""A light-weight wrapper for the Latin WordNet API"""
import requests


class Semfields:
    def __init__(self, host, code=None, english=None, token=None):
        self.host = host
        self.code = code
        self.english = english
        self.json = None
        self.token = token

    def get(self):
        if self.json is None:
            self.json = requests.get(
                f"{self.host}/api/semfields/{self.code}/?format=json", auth=self.token,
                timeout=(10.0, 60.0)
            ).json()['results']
        return self.json

    def search(self):
        if self.english:
            return requests.get(
                f"{self.host}/api/semfields?search={self.english}", auth=self.token,
                timeout=(10.0, 60.0)
            ).json()["results"]
        else:
            return None

    def __iter__(self):
        return iter(self.get())

    @property
    def lemmas(self):
        
        return iter(
            requests.get(
                f"{self.host}/api/semfields/{self.code}/lemmas/?format=json", auth=self.token,
                timeout=(10.0, 60.0)
            ).json()
        )

    @property
    def synsets(self):
        
        return iter(
            requests.get(
                f"{self.host}/api/semfields/{self.code}/synsets/?format=json", auth=self.token,
                timeout=(10.0, 60.0)
            ).json()
        )


class Synsets:
    def __init__(self, host, pos=None, offset=None, gloss=None, token=None):
        self.host = host
        self.offset = f"{offset}/" if offset else ""
        self.pos = f"{pos}/" if pos else ""
        self.gloss = gloss
        self.json = None
        self.token = token

    def get(self):
        if self.json is None:
            self.json = []
            results = requests.get(
                f"{self.host}/api/synsets/{self.pos}{self.offset}?format=json", auth=self.token,
                timeout=(10.0, 60.0)
            ).json()
            if 'results' in results:
                self.json.extend(results["results"])
                while results["next"]:
                    results = requests.get(results["next"], auth=self.token, timeout=(10.0, 60.0)).json()
                    self.json.extend(results["results"])
            else:
                self.json = [results,]
            return self.json

    def search(self):
        if self.gloss:
            return requests.get(
                f"{self.host}/api/synsets?search={self.gloss}", auth=self.token,
                timeout=(10.0, 60.0)
            ).json()["results"]
        else:
            return None

    def __iter__(self):
        yield from self.get()

    @property
    def lemmas(self):
        return requests.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}lemmas/?format=json", auth=self.token,
            timeout=(10.0, 60.0)
        ).json()


    @property
    def relations(self):
        
        return requests.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}relations/?format=json",
            auth=self.token,
            timeout=(10.0, 60.0)
        ).json()["relations"]

    @property
    def sentiment(self):
        return requests.get(
            f"{self.host}/api/synsets/{self.pos}{self.offset}sentiment/?format=json",
            auth=self.token,
            timeout=(10.0, 60.0)
        ).json()["sentiment"]


class Lemmas:
    def __init__(self, host, lemma=None, pos=None, morpho=None, uri=None, token=None):
        self.host = host
        self.lemma = f"{lemma}/" if lemma else "*/"
        self.pos = f"{pos}/" if pos else "*/"
        self.morpho = f"{morpho}/" if morpho else ""
        self.uri = uri
        self.json = None
        self.token = token

    def get(self):
        if self.json is None:
            if self.uri is not None:
                self.json = requests.get(
                    f"{self.host}/api/uri/{self.uri}?format=json",
                    auth=self.token,
                    timeout=(10.0, 60.0)
                ).json()
            else:
                self.json = []
                results = requests.get(
                    f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}?format=json", auth=self.token,
                    timeout=(10.0, 60.0)
                ).json()
                if 'results' in results:
                    self.json.extend(results["results"])
                    while results["next"]:
                        results = requests.get(results["next"], auth=self.token, timeout=(10.0, 60.0)).json()
                        self.json.extend(results["results"])
                else:
                    self.json = [results, ]
        return self.json

    def search(self):
        if self.lemma:
            results = self.json = requests.get(
                f"{self.host}/api/lemmas/?search={self.lemma.strip('/')}",
                auth=self.token,
                timeout=(10.0, 60.0)
                ).json()
            yield from results["results"]
            while results["next"]:
                results = requests.get(results["next"], auth=self.token, timeout=(10.0, 60.0)).json()
                yield from results["results"]

    def __iter__(self):
        return iter(self.get())

    @property
    def synsets(self):
        if self.uri is not None:
            return requests.get(
                f"{self.host}/api/uri/{self.uri}/synsets/?format=json",
                auth=self.token,
                timeout=(10.0, 60.0)
            ).json()
        else:
            return requests.get(
                f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}synsets/?format=json",
                auth=self.token,
                timeout=(10.0, 60.0)
            ).json()

    @property
    def relations(self):
        if self.uri is not None:
            return requests.get(
                f"{self.host}/api/uri/{self.uri}/relations/?format=json",
                auth=self.token,
                timeout=(10.0, 60.0)
            ).json()
        else:
            return requests.get(
                f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}relations/?format=json",
                auth=self.token,
                timeout=(10.0, 60.0)
            ).json()

    @property
    def synsets_relations(self):
        if self.uri is not None:
            return requests.get(
                f"{self.host}/api/uri/{self.uri}/synsets/relations/?format=json",
                auth=self.token,
                timeout=(10.0, 60.0)
            ).json()
        return requests.get(
            f"{self.host}/api/lemmas/{self.lemma}{self.pos}{self.morpho}synsets/relations/?format=json",
            auth=self.token,
            timeout=(10.0, 60.0)
        ).json()


class LatinWordNet:
    def __init__(self, host="https://latinwordnet.exeter.ac.uk", token=None):
        self.host = host.rstrip("/")
        self.token = token

    def lemmatize(self, form: str, pos: str = None):
        results = requests.get(
            f"{self.host}/lemmatize/{form}/{f'{pos}/' if pos else ''}?format=json", auth=self.token,
            timeout=(10.0, 60.0)
        )
        return iter(results.json()) if results else []

    def translate(self, language: str, form: str, pos: str = "*"):
        pos = f"{pos}/" if pos else ""
        results = requests.get(
            f"{self.host}/translate/{language}/{form}/{pos}?format=json", auth=self.token,
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
        
        data = {
                'text': text,
        }
        if weighting:
            data['weighting'] = weighting
        if excluded:
            data['excluded'] = excluded
        results = requests.post(f"{self.host}/sentiment/", data=data, auth=self.token, verify=True)
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
        pos = f"{pos}/" if pos else "*/"
        morpho = f"{morpho}/" if morpho else ""
        results = requests.get(
            f"{self.host}/api/index/{pos}{morpho}/?format=json", auth=self.token,
            timeout=(10.0, 60.0)
        ).json()
        yield from results["results"]
        while results["next"]:
            results = requests.get(results["next"], auth=self.token, timeout=(10.0, 60.0)).json()
            yield from results["results"]

    def get_token(self):
        return self.token

    def set_token(self, t):
        self.token = t

    def obtain_auth_token(self, username, password):
        results = requests.post(f"{self.host}/api-token-auth/", data={'username': username, 'password': password},
                             verify=True)
        if results:
            return results.json()['token']


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
