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

import config
import os
import glob
import json
import re
import pandas as pd


def main():
    json_output_dir = os.path.join(config.OUTPUT_DIR, "json")
    json_files = glob.glob(f"{json_output_dir}/*.json")  # 获取所有 JSON 文件的路径
    json_output_dir = os.path.join(config.OUTPUT_DIR, "json_new")
    new_json_files = glob.glob(f"{json_output_dir}/*.json")
    json_files.extend(new_json_files)

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
            "Specification",
            "Tool Category",
            "Bug Types",
        ]
    )
    for json_file in json_files:
        print(f"Parsing {json_file}...")
        # df = pd.read_json(json_file)
        with open(json_file, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
            df_new.loc[len(df_new)] = [
                data_dict["Title"],
                data_dict["APR Tool Name"],
                data_dict["Authors"],
                int(data_dict["Year"]),
                data_dict["Venue"],
                data_dict["Repo URL"],
                data_dict["Target Language"],
                data_dict["Used Dataset"],
                data_dict["CCF Rank"],
                data_dict["Paper Category"],
                data_dict["Bibtex"],
                data_dict["Specification"],
                data_dict["Tool Category"],
                data_dict["Bug Types"],
            ]
    df_new.sort_values(
        by=["Year", "Title"], ascending=False, inplace=True, ignore_index=True
    )
    excel_path = os.path.join(config.OUTPUT_DIR, "apr_literature_metadata.xlsx")
    print(df_new)

    df_new.to_excel(excel_path, index=True, index_label="ID")
    df_new.index = range(1, len(df_new) + 1)
    markdown_table_content = df_new[
        [
            "Title",
            "APR Tool Name",
            "Year",
            "Venue",
            "Repo URL",
            "Target Language",
            "Used Dataset",
            "CCF Rank",
        ]
    ].to_markdown(index=True)

    readme_path = os.path.join(config.PROJ_DIR, "../README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    # matches = re.findall('## APR Tool List \(sorted by year\).*', readme_content, flags=re.DOTALL)
    updated_content = re.sub(
        "## APR Tool List \(sorted by year\).*",
        f"## APR Tool List (sorted by year)\n\n{markdown_table_content}",
        readme_content,
        flags=re.DOTALL,
    )
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    # with open(os.path.join(config.OUTPUT_DIR, 'apr_literature_metadata.md'), 'w', encoding='utf-8') as f:
    #     f.write(markdown_table_content)


if __name__ == "__main__":
    main()
