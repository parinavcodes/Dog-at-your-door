import win32gui
import win32ui
import win32con
import numpy as np


class WindowCapture:
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        self.window_name = window_name
        self.window_bound = win32gui.GetWindowRect(self.hwnd)
        # print(self.window_bound)
        # print(self.window_bound)
        self.w = int((self.window_bound[2]-self.window_bound[0])/1.75)
        self.h = int((self.window_bound[3]-self.window_bound[1])/1.95)
        self.offset_x = int(self.window_bound[0]+self.w*0.21)
        self.offset_y = int(self.window_bound[1]+self.h*0.35)

    def screenshot(self):
        # hwnd=self.hwnd
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(mfcDC, self.w, self.h)

        saveDC.SelectObject(dataBitMap)
        saveDC.BitBlt((0, 0), (self.w, self.h),
                      mfcDC, (int(self.w*0.21), int(self.h*0.35)), win32con.SRCCOPY)
        # dataBitMap.SaveBitmapFile(saveDC, "out3.bmp")
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]

        img = np.ascontiguousarray(img)

        return img

    # def move_window(self, x, y):
    #     win32gui.MoveWindow(
    #         self.hwnd, x, y, self.window_bound[2]-self.window_bound[0], self.window_bound[3]-self.window_bound[1], True)
    #     self.hwnd = win32gui.FindWindow(None, self.window_name)

    #     self.window_bound = win32gui.GetWindowRect(self.hwnd)

    #     self.w = int((self.window_bound[2]-self.window_bound[0])/1.75)
    #     self.h = int((self.window_bound[3]-self.window_bound[1])/1.95)

    # def bring_window_top(self, replace):
    #     import time
    #     print(type(replace))
    #     if replace == "":
    #         hwnd2 = win32gui.FindWindow(None, replace)
    #         win32gui.ShowWindow(hwnd2, 5)
    #         win32gui.SetForegroundWindow(hwnd2)
    #         print("replaced")
    #         time.sleep(3)
    #     else:
    #         self.move_window(0, 0)
    #         win32gui.ShowWindow(self.hwnd, 5)
    #         win32gui.SetForegroundWindow(self.hwnd)
    #         time.sleep(5)

        # self.window_bound = win32gui.GetWindowRect(self.hwnd)
        # # print(self.window_bound)
        # self.w = int((self.window_bound[2]-self.window_bound[0])/1.75)
        # self.h = int((self.window_bound[3]-self.window_bound[1])/1.95)
