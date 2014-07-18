import re
import os

PATTERN_SUFFIX = '.patt'
DEFAULT_PATTERNS_DIR = './patterns'

predefined_patterns = {}
loaded_pre_patterns = False
"""
predefined_patterns = {
    'INT'      : r'(?:[+-]?(?:[0-9]+))',
    'WORD'     : r'\b\w+\b',
    'NOTSPACE' : r'\S+',
    'SPACE'    : r'\s*'
}
"""


class GrokError(Exception):
    pass
class PatternNotFound(GrokError):
    pass


def grok_match(text, pattern, patterns_dir = DEFAULT_PATTERNS_DIR):
    """
    """
    if loaded_pre_patterns is False:
        _reload_patterns(patterns_dir)

    #attention: this may cause performance problems
    while True:
        py_regex_pattern = re.sub(r'%{(\w+):(\w+)}',
            lambda m: "(?P<" + m.group(2) + ">" + predefined_patterns[m.group(1)].regex_str + ")", pattern)
        if re.search('%{\w+}', py_regex_pattern) is None:
            break

    return re.search(py_regex_pattern, text).groupdict()

def _wrap_pattern_name(pat_name):
    return '%{' + pat_name + '}'

def _reload_patterns(patterns_dir):
    """
    BASE10NUM (?<![0-9.+-])(?>[+-]?(?:(?:[0-9]+(?:\.[0-9]+)?)|(?:\.[0-9]+)))
    NUMBER (?:%{BASE10NUM})

         BASE10NUM
           /
          /
       NUMBER
    
    PATH (?:%{UNIXPATH}|%{WINPATH})
    UNIXPATH (?>/(?>[\w_%!$@:.,-]+|\\.)*)+
    TTY (?:/dev/(pts|tty([pq])?)(\w+)?/?(?:[0-9]+))
    WINPATH (?>[A-Za-z]+:|\\)(?:\\[^\\?*]*)+
    URIPROTO [A-Za-z]+(\+[A-Za-z+]+)?
    URIHOST %{IPORHOST}(?::%{POSINT:port})?
    URIPATH (?:/[A-Za-z0-9$.+!*'(){},~:;=@#%_\-]*)+
    URIPARAM \?[A-Za-z0-9$.+!*'|(){},~@#%&/=:;_?\-\[\]]*
    URIPATHPARAM %{URIPATH}(?:%{URIPARAM})?
    URI %{URIPROTO}://(?:%{USER}(?::[^@]*)?@)?(?:%{URIHOST})?(?:%{URIPATHPARAM})?

    UNIXPATH   WINPATH
       \          /
        \        /
         \      /
          \    /
           PATH
                                      IPV6    IPV4
                                        \     /
                                         \   /
                                          \ /
                              HOSTNAME    IP
                                  \       /
                                   \     /
                                    \   /
             USERNAME              IPORHOST  POSINT
               \                       \      /
                \                       \    / 
                 \                       \  /
                USER      URIPROTO      URIHOST        URIPATH     URIPARAM
                  \          \             \              \          /
                   \          \             \              \        /
                    \          \             \              \      /
                     \          \             \           URIPATHPARAM
                      \          \             \              /
                       \          \             \            /
                        \          \             \          /
                         \----------\------------/---------/
                                         \/
                                       URI
    
    """
    global predefined_patterns
    predefined_patterns = {}
    for f in os.listdir(patterns_dir):
        patterns = _load_patterns_from_file(f)
        predefined_patterns.update(patterns)

    global loaded_pre_patterns
    loaded_pre_patterns = True


def _load_patterns_from_file(file):
    """
    """
    patterns = {}
    with open(file, 'r') as f:
        for l in f:
            pat_regex = l.split()
            pat = Pattern(pat_regex[0], pat_regex[1])
            pat.sub_patterns = re.findall(_wrap_pattern_name(pat.pattern_name), pat.regex_str)
            patterns[pat.pattern_name] = pat
    return patterns


def _extract_pattern_names(regex_str):
    """
    """
    re.findall(, regex_str)


def _build_pattern_regex(pattern_name, regex_map):
    """
    """
    pattern = None
    pat_name = pattern_name
    while True:
        try:
            pattern_temp = regex_map[pat_name]
        except KeyError as e:
            raise PatternNotFound

        if pat_name == pattern_name:
            pattern = pattern_temp

        if len(pattern.sub_patterns) > 0 and pat_name != pattern_name:
            pattern.regex_str = _replace_sub_pattern_regex(pattern.regex_str, pat_name, pattern_temp.regex_str)
            pattern.sub_patterns.remove(pat_name)

        if len(pattern.sub_patterns) > 0:
            pat_name = pattern.sub_patterns[0] 
        else:
            return pattern.regex_str


def _replace_sub_pattern_regex(regex_str, sub_pattern_name, sub_pattern_regex_str):
    """
    replace sub pattern name with sub pattern regex
    """
    return regex_str.replace(_wrap_pattern_name(sub_pattern_name), sub_pattern_regex_str)


class Pattern(object):
    """
    """
    def __init__(self, pattern_name, regex_str, sub_patterns = {}):
        self.pattern_name = pattern_name
        self.regex_str = regex_str
        self.sub_patterns = sub_patterns # sub_pattern name list

