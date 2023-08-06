from .error import UserAgentExistsError

class Make:
    def __init__(self):
        self._useragent = {}
        self._sitemap = []

    def add_useragent(self, useragent="*"):
        if isinstance(useragent, str):
            if useragent in self._useragent:
                raise UserAgentExistsError(f"{useragent} has already exists")
            instance = UserAgent()
            self._useragent[useragent] = instance
            return instance
        else:
            raise ValueError("useragent must be str")

    def add_sitemap(self, url):
        if isinstance(url, (list, set, tuple)):
            self._sitemap.extend(list(url))
        elif isinstance(url, str):
            self._sitemap.append(url)
        else:
            raise ValueError("url must be str or list or set or tuple")

    def make(self):
        text = ""
        for useragent, instance in self._useragent.items():
            value = "\nUser-agent: {}\n".format(useragent)
            if instance.disallow:
                value += "{}\n".format("Disallow: "+"\nDisallow: ".join(instance.disallow))
            if instance.allow:
                value += "{}\n".format("Allow: "+"\nAllow: ".join(instance.allow))
            text += value
        if self._sitemap:
            text += "\nSitemap: " + "\nSitemap: ".join(self._sitemap)
        return text.strip()

    def to_file(self, path):
        info = self.make()
        with open(path, "w") as f:
            f.write(info)

class UserAgent:
    def __init__(self):
        self.disallow = []
        self.allow = []
    def add_disallow(self, disallow):
        if isinstance(disallow, (list, set, tuple)):
            self.disallow.extend(list(disallow))
        elif isinstance(disallow, str):
            self.disallow.append(disallow)
        else:
            raise ValueError("disallow must be str or list or set or tuple")
    def add_allow(self, allow):
        if isinstance(allow, (list, set, tuple)):
            self.allow.extend(list(allow))
        elif isinstance(allow, str):
            self.allow.append(allow)
        else:
            raise ValueError("allow must be str or list or set or tuple")