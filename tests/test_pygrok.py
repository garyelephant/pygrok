from pygrok import grok_match

def test_one_pat():
    text = '1024'
    pat = '%{INT:test_int}'
    m = grok_match(text, pat)
    assert m['test_int'] == '1024', 'grok match failed:%s, %s' % (text, pat, )
    
    text = '1024'
    pat = '%{NUMBER:test_num}'
    m = grok_match(text, pat)
    assert m['test_num'] == '1024', 'grok match failed:%s, %s' % (text, pat, )

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

    text = '1989-11-04 05:33:02+0800'
    pat = '%{TIMESTAMP_ISO8601:ts}'
    m = grok_match(text, pat)
    assert m['ts'] == text.strip(), 'grok match failed:%s, %s' % (text, pat, )

    text = 'github'
    pat = '%{WORD}'
    m = grok_match(text, pat)
    assert m == {}, 'grok match failed:%s, %s' % (text, pat, )
    #you get nothing because variable name is not set, compare "%{WORD}" and "%{WORD:variable_name}"

    text = 'github'
    pat = '%{NUMBER:test_num}'
    m = grok_match(text, pat)
    assert m is None, 'grok match failed:%s, %s' % (text, pat, )
    #not match


def test_multiple_pats():
    text = 'gary 25 "never quit"'
    pat = '%{WORD:name} %{INT:age} %{QUOTEDSTRING:motto}'
    m = grok_match(text, pat)
    assert m['name'] == 'gary' and m['age'] == '25' and m['motto'] == '"never quit"', \
        'grok match failed:%s, %s' % (text, pat, )

    #variable names are not set
    text = 'gary 25 "never quit"'
    pat = '%{WORD} %{INT} %{QUOTEDSTRING}'
    m = grok_match(text, pat)
    assert m == {}, 'grok match failed:%s, %s' % (text, pat, )

    #"male" is not INT
    text = 'gary male "never quit"'
    pat = '%{WORD:name} %{INT:age} %{QUOTEDSTRING:motto}'
    m = grok_match(text, pat)
    assert m is None, 'grok match failed:%s, %s' % (text, pat, )

    #nginx log
    text = 'edge.v.iask.com.edge.sinastorage.com 14.18.243.65 6.032s - [21/Jul/2014:16:00:02 +0800]' \
        + ' "GET /edge.v.iask.com/125880034.hlv HTTP/1.0" 200 70528990 "-"' \
        + ' "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' \
        + ' Chrome/36.0.1985.125 Safari/537.36"'
    pat = '%{HOST:host} %{IP:client_ip} %{NUMBER:delay}s - \[%{DATA:time_stamp}\]' \
        + ' "%{WORD:verb} %{URIPATHPARAM:uri_path} HTTP/%{NUMBER:http_ver}" %{INT:http_status} %{INT:bytes} %{QS}' \
        + ' %{QS:client}'
    m = grok_match(text, pat)
    assert m['host'] == 'edge.v.iask.com.edge.sinastorage.com' and m['client_ip'] == '14.18.243.65' \
        and m['delay'] == '6.032' and m['time_stamp'] == '21/Jul/2014:16:00:02 +0800' and m['verb'] == 'GET' \
        and m['uri_path'] == '/edge.v.iask.com/125880034.hlv' and m['http_ver'] == '1.0' \
        and m['http_status'] == '200' and m['bytes'] == '70528990' \
        and m['client'] == '"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' \
        + ' Chrome/36.0.1985.125 Safari/537.36"', 'grok match failed:%s, %s' % (text, pat, )

    
def test_custom_pats():
    custom_pats = {'ID' : '%{WORD}-%{INT}'}
    text = 'Beijing-1104,gary 25 "never quit"'
    pat = '%{ID:user_id},%{WORD:name} %{INT:age} %{QUOTEDSTRING:motto}'
    m = grok_match(text, pat, custom_patterns = custom_pats)
    assert m['user_id'] == 'Beijing-1104' and m['name'] == 'gary' and m['age'] == '25' \
        and m['motto'] == '"never quit"', 'grok match failed:%s, %s' % (text, pat, )


def test_custom_pat_files():
    pats_dir = './test_patterns'
    text = 'Beijing-1104,gary 25 "never quit"'
    #pattern "ID" is defined in ./test_patterns/pats
    pat = '%{ID:user_id},%{WORD:name} %{INT:age} %{QUOTEDSTRING:motto}'
    m = grok_match(text, pat, custom_patterns_dir = pats_dir)
    assert m['user_id'] == 'Beijing-1104' and m['name'] == 'gary' and m['age'] == '25' \
        and m['motto'] == '"never quit"', 'grok match failed:%s, %s' % (text, pat, )

if __name__ == '__main__':
    test_one_pat()
    test_multiple_pats()
    test_custom_pats()
    test_custom_pat_files()

