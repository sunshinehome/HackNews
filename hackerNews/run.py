
from scrapy import cmdline

name='DayNews'
cmd=' scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
