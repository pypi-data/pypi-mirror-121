import requests
from apitorch.errors import ApitorchServerError, BadRequestError, InvalidApiKey, NotFoundError
from apitorch.utils import get_api_base_url, get_api_key
from urllib.parse import urljoin
from . import logger


def raise_on_bad_response(response):
    status_code = response.status_code

    if status_code == 400:
        logger.error(
            f'[error] Server returned 400 bad request, response: {response.json()}')
        raise BadRequestError('Server returned 400 bad request')

    if status_code == 401:
        logger.error(
            f'[error] Server returned 401, response: {response.json()}')
        raise InvalidApiKey(
            'Invalid API key. Repeat this call with a valid API key: https://www.apitorch.com/account')

    if status_code == 404:
        logger.error(
            f'[error] Server returned 404 not found, response: {response.json()}')
        raise NotFoundError('Server returned 404 not found')

    if status_code != 200:
        logger.error(
            f'[error] Server returned non-200, response: {response.json()}')
        raise ApitorchServerError(
            f'A server error prevented this request from executing. status: {status_code}')


class Client(object):
    def __init__(self):
        self.api_base_url = get_api_base_url()
        self.api_key = get_api_key()
        self.session = requests.Session()
        logger.debug(
            f'Instantiating API Client (base url: {self.api_base_url})')

    def get(self, path):
        url = urljoin(self.api_base_url, path)
        response = self.session.get(url, auth=self.auth())
        raise_on_bad_response(response)
        return response

    def post(self, path, data):
        url = urljoin(self.api_base_url, path)
        response = self.session.post(url, json=data, auth=self.auth())
        raise_on_bad_response(response)
        return response

    def delete(self, path):
        url = urljoin(self.api_base_url, path)
        response = self.session.delete(url, auth=self.auth())
        raise_on_bad_response(response)
        return response

    def post_with_file(self, path, filepath):
        url = urljoin(self.api_base_url, path)
        try:
            files = {'image': open(filepath, 'rb')}
        except FileNotFoundError:
            raise BadRequestError(f"File not found: {filepath}")

        response = self.session.post(url, files=files, auth=self.auth())
        raise_on_bad_response(response)
        return response

    def auth(self):
        return (self.api_key, '')
