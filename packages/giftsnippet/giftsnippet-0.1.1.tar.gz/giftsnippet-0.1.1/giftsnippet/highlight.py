import base64
import os
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name


def get_data_uri_snippet(file, lexer='python', gift_escape=True):
    snippet = load_snippet(file)
    image = highlight(snippet, get_lexer_by_name(lexer), get_formatter_by_name('png'))
    data_uri = 'data:image/png;base64,' + base64.b64encode(image).decode("utf-8")

    # : and = must be escaped inside the question content for gift and moodle import
    if gift_escape:
        data_uri = data_uri.replace(":", "\\:")
        data_uri = data_uri.replace("=", "\\=")

    return data_uri


def load_snippet(file):
    assert os.path.exists(file)
    with open(file) as file_object:
        return file_object.read()
