import sys
import sqlite3

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн

        self.con = sqlite3.connect("coffee.sqlite")

        self.cur = self.con.cursor()

        names = self.cur.execute(f"""SELECT name FROM coffee""").fetchall()

        for i in names:
            self.comboBox.addItem(i[0])

        self.comboBox.addItem('qwerty')
        self.run(names[0][0])

        self.comboBox.currentIndexChanged.connect(self.run)

    def run(self, name):
        name = self.comboBox.currentText()
        parameters = self.cur.execute(f"""SELECT * FROM coffee WHERE name = '{name}'""").fetchall()[0]
        for i in parameters:
            print(i)
        self.label_8.setText(parameters[1])
        if parameters[1]:
            self.label_3.setText('молотый')
        else:
            self.label_3.setText('в зернах')

        self.label_4.setText(parameters[4])

        self.label_6.setText(f'{parameters[5] // 100} руб. {parameters[5] % 100} коп.')

        size = f'{parameters[6]}x{parameters[7]}x{parameters[8]}'

        if parameters[3] == 0:
            self.label_7.setText('Светлая')
        elif parameters[3] == 1:
            self.label_7.setText('Средняя')
        else:
            self.label_7.setText('Темная')


        self.label_10.setText(size)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())