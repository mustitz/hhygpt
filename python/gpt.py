import json
import os
import requests


API_URL = 'https://api.openai.com/v1'


class GptError(Exception):
    pass

def error(msg):
    raise GptError(msg)


def ss(s):
    if s is None:
        return 'None'
    return str(s)


class GptAgent:
    def __init__(self):
        self._api_key = None
        self._models = []

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

    def print_status(self):
        print('Hhy Gpt Plugin status:')
        print('  ApiKey =', ss(self.api_key))


default = GptAgent()
