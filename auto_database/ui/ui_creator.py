import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QPushButton,QFrame,QMessageBox
from Ui_apr_ui import Ui_MainWindow  #导入你写的界面类
import os,json

import config


from bib_parser import bibtex_parser
 
class MyMainWindow(QMainWindow,Ui_MainWindow): #这里也要记得改
    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

        self.textEdit.setPlaceholderText("Enter your bibtex here")
        self.pushButton_2.clicked.connect(self.on_clicked_2)
        self.pushButton.clicked.connect(self.on_clicked)

        self.authors, self.title, self.year = "", "", ""

    def on_clicked_2(self):
        print("Parsing the entered bibtex now")
        bibtex = self.textEdit.toPlainText()
        self.title, self.authors, self.year = bibtex_parser.parse_bibtex(bibtex)
        self.lineEdit_15.setText(f"{self.title}")
        self.lineEdit_19.setText(f"{self.year}")  
        self.lineEdit_21.setText(f"{', '.join(self.authors)}")

    def on_clicked(self):
        try:
            # write the data to a json file
            row_dict={} #['Title', 'APR Tool Name', 'Authors', 'Year', 'Venue', 'Repo URL', 'Target Language', 'Evaluated Dataset', 'CCF Rank', 'Paper Category', 'Bibtex'])
            row_dict["Title"] = self.title
            row_dict["APR Tool Name"] = self.lineEdit.text()
            row_dict["Authors"] = self.authors
            row_dict["Year"] = self.year
            row_dict["Venue"] = self.lineEdit_20.text()
            row_dict["Repo URL"] = self.lineEdit_22.text()
            row_dict["Target Language"] = self.lineEdit_23.text()
            row_dict["Used Dataset"] = self.lineEdit_2.text()
            row_dict["CCF Rank"] = self.lineEdit_24.text()
            row_dict["Paper Category"] = self.comboBox.currentText()
            row_dict["Bibtex"] = self.textEdit.toPlainText()

            row_dict["Specification"] = self.lineEdit_16.text()
            row_dict["Tool Category"] = self.lineEdit_17.text()
            row_dict["Bug Types"] = self.lineEdit_18.text()
            
            json_output_dir = os.path.join(config.OUTPUT_DIR, "json_new")
            if not os.path.exists(json_output_dir):
                os.makedirs(json_output_dir)
            json_output_path = os.path.join(json_output_dir, f"{self.year}-{get_formatted_title(self.title)}.json")
            if os.path.exists(json_output_path):
                overwrite = QMessageBox.information(self, "WARNING", f"JSON file already exists. Do you want to overwrite it?",QMessageBox.Yes|QMessageBox.No)
                if overwrite == QMessageBox.Yes:
                    print('Overwrite')
                    json.dump(row_dict, open(json_output_path, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
                else:
                    print('Skipped')
            else:
                json.dump(row_dict, open(json_output_path, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.information(self, "WARNING", f"Error while writing to json file: {e}")

def get_formatted_title(title):
    """
    format the title to a valid file name
    """
    return title.replace(':', '-').replace('?', '').replace(',', '')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())