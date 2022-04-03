
import hashlib

def is_external_link(href):
    schemas = ['http:', 'https:', 'mailto:']
    for schema in schemas:
        if href.startswith(schema):
            return True
    return False

def is_anchor_link(href):
    return href.startswith('#')

def is_markdown_link(href):
    return '.html' in href

def hash_to_md5(string):
    return hashlib.md5(string.encode()).hexdigest()
