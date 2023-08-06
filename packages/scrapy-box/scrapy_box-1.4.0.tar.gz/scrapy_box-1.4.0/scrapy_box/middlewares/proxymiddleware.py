"""
@Description:
@Usage:
@Author: liuxianglong
@Date: 2021/9/1 下午8:20
"""
import re
import time
import logging
import treq
from twisted.internet import defer
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class RandomProxyDownloaderMiddleware(object):
    def __init__(self, proxy_addr):
        self.proxy_addr = proxy_addr

    @classmethod
    def from_crawler(cls, crawler):
        proxy_addr = crawler.settings.get('PROXY_ADDR')
        if proxy_addr is None or not proxy_addr.startswith('http'):
            raise NotConfigured

        return cls(proxy_addr)

    @defer.inlineCallbacks
    def process_request(self, request, spider):
        proxy = yield self.get_proxy()
        logger.debug('using proxy %s for request %s' % (proxy, request.url))
        request.meta['proxy'] = 'http://%(ip)s:%(port)s' % proxy

    @defer.inlineCallbacks
    def get_proxy(self):
        """ Get proxy from your PROXY_ADDR, this function should be rewrite if it can't satisfy your need.

            It Should return json format proxy like:
            {
                'ip': '192.168.0.32',
                'port': 23,
                ...
            }
        """
        while True:
            response = yield treq.get(url=self.proxy_addr)
            proxy = yield response.json()
            if proxy:
                defer.returnValue(proxy)
            else:
                time.sleep(2)
                logger.info('未获取到代理，等待两秒，重新获取')


class SplashProxyDownloaderMiddleware(object):
    def __init__(self, proxy_addr, splash_url):
        self.proxy_addr = proxy_addr
        self.splash_url = splash_url

    @classmethod
    def from_crawler(cls, crawler):
        proxy_addr = crawler.settings.get('PROXY_ADDR')
        splash_url = crawler.settings.get('SPLASH_URL')
        if proxy_addr is None or splash_url is None or not proxy_addr.startswith('http'):
            raise NotConfigured

        return cls(proxy_addr, splash_url)

    @defer.inlineCallbacks
    def process_request(self, request, spider):
        proxy = yield self.get_proxy()
        if not request.url.startswith(self.splash_url):
            logger.debug('using proxy %s for request %s' % (proxy, request.meta['splash']['args']['url']))
            request.meta['splash']['args']['proxy'] = 'http://%(ip)s:%(port)s' % proxy

    @defer.inlineCallbacks
    def get_proxy(self):
        """ Get proxy from your PROXY_ADDR, this function should be rewrite if it can't satisfy your need.

            It Should return json format proxy like:
            {
                'ip': '192.168.0.32',
                'port': 23,
                ...
            }
        """
        while True:
            response = yield treq.get(url=self.proxy_addr)
            proxy = yield response.json()
            if proxy:
                defer.returnValue(proxy)
            else:
                time.sleep(2)
                logger.info('未获取到代理，等待两秒，重新获取')


class SplashRetryProxyMiddleware(SplashProxyDownloaderMiddleware):
    retry_processed = dict()

    @defer.inlineCallbacks
    def process_request(self, request, spider):
        retry_times = request.meta.get('retry_times')
        if retry_times:
            if self.retry_processed.get(retry_times) is None:
                self.retry_processed[retry_times] = True

                proxy = yield self.get_proxy()
                body = request.body.decode()
                old_proxy = ''.join(re.findall(r'"proxy": "(.*?)"', body))
                if old_proxy:
                    logger.info(f"{request.meta['splash']['args']['url']} retry times: {retry_times}, using new proxy: {proxy}")
                    new_body = body.replace(old_proxy, 'http://%(ip)s:%(port)s' % proxy)
                    new_request = request.replace(
                        body=new_body.encode(),
                    )
                    return new_request
