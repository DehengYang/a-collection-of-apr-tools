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
from pyutils import File_util
import bibtex_parser
import config
import os
import json
import time
import pandas as pd


def main_json_creator_from_excel_file(excel_path):
    """
    1. read excel to pandas
    2. output to json
    """
    # 1) create directories to save: json and bib files
    json_output_dir = os.path.join(config.OUTPUT_DIR, "json")
    if not os.path.exists(json_output_dir):
        os.makedirs(json_output_dir)
    bib_output_dir = os.path.join(config.OUTPUT_DIR, "bibtex")
    if not os.path.exists(bib_output_dir):
        os.makedirs(bib_output_dir)

    # 2) read current excel to pandas dataframe
    df = pd.read_excel(
        excel_path, sheet_name="工作表1", header=0
    )  # 表头在第0行（即第一行，Python中索引从0开始）
    # new_excel_path = os.path.join(config.OUTPUT_DIR, 'apr_literature_metadata_new.xlsx')
    df_new = pd.DataFrame(
        columns=[
            "Title",
            "APR Tool Name",
            "Authors",
            "Year",
            "Venue",
            "Repo URL",
            "Target Language",
            "Used Dataset",
            "CCF Rank",
            "Paper Category",
            "Bibtex",
        ]
    )
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        print("Current paper: ", row_dict["Title"])
        title = row_dict["Title"]
        apr_tool_name = row_dict["APR Tool Name"]
        year = row_dict["Year"]
        venue = row_dict["Venue"]
        repo_url = row_dict["Repo URL"]
        target_language = [
            language.strip() for language in row_dict["Target Language"].split(",")
        ]
        used_dataset = [
            dataset.strip().replace("\n", " ")
            for dataset in row_dict["Used Dataset"].split(",")
        ]
        ccf_rank = row_dict["CCF Rank"]
        paper_category = "-"

        # 3) get and parse bibtex from dblp
        bib_output_file_name = f"{year}{get_formatted_title(title)}.bib"
        if bib_output_file_name in os.listdir(bib_output_dir) and os.path.getsize(
            os.path.join(bib_output_dir, bib_output_file_name)
        ):
            print(f"[Skip] {bib_output_file_name} already exists.")
            bibtex = File_util.read_file(
                os.path.join(bib_output_dir, bib_output_file_name)
            )
        else:
            bibtex = bibtex_parser.get_bibtex_from_dblp(title)
            time.sleep(
                4
            )  # avoid frequent queries to dblp sites. refer to: https://dblp.org/robots.txt
            if bibtex != "":
                bib_output_path = os.path.join(bib_output_dir, bib_output_file_name)
                File_util.write_to_file(bib_output_path, bibtex, append=False)
        authors = []
        if bibtex != "":
            authors, year = bibtex_parser.parse_bibtex(bibtex)
        df_new.loc[len(df_new)] = [
            title,
            apr_tool_name,
            authors,
            year,
            venue,
            repo_url,
            target_language,
            used_dataset,
            ccf_rank,
            paper_category,
            bibtex,
        ]

    # 3) save df_new to new_excel_path
    # df_new.to_excel(new_excel_path, sheet_name='工作表1', index=True, index_label='ID')

    # 4) save df_new to json files
    for index, row in df_new.iterrows():
        row_dict = row.to_dict()
        formmated_title = get_formatted_title(row_dict["Title"])
        year = row_dict["Year"]

        #  'Specification', 'Tool Category', 'Bug Types',
        row_dict["Specification"] = "-"
        row_dict["Tool Category"] = "-"
        row_dict["Bug Types"] = "-"
        json_output_path = os.path.join(
            json_output_dir, f"{year}-{formmated_title}.json"
        )
        json.dump(
            row_dict,
            open(json_output_path, "w", encoding="utf-8"),
            indent=4,
            ensure_ascii=False,
        )


def get_formatted_title(title):
    """
    format the title to a valid file name
    """
    return title.replace(":", "-").replace("?", "").replace(",", "")


if __name__ == "__main__":
    main_json_creator_from_excel_file(
        excel_path=os.path.join(config.PROJ_DIR, "input/A_collection_of_apr_tools.xlsx")
    )
