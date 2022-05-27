import math
import datetime
import json
import time

from . import _errors


__all__ = ('Client',)


class Client:

    """
    Main point of contact with the service.

    :param session requests.Session:
        Used for making requests.
    :param str token:
        Authorization api key.
    """

    _base_uri = 'https://api.duffel.com'

    _version = 'beta'

    __slots__ = ('_session', '_token')

    def __init__(self, session, token):

        self._session = session

        self._token = token

    @property
    def _default_headers(self):

        return {
            'Authorization': f'Bearer {self._token}',
            'Duffel-Version': self._version
        }

    def _execute(self,
                 verb, path,
                 query = None, data = None, headers = None):

        uri = self._base_uri + path

        headers = self._default_headers | (headers or {})

        while True:
            response = self._session.request(
                verb, uri,
                params = query, json = data, headers = headers
            )
            if not response.status_code == 429:
                break
            dt_reset = datetime.datetime.strptime(
                response.headers['ratelimit-reset'],
                '%a, %d %b %Y %H:%M:%S %Z'
            )
            dt_now = datetime.datetime.utcnow()
            ellapse = (dt_reset - dt_now).total_seconds()
            if not ellapse > 0:
                continue
            time.sleep(ellapse)

        try:
            data = response.json()
        except json.JSONDecodeError:
            data = None

        if not response.status_code < 400:
            nrm =  response.status_code < 500
            cls = _errors.ApiError if nrm else _errors.HttpError
            raise cls(response, data)

        return data

    def request(self, verb, path, query = {}, body = None, **kwargs):

        """
        Execute a single request and get the date.

        :param str verb:
            HTTP method verb.
        :param str path:
            Api uri path.
        :param dict query:
            Request parameters.
        :param json body:
            Request data body.
        :param dict headers:
            Request additional headers.
        """

        if not body is None:
            body = {'data': body}

        data = self._execute(verb, path, query, body, **kwargs)

        return data['data']

    def iterate(self, verb, path, query = {}, body = None, **kwargs):

        """
        Same as :meth:`.request`, but also accepts `limit` and `after` in
        `query` for pagination. `limit` can be `None` for continuous pagination.
        """

        if not body is None:
            body = {'data': body}

        limit = query.get('limit')

        if limit is None:
            limit = math.inf

        after = None

        while True:
            query['limit'] = min(limit, 200)
            query['after'] = after
            data = self._execute(verb, path, query, body, **kwargs)
            meta = data['meta']
            data = data['data']
            yield from iter(data)
            after = meta['after']
            if after is None:
                break
            limit -= len(data)
            if limit > 0:
                continue
            break
