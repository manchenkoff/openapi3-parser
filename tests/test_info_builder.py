import pytest

from swagger_parser.builders import InfoBuilder
from swagger_parser.specification import Contact, Info, License

data_provider = (
    (
        {
            "title": "Sample Pet Store App",
            "version": "1.0.1"
        },
        Info(title="Sample Pet Store App", version="1.0.1"),
    ),
    (
        {
            "title": "Sample Pet Store App",
            "description": "This is a sample server for a pet store.",
            "termsOfService": "http://example.com/terms/",
            "contact": {
                "name": "API Support",
                "url": "http://www.example.com/support",
                "email": "support@example.com"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            },
            "version": "1.0.1"
        },
        Info(title="Sample Pet Store App",
             version="1.0.1",
             description="This is a sample server for a pet store.",
             terms_of_service="http://example.com/terms/",
             contact=Contact(name="API Support", url="http://www.example.com/support", email="support@example.com"),
             license=License(name="Apache 2.0", url="https://www.apache.org/licenses/LICENSE-2.0.html")),
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_build(data: dict, expected: Info):
    builder = InfoBuilder()

    assert expected == builder.build(data)
