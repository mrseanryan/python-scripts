# python 3
"""
build-index.py

Creates a index.html at the given directory, listing its contents.

USAGE: build-index.py <path to directory>
"""
import datetime
import getopt
from os import walk
import os
import sys

TITLE = "TO READ"


def create_styling_html():
    return """
<style>
div {padding:5px;}
</style>
    """


def create_head():
    # disable browser caching
    html_no_cache = """
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<meta http-equiv="Pragma" content="no-cache" />
<meta http-equiv="Expires" content="0" />
    """ + create_styling_html() + create_tag("title", TITLE)
    return create_tag("head", html_no_cache)


def create_opening_tag(tag, attributes=""):
    return f"<{tag} {attributes}>"


def create_closing_tag(tag):
    return f"</{tag}>"


def create_tag(tag, content, attributes=""):
    return f"<{tag} {attributes}>{content}</{tag}>"


def create_html_for_filename(filename):
    link = create_tag(f"a", filename, f"href='{filename}'")
    return create_tag("div", link)


def write_html_tags_to_file(tags, filepath):
    html = os.linesep.join(tags)
    text_file = open(filepath, "w")
    text_file.write(html)
    text_file.close()


def create_today():
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    return create_tag("div", f"updated on {today}")


def build_index(dir_path):
    (_, _, filenames) = next(os.walk(dir_path))

    filenames = filter(lambda f: not f.endswith(
        ".py") and not f.endswith(
        ".bat") and not f.endswith(
        ".sh") and not f == "index.html", filenames)

    html_tags = []

    html_tags.append(create_opening_tag("html"))
    html_tags.append(create_head())
    html_tags.append(create_opening_tag("body"))

    html_tags.append(create_tag("div", TITLE))

    html_tags.append(create_today())

    html_tags.append(create_opening_tag(
        "div", "style='display:flex; flex-direction:column;'"))

    for filename in filenames:
        print(f"Adding file {filename}")
        html_tags.append(create_html_for_filename(filename))

    html_tags.append(create_closing_tag("div"))

    html_tags.append(create_closing_tag("body"))
    html_tags.append(create_closing_tag("html"))

    html_file_out = os.path.join(dir_path, "index.html")
    print(f"Writing out HTML to {html_file_out}")
    write_html_tags_to_file(html_tags, html_file_out)


def get_usage():
    return 'build-index.py -d <path to directory>'

# main - processes cli args


def main(argv):
    path_to_dir = ''

    if (len(sys.argv) != 3):
        print(get_usage())
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hd:")
    except getopt.GetoptError:
        print(get_usage())
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(get_usage())
            sys.exit()
        elif opt in ("-d", "--dir"):
            path_to_dir = arg
    build_index(path_to_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
