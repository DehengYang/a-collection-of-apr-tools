import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
)
from ui.Ui_apr_ui import Ui_MainWindow  # 导入你写的界面类
import os
import json
import glob
import config
from bib_parser import bibtex_parser


class MyMainWindow(QMainWindow, Ui_MainWindow):  # 这里也要记得改
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.textEdit.setPlaceholderText("Enter your bibtex here")

        # specifications
        self.lineEdit_specification.setPlaceholderText(
            "Possible candidates: test, issue, bug report, formal specification, etc."
        )
        # repo url
        self.lineEdit_repo_url.setPlaceholderText(
            "Enter the public repository of the APR tool, if available."
        )
        # target language
        self.lineEdit_target_language.setPlaceholderText(
            "Possible candidates: Java, Python, C, C++, etc. (if there exist multiple target languages, separate them by comma)."
        )
        # CCF rank
        self.lineEdit_ccf_rank.setPlaceholderText(
            "Possible candidates: A, B, C, other."
        )
        # Tool category
        self.lineEdit_tool_category.setPlaceholderText(
            "Possible candidates: search-based, semantics-based, learning-based, llm-based, etc."
        )
        # Bug types
        self.lineEdit_bug_types.setPlaceholderText(
            "Possible candidates: general bugs, syntax errors, vulnerabilities, etc. (if there exist multiple bug types, separate them by comma)."
        )

        self.pushButton_2.clicked.connect(self.on_clicked_2)
        self.pushButton.clicked.connect(self.on_clicked)

        self.authors, self.title, self.year = "", "", ""

    def on_clicked_2(self):
        print("Parsing the entered bibtex now")
        bibtex = self.textEdit.toPlainText()
        self.title, self.authors, self.year = bibtex_parser.parse_bibtex(bibtex)
        self.lineEdit_title.setText(f"{self.title}")
        self.lineEdit_year.setText(f"{self.year}")
        self.lineEdit_authors.setText(f"{', '.join(self.authors)}")

        files = glob.glob(
            f"{config.OUTPUT_DIR}/**/{self.year}-{get_formatted_title(self.title)}.json",
            recursive=True,
        )
        if len(files) > 0:
            assert len(files) == 1
            QMessageBox.information(
                self,
                "WARNING",
                f"JSON file already exists: {files[0]}.",
                QMessageBox.Yes,
            )
            with open(files[0], "r", encoding="utf-8") as f:
                data_dict = json.load(f)
                self.lineEdit_apr_tool_name.setText(data_dict["APR Tool Name"])
                self.lineEdit_venue.setText(data_dict["Venue"])
                self.lineEdit_repo_url.setText(data_dict["Repo URL"])
                self.lineEdit_target_language.setText(
                    ",".join(data_dict["Target Language"])
                )
                self.lineEdit_used_dataset.setText(",".join(data_dict["Used Dataset"]))
                self.lineEdit_ccf_rank.setText(data_dict["CCF Rank"])
                self.comboBox.setCurrentText(data_dict["Paper Category"])
                if data_dict["Specification"] != "-":
                    self.lineEdit_specification.setText(data_dict["Specification"])
                if data_dict["Tool Category"] != "-":
                    self.lineEdit_tool_category.setText(data_dict["Tool Category"])
                if data_dict["Bug Types"] != "-":
                    self.lineEdit_bug_types.setText(data_dict["Bug Types"])

    def on_clicked(self):
        try:
            # write the data to a json file
            row_dict = (
                {}
            )  # ['Title', 'APR Tool Name', 'Authors', 'Year', 'Venue', 'Repo URL', 'Target Language', 'Evaluated Dataset', 'CCF Rank', 'Paper Category', 'Bibtex'])
            row_dict["Title"] = self.title
            row_dict["APR Tool Name"] = self.lineEdit_apr_tool_name.text()
            row_dict["Authors"] = self.authors
            row_dict["Year"] = self.year
            row_dict["Venue"] = self.lineEdit_venue.text()
            row_dict["Repo URL"] = self.lineEdit_repo_url.text()
            row_dict["Target Language"] = self.lineEdit_target_language.text()
            row_dict["Used Dataset"] = self.lineEdit_used_dataset.text()
            row_dict["CCF Rank"] = self.lineEdit_ccf_rank.text()
            row_dict["Paper Category"] = self.comboBox.currentText()
            row_dict["Bibtex"] = self.textEdit.toPlainText()

            row_dict["Specification"] = self.lineEdit_specification.text()
            row_dict["Tool Category"] = self.lineEdit_tool_category.text()
            row_dict["Bug Types"] = self.lineEdit_bug_types.text()

            json_output_dir = os.path.join(config.OUTPUT_DIR, "json")
            if not os.path.exists(json_output_dir):
                os.makedirs(json_output_dir)
            json_output_path = os.path.join(
                json_output_dir, f"{self.year}-{get_formatted_title(self.title)}.json"
            )
            if os.path.exists(json_output_path):
                overwrite = QMessageBox.information(
                    self,
                    "WARNING",
                    "JSON file already exists. Do you want to overwrite it?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if overwrite == QMessageBox.Yes:
                    print("Overwrite")
                    json.dump(
                        row_dict,
                        open(json_output_path, "w", encoding="utf-8"),
                        indent=4,
                        ensure_ascii=False,
                    )
                else:
                    print("Skipped")
            else:
                json.dump(
                    row_dict,
                    open(json_output_path, "w", encoding="utf-8"),
                    indent=4,
                    ensure_ascii=False,
                )
        except Exception as e:
            QMessageBox.information(
                self, "WARNING", f"Error while writing to json file: {e}"
            )


def get_formatted_title(title):
    """
    format the title to a valid file name
    """
    return title.replace(":", "-").replace("?", "").replace(",", "")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
