import ctypes
import time
import subprocess
from abspath import resource_path


class VirtualDesktop:
    def __init__(self):
        self.virtual_desktop_accessor = ctypes.WinDLL(
            resource_path("VirtualDesktopAccessor.dll"))
        self.hwnd = None

    def launch_cam_app(self, command_lines, desktops=2):
        # for i in range(desktops):
        #     if i == 1:
        self.virtual_desktop_accessor.GoToDesktopNumber(1)
        time.sleep(2)  # Wait for the desktop to switch
        subprocess.Popen(command_lines, stdout=subprocess.PIPE,
                         shell=True)
        # time.sleep(20)  # Wait for apps to open their windows

    def main_desk(self):
        self.virtual_desktop_accessor.GoToDesktopNumber(
            0)  # Go back to the 1st desktop

    def enum_handler(self, hwnd, seq):
        import win32gui
        # import win32con
        if win32gui.IsWindowVisible(hwnd) and ("IMICamera.exe" in win32gui.GetWindowText(hwnd)) if seq == "visible" else ("python.exe" in win32gui.GetWindowText(hwnd) or "door_cam_detector" in win32gui.GetWindowText(hwnd)):
            # print(win32gui.GetWindowText(hwnd))
            # print(hwnd)
            self.hwnd = hwnd
            # if seq == "":
            #     win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
            # else:
            self.virtual_desktop_accessor.MoveWindowToDesktopNumber(
                self.hwnd, 1)
            # return False

    def move_app(self, seq=""):
        import win32gui
        win32gui.EnumWindows(self.enum_handler, seq)
        # self.hwnd = win32gui.FindWindow(
        #     None, "D:\\pycharm\\venv\\Scripts\\python3env\\Scripts\\python.exe")
        # print(self.hwnd)

    # command_lines = r"E: && cd IM Cam\IM* && IMICamera.exe "

    # launch_apps_to_virtual_desktops(command_lines)
    # move_app()


# virtual_desktop = VirtualDesktop()
# virtual_desktop.move_app()
