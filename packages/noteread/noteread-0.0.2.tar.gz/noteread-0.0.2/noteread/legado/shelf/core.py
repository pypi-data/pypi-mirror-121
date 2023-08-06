from noteread.legado.shelf.base import BookSource


def add_source():
    import json

    import requests
    book = BookSource()

    url = "https://namofree.gitee.io/yuedu3/legado3_booksource_by_Namo.json"
    text = requests.get(url).text

    for line in json.loads(text):
        print(len(json.dumps(line)))
        book.add_json(json.dumps(line))


add_source()
