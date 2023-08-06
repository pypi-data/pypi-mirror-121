"""
@Description: 
@Usage: 
@Author: liuxianglong
@Date: 2021/9/1 下午8:50
"""
import re
import logging
from w3lib.url import safe_url_string
from urllib.parse import urljoin, urlparse
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.redirect import BaseRedirectMiddleware

logger = logging.getLogger(__name__)


class ErrorRedirectMiddleware(BaseRedirectMiddleware, RetryMiddleware):
    """ This build-in RedirectMiddleware like below
        'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,

        You should use ErrorRedirectMiddleware like below, make use the num larger than 600

        'scrapy_box.ErrorRedirectMiddleware': 601
    """
    def __init__(self, settings):
        super(ErrorRedirectMiddleware, self).__init__(settings)
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        self.error_redirect_url_snippet = settings.get('ERROR_REDIRECT_URL_SNIPPET', [])

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if (
            request.meta.get('dont_redirect', False)
            or response.status in getattr(spider, 'handle_httpstatus_list', [])
            or response.status in request.meta.get('handle_httpstatus_list', [])
            or request.meta.get('handle_httpstatus_all', False)
        ):
            return response

        allowed_status = (301, 302, 303, 307, 308)
        if 'Location' not in response.headers or response.status not in allowed_status:
            return response

        location = safe_url_string(response.headers['Location'])
        if response.headers['Location'].startswith(b'//'):
            request_scheme = urlparse(request.url).scheme
            location = request_scheme + '://' + location.lstrip('/')

        redirected_url = urljoin(request.url, location)

        for snippet in self.error_redirect_url_snippet:
            if snippet in redirected_url:
                logger.info('Error redirect url <%s> via <%s>, retry..' % (redirected_url, request.url))
                req = self._retry(request, "error_redirect", spider)
                if req is not None:
                    return req
                else:
                    raise IgnoreRequest

        if response.status in (301, 307, 308) or request.method == 'HEAD':
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        redirected = self._redirect_request_using_get(request, redirected_url)
        return self._redirect(redirected, request, spider, response.status)


class ErrorResponseMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super(ErrorResponseMiddleware, self).__init__(settings)
        self.error_response_snippet = settings.get('ERROR_RESPONSE_SNIPPET', [])

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def error_validation(self, res):
        for error in self.error_response_snippet:
            if re.search(error, res.text):
                return True, error
        return False, 'success'

    def process_response(self, request, response, spider):
        iserror, error = self.error_validation(response)
        if iserror:
            logger.info(f"error response: {error} from <{request.url}>, retry...")
            req = self._retry(request, "error_response", spider)
            if req is not None:
                return req
            else:
                raise IgnoreRequest
        return response
