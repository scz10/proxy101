from asyncio import tasks
import requests
import lxml.html
import aiohttp
import asyncio
import sys

class Proxy101():
    def __init__(self):
        self.s = requests.Session()
        self.headers = {
            'authority': 'www.proxydocker.com',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        }

        self.url = "https://www.proxydocker.com/en/proxylist/"
        self.payloads = {
            'token': '',
            'country': 'all',
            'city': 'all',
            'state': 'all',
            'port': 'all',
            'type': 'all',
            'anonymity': 'all',
            'need': 'all',
            'page': '1'
        }
        

    def _get_token(self):
        html = self.s.get(self.url)
        doc = lxml.html.fromstring(html.content)
        meta_token = doc.xpath("/html/head/meta[18]")
        self.payloads['token'] = meta_token[0].get("content")

    def _execute(self):
        self._get_token()
        self.url = "https://www.proxydocker.com/en/api/proxylist/"
        response = self.s.post(url=self.url, headers=self.headers, data=self.payloads)
        return response.status_code, response.json()['proxies']
    
    def set_params(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.payloads.keys():
                self.payloads[key] = value
        
        return self._execute()

    async def _get_origin(self, session, ip, port):
        try:
            async with session.get("https://httpbin.org/ip", proxy="http://{}:{}".format(ip, port)) as resp:
                origin = await resp.json()
                return {'ip' : origin['origin'], 'port' : port}
        except:
            pass

    async def _check_proxies(self, proxies, timeout=2):
        working_proxies = []
        timeout_setting = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout_setting) as session:
            tasks = []
            for proxy in proxies:
                tasks.append(asyncio.ensure_future(self._get_origin(session, proxy['ip'], proxy['port'])))
            original_origin = await asyncio.gather(*tasks)
            for origin in original_origin:
                if origin != None:
                    working_proxies.append(origin)
            
            return working_proxies

    def check_proxies(self, proxies, timeout):
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        working_proxies = asyncio.run(self._check_proxies(proxies, timeout))
        return working_proxies