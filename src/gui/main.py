from PyQt5 import QtWidgets
from appui import Ui_MainWindow
import threading
import time
import sys

from src.gui.task_logic import (MemoryProgress, ProccessProgress, DiskProgress,
                                MemoryData, DiskData, SystemInformation)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.system_data = SystemInformation()
        self.setSysinfo()

        self.ram_progress = MemoryProgress()
        self.ram_data = MemoryData()

        self.cpu_progress = ProccessProgress()

        self.disk_progress = DiskProgress()
        self.disk_data = DiskData()

        self.StartThread()
        self.actionAbout.triggered.connect(self.about)
        self.actionExit.triggered.connect(self.exit)
        th = threading.Thread(target=self.setStatsInfo)
        th.setDaemon(True)
        th.start()

    def setSysinfo(self):
        """
        Метод для заполнения раздела 'SystemInformation'
        """

        try:
            self._set_text_to_obj(self.pltf, self.system_data.get_platform())
            self._set_text_to_obj(self.pltf_ver, self.system_data.get_platform_version())
            self._set_text_to_obj(self.pltf_re, self.system_data.get_platform_release())
            self._set_text_to_obj(self.cpu, self.system_data.get_platform_processor())

            self._set_text_to_obj(self.ram, self.system_data.get_total_ram())
            self._set_text_to_obj(self.cpu_cores, self.system_data.get_cpu_count())

            self._set_text_to_obj(self.host, self.system_data.get_hostname())
            self._set_text_to_obj(self.ip, self.system_data.get_ip())

            self._set_text_to_obj(self.mac, self.system_data.get_mac())

        except:
            self.statusBar.showMessage("Error in getting System informations")

    @staticmethod
    def _set_text_to_obj(obj, text=""):
        """
        obj: QWidget из PyQt
        text: str

        Устанавливает text, как текстовое отображение объекта obj
        """
        obj.setText(obj.text() + " " + str(text))

    def StartThread(self):
        """
        В этом методе происходит подключение сигнала hook к методу обновления объекта QProgressBar,
        который обновляет интерфейс с текущими значением.
        Затем поток запускается с помощью self.ram_progress.start(), что вызывает метод run в отдельном потоке.

        На примере self.ram_progress:

        self.ram_progress.hook.connect(self.set_ram_progress):

        Здесь происходит подключение к self.ram_progress.hook функции self.set_ram_progress. Эта функция будет решать,
        что делать при передаче нового значения в self.ram_progress.hook (в нашем случае она обновляет полоску
        загруженности оперативной памяти).

        self.ram_progress.start():

        Запускаем в отдельном потоке функцию self.ram_progress.run(), которая каждую секунду передает
        значение в self.ram_progress.hook и, как мы рассмотрели выше,
        обновляет полоску загруженности оперативной памяти.

        То есть hook является просто сигналом, который, принимая значение в классе MemoryProgress (файл task_logic.py),
        через метод emit, пробрасывает его в метод set_ram_progress этого класса.
        Метод set_ram_progress, в свою очередь, передает объекту
        PyQt self.RamProgressBar (он отвечает за полоску заполнения оперативной памяти) значение,
        на которое нужно полоску обновить. И это происходит каждую секунду.
        """

        self.ram_progress.hook.connect(self.set_ram_progress)
        self.cpu_progress.hook.connect(self.set_cpu_progress)
        self.disk_progress.hook.connect(self.set_disk_progress)
        self.ram_progress.start()
        self.cpu_progress.start()
        self.disk_progress.start()

    def setStatsInfo(self):
        """
        Устанавливает значения загруженности ram и диска
        """
        try:
            while True:
                self._set_ram_info(
                    self.ram_data.get_available(),
                    self.ram_data.get_used(),
                )

                self._set_disk_info(
                    self.disk_data.get_total(),
                    self.disk_data.get_used(),
                    self.disk_data.get_free()
                )

                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting additional information about ram and cpu")

    def _set_ram_info(self, available_memory, used_memory):
        self.ram_info.setText(
            f"\nAvailable Memory :{available_memory} Go\n\nUsed Memory :{used_memory} Go")

    def _set_disk_info(self, total_disk, used_memory, free_disk):
        self.diskinfo.setText(
            f"\ntotal Disk  :{total_disk} Go\n\nused Disk  :{used_memory} Go\n\nfree Disk  :{free_disk} Go")

    def set_ram_progress(self, value):
        self.RamProgressBar.setValue(value)

    def set_cpu_progress(self, value):
        self.CpuProgressBar.setValue(value)

    def set_disk_progress(self, value):
        self.DiskProgressBar.setValue(value)

    def about(self):
        """
        Повоедение вкладки About
        """
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("About")
        msg.setText("PC Monitoring:\nVersion:1.0")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()

    def exit(self):
        """
        Повоедение вкладки Exit
        """
        QtWidgets.QApplication.quit()


app = QtWidgets.QApplication(sys.argv)
win = MyWindow()
sys.exit(app.exec_())
