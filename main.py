import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog
import traceback
from ui_file import Ui_Form as first
from addEditCoffeeForm import Ui_Form as second


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)


sys.excepthook = excepthook


class changeDB(QDialog, second):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        names = ex.cur.execute(f"""SELECT name FROM coffee""").fetchall()

        for i in names:
            self.comboBox.addItem(i[0])

        self.pushButton.clicked.connect(self.change)
        self.pushButton_2.clicked.connect(self.new)

        self.spinBox_2.setMaximum(10000)
        self.update()
        self.comboBox.currentIndexChanged.connect(lambda s: self.update())

        self.spinBox.setMaximum(10000)
        self.spinBox_3.setMaximum(10000)
        self.spinBox_4.setMaximum(10000)

        self.spinBox.setMinimum(10)
        self.spinBox_3.setMinimum(10)
        self.spinBox_4.setMinimum(10)

    def change(self, _):
        name = self.comboBox.currentText()

        if self.comboBox_3.currentText() == 'Светлая':
            d = 0
        elif self.comboBox_3.currentText() == "Средняя":
            d = 1
        else:
            d = 2

        ex.cur.execute(f"""UPDATE coffee 
        SET volume_x={self.spinBox.value()},
        volume_y={self.spinBox_3.value()},
        volume_z={self.spinBox_4.value()},
        price = {self.spinBox_2.value()},
        taste='{self.textEdit.toPlainText()}',
        ground={self.comboBox_3.currentIndex()},
        degreeOfRosting={self.comboBox_2.currentIndex()}
        WHERE name='{name}'""")

        ex.con.commit()
        self.close()
        ex.run(name)

    def new(self, _):
        name, ok_pressed = QInputDialog.getText(self, "Введите название кофе",
                                                "Новый кофе")
        if not ok_pressed:
            return
        ex.cur.execute(f"""INSERT INTO coffee (name)
        VALUES('{name}')""")

        ex.cur.execute(f"""UPDATE coffee 
        SET volume_x={self.spinBox.value()},
        volume_y={self.spinBox_3.value()},
        volume_z={self.spinBox_4.value()},
        price = {self.spinBox_2.value()},
        taste='{self.textEdit.toPlainText()}',
        ground={self.comboBox_3.currentIndex()},
        degreeOfRosting={self.comboBox_2.currentIndex()}
        WHERE name='{name}'""")

        ex.con.commit()
        self.close()
        ex.run(name)

        ex.comboBox.addItem(name)

    def update(self):
        name = self.comboBox.currentText()
        parameters = ex.cur.execute(f"""SELECT * FROM coffee WHERE name = '{name}'""").fetchall()[0]

        if parameters[2] == 0:
            self.comboBox_2.setCurrentText('Светлая')
        elif parameters[2] == 1:
            self.comboBox_2.setCurrentText('Средняя')
        else:
            self.comboBox_2.setCurrentText('Темная')

        if parameters[3]:
            self.comboBox_3.setCurrentText('Молотый')
        else:
            self.comboBox_3.setCurrentText('В зернах')

        self.textEdit.setText(parameters[4])

        self.spinBox_2.setValue(parameters[5])

        self.spinBox.setValue(parameters[6])
        self.spinBox_3.setValue(parameters[7])
        self.spinBox_4.setValue(parameters[8])


class MyWidget(QMainWindow, first):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")

        self.cur = self.con.cursor()

        names = self.cur.execute(f"""SELECT name FROM coffee""").fetchall()

        for i in names:
            self.comboBox.addItem(i[0])

        self.run(names[0][0])

        self.comboBox.currentIndexChanged.connect(self.run)

        self.pushButton.clicked.connect(self.openWindow)

    def run(self, name):
        name = self.comboBox.currentText()
        parameters = self.cur.execute(f"""SELECT * FROM coffee WHERE name = '{name}'""").fetchall()[0]

        self.label_8.setText(parameters[1])
        if parameters[3]:
            self.label_3.setText('Молотый')
        else:
            self.label_3.setText('В зернах')

        self.label_4.setText(parameters[4])

        self.label_6.setText(f'{parameters[5] // 100} руб. {parameters[5] % 100} коп.')

        size = f'{parameters[6]}x{parameters[7]}x{parameters[8]}'

        if parameters[2] == 0:
            self.label_7.setText('Светлая')
        elif parameters[2] == 1:
            self.label_7.setText('Средняя')
        else:
            self.label_7.setText('Темная')

        self.label_10.setText(size)

    def openWindow(self):
        window = changeDB(self)
        print('done')
        window.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())