import re
import ipaddress
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from requests.exceptions import RequestException

class FeatureExtraction:
    def __init__(self, url, load_html=False):
        self.url = url.strip()
        self.urlparse = urlparse(self.url)
        self.domain = self.urlparse.netloc
        self.scheme = self.urlparse.scheme
        self.html = ""
        self.soup = None

        if load_html:
            try:
                r = requests.get(self.url, timeout=(2, 2))
                r.raise_for_status()
                self.html = r.text
                self.soup = BeautifulSoup(self.html, "html.parser")
            except RequestException:
                self.html = ""
                self.soup = None

    # ===== Các hàm trích xuất đặc trưng =====
    def URLLength(self): return len(self.url)
    def DomainLength(self): return len(self.domain)
    def IsDomainIP(self):
        try: ipaddress.ip_address(self.domain); return 1
        except: return 0
    def URLSimilarityIndex(self):
        return SequenceMatcher(None, self.domain, self.urlparse.path).ratio()
    def CharContinuationRate(self):
        matches = re.findall(r'(.)\1+', self.url)
        return len(matches) / len(self.url) if self.url else 0
    def TLDLegitimateProb(self):
        tld = self.domain.split('.')[-1]
        common_tld = {"com", "org", "net", "edu", "gov"}
        return 1 if tld in common_tld else 0
    def URLCharProb(self):
        letters = sum(c.isalpha() for c in self.url)
        return letters / len(self.url) if self.url else 0
    def TLDLength(self): return len(self.domain.split('.')[-1]) if '.' in self.domain else 0
    def NoOfSubDomain(self): return max(0, self.domain.count('.') - 1)
    def HasObfuscation(self): return 1 if "%" in self.url or "@" in self.url else 0
    def NoOfObfuscatedChar(self): return self.url.count('%') + self.url.count('@')
    def ObfuscationRatio(self):
        obs = self.NoOfObfuscatedChar()
        return obs / len(self.url) if self.url else 0
    def NoOfLettersInURL(self): return sum(c.isalpha() for c in self.url)
    def LetterRatioInURL(self):
        return self.NoOfLettersInURL() / len(self.url) if self.url else 0
    def NoOfDegitsInURL(self): return sum(c.isdigit() for c in self.url)
    def DegitRatioInURL(self):
        return self.NoOfDegitsInURL() / len(self.url) if self.url else 0
    def NoOfEqualsInURL(self): return self.url.count('=')
    def NoOfQMarkInURL(self): return self.url.count('?')
    def NoOfAmpersandInURL(self): return self.url.count('&')
    def NoOfOtherSpecialCharsInURL(self):
        return len(re.findall(r'[^a-zA-Z0-9]', self.url)) - (
            self.NoOfEqualsInURL() + self.NoOfQMarkInURL() + self.NoOfAmpersandInURL()
        )
    def SpacialCharRatioInURL(self):
        special = self.NoOfOtherSpecialCharsInURL()
        return special / len(self.url) if self.url else 0
    def IsHTTPS(self): return 1 if self.scheme.lower() == "https" else 0
    def LineOfCode(self): return len(self.html.splitlines()) if self.html else 0
    def LargestLineLength(self): return max((len(line) for line in self.html.splitlines()), default=0)
    def HasTitle(self): return 1 if self.soup and self.soup.title else 0
    def DomainTitleMatchScore(self):
        title = self.soup.title.string.strip() if self.HasTitle() else ""
        return SequenceMatcher(None, self.domain, title).ratio() if title else 0
    def URLTitleMatchScore(self):
        title = self.soup.title.string.strip() if self.HasTitle() else ""
        return SequenceMatcher(None, self.url, title).ratio() if title else 0
    def HasFavicon(self):
        return 1 if self.soup and self.soup.find("link", rel=lambda v: v and "icon" in v.lower()) else 0
    def Robots(self):
        return 1 if self.soup and self.soup.find("meta", {"name": "robots"}) else 0
    def IsResponsive(self):
        return 1 if self.soup and self.soup.find("meta", {"name": "viewport"}) else 0
    def NoOfURLRedirect(self):
        try:
            return len(getattr(requests.get(self.url, allow_redirects=True, timeout=(2, 2)), "history", []))
        except: return 0
    def NoOfSelfRedirect(self): return 1 if self.NoOfURLRedirect() > 0 else 0
    def HasDescription(self):
        return 1 if self.soup and self.soup.find("meta", {"name": "description"}) else 0
    def NoOfPopup(self): return self.html.count("window.open(") if self.html else 0
    def NoOfiFrame(self): return len(self.soup.find_all("iframe")) if self.soup else 0
    def HasExternalFormSubmit(self):
        if self.soup:
            forms = self.soup.find_all("form", action=True)
            for f in forms:
                if self.domain not in f["action"]:
                    return 1
        return 0
    def HasSocialNet(self):
        if self.html:
            return 1 if re.search(r"(facebook|twitter|instagram|linkedin)\.com", self.html, re.I) else 0
        return 0
    def HasSubmitButton(self):
        return 1 if self.soup and self.soup.find("input", {"type": "submit"}) else 0
    def HasHiddenFields(self):
        return 1 if self.soup and self.soup.find("input", {"type": "hidden"}) else 0
    def HasPasswordField(self):
        return 1 if self.soup and self.soup.find("input", {"type": "password"}) else 0
    def Bank(self): return 1 if re.search(r"bank", self.url, re.I) else 0
    def Pay(self): return 1 if re.search(r"pay", self.url, re.I) else 0
    def Crypto(self): return 1 if re.search(r"crypto|bitcoin|eth", self.url, re.I) else 0
    def HasCopyrightInfo(self):
        return 1 if self.html and "©" in self.html else 0
    def NoOfImage(self): return len(self.soup.find_all("img")) if self.soup else 0
    def NoOfCSS(self): return len(self.soup.find_all("link", {"rel": "stylesheet"})) if self.soup else 0
    def NoOfJS(self): return len(self.soup.find_all("script")) if self.soup else 0
    def NoOfSelfRef(self):
        return sum(1 for a in self.soup.find_all("a", href=True) if self.domain in a["href"]) if self.soup else 0
    def NoOfEmptyRef(self):
        return sum(1 for a in self.soup.find_all("a", href=True) if a["href"].strip() in ["#", ""]) if self.soup else 0
    def NoOfExternalRef(self):
        return sum(1 for a in self.soup.find_all("a", href=True) if self.domain not in a["href"]) if self.soup else 0

    # ===== Trả về list đặc trưng (bỏ Title) =====
    def get_features_list(self):
        return [
            self.URLLength(),
            self.DomainLength(),
            self.IsDomainIP(),
            self.URLSimilarityIndex(),
            self.CharContinuationRate(),
            self.TLDLegitimateProb(),
            self.URLCharProb(),
            self.TLDLength(),
            self.NoOfSubDomain(),
            self.HasObfuscation(),
            self.NoOfObfuscatedChar(),
            self.ObfuscationRatio(),
            self.NoOfLettersInURL(),
            self.LetterRatioInURL(),
            self.NoOfDegitsInURL(),
            self.DegitRatioInURL(),
            self.NoOfEqualsInURL(),
            self.NoOfQMarkInURL(),
            self.NoOfAmpersandInURL(),
            self.NoOfOtherSpecialCharsInURL(),
            self.SpacialCharRatioInURL(),
            self.IsHTTPS(),
            self.LineOfCode(),
            self.LargestLineLength(),
            self.HasTitle(),
            self.DomainTitleMatchScore(),
            self.URLTitleMatchScore(),
            self.HasFavicon(),
            self.Robots(),
            self.IsResponsive(),
            self.NoOfURLRedirect(),
            self.NoOfSelfRedirect(),
            self.HasDescription(),
            self.NoOfPopup(),
            self.NoOfiFrame(),
            self.HasExternalFormSubmit(),
            self.HasSocialNet(),
            self.HasSubmitButton(),
            self.HasHiddenFields(),
            self.HasPasswordField(),
            self.Bank(),
            self.Pay(),
            self.Crypto(),
            self.HasCopyrightInfo(),
            self.NoOfImage(),
            self.NoOfCSS(),
            self.NoOfJS(),
            self.NoOfSelfRef(),
            self.NoOfEmptyRef(),
            self.NoOfExternalRef()
        ]