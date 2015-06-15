"""Read in specifications from the pact-specifications repository."""
import json
from os import walk, path

import pytest
from pact import Fragment


def get_path():
    return '/home/eric/github/python-pact/pact-specification/testcases'


def get_request_body_path():
    return get_path() + '/request/body/'


def get_spec_files(filepath):
    for (dirpath, _, filenames) in walk(filepath):
        for filename in filenames:
            if filename.endswith('.json'):
                yield path.join(dirpath, filename)


def get_spec_from_file(filename):
    with open(filename, 'r') as specfile:
        spec = json.load(specfile)
    return spec


@pytest.mark.parametrize(
    'spec', [get_spec_from_file(filename) for filename in
             get_spec_files(get_request_body_path())])
def test_request_body_spec(spec):
    fragment = Fragment(spec['expected'])
    should_match = spec['match']
    actual = spec['actual']
    name = spec['comment']

    assert fragment.matches(actual) is should_match, name


if __name__ == '__main__':
    print([f for f in get_spec_files(get_request_body_path())])
