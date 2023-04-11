import json
import os
import re
import requests


API_URL = 'https://api.openai.com/v1'

BEST_TEXT_NN_PATTERNS = [ r'^text-davinci-[0-9]+$', 'text-davinci', 'text', 'davinci' ]
BEST_TEXT_NN_REGEXPS = [ re.compile(regexp) for regexp in BEST_TEXT_NN_PATTERNS ]


class GptError(Exception):
    pass

def error(msg):
    raise GptError(msg)


def ss(s):
    if s is None:
        return 'None'
    return str(s)

def best_text_nn(models):
    if not models:
        return None
    candidates = models[:]

    def try_regexp(candidates, regexp):
        filtered = [ m for m in candidates if regexp.match(m) ]
        if filtered:
            candidates[:] = filtered

    for regexp in BEST_TEXT_NN_REGEXPS:
        try_regexp(candidates, regexp)

    candidates.sort()
    return candidates[-1]


class GptAgent:
    def __init__(self):
        self._api_key = None
        self._models = []
        self._best_text_nn = None

    def query(self, endpoint, data=None):
        url = f"{API_URL}/{endpoint}"
        if self.api_key is None:
            error("Cannot call API without a key")
        headers = { "Authorization": f"Bearer {self.api_key}" }

        if data is None:
            response = requests.get(url, headers=headers)
        else:
            headers['Content-Type'] = 'application/json'
            json_text = json.dumps(data)
            response = requests.post(url, headers=headers, data=json_text)

        if response.status_code != 200:
            error(f"Invalid status code {response.status_code}")
        return json.loads(response.content)

    @staticmethod
    def get_api_key():
        value = os.environ.get('OPENAI_API_KEY', '').strip()
        return value or None

    def update_api_key(self):
        api_key = self.get_api_key()
        if api_key is not None:
            self._api_key = api_key
        return self._api_key

    @property
    def api_key(self):
        if self._api_key is None:
            self.update_api_key()
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def get_models(self):
        content = self.query('models')
        return [m['id'] for m in content['data']]

    def update_models(self):
        models = self.get_models()
        if models:
            self._models = models
        return self._models

    @property
    def models(self):
        if not self._models:
            self.update_models()
        return self._models

    def get_best_text_nn(self):
        return best_text_nn(self.models)

    def update_best_text_nn(self):
        best_text_nn = self.get_best_text_nn()
        if best_text_nn:
            self._best_text_nn = best_text_nn
        return self._best_text_nn

    @property
    def best_text_nn(self):
        if self._best_text_nn is None:
            self.update_best_text_nn()
        return self._best_text_nn

    @best_text_nn.setter
    def best_text_nn(self, value):
        if value not in models:
            error(f"The model {value} not in model list.")
        self._best_text_nn = value

    def print_status(self):
        print('Hhy Gpt Plugin status:')
        print('  ApiKey =', ss(self.api_key))
        print('  TextNN =', ss(self.best_text_nn))


default = GptAgent()
