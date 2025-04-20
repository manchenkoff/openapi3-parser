# OpenAPI Parser

![PyPI - Version](https://img.shields.io/pypi/v/openapi3-parser)
![PyPI - Downloads](https://img.shields.io/pypi/dm/openapi3-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openapi3-parser)
![PyPI - Format](https://img.shields.io/pypi/format/openapi3-parser)
![PyPI - License](https://img.shields.io/pypi/l/openapi3-parser)

A simple package to parse your OpenAPI 3 documents into Python object to work with.

Supported versions:

| Version | Status         |
| ------- | -------------- |
| 2.0     | Deprecated     |
| 3.0     | **Supported**  |
| 3.1     | In development |

## How to install

To install package run the following command

```
pip install openapi3-parser
```

## How to use

Example of parser usage

```
>>> from openapi_parser import parse
>>> content = parse('swagger.yml')
>>> print(content)
```

Get application servers

```python
from openapi_parser import parse

specification = parse('data/swagger.yml')

print("Application servers")

for server in specification.servers:
    print(f"{server.description} - {server.url}")

# Output
#
# >> Application servers
# >> production - https://users.app
# >> staging - http://stage.users.app
# >> development - http://users.local
```

Get list of application URLs

```python
from openapi_parser import parse

specification = parse('tests/data/swagger.yml')

urls = [x.url for x in specification.paths]

print(urls)

# Output
#
# >> ['/users', '/users/{uuid}']
```

Get operation with supported HTTP methods

```python
from openapi_parser import parse

specification = parse('tests/data/swagger.yml')

for path in specification.paths:
    supported_methods = ','.join([x.method.value for x in path.operations])

    print(f"Operation: {path.url}, methods: {supported_methods}")

# Output
#
# >> Operation: /users, methods: get,post
# >> Operation: /users/{uuid}, methods: get,put
```

### Convert OpenAPIv2 to OpenAPIv3

To convert OpenAPIv2 to OpenAPIv3, you can use the `prance` library. Install it using (after activate the virtual environment):

```bash
pip install prance
```

Then, you can use the following code:

```bash
prance convert openapi_v2.yaml openapi_v3.yaml
```

### Some Issues may exist in the generated OpenAPIv3 file

- `description` field in some places may convert as multi-line string (bad format). use this code to fix it:

```python
import yaml
import re

def process_descriptions(data):
    """
    Recursively process a dictionary/list to modify all 'description' fields to a single line.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'description' and isinstance(value, str):
                # Replace newlines, tabs, and multiple spaces with a single space
                cleaned_description = re.sub(r'\s+', ' ', value.strip())
                data[key] = cleaned_description
            else:
                process_descriptions(value)
    elif isinstance(data, list):
        for item in data:
            process_descriptions(item)

def modify_yaml_file(input_file, output_file):
    try:
        # Read the YAML file
        with open(input_file, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)

        # Process all description fields
        process_descriptions(yaml_data)

        # Write the modified data to a new YAML file
        with open(output_file, 'w', encoding='utf-8') as file:
            yaml.dump(yaml_data, file, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

        print(f"Modified YAML file saved as: {output_file}")
    except yaml.YAMLError as ye:
        print(f"YAML parsing error: {ye}")
    except Exception as e:
        print(f"Error processing YAML file: {e}")

# Example usage
input_yaml = 'openapi_v3.yaml'  # Replace with your input YAML file path
output_yaml = 'openapi_v3_output.yaml'  # Replace with desired output YAML file path
modify_yaml_file(input_yaml, output_yaml)
```

- `successfull_response` in `responses` section. this is not a standard field in OpenAPIv3. You can remove it. remove it and put `example` right after `schema` field in `responses` section.

```yaml
responses:
  "200":
    description: successful operation
    content:
      application/json:
        schema:
          $ref: "#/components/schemas/API_Entities_AccessRequester"
        example:
          id: 1
          username: ali
          name: ali karami
          state: active
          created_at: 2012-10-22T14:13:35Z
          access_level: 20
```

- `type:file` in `parameters` or `schema` section. this is not a standard field in OpenAPIv3. You can replace it with `type: string` and add `format: binary` field to it.

- `application/x-tar` in `content` section. this may be cause of error in some cases. you can remove it and replace it with `application/octet-stream` or other standard types for binary files.
