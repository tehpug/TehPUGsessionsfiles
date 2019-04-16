import pymysql
from scrapy.utils.project import get_project_settings
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class IrancookPipeline(object):
    def open_spider(self, spider):
        database_config = get_project_settings().get('DATABASE_IRANCOOK')
        self.db = pymysql.connect(
                            host=database_config['host'],
                            user=database_config['user'],
                            password=database_config['password'],
                            db=database_config['db'],
                            charset=database_config['charset'],
                            cursorclass=pymysql.cursors.DictCursor,
                            autocommit=True
                        )


    def process_item(self, item, spider):
        cursor = self.db.cursor()

        query = """insert ignore foods (food_id, food_type, food_name, food_image, food_url, ingredients, recipe) 
        values ({}, "{}", "{}", "{}", "{}", "{}", "{}")"""
        cursor.execute(
                        query.format(
                            item['food_id'],
                            item['food_type'],
                            item['food_name'],
                            item['food_image'],
                            item['food_url'],
                            item['ingredients'],
                            item['recipe']
                        )
                    )

        return item

    def close_spider(self, spider):
        self.db.close()
