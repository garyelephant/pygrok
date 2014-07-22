from pygrok import grok_match

def test_one_pat():
    text = '1024'
    pat = '%{INT:test_int}'
    m = grok_match(text, pat)
    assert m['test_int'] == 1024, 'grok match failed:%s, %s' % (text, pat, )
    
    text = '1024'
    pat = '%{NUMBER:test_num}'
    m = grok_match(text, pat)
    assert m['test_num'] == 1024, 'grok match failed:%s, %s' % (text, pat, )

    text = 'garyelephant '
    pat = '%{WORD:name} '
    m = grok_match(text, pat)
    assert m['name'] == text.strip(), 'grok match failed:%s, %s' % (text, pat, )

    text = '192.168.1.1'
    pat = '%{IP:ip}'
    m = grok_match(text, pat)
    assert m['ip'] == text.strip(), 'grok match failed:%s, %s' % (text, pat, )

    text = 'github.com'
    pat = '%{HOST:website}'
    m = grok_match(text, pat)
    assert m['website'] == text.strip(), 'grok match failed:%s, %s' % (text, pat, )

    text = '1989-11-04 05:33:02 +0800'
    pat = '%{TIMESTAMP_ISO8601:ts}'
    m = grok_match(text, pat)
    assert m['ts'] == text.strip(), 'grok match failed:%s, %s' % (text, pat, )

    text = 'github'
    pat = '%{WORD}'
    m = grok_match(text, pat)
    assert m == {}, 'grok match failed:%s, %s' % (text, pat, )
    #you get nothing because variable name is not set, compare "%{WORD}" and "%{WORD:variable_name}"

    text = 'github'
    pat = '%{NUMBER}'
    m = grok_match(text, pat)
    assert m is None, 'grok match failed:%s, %s' % (text, pat, )
    #not match


def test_multiple_pats():
    text = 'gary 25 "never quit"'
    pat = '%{WORD:name} %{INT:age} %{QUOTEDSTRING:motto}'
    m = grok_match(text, pat)
    assert m['name'] == 'gary' and m['age'] == '25' and m['motto'] == 'never quit', 
        'grok match failed:%s, %s' % (text, pat, )


def test_custom_pats():
    pass


def test_custom_pat_files():
    pass

