# pipelines.py
from datetime import datetime, timezone
from databases.database import Session
from databases.models import Category, PriceIndex

class PostgresPipeline:
    def open_spider(self, spider):
        self.db = Session()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        if not item.get('price'):
            return item
            
        category = self.db.query(Category).filter_by(name=item['category_name']).first()
        if not category:
            category = Category(name=item['category_name'], description="Auto-scraped")
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)

        price_index = PriceIndex(
            category_id=category.id,
            index_value=float(item['price']),
            source=item['source'],
            time=datetime.now(timezone.utc)
        )
        self.db.add(price_index)
        self.db.commit()
        return item