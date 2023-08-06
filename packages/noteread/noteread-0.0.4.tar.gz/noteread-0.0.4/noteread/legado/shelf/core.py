import json

import requests
from noteread.legado.shelf.base import BookSource
from notetool.log import logger
from tqdm import tqdm


def add_source(urls=None):
    if urls is None:
        return

    book = BookSource()
    logger.info("begin")
    for url in tqdm(urls):
        try:
            text = requests.get(url).text
            for line in json.loads(text):
                book.add_json(json.dumps(line))
        except Exception as e:
            logger.error(e)





urls = [
    "https://namofree.gitee.io/yuedu3/legado3_booksource_by_Namo.json",
    "https://shuyuan.miaogongzi.net/shuyuan/1630342495.json",
    "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/syhj.json",
    "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/yshj.json",
    "https://haxc.coding.net/p/booksrc/d/booksrc/git/raw/master/Book3.0Source.json",
    "https://tangguochaotian.coding.net/p/tangguoshuyuan1015/d/tangguo/git/raw/master/exportBookSource.json",
    "https://guaner001125.coding.net/p/coding-code-guide/d/booksources/git/raw/master/sources/guaner.json"
]
add_source(urls)
