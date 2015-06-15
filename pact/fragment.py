__all__ = ['RequestFragment', 'ResponseFragment']


class Fragment(object):

    def __init__(self, spec):
        self.spec = spec
        self.headers = self.clean_headers(spec.get('headers', {}))

    @staticmethod
    def clean_headers(headers):
        return {
            key.lower(): ','.join([part.strip() for part in value.split(',')])
            for key, value in headers.items()}

    @staticmethod
    def clean_query(query):
        result = query.split('&')
        if not result[-1]:
            result = result[:-1]
        return sorted(result, key=lambda x: x.split('=')[0])

    def matches_exactly(self, actual, key):
        value = self.spec.get(key)
        if value is None:
            return True

        return value == actual.get(key)

    def matches_body(self, actual):
        return self.matches_exactly(actual, 'body')

    def matches_headers(self, actual):
        actual_headers = self.clean_headers(actual.get('headers', {}))
        for key, value in self.headers.items():
            if value != actual_headers[key]:
                return False

        return True

    def matches(self, actual):
        return all(m(actual) for m in self.matchers)


class RequestFragment(Fragment):

    def __init__(self, spec):
        super(RequestFragment, self).__init__(spec)
        self.method = spec.get('method', '').lower()
        self.query = self.clean_query(spec.get('query', ''))
        self.matchers = [
            self.matches_body, self.matches_path, self.matches_method,
            self.matches_query, self.matches_headers]

    def matches_path(self, actual):
        return self.matches_exactly(actual, 'path')

    def matches_method(self, actual):
        return self.method == actual['method'].lower()

    def matches_query(self, actual):
        if not self.query:
            return True

        return self.query == self.clean_query(actual['query'])


class ResponseFragment(Fragment):

    def __init__(self, spec):
        super(ResponseFragment, self).__init__(spec)
        self.matchers = [
            self.matches_body, self.matches_status, self.matches_headers]

    def matches_status(self, actual):
        return self.matches_exactly(actual, 'status')

    def matches_body(self, actual):
        body = self.spec.get('body')
        if not body:
            return True

        actual_body = actual.get('body', {})
        if body == actual_body:
            return True

        if not isinstance(body, dict):
            return False

        if self.matches_dict(body, actual_body):
            return True

        return False

    def matches_dict(self, expected, actual):
        for key, value in expected.items():
            actual_value = actual.get(key)
            if isinstance(value, dict):
                if not self.matches_dict(value, actual_value):
                    return False

            elif value != actual_value:
                return False

        return True
