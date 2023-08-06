from .highlight import get_data_uri_snippet
import re
import fileinput
import os


def process_gift_file(file):
    base_dir = get_base_dir(file)
    lines = find_snippet_lines(file)

    replace_line_indices = []
    new_lines = []

    for line in lines:
        data_uri = get_data_uri_snippet(base_dir + "/" + line['snippet_file'])
        replace_line_indices.append(line['line_index'])
        new_lines.append('{}<img data-gift-snippet\\="{}" src\\="{}">\n'.format(line['whitespace'], line['snippet_file'], data_uri))

    replace_lines(file, replace_line_indices, new_lines)


def find_snippet_lines(file):
    assert os.path.exists(file)
    lines = []

    with open(file) as file_object:
        for line_index, line in enumerate(file_object):
            m = re.match('^( *)<img data-gift-snippet\\\="([^"]*?)"', line)

            if m:
                lines.append({
                    "line": line,
                    "line_index": line_index,
                    "whitespace": m.group(1),
                    "snippet_file": m.group(2)
                })

    return lines


def get_base_dir(file):
    return os.path.dirname(file)


def replace_lines(file, replace_line_indices=[], new_lines=[]):
    assert len(replace_line_indices) >= 1 and len(replace_line_indices) == len(new_lines)

    for line_index, line in enumerate(fileinput.input(file, inplace=True)):
        if line_index in replace_line_indices:
            index = replace_line_indices.index(line_index)
            print(new_lines[index], end='')
        else:
            print(line, end='')

