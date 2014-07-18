import re

PATTERN_SUFFIX = '.patt'
DEFAULT_PATTERNS_DIR = './patterns'

predefined_patterns = {
    'INT'      : r'(?:[+-]?(?:[0-9]+))',
    'WORD'     : r'\b\w+\b',
    'NOTSPACE' : r'\S+',
    'SPACE'    : r'\s*'
}

class GrokError(Exception):
    pass
class PatternNotFound(GrokError):
    pass


def grok_match(text, pattern, patterns_dir = DEFAULT_PATTERNS_DIR):
    """
    """
    _load_patterns(patterns_dir)
    py_regex_pattern = re.sub(r'%{(\w+):(\w+)}',
        lambda m: "(?P<" + m.group(2) + ">" + predefined_patterns[m.group(1)] + ")", pattern)

    return re.search(py_regex_pattern, text).groupdict()


def _load_patterns(patterns_dir):
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
    pass


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

        if len(pattern.sub_pattern) > 0 and pat_name != pattern_name:
            pattern.regex_str = _replace_sub_pattern_regex(pattern.regex_str, pat_name, pattern_temp.regex_str)
            pattern.sub_pattern.remove(pat_name)

        if len(pattern.sub_pattern) > 0:
            pat_name = pattern.sub_pattern[0] 
        else:
            return pattern.regex_str


def _replace_sub_pattern_regex(regex_str, sub_pattern_name, sub_pattern_regex_str):
    """
    replace sub pattern name with sub pattern regex
    """
    sub_pat_str = '%{' + sub_pattern_name + '}'
    return regex_str.replace(sub_pat_str, sub_pattern_regex_str)


class Pattern(object):
    """
    """
    def __init__(self, pattern_name, regex_str, sub_pattern):
        self.pattern_name = pattern_name
        self.regex_str = regex_str
        self.sub_pattern = sub_pattern # sub_pattern name list

