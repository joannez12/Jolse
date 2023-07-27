from multiprocessing import Queue, Process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from Pipeline.spiders.store_items import StoreItemsSpider

def script(queue):
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(StoreItemsSpider)
        process.start()
        queue.put(None)
    except Exception as e:
        queue.put(e)

def main(request=None):
    queue = Queue()
    main_process = Process(target=script, args=(queue,))
    main_process.start()
    main_process.join()
    result = queue.get()
    if result is not None:
        raise result
    return "ok"

if __name__ == '__main__':
    main()
