import csv
import os
import re
from inspect import getsourcefile
from os.path import abspath
from string import Template
from typing import List, Dict, Final, Optional, Any, Union

INT_MAP: Final = {
    0: "ZERO",
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
    6: "SIX",
    7: "SEVEN",
    8: "EIGHT",
    9: "NINE"
}

CSV_FILES: Final = {
    "application.csv",
    "audio.csv",
    "font.csv",
    "image.csv",
    "message.csv",
    "model.csv",
    "multipart.csv",
    "text.csv",
    "video.csv"
}

# Mime types supported by OpenAPI but not IANA (https://swagger.io/docs/specification/media-types/)
OPENAPI_SPECIFIC_MIME_TYPES: Final = {
    "*/*": "ANY",
    "application/*": "APPLICATION_ANY",
    "application/*+json": "JSON_ANY",
    "audio/*": "AUDIO_ANY",
    "font/*": "FONT_ANY",
    'image/*': "Image",
    "message/*": "MESSAGE_ANY",
    "model/*": "MODEL_ANY",
    "multipart": "MULTIPART_ANY",
    "text/*": "TEXT_ANY",
    "video/*": "VIDEO_ANY",
    'text/json': "JSON_TEXT",  # This isn't an OpenAPI specific mime type but it is needed as it already is in use
}

#  Existing mime types that we keep the ENUM names for for backwards compatibility
BACKWARDS_COMPATIBLE_MIME_TYPES: Final = {
    'application/json': "JSON",
    'application/problem+json': "JSON_PROBLEM",
    'application/xml': "XML",
    'application/x-www-form-urlencoded': "FORM",
    'multipart/form-data': "MULTIPART_FORM",
    'text/plain': "PLAIN_TEXT",
    'text/html': "HTML",
    'application/pdf': "PDF",
    'image/png': "PNG",
    'image/jpeg': "JPEG",
    'image/gif': "GIF",
    'image/svg+xml': "SVG",
    'image/avif': "AVIF",
    'image/bmp': "BMP",
    'image/webp': "WEBP",
    'application/octet-stream': "BINARY",
}


def _to_enum_name(template: str) -> str:
    """
    Converts the IANA template to an enum name
    :param template: IANA template value
    :return: parsed and formatted name
    """
    # Of course there is one outlier with a + at the end of it
    name_suffix: str = ""
    if template.endswith('+'):
        name_suffix = "_PLUS"

    name_parts: List[str] = [x for x in re.split(r'[+.\-/]+', template) if x]
    for i, part in enumerate(name_parts):
        part = re.sub(r"\*", "ANY", part)
        name_parts[i] = part

    enum_name: str = "_".join(name_parts)
    enum_name += name_suffix

    return enum_name.upper()


class MimeType:
    """
    Holds a representation of an IANA mime type
    """
    def __init__(self, template: str, name: Optional[str] = None):
        """
        Information about a mime type
        :param template: Template / header value
        """
        if name is None:
            name = _to_enum_name(template=template)
        self.enum_value = template
        self.enum_name = name


def get_mime_types_from_row(row: List[Any], mime_extension: str) -> Union[List[MimeType], None]:
    """
    Gets one or more MimeTypes (since OpenAPI allows wildcards with *) if the row is usable

    :param row: CSV row
    :param mime_extension: Name of the mime extension we are parsing rows for. i.e. "application"
    :return: MimeType or None if we will discard this row
    """
    name: str = row[0]
    template: str = row[1]

    mime_types: List[MimeType] = []

    if (
            name is not None
            and name != ''
            and "OBSOLETE" not in name
            and "DEPRECATED" not in name

    ):
        if template is None or template == '':
            template = f"{mime_extension}/{row[0]}"

        if template in BACKWARDS_COMPATIBLE_MIME_TYPES:
            name = BACKWARDS_COMPATIBLE_MIME_TYPES[template]
            mime_type = MimeType(template=template, name=name)
            return [mime_type]
        else:
            mime_type = MimeType(template=template)
            mime_types.append(mime_type)

        # Theoretically, * could be used anywhere but it seems most useful at
        # {mime_extension}/* and {mime_extension}/*+{mime_format} so we will add those
        if '+' in template:
            mime_format: str = template.split('+')[1]
            pattern_match_template = f"{mime_extension}/*+{mime_format}"
            mime_type_pattern_match = MimeType(template=pattern_match_template)
            mime_types.append(mime_type_pattern_match)

        return mime_types

    return None


def load_all_mime_types(cur_dir: str) -> Dict[str, MimeType]:
    """
    Loads mime types from all of our CSV files

    :param cur_dir: Current directory this script is located in
    :return:
    """
    mime_types_dict: Dict[str, MimeType] = {}

    for template, name in OPENAPI_SPECIFIC_MIME_TYPES.items():
        mime_type = MimeType(template=template, name=name)
        mime_types_dict[mime_type.enum_value.lower()] = mime_type

    for file in CSV_FILES:
        with open(f"{cur_dir}{file}", mode='r', encoding='utf-8') as csvfile:
            mime_extension: str = file.rstrip(".csv")
            reader: csv.reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for row in reader:
                mime_types: Union[List[MimeType], None] = get_mime_types_from_row(
                    row=row,
                    mime_extension=mime_extension,
                )
                if mime_types is not None:
                    for mime_type in mime_types:
                        if mime_types_dict.get(mime_type.enum_value.lower()) is None:
                            mime_types_dict[mime_type.enum_value.lower()] = mime_type
        csvfile.close()

    return mime_types_dict


def build_mime_types_file():
    """
    Loads application.csv and outputs a ContentType() class in
    src/openapi_parser/mime_types.py.

    Allows for easy update of ContentTypes when the IANA list changes

    :return: None
    """

    template_string = '''""" AUTO_GENERATED BY build_mime_types.py - DO NOT EDIT """

from enum import Enum, unique
    
    
@unique
class ContentType(Enum):\n'''

    cur_file: str = abspath(getsourcefile(lambda: 0))
    cur_dir: str = cur_file.rstrip("build_mime_types.py")

    mime_types_dict: Dict = {}

    mime_types: Dict[str, MimeType] = load_all_mime_types(cur_dir=cur_dir)

    i: int = 0
    for mime_type in mime_types.values():
        mime_types_dict[f"name_{i}"] = mime_type.enum_name
        mime_types_dict[f"value_{i}"] = mime_type.enum_value
        template_string += f"    $name_{i} = '$value_{i}'\n"
        i += 1

    template_string += "\n"
    template: Template = Template(template=template_string)
    class_file_path = os.path.join(cur_dir, "../src/openapi_parser/mime_types.py")

    with open(class_file_path, mode='w', encoding='utf-8') as class_file:
        class_file.write(template.safe_substitute(mime_types_dict))
    class_file.close()


if __name__ == "__main__":
    build_mime_types_file()
