import os


def ss(s):
    if s is None:
        return 'None'
    return str(s)


class GptAgent:
    def __init__(self):
        self._api_key = None

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

    def print_status(self):
        print('Hhy Gpt Plugin status:')
        print('  ApiKey =', ss(self.api_key))


default = GptAgent()
