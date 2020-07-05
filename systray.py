from infi.systray import SysTrayIcon


def create_system_tray(on_quit=None,title='App'):
    systray=SysTrayIcon(None,title,on_quit=on_quit)
    systray.start()
    return systray

