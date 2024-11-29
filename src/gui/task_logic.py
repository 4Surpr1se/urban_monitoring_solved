import platform
import re
import socket
import time
import uuid

import psutil
from PyQt5.QtCore import QThread, pyqtSignal

from appui import Ui_MainWindow


class SystemInformation:
    @staticmethod
    def get_platform():
        """
        Функция возвращает платформу ПК (Windows, Linux, Mac OS X, etc.)
        """
        # TODO Задание 1
        return platform.system()

    @staticmethod
    def get_platform_version():
        """
        Функция возвращает версию платформы ПК
        """
        # TODO Задание 1
        return platform.version()

    @staticmethod
    def get_platform_release():
        """
        Функция возвращает версию релиза платформы ПК
        """
        # TODO Задание 1
        return platform.release()

    @staticmethod
    def get_platform_processor():
        """
        Функция возвращает процессор, используемый ПК
        """
        # TODO Задание 1
        return platform.processor()

    @staticmethod
    def get_total_ram():
        """
        Функция возвращает общее кол-во оперативной памяти, используемой ПК
        """
        # TODO Задание 2
        return round(psutil.virtual_memory().total / (1024.0 ** 3))

    @staticmethod
    def get_cpu_count():
        """
        Функция возвращает кол-во ядер процессора, используемых ПК
        """
        # TODO Задание 2
        return psutil.cpu_count()

    @staticmethod
    def get_hostname():
        """
        Функция возвращает имя хоста/домена ПК
        """
        # TODO Задание 2
        return socket.gethostname()

    @staticmethod
    def get_ip():
        """
        Функция возвращает ip ПК
        """
        # TODO Задание 2
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def get_mac():
        """
        Функция возвращает mac адерс сетевого интерфейса ПК
        """
        # TODO Задание 2
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


class MemoryProgress(QThread, Ui_MainWindow):
    """
    Поток для вычисления загрузки оперативной памяти в процентах в реальном времени
    """
    hook = pyqtSignal(int)

    def run(self):
        # TODO Задание 3
        try:
            while True:
                value = psutil.virtual_memory().percent
                self.hook.emit(int(value))
                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting Ram informations")


class ProccessProgress(QThread, Ui_MainWindow):
    """
    Поток для вычисления загрузки процессора в процентах в реальном времени
    """
    hook = pyqtSignal(int)

    def run(self):
        # TODO Задание 3
        try:
            while True:
                value = psutil.cpu_percent()
                self.hook.emit(int(value))
                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting Cpu informations")


class DiskProgress(QThread, Ui_MainWindow):
    """
    Поток для вычисления загрузки диска в процентах в реальном времени
    """
    hook = pyqtSignal(int)

    def run(self):
        # TODO Задание 3
        try:
            while True:
                obj_Disk = psutil.disk_usage('/')
                self.hook.emit(int(obj_Disk.percent))
                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting disk informations")


class MemoryData:
    # TODO Задание 4

    def get_available(self):
        """
        Метод для вычисления доступной оперативной памяти в реальном времени в Гб,
        метод будет вызывать ежесекундно.
        """
        return round(psutil.virtual_memory().available / (1024.0 ** 3), 2)

    def get_used(self):
        """
        Метод для вычисления используемой оперативной памяти в реальном времени в Гб,
        метод будет вызывать ежесекундно.
        """
        return round(psutil.virtual_memory().used / (1024.0 ** 3), 2)


class DiskData:
    # TODO Задание 4

    def __init__(self):
        self.psutil_disk_obj = psutil.disk_usage('/')

    def get_total(self):
        """
        Метод для вычисления общей ёмкости диска в реальном времени в Гб,
        метод будет вызывать ежесекундно.
        """
        return round(self.psutil_disk_obj.total / (1024.0 ** 3), 2)

    def get_free(self):
        """
        Метод для вычисления свободной ёмкости диска в реальном времени в Гб,
        метод будет вызывать ежесекундно.
        """
        return round(self.psutil_disk_obj.free / (1024.0 ** 3), 2)

    def get_used(self):
        """
        Метод для вычисления используемой ёмкости диска в реальном времени в Гб,
        метод будет вызывать ежесекундно.
        """
        return round(self.psutil_disk_obj.used / (1024.0 ** 3), 2)
