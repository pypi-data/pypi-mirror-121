import urllib.request
import urllib.parse
import re

class NoRedirection(urllib.request.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
    https_response = http_response

def replace(url, your_key):
    """
    change simple format your affiliate link.
    https://affiliate.amazon.co.jp/help/node/topic/GP38PJ6EUR6PFBEC
    """
    target_url = get_target_url(url)
    params = { 'language':'ja_JP','tag': your_key }
    url_parts = list(urllib.parse.urlparse(target_url))
    url_parts[4] = urllib.parse.urlencode(params) # 4 is query

    return urllib.parse.urlunparse(url_parts)

def get_asin_from_url(url):
    '''
    get asin code.
    Amazon Standard Identification Number: ASIN
    '''
    url = url.lower()
    amazon_r = re.compile(r'^https?://(?:[^.]+\.)?(?:images-)?amazon\.(?:com|ca|co\.uk|de|co\.jp|jp|fr|cn)(/.+)$')
    amazon = amazon_r.match(url)
    if not amazon:
      return None
    pattern = r'(?:[/dp/]|$)([A-Z0-9]{10})'
    asin_r = re.compile(pattern, re.VERBOSE)
    asin = asin_r.search(url)
    if asin:
      return asin.group(1).upper()
    else:
      return None

def get_target_url(url):
    req = urllib.request.Request(url, method="HEAD")
    opener = urllib.request.build_opener(NoRedirection)
    resp = opener.open(req)
    if resp.status == 301:
      url = resp.headers['Location']
    else:
      url = resp.url
    return url
