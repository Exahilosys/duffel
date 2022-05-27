import json


__all__ = ('HttpError', 'ApiError')


class BaseError(Exception):

    __slots__ = ()


class HttpError(BaseError):

    __slots__ = ('_response', '_data')

    def __init__(self, response, data = None, message = None):

        self._response = response
        self._data = data

        if message is None:
            message = data

        super().__init__(data)

    @property
    def response(self):

        return self._response

    @property
    def data(self):

        return self._data


class ApiError(BaseError):

    __slots__ = ()

    def __init__(self, response, data):

        data = data['errors']

        message = json.dumps(data, indent = 4)

        super().__init__(response, data, message)
