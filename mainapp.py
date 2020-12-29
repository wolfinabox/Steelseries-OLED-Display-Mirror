from PySide2.QtWidgets import QMainWindow,QApplication
from PySide2.QtCore import QEvent
from PySide2.QtGui import QStatusTipEvent
from main_ui import Ui_MainWindow
import sys
from main import OLED_Displayer,SCT
import threading

def is_int(s:str):
    try:
        int(s)
        return True
    except Exception:
        return False

valid_oled_screens={
    'screened-128x36: Rival 700, Rival 710':(128,36),
    'screened-128x40: Apex 7, Apex 7 TKL, Apex Pro, Apex Pro TKL':(128,40),
    'screened-128x48: Arctis Pro Wireless':(128,48),
    'screened-128x52: GameDAC / Arctis Pro + GameDAC':(128,52)}


class Worker(threading.Thread):
    def __init__(self,device_size,width,height):
        super().__init__()
        self.device_size=device_size
        self.width=width
        self.height=height
        self.screen_bounds=(0,0,width,height)
        self.kill=threading.Event()
        
    def stop(self):
        self.kill.set()

    def stopped(self):
        return self.kill.is_set()

    def run(self):
        try:
            shower=OLED_Displayer(self.screen_bounds,self.device_size)
        except ConnectionError as e:
            
            return
        else:
            while True:
                if self.stopped(): return
                shower.run_frame()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.worker:Worker=None
        
        #add OLED devices
        for scrn,size in valid_oled_screens.items():
            self.ui.oled_device_box.addItem(scrn,size)
        # self.ui.oled_device_box.currentIndexChanged.connect(lambda i:print(self.ui.oled_device_box.itemData(i)))
        #set default res
        monitors=SCT.monitors
        width,height=[(monitor['width'],monitor['height']) for monitor in monitors if monitor['left']==0][0]
        self.ui.width_text.setText(str(width))
        self.ui.height_text.setText(str(height))
        self.ui.start_button.pressed.connect(self.start_worker)
        self.ui.stop_button.pressed.connect(self.stop_worker)
        self.ui.stop_button.setDisabled(True)
        self.event(QStatusTipEvent('https://github.com/wolfinabox/Steelseries-OLED-Display-Mirror'))
        
    def event(self, e):
        if e.type() == QEvent.StatusTip:
            if e.tip() == '':
                e = QStatusTipEvent('https://github.com/wolfinabox/Steelseries-OLED-Display-Mirror')
        return super().event(e)

    def start_worker(self):
        if self.worker is not None:return
        if not is_int(self.ui.width_text.text()) or not is_int(self.ui.height_text.text()):
            return
        for t in (self.ui.width_text,self.ui.height_text,self.ui.start_button,self.ui.oled_device_box):
            t.setDisabled(True)
        self.ui.stop_button.setEnabled(True)
        device_size=self.ui.oled_device_box.itemData(self.ui.oled_device_box.currentIndex())

        self.worker=Worker(device_size,int(self.ui.width_text.text()),int(self.ui.height_text.text()))
        self.worker.start()


    def stop_worker(self):
        self.worker.stop()
        self.worker.join()
        self.worker=None
        for t in (self.ui.width_text,self.ui.height_text,self.ui.start_button,self.ui.oled_device_box):
            t.setEnabled(True)
        self.ui.stop_button.setDisabled(True)


def main(args):
    app = QApplication(args)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    sys.exit(main(sys.argv))
