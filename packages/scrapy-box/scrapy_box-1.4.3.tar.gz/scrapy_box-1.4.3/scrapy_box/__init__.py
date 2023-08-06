
from scrapy_box.middlewares.proxymiddleware import \
    RandomProxyDownloaderMiddleware, \
    SplashProxyDownloaderMiddleware, \
    SplashRetryProxyMiddleware

from scrapy_box.middlewares.retrymiddleware import ErrorRedirectMiddleware, ErrorResponseMiddleware
from scrapy_box.pipelines.mongo import MongoBatchInsertPipeline
from scrapy_box.pipelines.mysql import MysqlInsertPipeline, MysqlUpdatePipeline
