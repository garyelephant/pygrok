import re

PATTERN_SUFFIX = '.patt'
DEFAULT_PATTERNS_DIR = './patterns'

predefined_patterns = {
    'INT'      : r'(?:[+-]?(?:[0-9]+))',
    'WORD'     : r'\b\w+\b',
    'NOTSPACE' : r'\S+',
    'SPACE'    : r'\s*'
}

def grok_match(text, pattern, patterns_dir = DEFAULT_PATTERNS_DIR):
    _load_patterns(patterns_dir)
    py_regex_pattern = re.sub(r'%{(\w+):(\w+)}',
        lambda m: "(?P<" + m.group(2) + ">" + predefined_patterns[m.group(1)] + ")", pattern)

    return re.search(py_regex_pattern, text).groupdict()

def _load_patterns(patterns_dir):
    pass
