from tkinter import *
from tkinter.ttk import *
import ctypes

winuser = ctypes.windll.user32
wingdi  = ctypes.windll.gdi32


class TkDesktopTool(Tk):
    """
    一个基于Tk的windows桌面小工具窗口类.
    所有参数与方法均与Tk类相同,
    本类仅实现了一些纯Tk难以实现的功能.
    """

    def __init__(self, screenName=None, baseName=None, className="Tk", useTk=1):
        super().__init__(screenName, baseName, className, useTk)
        # 设置窗口为无边框
        self.overrideredirect(True)

        # 将窗口设置为桌面的子窗口
        def set_TkTool_on_desktop():
            winuser.SetParent(
                self.winfo_id(), winuser.FindWindowW(ctypes.c_wchar_p("Progman"), None)
            )
            self.wm_withdraw()
            self.after(10, lambda: self.wm_deiconify())
        self.after(10, lambda: set_TkTool_on_desktop())

        self.tk_move()

    def tk_move(self):
        """无边框窗体拖动实现"""
        mous_x, mous_y = None, None

        def mouse_down(event):
            nonlocal mous_x, mous_y
            mous_x, mous_y = event.x, event.y

        def mouse_move(event):
            winuser.MoveWindow(
                self.winfo_id(),
                event.x_root - mous_x,
                event.y_root - mous_y,
                self.winfo_width(),
                self.winfo_height(),
                True,
            )

        self.bind("<Button-1>", mouse_down)
        self.bind("<B1-Motion>", mouse_move)
