import re
import tldextract
import numpy as np
import pandas as pd
from urllib.parse import urlparse

class FeatureExtraction:
    def __init__(self, url):
        self.url = url
        self.parsed = urlparse(url)
        self.domain = self.parsed.netloc
        self.path = self.parsed.path

    # 1. Chiều dài URL
    def URLLength(self):
        return len(self.url)

    # 2. Chiều dài domain
    def DomainLength(self):
        return len(self.domain)

    # 3. Domain có phải dạng IP
    def IsDomainIP(self):
        ip_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
        return 1 if ip_pattern.match(self.domain) else 0

    # 4. Chỉ số tương đồng URL (giả sử: domain == path thì similarity cao)
    def URLSimilarityIndex(self):
        if not self.path:
            return 0
        return len(set(self.domain).intersection(set(self.path))) / len(self.path)

    # 5. Xác suất hợp lệ của TLD (tạm: nếu TLD trong danh sách phổ biến thì 1, ngược lại 0)
    def TLDLegitimateProb(self):
        tld = tldextract.extract(self.url).suffix
        common_tlds = {"com", "org", "net", "edu", "gov", "vn", "info"}
        return 1 if tld in common_tlds else 0

    # 6. Chiều dài TLD
    def TLDLength(self):
        return len(tldextract.extract(self.url).suffix)

    # 7. Số lượng subdomain
    def NoOfSubDomain(self):
        sub = tldextract.extract(self.url).subdomain
        return 0 if sub == "" else len(sub.split("."))

    # 8. Số dấu "="
    def NoOfEqualsInURL(self):
        return self.url.count("=")

    # 9. Số dấu "?"
    def NoOfQMarkInURL(self):
        return self.url.count("?")

    # 10. Số dấu "&"
    def NoOfAmpersandInURL(self):
        return self.url.count("&")

    # 11. Số ký tự đặc biệt khác
    def NoOfOtherSpecialCharsInURL(self):
        return len(re.findall(r'[@!~*]', self.url))

    # 12. Tỉ lệ ký tự đặc biệt trong URL
    def SpacialCharRatioInURL(self):
        if len(self.url) == 0:
            return 0
        special_chars = re.findall(r'[^a-zA-Z0-9]', self.url)
        return len(special_chars) / len(self.url)

    # 13. Có dùng HTTPS không
    def IsHTTPS(self):
        return 1 if self.parsed.scheme == "https" else 0

    # 14. Xác suất ký tự trong URL (trung bình ASCII / 128)
    def URLCharProb(self):
        if len(self.url) == 0:
            return 0
        return np.mean([ord(c) for c in self.url]) / 128.0

    # Trả về list 14 đặc trưng
    def get_features_list(self):
        return [
            self.URLLength(),
            self.DomainLength(),
            self.IsDomainIP(),
            self.URLSimilarityIndex(),
            self.TLDLegitimateProb(),
            self.TLDLength(),
            self.NoOfSubDomain(),
            self.NoOfEqualsInURL(),
            self.NoOfQMarkInURL(),
            self.NoOfAmpersandInURL(),
            self.NoOfOtherSpecialCharsInURL(),
            self.SpacialCharRatioInURL(),
            self.IsHTTPS(),
            self.URLCharProb()
        ]