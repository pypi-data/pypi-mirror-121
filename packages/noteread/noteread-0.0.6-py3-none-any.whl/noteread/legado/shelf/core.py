import json
import sys

import requests
from noteread.legado.shelf.base import BookSource
from notetool.log import logger
from notetool.secret import write_secret
from tqdm import tqdm

write_secret(value="/root/workspace/notechats/noteread/noteread/legado/shelf/data/read.db",
             cate1="local", cate2="path", cate3="noteread", cate4="db_path")


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
    "https://namofree.gitee.io/yuedu3/legado3_booksource_by_Namo.json",
    "https://shuyuan.miaogongzi.net/shuyuan/1630342495.json",
    "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/syhj.json",
    "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/yshj.json",
    "https://haxc.coding.net/p/booksrc/d/booksrc/git/raw/master/Book3.0Source.json",
    "https://tangguochaotian.coding.net/p/tangguoshuyuan1015/d/tangguo/git/raw/master/exportBookSource.json",
    "https://guaner001125.coding.net/p/coding-code-guide/d/booksources/git/raw/master/sources/guaner.json"
]
add_source(urls)
