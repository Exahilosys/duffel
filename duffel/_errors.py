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


class ApiError(HttpError):

    __slots__ = ()

    def __init__(self, response, data):

        data = data['errors']

        super().__init__(response, data)

    def __str__(self):

        info = json.dumps(self._data, indent = 2)

        return info

    def __repr__(self):

        return f'{self.__class__.__name__}: {self.__str__()}'
