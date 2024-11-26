# Copyright (c) 2024 DehengYang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import bibtexparser
import bibtexparser.middlewares as m
import re

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
    title = re.sub(r"\s+", " ", entry['title'])
    return title, authors, year

if __name__ == '__main__':
    bibtex = """
    @article{DBLP:journals/cmpb/DeryckeAVPBAAM24,
  author       = {Lucie Derycke and
                  Stephane Avril and
                  Jeroen K. Vermunt and
                  David Perrin and
                  S. El Batti and
                  Jean{-}Marc Alsac and
                  J.{-}N. Albertini and
                  A. Millon},
  title        = {Computational prediction of proximal sealing in endovascular abdominal
                  aortic aneurysm repair with unfavorable necks},
  journal      = {Comput. Methods Programs Biomed.},
  volume       = {244},
  pages        = {107993},
  year         = {2024},
  url          = {https://doi.org/10.1016/j.cmpb.2023.107993},
  doi          = {10.1016/J.CMPB.2023.107993},
  timestamp    = {Sat, 08 Jun 2024 13:14:06 +0200},
  biburl       = {https://dblp.org/rec/journals/cmpb/DeryckeAVPBAAM24.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}     
                 """
    print(parse_bibtex(bibtex))