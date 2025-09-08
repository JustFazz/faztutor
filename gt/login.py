import requests
import random
import re
import json

class login:
    def __init__(self):
        self.token = ""
        self._token = ""
        self.mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.rid = ''.join(random.choices("0123456789", k=8))
        
    def get_token(self, growid="", password=""):
        payload = {"version": "5.26",
                   "platform": "0",
                   "protocol": "217"}
        url = "http://www.growtopia1.com/growtopia/server_data.php"
        response = requests.post(url, data=payload)
        for line in response.text.strip().split('\n'):
            parts = line.split('|', 1)
            if len(parts) == 2:
                key, value = parts
                match key:
                    case "server":
                        self.host = value
                    case "port":
                        self.port = int(value)
                    case "loginurl":
                        self.url = value
                    case "meta":
                        self.meta = value
        raw_data = f"""requestedName|FairyGrow
f|1
protocol|216
game_version|5.26
fz|23282360
cbits|1024
player_age|24
GDPR|1
category|_-5100
totalPlaytime|0
klv|74e7d188df5951f033fbf04a9423cc29d31338ef0ea4a9b1aae4c5548b8a520c
hash2|1926385939
meta|{self.meta}
fhash|-716928004
rid|{self.rid}
platformID|0,1,1
deviceVersion|0
country|ma
hash|546519745
mac|{self.mac}
wk|023771B21761F29108ACF22E0A288CE3
zf|1596444234
"""
        post_data = raw_data.encode("utf-8").hex()
        url = "https://login.creativeps.eu/player/login/dashboard?valKey=40db4045f2d8c572efe8c4a060605726"
        response = requests.post(url, data=post_data)
        
        # parsing HTML

        match = re.search(r'name="_token"\s+type="hidden"\s+value="([^"]+)"', response.text)
        if match:
            token = match.group(1)

        # URL tujuan login
        url = "https://login.creativeps.eu/player/growid/login/validate"

        # Data form yang dikirim (sesuai input di HTML)
        payload = {"_token": token,
                   "growId": growid,
                   "password": password
                }

        # Kirim POST request
        response = requests.post(url, data=payload)
        res = json.loads(response.text)

        # Hasil
        if response.status_code == 200:
            return res["token"]
        return