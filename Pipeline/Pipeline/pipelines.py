# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker

from Pipeline.models import Item, Price, create_items_table

from Pipeline.connection import connect_db


class CrawlPipeline:
    def __init__(self):
        self.products_seen = set()
        engine = connect_db()
        create_items_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        adapter = ItemAdapter(item)
        if adapter['name'] in self.products_seen:
            return item

        product = session.query(Item).filter(Item.name == adapter['name']).first()
        try:
            if product:
                new_price = Price(original_price = adapter['original_price'], sale_price = adapter['sale_price'], item=product)
                session.add(new_price)
                session.commit()
            else:
                new_item = Item(name=adapter['name'], img=adapter['img'])

                session.add(new_item)
                session.commit()

                new_price = Price(original_price = adapter['original_price'], sale_price = adapter['sale_price'], item=new_item)
                session.add(new_price)
                session.commit()
        except:
            session.rollback()
            raise ValueError("error committing")
        finally:
            self.products_seen.add(adapter['name'])
            session.close()

        return item
