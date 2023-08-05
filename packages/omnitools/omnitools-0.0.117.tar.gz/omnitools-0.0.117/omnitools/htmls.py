import lxml.html
import html
import urllib.parse
from .encoding import try_utf8d


def html2xml(s):
    return lxml.html.fromstring(try_utf8d(s))


def str2html(s):
    return html.escape(s).replace(" ", "&nbsp;").replace("\n", "<br/>\n")


def encodeURIComponent(s):
    return urllib.parse.quote(s)


def decodeURIComponent(s):
    return urllib.parse.unquote(s)


