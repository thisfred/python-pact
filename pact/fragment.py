__all__ = ['Fragment']


class Fragment(object):

    def __init__(self, spec):
        self.spec = spec

    def matches(self, actual):
        if self.spec == actual:
            return True

        return False
