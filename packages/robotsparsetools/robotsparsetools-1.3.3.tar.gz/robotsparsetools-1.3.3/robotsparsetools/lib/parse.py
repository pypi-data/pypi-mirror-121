from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from .error import NotFoundError, NotURLError
from urllib.parse import urljoin, urlparse
import re
import os

class Parse(dict):
    def __init__(self, url=None, requests=False, text=None, **kwargs):
        """
        Parse robots.txt and returns a Parse instance.

        >>> p = Parse("https://www.google.com/")
        >>> {'*': ~~}
        >>> Returns the Parse type of description for each User-Agent.
        """
        if not isinstance(url, str) and not text:
            raise TypeError("__init__() missing 1 required positional argument: 'url'")
        if not text:
            if not url.endswith("robots.txt"):
                url = urljoin(url, "/robots.txt")
            self.home = _get_home(url)
            text = request(url, use_requests=requests, option=kwargs)
        data = parse(text.splitlines())
        super().__init__(**data)

    def Allow(self, useragent="*"):
        """
        Get allow list from robots.txt.
        If there was nothing, return None.
        """
        data = self.get(useragent)
        if data:
            return data.get("allow")

    def Disallow(self, useragent="*"):
        """
        Get disallow list from robots.txt.
        If there was nothing, return None
        """
        data = self.get(useragent)
        if data:
            return data.get("disallow")

    def delay(self, useragent="*"):
        data = self.get(useragent)
        if data:
            try:
                return data.get("crawl-delay")
            except (TypeError, ValueError):
                return None

    def _query_rep(self, url):
        string = url.split("?")
        return r"\?".join(string)

    def can_crawl(self, url, useragent="*"):
        """
        Returns True if crawl is allowed, False otherwise.
        """
        if not isinstance(url, str):
            raise ValueError("'url' argument must give a string type")
        if not url.startswith(self.home):
            return True
        disallow = self.Disallow(useragent)
        allow = self.Allow(useragent)
        if allow:
            for a in map(self._query_rep, allow):
                a = a.replace("*", ".*")
                if a[-1] in {"/", "*", "$"}:
                    pattern = re.compile(rf"^{urljoin(self.home, a)}.*")
                elif a[-1] == "?":
                    pattern = re.compile(r"^{}\?".format(urljoin(self.home, a.rstrip(r"\?"))))
                else:
                    pattern = re.compile(rf"^{urljoin(self.home, a)}$")
                if pattern.match(url):
                    return True
        if disallow:
            for d in map(self._query_rep, disallow):
                d = d.replace("*", ".*")
                if d[-1] in {"/", "*", "$"}:
                    pattern = re.compile(rf"^{urljoin(self.home, d)}.*")
                elif d[-1] == "?":
                    pattern = re.compile(r"^{}\?".format(urljoin(self.home, d.rstrip(r"\?"))))
                else:
                    pattern = re.compile(rf"^{urljoin(self.home, d)}$")
                if pattern.match(url):
                    return False
        return True
                
def Read(text):
    if os.path.isfile(text):
        with open(text, "r") as f:
            return Parse(text=f.read())
    else:
        return Parse(text=text)

def request(url, *, use_requests=False, option={}):
    """
    Send a request to robots.txt.
    If use_requests argument is True, use requests module at the time of request
    """
    try:
        if use_requests:
            import requests
            r = requests.get(url, **option)
            if 400 <= r.status_code:
                raise NotFoundError(f"Status code {r.status_code} was returned")
            else:
                result = r.text
        else:
            with urlopen(url, **option) as r:
                result = r.read().decode()
        return result
    except (URLError, HTTPError) as e:
        raise NotFoundError(e)

def parse(info):
    """
    Parse robots.txt
    """
    datas = {}
    for i in info:
        if not i or i.strip().startswith("#"):
            continue
        if i.lower().startswith("user-agent:"):
            useragent = _get_value(i)
            datas[useragent] = {}
        elif i.lower().startswith("sitemap:"):
            url = _get_value(i)
            if "sitemap" not in datas:
                datas["sitemap"] = []
            datas["sitemap"].append(url)
        else:
            split = i.split(":")
            name = split[0].lower()
            data = split[1].strip()
            if name not in datas[useragent]:
                datas[useragent][name] = []
            if name == "crawl-delay":
                datas[useragent][name] = int(data)
            else:
                datas[useragent][name].append(data)
    return datas

def _get_value(name):
    index = name.find(":")+1
    return name[index:].strip()

def _get_home(url):
    parsed = urlparse(url)
    if parsed.scheme:
        return f"{parsed.scheme}://{parsed.netloc}"
    else:
        raise NotURLError(f"'{url}' is not url")