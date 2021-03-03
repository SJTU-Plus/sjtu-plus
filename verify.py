#!/usr/bin/env python3

import requests
import sys

# Usage: ./verify <QQ> <token> <API key>

qq = sys.argv[1]
token = sys.argv[2]
api_key = sys.argv[3]

print(qq, token, api_key)

resp = requests.post("https://plus.sjtu.edu.cn/attest/verify",
        json={ 'qq_number' : qq, 'token': token }, headers={ 'Api-Key': api_key })

print(resp.json())
