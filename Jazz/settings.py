# Scrapy settings for Jazz project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Jazz'

SPIDER_MODULES = ['Jazz.spiders']
NEWSPIDER_MODULE = 'Jazz.spiders'
LOG_LEVEL = 'INFO'
ITEM_PIPELINES = {
    'Jazz.pipelines.EmptyItemPipeline': 100,
    'Jazz.pipelines.DuplicatesPipeline': 200,
    'Jazz.pipelines.MySQLPipeline': 300
}
LOG_LEVEL = 'CRITICAL'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Jazz (+http://www.yourdomain.com)'
