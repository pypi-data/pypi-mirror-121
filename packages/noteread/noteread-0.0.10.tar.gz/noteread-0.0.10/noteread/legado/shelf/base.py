import os

from notedrive.tables import SqliteTable
from notetool.secret import get_md5_str, read_secret


class BookSource(SqliteTable):
    def __init__(self, table_name='book_shelf_source', db_path=None, *args, **kwargs):
        if db_path is None:
            db_path = read_secret(cate1="local", cate2="path", cate3="noteread",cate4="db_path")
        if db_path is None:
            db_path = os.path.abspath(os.path.dirname(__file__)) + '/data/read.db'
        super(BookSource, self).__init__(db_path=db_path, table_name=table_name, *args, **kwargs)
        self.columns = ['md5', 'jsons']
        self.create()

    def create(self):
        self.execute("""
            create table if not exists {} (               
              md5           VARCHAR(35) primary key 
              ,jsons        VARCHAR(10000)
                         
              )
            """.format(self.table_name))

    def add_json(self, json_str):
        md5 = get_md5_str(json_str)
        properties = {
            "md5": md5,
            "jsons": json_str
        }
        self.insert(properties=properties)
