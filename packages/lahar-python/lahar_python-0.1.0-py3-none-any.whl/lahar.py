import requests
from enum import Enum


class LeadStage(Enum):
    LEAD = 1
    OPORTUNITY = 2
    CLIENT = 3


class Client:

    BASE_URL = "http://app.lahar.com.br/api"

    def __init__(self, token, event="integration"):
        self.token = token
        self.event = event

    def create_lead(self, data=dict()):
        self._prepare_data(data)

        if 'nome_formulario' not in data.keys():
            data.update(self.get_event_hash())

        self.post_with_body('/conversions', data)

    def change_lead_status(self, data=dict(), stage=LeadStage.LEAD):
        data = self._prepare_data(data)
        data.update(dict(estagio_lead=stage.value))
        self.put_with_body("/leads", data)

    def post_with_body(self, endpoint, data):
        requests.post(self.get_url(endpoint), data=data)

    def put_with_body(self, endpoint, data):
        requests.put(self.get_url(endpoint), data=data, headers={
                     'Content-Type': 'application/json'})

    def get_token_hash(self):
        return dict(token_api_lahar=self.token)

    def get_event_hash(self):
        return dict(nome_formulario=self.event)

    def get_url(self, endpoint):
        endpoint = self._add_trailing_slash(endpoint)
        return f'{self.BASE_URL}{endpoint}'

    def _prepare_data(self, data):
        data.update(self.get_token_hash())
        return data

    @staticmethod
    def _add_trailing_slash(endpoint=''):
        if not endpoint.startswith('/'):
            return f'/{endpoint}'
        return endpoint
