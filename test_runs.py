import requests

response = requests.get(url = "https://qrng-generation-server.dorafactory.org/QRNG/JobResults?jobID=cw20jpavka8g008bbn40", headers={"API-Key": "Vld6Xia-u8uJ5AqjMXwp6g"})

print(response.text)