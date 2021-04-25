import sys

import random
import os
from shutil import copyfile
import sqlite3
from math import sqrt
from PIL import Image, ImageDraw, ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QMenuBar, \
    QAction, QInputDialog, QColorDialog, QSlider, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets


class infopokaz(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle('Информация')
        self.lbl = QLabel(self)
        self.lbl.setGeometry(QtCore.QRect(15, 15, 385, 250))
        self.btn = QPushButton('Ок', self)
        self.btn.setGeometry(QtCore.QRect(180, 260, 40, 40))
        self.btn.clicked.connect(self.close)
        f = open('materialsforproject/info.txt', encoding='utf8').read()
        self.lbl.setText(f)


class BrushkaRisovashka(QWidget):  # класс открывающий окно с кистью и ластиком
    def __init__(self, sender):
        super().__init__()
        self.setFixedSize(560, 650)
        self.setWindowTitle('Кисть')
        self.do_paint = False
        self.mode = ''
        im = Image.open('materialsforproject/copy1.png')
        im.save('materialsforproject/copy3.png')  # изменяемая
        im.save('materialsforproject/copy4.png')  # фон для ластика
        self.send = sender
        self.lbl = QLabel('', self)
        self.lbl.setGeometry(QtCore.QRect(30, 20, 470, 550))
        self.button = QPushButton('', self)
        self.button.setGeometry(QtCore.QRect(30, 580, 30, 30))
        self.button.clicked.connect(self.changecolor)
        self.color = (255, 255, 255)
        self.button.setStyleSheet(
            "background-color: #FFFFFF}")
        self.pushButton_2 = QtWidgets.QPushButton('', self)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 580, 30, 30))
        self.pushButton_2.setIcon(QtGui.QIcon('materialsforproject/pipetka.png'))
        self.pushButton_2.clicked.connect(self.getcolor)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.move(30, 620)
        self.slider.resize(200, 25)
        self.slider.setMinimum(1)
        self.slider.setMaximum(200)
        self.radius = 1
        self.slider.valueChanged.connect(self.changevalue)
        self.radiuslabel = QLabel('Радиус: 1', self)
        self.radiuslabel.move(250, 600)
        self.radiuslabel.resize(300, 50)
        self.ok = QPushButton('Готово', self)
        self.otmena = QPushButton('Отмена', self)
        self.ok.setGeometry(QtCore.QRect(410, 580, 60, 30))
        self.ok.clicked.connect(self.gotovo)
        self.otmena.setGeometry(QtCore.QRect(470, 580, 60, 30))
        self.otmena.clicked.connect(self.close)
        self.drawimage()

    def changecolor(self):
        color = QColorDialog.getColor()
        color1 = tuple(int(color.name().lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        self.color = color1
        self.button.setStyleSheet(
            "background-color: {}".format(color.name()))

    def changevalue(self):
        self.radius = self.slider.value()
        self.radiuslabel.setText(f"Радиус: {self.radius}")

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        im = Image.open('materialsforproject/copy3.png')
        xf = x - ((470 - im.size[0]) // 2) - 30
        yf = y - ((550 - im.size[1]) // 2) - 20
        if self.mode == 'getcolor' and im.size[0] >= xf > 0 and im.size[1] >= yf > 0:
            pixels = im.load()
            r, g, b, a = pixels[xf, yf]
            self.color = r, g, b, a
            self.mode = ''
            self.button.setStyleSheet(
                "background-color: rgb{}".format(self.color))
        elif (event.button() == Qt.LeftButton):
            self.mode = 'risovat'
            self.draw(xf, yf, self.radius)
        elif (event.button() == Qt.RightButton):
            self.mode = 'eraser'
            self.erase(xf, yf, self.radius)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        r = self.radius
        im = Image.open('materialsforproject/copy3.png')
        xf = x - 30
        yf = y - ((550 - im.size[1]) // 2) - 20
        if self.mode == 'risovat':
            self.draw(xf, yf, r)
        elif self.mode == 'eraser':
            self.erase(xf, yf, r)

    def draw(self, xf, yf, r):
        im = Image.open('materialsforproject/copy3.png')
        draw = ImageDraw.Draw(im)
        draw.ellipse((
            (xf - r, yf - r),
            (xf + r, yf + r)),
            self.color)
        im.save('materialsforproject/copy3.png')
        self.drawimage()

    def mouseReleaseEvent(self, event):
        self.mode = ''

    def erase(self, xf, yf, r):  # ластик
        im = Image.open('materialsforproject/copy3.png')
        pixels = im.load()
        im1 = Image.open('materialsforproject/copy4.png')
        peckels = im1.load()
        minix, maxx = max([xf - r, 0]), min([xf + r, im.size[0]])
        miniy, maxy = max([yf - r, 0]), min([yf + r, im.size[1]])
        for i in range(minix, maxx):
            for j in range(miniy, maxy):
                rasst = int(sqrt((xf - i) ** 2 + (yf - j) ** 2))
                if rasst <= r:
                    t, h, n, a = peckels[i, j]
                    pixels[i, j] = t, h, n, a
        im.save('materialsforproject/copy3.png')
        self.drawimage()

    def drawimage(self):
        ima = QPixmap('materialsforproject/copy3.png')
        self.lbl.setPixmap(ima)

    def getcolor(self):
        self.mode = 'getcolor'

    def gotovo(self):
        self.send.prinyatrisovashku()
        self.close()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(930, 620)
        self.setWindowTitle('Photopaint')
        self.can_use = False
        self.mode = ''
        self.points = []
        im = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
        im.save('materialsforproject/copy1.png')
        im.save('materialsforproject/copy2.png')
        self.tableWidget = QtWidgets.QTableWidget(self)  # список фильтров
        self.tableWidget.setGeometry(QtCore.QRect(590, 130, 331, 192))
        self.label = QtWidgets.QLabel('X курсора:', self)  # здесь информация справа сверху
        self.label.setGeometry(QtCore.QRect(590, 30, 141, 16))
        self.label_2 = QtWidgets.QLabel('Y курсора:', self)
        self.label_2.setGeometry(QtCore.QRect(740, 30, 181, 16))
        self.label_3 = QtWidgets.QLabel('Разрешение картинки:', self)
        self.label_3.setGeometry(QtCore.QRect(590, 70, 331, 16))
        self.pushButton_2 = QtWidgets.QPushButton('', self)  # кнопки слева
        self.pushButton_2.setGeometry(QtCore.QRect(10, 80, 31, 31))
        self.pushButton_2.setIcon(QtGui.QIcon('materialsforproject/kistochka.png'))  # иконки
        self.pushButton_2.clicked.connect(self.risovat)
        self.pushButton = QtWidgets.QPushButton('', self)
        self.pushButton.setGeometry(QtCore.QRect(10, 40, 31, 31))
        self.pushButton.clicked.connect(self.cropimage)
        self.pushButton.setIcon(QtGui.QIcon('materialsforproject/ramka.png'))  # иконки
        self.pushButton_3 = QtWidgets.QPushButton('', self)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 120, 31, 31))
        self.pushButton_3.clicked.connect(self.drawkrug)
        self.pushButton_3.setIcon(QtGui.QIcon('materialsforproject/krug.png'))  # иконки
        self.pushButton_4 = QtWidgets.QPushButton('', self)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 160, 31, 31))
        self.pushButton_4.clicked.connect(self.drawpramougolnik)
        self.pushButton_4.setIcon(QtGui.QIcon('materialsforproject/pramougolnik.png'))  # иконки
        self.pushButton_5 = QtWidgets.QPushButton('', self)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 200, 31, 31))
        self.pushButton_5.clicked.connect(self.drawtreugolnik)
        self.pushButton_5.setIcon(QtGui.QIcon('materialsforproject/treugolnik.png'))  # иконки
        self.pushButton_6 = QtWidgets.QPushButton('', self)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 240, 31, 31))
        self.pushButton_6.clicked.connect(self.drawnechto)
        self.pushButton_6.setIcon(QtGui.QIcon('materialsforproject/polygon.png'))  # иконки
        self.pushButton_7 = QtWidgets.QPushButton('', self)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 280, 31, 31))
        self.pushButton_7.clicked.connect(self.drawlinia)
        self.pushButton_7.setIcon(QtGui.QIcon('materialsforproject/linia.png'))  # иконки
        self.menubar = QMenuBar(self)
        self.menushka1 = self.menubar.addMenu("Файл")  # создание менюшек
        self.newaction = QAction('&Создать', self)
        self.newaction.triggered.connect(self.createnew)
        self.openaction = QAction('&Открыть', self)
        self.openaction.triggered.connect(self.opennew)
        self.saveaction = QAction('&Сохранить', self)
        self.saveaction.triggered.connect(self.save)
        self.saveasaction = QAction('&Сохранить как', self)
        self.saveasaction.triggered.connect(self.saveas)
        self.exitaction = QAction('&Выйти', self)
        self.exitaction.triggered.connect(self.zakrit)
        self.menushka1.addAction(self.newaction)
        self.menushka1.addAction(self.openaction)
        self.menushka1.addAction(self.saveaction)
        self.menushka1.addAction(self.saveasaction)
        self.menushka1.addSeparator()
        self.menushka1.addAction(self.exitaction)
        self.menushka2 = self.menubar.addMenu("Изображение")  # создание менюшек
        self.brightaction = QAction('&Яркость', self)
        self.brightaction.triggered.connect(self.brightcontrol)
        self.kontrastaction = QAction('&Контраст', self)
        self.kontrastaction.triggered.connect(self.kontrastcontrol)
        self.povpochaction = QAction('&Повернуть по часовой', self)
        self.povpochaction.triggered.connect(self.rightrotate)
        self.povprochaction = QAction('&Повернуть против часовой', self)
        self.povprochaction.triggered.connect(self.leftrotate)
        self.menushka2.addAction(self.brightaction)
        self.menushka2.addAction(self.kontrastaction)
        self.menushka2.addAction(self.povpochaction)
        self.menushka2.addAction(self.povprochaction)
        self.menushka3 = self.menubar.addMenu("Коррекция")  # создание менюшек
        self.bluraction = QAction('&Размытие', self)
        self.bluraction.triggered.connect(self.blurcreate)
        self.alphaction = QAction('&Прозрачность', self)
        self.alphaction.triggered.connect(self.changealpha)
        self.shumaction = QAction('&Шум', self)
        self.shumaction.triggered.connect(self.noisecreate)
        self.menushka3.addAction(self.bluraction)
        self.menushka3.addAction(self.alphaction)
        self.menushka3.addAction(self.shumaction)
        self.menushka4 = self.menubar.addMenu("Фильтры")  # создание менюшек
        self.negativaction = QAction('&Негатив', self)
        self.negativaction.triggered.connect(self.negative)
        self.whiteblackaction = QAction('&Черно-белый', self)
        self.whiteblackaction.triggered.connect(self.whiteblack)
        self.greyaction = QAction('&Обесцвечивание', self)
        self.greyaction.triggered.connect(self.seriy)
        self.sepiaction = QAction('&Сепия', self)
        self.sepiaction.triggered.connect(self.sepia)
        self.anaglifaction = QAction('&Анаглиф', self)
        self.anaglifaction.triggered.connect(self.makeanagliph)
        self.menushka4.addAction(self.negativaction)
        self.menushka4.addAction(self.whiteblackaction)
        self.menushka4.addAction(self.greyaction)
        self.menushka4.addAction(self.sepiaction)
        self.menushka4.addAction(self.anaglifaction)
        self.menushka5 = self.menubar.addMenu("Справка")  # создание менюшек
        self.infoaction = QAction('&О программе', self)
        self.infoaction.triggered.connect(self.infoshow)
        self.menushka5.addAction(self.infoaction)
        self.setMouseTracking(True)
        self.imagelbl = QLabel(self)
        self.imagelbl.move(80, 40)
        self.imagelbl.resize(480, 560)
        self.imagelbl.setMouseTracking(True)
        self.button = QPushButton('', self)
        self.button.setGeometry(QtCore.QRect(10, 320, 30, 30))  # меняющая цвет
        self.button.clicked.connect(self.changecolor)
        self.color = (255, 255, 255)
        self.button.setStyleSheet(
            "background-color: #FFFFFF}")
        self.mnogougolnikok = QPushButton('Ок', self)  # многоугольника
        self.mnogougolnikok.setGeometry(QtCore.QRect(10, 360, 31, 31))
        self.mnogougolnikotmena = QPushButton('Отмена', self)
        self.mnogougolnikotmena.setGeometry(QtCore.QRect(10, 400, 61, 31))
        self.mnogougolnikotmena.hide()
        self.mnogougolnikok.hide()
        self.mnogougolnikotmena.clicked.connect(self.otmenamnogougolnika)
        self.mnogougolnikok.clicked.connect(self.makemnogougolnik)
        copyfile("materialsforproject/photobase.db", "materialsforproject/photobase1.db")
        self.bd = sqlite3.connect("materialsforproject/photobase1.db")  # базы данных подъехали

    def createnew(self):  # создание холста
        self.bd.close()
        copyfile("materialsforproject/photobase.db", "materialsforproject/photobase1.db")
        self.bd = sqlite3.connect("materialsforproject/photobase1.db")
        self.width, ok_pressed = QInputDialog.getInt(
            self, "Введите ширину", "Введите ширину изображения",
            470, 1, 470, 1)
        if ok_pressed:
            self.height, ok_pressed = QInputDialog.getInt(
                self, "Введите высоту", "Введите высоту изображения",
                550, 1, 550, 1)
            if ok_pressed:
                color = QColorDialog.getColor()
                if color.isValid():
                    self.fname, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                                  "Название файла")
                    if ok_pressed:
                        self.fname = self.fname + '.png'
                        h = color.name().lstrip('#')
                        color = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # hex в ргб
                        color = (color[0], color[1], color[2], 255)
                        im = Image.new("RGBA", (self.width, self.height), color)
                        if len(im.load()[0, 0]) == 3:
                            im.putalpha(255)
                        im.save('materialsforproject/copy1.png')
                        im.save('materialsforproject/copy2.png')
                        self.can_use = True
                        self.drawimage(im.size[0], im.size[1])

    def opennew(self):  # открытие картинки
        self.bd.close()
        copyfile("materialsforproject/photobase.db", "materialsforproject/photobase1.db")
        self.bd = sqlite3.connect("materialsforproject/photobase1.db")
        self.fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        if self.fname != '':
            im = Image.open(self.fname)
            x, y = im.size
            if y > 550:
                coeff = 550 / y
                im.thumbnail((int(x * coeff), int(y * coeff)), Image.ANTIALIAS)
            if x > 470:
                coeff = 470 / x
                im.thumbnail((int(x * coeff), int(y * coeff)), Image.ANTIALIAS)
            if len(im.load()[0, 0]) == 3:
                im.putalpha(255)
            im.save('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            self.drawimage(im.size[0], im.size[1])
            self.can_use = True
            self.drawbase()

    def save(self):
        im = Image.open('materialsforproject/copy1.png')
        if self.fname[-3:] == 'jpg':
            im1 = im.convert('RGB')
            im1.save(self.fname)
        else:
            im.save(self.fname)
        self.bd.close()
        os.remove("materialsforproject/photobase.db")
        os.rename("materialsforproject/photobase1.db", "materialsforproject/photobase.db")
        copyfile("materialsforproject/photobase.db", "materialsforproject/photobase1.db")
        self.bd = sqlite3.connect("materialsforproject/photobase1.db")

    def saveas(self):
        name = QFileDialog.getSaveFileName(self, 'Выбрать картинку', '',
                                           'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        if name != '':
            im = Image.open('materialsforproject/copy1.png')
            if name[-3:] == 'jpg':
                im1 = im.convert('RGB')
                im1.save(name)
            else:
                im.save(name)
            oldname = self.fname
            self.fname = name
            cur = self.bd.cursor()
            cur.execute("""UPDATE first
            SET fname = ?
            WHERE fname = ?""", [self.fname, oldname])
            self.bd.commit()
            self.bd.close()
            os.remove("materialsforproject/photobase.db")
            os.rename("materialsforproject/photobase1.db", "materialsforproject/photobase.db")
            copyfile("materialsforproject/photobase.db", "materialsforproject/photobase1.db")
            self.bd = sqlite3.connect("materialsforproject/photobase1.db")

    def brightcontrol(self):
        bright, ok_pressed = QInputDialog.getInt(
            self, "Введите яркость", "Введите силу освещения",
            1, 1, 100, 1)
        if ok_pressed and self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            pixels = im.load()
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    r = pixels[i, j][0] + bright
                    g = pixels[i, j][1] + bright
                    b = pixels[i, j][2] + bright
                    a = pixels[i, j][3]
                    r = max([0, r])
                    r = min(255, r)
                    g = max([0, g])
                    g = min(255, g)
                    b = max([0, b])
                    b = min(255, b)
                    pixels[i, j] = (r, g, b, a)
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Яркость')

    def kontrastcontrol(self):
        kontrast, ok_pressed = QInputDialog.getInt(
            self, "Введите контраст", "Введите увеличение контрастности",
            1, 1, 10, 1)
        if ok_pressed and self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            im1 = Image.new('RGBA', im.size)
            avg = 0
            for x in range(im.size[0]):
                for y in range(im.size[1]):
                    r, g, b, a = im.getpixel((x, y))
                    avg = avg + (r * 0.299 + g * 0.587 + b * 0.114)
            avg /= im.size[0] * im.size[1]
            palette = []
            for i in range(256):
                temp = int(avg + kontrast * (i - avg))
                temp = max([0, temp])
                temp = min([255, temp])
                palette.append(temp)
            for x in range(im.size[0]):
                for y in range(im.size[1]):
                    z = im.getpixel((x, y))
                    r, g, b, a = z
                    im1.putpixel((x, y), (palette[r], palette[g], palette[b], a))
            im1.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Контраст')

    def rightrotate(self):  # повороты
        if self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            im1 = im.transpose(Image.ROTATE_270)
            im1.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Поворот направо')

    def leftrotate(self):  # повороты
        if self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            im1 = im.transpose(Image.ROTATE_90)
            im1.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Поворот налево')

    def blurcreate(self):  # размытие
        rad, ok_pressed = QInputDialog.getInt(
            self, "Введите радиус", "Введите радиус размытия",
            1, 1, 100, 1)
        if ok_pressed and self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            im1 = im.filter(ImageFilter.GaussianBlur(radius=rad))
            im1.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Размытие')

    def noisecreate(self):  # шум
        if self.can_use:
            chanse = [True] + [False] * 100
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            pixels = im.load()
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    if random.choice(chanse):
                        pixels[i, j] = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Шум')

    def negative(self):
        if self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            pixels = im.load()
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    r, g, b, a = pixels[i, j]
                    pixels[i, j] = 255 - r, 255 - g, 255 - b, a
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Негатив')

    def whiteblack(self):
        if self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            pixels = im.load()
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    r, g, b, a = pixels[i, j]
                    if (r + g + b) / 3 > 128:
                        r, g, b = 255, 255, 255
                        pixels[i, j] = r, g, b, a
                    else:
                        r, g, b = 0, 0, 0
                        pixels[i, j] = r, g, b, a
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Черно-белый')

    def seriy(self):
        if self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            pixels = im.load()
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    r, g, b, a = pixels[i, j]
                    gray = int(r * 0.2 + g * 0.7 + b * 0.1)  # чтобы смотрелось не средне а с учетом яркости
                    pixels[i, j] = gray, gray, gray
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Обесцвечивание')

    def sepia(self):
        if self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            pixels = im.load()
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    r, g, b, a = pixels[i, j]
                    r = int(r * 0.4 + g * 0.75 + b * 0.2)
                    g = int(r * 0.35 + g * 0.7 + b * 0.2)
                    b = int(r * 0.3 + g * 0.5 + b * 0.13)
                    pixels[i, j] = r, g, b, a
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Сепия')

    def changealpha(self):
        percents, ok_pressed = QInputDialog.getInt(
            self, "Введите прозрачность", "Введите процент непрозрачности",
            100, 1, 100, 1)
        if ok_pressed and self.can_use:
            alpha = int(2.55 * percents)
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            im.putalpha(alpha)
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Смена прозрачности')

    def risovat(self):
        if self.can_use:
            self.testclass = BrushkaRisovashka(self)
            self.testclass.show()

    def infoshow(self):
        if self.can_use:
            self.a = infopokaz()
            self.a.show()

    def drawimage(self, x, y):
        self.label_3.setText('Разрешение картинки: ' + f"{x} на {y}")
        risovat = QPixmap('materialsforproject/copy1.png')
        self.imagelbl.setPixmap(risovat)

    def mouseMoveEvent(self, event):  # когда мышка двигается
        self.label.setText('X курсора:' + str(event.x() - 80))
        self.label_2.setText('Y курсора:' + str(event.y() - 40))

    def prinyatrisovashku(self): # когда фотка с кисточки приходит
        im = Image.open('materialsforproject/copy1.png')
        im.save('materialsforproject/copy2.png')
        im = Image.open('materialsforproject/copy3.png')
        im.save('materialsforproject/copy1.png')
        self.drawimage(im.size[0], im.size[1])
        self.addtodatabase('Кисточка')

    def cropimage(self):
        self.mode = 'crop'
        self.points = []

    def drawkrug(self):
        self.mode = 'krug'
        self.points = []

    def drawpramougolnik(self):
        self.mode = 'pramougolnik'
        self.points = []

    def mousePressEvent(self, event):  # когда жмут на мышку
        if not bool(self.mode):
            pass
        elif self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            xf = event.x() - 80
            yf = event.y() - ((560 - im.size[1]) // 2) - 40
            if xf not in range(0, im.size[0] + 1) or yf not in range(0, im.size[1] + 1):
                pass
            elif self.mode == 'crop':
                if self.points:
                    im = Image.open('materialsforproject/copy1.png')
                    im.save('materialsforproject/copy2.png')
                    im1 = im.crop((min([self.points[0], xf]), min([self.points[1], yf]),
                                    max([self.points[0], xf]), max([self.points[1], yf])))
                    im1.save('materialsforproject/copy1.png')
                    self.mode = ''
                    self.points = []
                    self.drawimage(im1.size[0], im1.size[1])
                    self.addtodatabase('Обрезание')
                else:
                    self.points.append(xf)
                    self.points.append(yf)
            elif self.mode == 'krug':
                if self.points:
                    im = Image.open('materialsforproject/copy1.png')
                    im.save('materialsforproject/copy2.png')
                    draw = ImageDraw.Draw(im)
                    draw.ellipse(((min([self.points[0], xf]), min([self.points[1], yf])),
                                  (max([self.points[0], xf]), max([self.points[1], yf]))), self.color)
                    im.save('materialsforproject/copy1.png')
                    self.mode = ''
                    self.points = []
                    self.drawimage(im.size[0], im.size[1])
                    self.addtodatabase('Нечто круглое')
                else:
                    self.points.append(xf)
                    self.points.append(yf)
            elif self.mode == 'pramougolnik':
                if self.points:
                    im = Image.open('materialsforproject/copy1.png')
                    im.save('materialsforproject/copy2.png')
                    draw = ImageDraw.Draw(im)
                    draw.rectangle(((self.points[0], self.points[1]), (xf, yf)), self.color)
                    im.save('materialsforproject/copy1.png')
                    self.mode = ''
                    self.points = []
                    self.drawimage(im.size[0], im.size[1])
                    self.addtodatabase('Прямоугольник')
                else:
                    self.points.append(xf)
                    self.points.append(yf)
            elif self.mode == 'treugolnik':
                if self.points:
                    if len(self.points) > 2:
                        im = Image.open('materialsforproject/copy1.png')
                        im.save('materialsforproject/copy2.png')
                        draw = ImageDraw.Draw(im)
                        draw.polygon(((self.points[0], self.points[1]),
                                       (self.points[2], self.points[3]), (xf, yf)), self.color)
                        im.save('materialsforproject/copy1.png')
                        self.mode = ''
                        self.points = []
                        self.drawimage(im.size[0], im.size[1])
                        self.addtodatabase('Треугольник')
                    else:
                        self.points.append(xf)
                        self.points.append(yf)
                else:
                    self.points.append(xf)
                    self.points.append(yf)
            elif self.mode == 'linia':
                if self.points:
                    im = Image.open('materialsforproject/copy1.png')
                    im.save('materialsforproject/copy2.png')
                    draw = ImageDraw.Draw(im)
                    draw.line((self.points[0], self.points[1], xf, yf), fill=self.color, width=self.shirina)
                    im.save('materialsforproject/copy1.png')
                    self.mode = ''
                    self.points = []
                    self.drawimage(im.size[0], im.size[1])
                    self.addtodatabase('Линия')
                else:
                    self.points.append(xf)
                    self.points.append(yf)
            elif self.mode == 'mnogougolnik':
                self.points.append((xf, yf))

    def changecolor(self):
        color = QColorDialog.getColor()
        if color != '':
            color1 = tuple(int(color.name().lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))  # hex to rgb
            self.color = color1
            self.button.setStyleSheet(
                "background-color: {}".format(color.name()))

    def makeanagliph(self):
        delta, ok_pressed = QInputDialog.getInt(
            self, "Введите значение", "Введите силу расхождения",
            10, 1, 10, 1)
        if ok_pressed and self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            specialcopy = im.copy()
            pixels = im.load()
            peckels = specialcopy.load()
            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    r, g, b, a = pixels[i, j]  # забирает красный из одной копии
                    pixels[i, j] = 0, g, b, a
                    r, g, b, a = peckels[i, j]  # и оставляет только красный в другой
                    peckels[i, j] = r, 0, 0
            for i in range(im.size[0] - delta):
                for j in range(im.size[1]):
                    r, g, b, a = pixels[i + delta, j]  # смешивает слои с отставанием нижнего
                    a, s, d, v = peckels[i, j]
                    pixels[i + delta, j] = a, g, b, a
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Анаглиф')

    def keyPressEvent(self, event):  # когда жмут на клавиатуру
        if int(event.modifiers()) == (QtCore.Qt.ControlModifier):
            if event.key() == QtCore.Qt.Key_Z:
                self.undown()

    def undown(self):
        if self.can_use:
            im = Image.open('materialsforproject/copy2.png')
            im.save('materialsforproject/copy1.png')
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Отмена')

    def drawtreugolnik(self):
        self.mode = 'treugolnik'
        self.points = []

    def drawnechto(self):
        self.mode = 'mnogougolnik'
        self.points = []
        self.mnogougolnikok.show()
        self.mnogougolnikotmena.show()

    def drawlinia(self):
        width, ok_pressed = QInputDialog.getInt(
            self, "Введите значение", "Введите ширину линии",
            10, 1, 10, 1)
        if ok_pressed:
            self.mode = 'linia'
            self.points = []
            self.shirina = width

    def otmenamnogougolnika(self):
        self.points = []
        self.mnogougolnikok.hide()
        self.mnogougolnikotmena.hide()

    def makemnogougolnik(self):
        if self.can_use:
            im = Image.open('materialsforproject/copy1.png')
            im.save('materialsforproject/copy2.png')
            draw = ImageDraw.Draw(im)
            draw.polygon(self.points, self.color)
            im.save('materialsforproject/copy1.png')
            self.mode = ''
            self.points = []
            self.mnogougolnikok.hide()
            self.mnogougolnikotmena.hide()
            self.drawimage(im.size[0], im.size[1])
            self.addtodatabase('Многоугольник')

    def addtodatabase(self, name):
        cur = self.bd.cursor()
        result = cur.execute("""SELECT MAX(number) FROM first
                    WHERE fname = ?""", [self.fname]).fetchone()
        if result[0] is None:
            result = [1, 0]
        cur.execute("INSERT INTO first(fname,number,aname) VALUES (?,?,?)", (self.fname, int(result[0]) + 1, name))
        self.bd.commit()
        self.drawbase()

    def drawbase(self):
        cur = self.bd.cursor()
        result = cur.execute("""SELECT number,aname FROM first
                            WHERE fname = ?""", [self.fname]).fetchall()
        if result is not None:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(1)
            for i, elem in enumerate(result):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(elem[1]))

    def zakrit(self):
        os.remove('materialsforproject/copy1.png')
        os.remove('materialsforproject/copy2.png')
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
