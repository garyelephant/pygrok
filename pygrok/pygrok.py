try:
    import regex as re
except ImportError as e:
    # If you import re, grok_match can't handle regular expression containing atomic group(?>)
    import re
import os
import copy

DEFAULT_PATTERNS_DIRS = [os.path.dirname(os.path.abspath(__file__)) + '/patterns']

predefined_patterns = {}
loaded_pre_patterns = False


class GrokError(Exception):
    pass
class PatternNotFound(GrokError):
    pass


def grok_match(text, pattern, custom_patterns = {}, custom_patterns_dir = None):
    """If text is matched with pattern, return variable names specified(%{pattern:variable name}) 
    in pattern and their corresponding values.If not matched, return None.
    custom patterns can be passed in by custom_patterns(pattern name, pattern regular expression pair)or custom_patterns_dir.
    """
    if loaded_pre_patterns is False:
       global predefined_patterns
       predefined_patterns = _reload_patterns(DEFAULT_PATTERNS_DIRS)
       global loaded_pre_patterns
       loaded_pre_patterns = True

    all_patterns = copy.deepcopy(predefined_patterns)

    custom_pats = {}
    if custom_patterns_dir is not None:
        custom_pats = _reload_patterns([custom_patterns_dir])

    for pat_name, regex_str in custom_patterns.items():
        custom_pats[pat_name] = Pattern(pat_name, regex_str)

    if len(custom_pats) > 0:
        all_patterns.update(custom_pats)

    #attention: this may cause performance problems
    py_regex_pattern = pattern
    while True:
        #replace %{pattern_name:custom_name} with regex and regex group name
        py_regex_pattern = re.sub(r'%{(\w+):(\w+)}',
            lambda m: "(?P<" + m.group(2) + ">" + all_patterns[m.group(1)].regex_str + ")", py_regex_pattern)
        #replace %{pattern_name} with regex
        py_regex_pattern = re.sub(r'%{(\w+)}',
            lambda m: "(" + all_patterns[m.group(1)].regex_str + ")", py_regex_pattern)

        if re.search('%{\w+}', py_regex_pattern) is None:
            break

    match_obj = re.search(py_regex_pattern, text)
    return match_obj.groupdict() if match_obj is not None else None

def _wrap_pattern_name(pat_name):
    return '%{' + pat_name + '}'

def _reload_patterns(patterns_dirs):
    """
    """
    all_patterns = {}
    for dir in patterns_dirs:
        for f in os.listdir(dir):
            patterns = _load_patterns_from_file(os.path.join(dir, f))
            all_patterns.update(patterns)

    return all_patterns


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

