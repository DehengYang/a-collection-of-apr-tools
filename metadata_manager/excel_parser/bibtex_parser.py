# This code is modified from https://github.com/kpole/bibtex2ref/blob/master/main.py

# -*- coding: utf-8 -*-
# ---------------------
# requirement:
# pip install requests
# pip install beautifulsoup4
# pip install lxml
# pip install --no-cache-dir --force-reinstall git+https://github.com/sciunto-org/python-bibtexparser@main
 

import requests
from bs4 import BeautifulSoup
import bibtexparser
from bibtexparser.middlewares import BlockMiddleware
import bibtexparser.middlewares as m
import re
import termcolor

# 自定义 name merge 中间件
# class MergeNameParts(BlockMiddleware):
#     def transform_entry(self, entry, *args, **kwargs):
#         MAX_AUTHOR_COUNT = 100
#         convert_names = []
#         for name_part in entry['author'][:MAX_AUTHOR_COUNT]:
#             # .replace("{", "").replace("{", "")
#             convert_names.append(' '.join([*name_part.first, *name_part.last]))
        
#         if len(entry['author']) > MAX_AUTHOR_COUNT:
#             convert_names.append("et al")
#         entry['author'] = ', '.join(convert_names)
#         return entry

def modify_book_title(entry, key):
    booktitle = []
    entry[key] = re.sub(r'\s+', ' ', entry[key])
    for item in entry[key].replace("\n", "").split(','):
        item = item.replace('{', '')
        item = item.replace('}', '')
        item = item.strip()
        booktitle.append(item)
    print(booktitle)
    entry[key] = ', '.join(booktitle)

def get_bibtex_from_dblp(paper_name):
    DEFAULT_RETURN = ""
    BASE_URL = "https://dblp.uni-trier.de"
    url = f"{BASE_URL}/search/publ/inc?q={paper_name}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # Find all <li> elements with class 'entry'
    entries = soup.find_all('li', class_='entry')

    final_bibtex_content = DEFAULT_RETURN
    if len(entries) == 0:
        print(termcolor.colored(f"No bibtex found from dblp for {paper_name}", "yellow"))
        return final_bibtex_content

    # Extract and print the 'id' attribute of each entry
    bibtex_content_list = []
    for (index, entry) in enumerate(entries):
        entry_id = entry.get('id')
        bibtex_url = BASE_URL + f"/rec/{entry_id}.html/?view=bibtex" 
        response = requests.get(bibtex_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            bibtex_content = soup.find('pre', class_='verbatim')
            bibtex_content = bibtex_content.text
        bibtex_content_list.append(bibtex_content)

    if len(bibtex_content_list) > 1:
        for bibtex_content in bibtex_content_list:
            if 'arxiv' not in bibtex_content:
                final_bibtex_content = bibtex_content
                break
        if final_bibtex_content == "": # 实在找不到非arxiv 链接的，就用第一个
            final_bibtex_content = bibtex_content_list[0]
            print(termcolor.colored(f"[WARNING] We cannot find non-arxiv link for {paper_name}, so we finally use the first bibtex.", "cyan"))
    final_bibtex_content = bibtex_content_list[0]
    
    return final_bibtex_content.strip()

def get_bibtex_from_input():
    ret = ""
    print("Please enter content in bibtex format, ending with a separate end:")
    while True:
        line = input()
        if line == "end":
            break
        ret += line
    print(ret)
    return ret

def parse_bibtex(bibtex_content):
    bib_database = bibtexparser.parse_string(bibtex_content)

    entry_dict = bib_database.entries[0]
    # print(termcolor.colored("Entry Content:", "blue"))
    # print(entry_dict)

    layers = [
        m.SeparateCoAuthors(),
        m.SplitNameParts(),
        # MergeNameParts(),
    ]
    library = bibtexparser.parse_string(bibtex_content, append_middleware=layers)
    entry = library.entries[0]

    authors = []
    for name_part in entry['author']:
        author = name_part.merge_first_name_first.replace("{", "").replace("}", "")
        authors.append(author)
    # print(authors)
    year = entry['year']
    return authors, year

def main():
    # opt = int(input("1. Search from above dblp.\n2. Manually enter bibtex\nPlease select a method: "))
    # while opt != 1 and opt != 2:
    #     opt = int(input("Please reselect a method: "))
    # if opt == 1:
    #     bibtex_content = get_bibtex_from_dblp()
    # else:
    #     bibtex_content = get_bibtex_from_input()

    title = "CodeR: Issue Resolving with Multi-Agent and Task Graphs"
    bibtex_content = get_bibtex_from_dblp(title)
    parse_bibtex(bibtex_content)

if __name__ == '__main__':
    main()


"""
test:
    title = "CodeR: Issue Resolving with Multi-Agent and Task Graphs"
entry[author]: Dong Chen, Shaoxin Lin, Muhan Zeng, Daoguang Zan, Jian{-}Gang Wang, Anton Cheshkov, Jun Sun, Hao Yu, Guoliang Dong, Artem Aliev, Jie Wang, Xiao Cheng, Guangtai Liang, Yuchi Ma, Pan Bian, Tao Xie, Qianxiang Wang

MergeNameParts() is not needed, as this function is already included in bibtexparser. 20241118-17:19:55

"""