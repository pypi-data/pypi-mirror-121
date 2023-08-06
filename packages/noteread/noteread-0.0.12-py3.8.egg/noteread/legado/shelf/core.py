import json
import sys

import requests
from noteread.legado.shelf.base import BookSource
from notetool.log import logger
from notetool.secret import write_secret
from tqdm import tqdm


def add_source(urls=None):
    if urls is None:
        return

    book = BookSource()
    print(book.db_path)
    for url in tqdm(urls):
        try:
            text = requests.get(url).text
            for line in json.loads(text):
                book.add_json(json.dumps(line))
        except Exception as e:
            logger.error(e)


urls = [
    "https://cdn.jsdelivr.net/gh/bushixuanqi/book-source/%E4%B9%A6%E6%BA%90%E5%90%88%E9%9B%86.json",

    "https://guaner001125.coding.net/p/coding-code-guide/d/booksources/git/raw/master/sources/guaner.json",
    "https://haxc.coding.net/p/booksrc/d/booksrc/git/raw/master/Book3.0Source.json",

    "https://namofree.gitee.io/yuedu3/legado3_booksource_by_Namo.json",
    "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/syhj.json",
    "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/yshj.json",

    "http://shuyuan.miaogongzi.net/shuyuan/1624832786.json",
    "https://shuyuan.miaogongzi.net/shuyuan/1630342495.json",
    "http://shuyuan.miaogongzi.net/shuyuan/1623355431.json",

    "https://tangguochaotian.coding.net/p/tangguoshuyuan1015/d/tangguo/git/raw/master/exportBookSource.json",
    "https://tianyuzhange.coding.net/p/booksource/d/shuyuan/git/raw/master/2.0shuyuan.json",
]
add_source(urls)
