from openapi_parser import parse


def test_run_parser():
    parse('tests/data/swagger.yml')
