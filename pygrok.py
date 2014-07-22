try:
    import regex as re
except ImportError as e:
    # If you import re, grok_match can't handle regular expression containing atomic group(?>)
    import re
import os

DEFAULT_PATTERNS_DIR = os.path.dirname(os.path.abspath(__file__)) + '/patterns'

predefined_patterns = {}
loaded_pre_patterns = False


class GrokError(Exception):
    pass
class PatternNotFound(GrokError):
    pass


def grok_match(text, pattern, custom_patterns = {}, custom_patterns_dir = None):
    """If text is matched with pattern, return variable names specified(%{pattern:variable name}) 
    in pattern and their corresponding values.If not matched, return None.
    custom patterns can be passed in by custom_patterns(pattern name, pattern regular expression pair)or patterns_dir.
    """
    patterns_dirs = [DEFAULT_PATTERNS_DIR]
    if patterns_dir is not None:
        patterns_dirs.append(patterns_dir)
    if loaded_pre_patterns is False:
        _reload_patterns(patterns_dirs)

    #attention: this may cause performance problems
    py_regex_pattern = pattern
    while True:
        #replace %{pattern_name:custom_name} with regex and regex group name
        py_regex_pattern = re.sub(r'%{(\w+):(\w+)}',
            lambda m: "(?P<" + m.group(2) + ">" + predefined_patterns[m.group(1)].regex_str + ")", py_regex_pattern)
        #replace %{pattern_name} with regex
        py_regex_pattern = re.sub(r'%{(\w+)}',
            lambda m: "(" + predefined_patterns[m.group(1)].regex_str + ")", py_regex_pattern)

        if re.search('%{\w+}', py_regex_pattern) is None:
            break

    match_obj = re.search(py_regex_pattern, text)
    return match_obj.groupdict() if match_obj is not None else None

def _wrap_pattern_name(pat_name):
    return '%{' + pat_name + '}'

def _reload_patterns(patterns_dirs):
    """
    """
    global predefined_patterns
    predefined_patterns = {}
    for dir in patterns_dirs:
        for f in os.listdir(dir):
            patterns = _load_patterns_from_file(os.path.join(dir, f))
            predefined_patterns.update(patterns)

    global loaded_pre_patterns
    loaded_pre_patterns = True


def _load_patterns_from_file(file):
    """
    """
    patterns = {}
    with open(file, 'r') as f:
        for l in f:
            l = l.strip()
            if l == '' or l.startswith('#'):
                continue

            sep = l.find(' ')
            pat_name = l[:sep]
            regex_str = l[sep:].strip()
            pat = Pattern(pat_name, regex_str)
            patterns[pat.pattern_name] = pat
    return patterns


class Pattern(object):
    """
    """
    def __init__(self, pattern_name, regex_str, sub_patterns = {}):
        self.pattern_name = pattern_name
        self.regex_str = regex_str
        self.sub_patterns = sub_patterns # sub_pattern name list

    def __str__(self):
        return '<Pattern:%s,  %s,  %s>' % (self.pattern_name, self.regex_str, self.sub_patterns)

