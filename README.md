# Proxy101 - Public proxies server scraper and checker

Proxy101 is a Python library for finding and checking public proxies

## Installation

Download the proxy101 folder and then copied to your root project folder. 

And then install the requirements using command
```bash
pip install - r requirements.txt
```

## Usage
### Scrape the proxies. 
```
Available Params: 
Default Value was : all
---
country: country name e.g "Indonesia", "Singapore", etc.
type: "http", "https", "http-https", "socks4", "socks5", "socks". 
anonymity:  "ELITE", "ANONYMOUS", "TRANSPARENT".
port: 80, 8080, etc. 
```
```python
from proxy101.proxy import Proxy101 as proxy101

proxy = proxy101()
status_code, res = proxy.set_params(country="Singapore")
if status_code == 200:
  print(res)
```

```json
[
  {
    "ip": "XXX.XXX.XXX.XXX",
    "port": 8080,
    "type": "5",
    "country": "Singapore",
    "code": "SG",
    "city": "Singapore",
    "anonymity": "3",
    "timeout": 2.2,
    "isGoogle": false,
    "lastcheck": {
      "date": "2021-12-06 21:05:38.000000",
      "timezone_type": 3,
      "timezone": "UTC"
    }
  },
  {
    "ip": "YYY.YYY.YYY.YYY",
    "port": 8080,
    "type": "126",
    "country": "Singapore",
    "code": "SG",
    "city": "Singapore",
    "anonymity": "3",
    "timeout": 5.5,
    "isGoogle": true,
    "lastcheck": {
      "date": "2021-12-06 20:52:05.000000",
      "timezone_type": 3,
      "timezone": "UTC"
    }
  },
]
```
### Check the proxies. 
```
proxies check was done by sending GET request to httpbin using asynchronus call. 

proxies: data type was list with dict inside with key ip and port like example below
timeout: timeout for checking the proxy before it was decided bad proxy. 
```
```python
from proxy101.proxy import Proxy101 as proxy101

proxy = proxy101()
status_code, res = proxy.set_params(country="Singapore")
if status_code == 200:
  proxies = []
  for p in res:
     ipport_proxy = {
        'ip' : p['ip'],
        'port' : p['port']
     }
     proxies.append(ipport_proxy)
  result = proxy.check_proxies(proxies, timeout=4)
  print(result)
```
```json
[
  {
    "ip": "XXX.XXX.XXX.XXX",
    "port": 8080
  },
]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)