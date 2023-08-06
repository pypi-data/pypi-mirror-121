from tornado import web
import win32clipboard
import win32con
from contextlib import contextmanager
from PIL import ImageGrab
import io
import base64
import os

@contextmanager
def clipboard_context():
    try:
        win32clipboard.OpenClipboard()
        yield win32clipboard
    finally:
        win32clipboard.CloseClipboard()

class HandlerImage(web.RequestHandler):

    def get(self):
        """
        获取图片
        """
        print("开始处理图片")
        # 终端有时候会卡死, 怎么办呢?
        image = ImageGrab.grabclipboard()

        if not image:
            # raise ValueError("粘贴板里面不是图片")
            print("没有图片")
            self.write({
                "code": -1,
                "message": "粘贴板没有图片",
                "data": ""
            })
            return
        if isinstance(image, list):
            # qq里面复制就是这种情况,郁闷了
            if os.path.exists(image[0]):
                data = open(image[0], 'rb').read()
        else:
        # data = image.tobytes()
            imgByteArr = io.BytesIO()
            image.save(imgByteArr, format='PNG')
            data = imgByteArr.getvalue()
        with clipboard_context() as win:
        
        
        
            # print("data:", data)
            image_base64 = base64.b64encode(data).decode("utf-8")
            # print("image_base64:", image_base64)
            image_base64 = "base64/"+image_base64
            # win.SetClipboardData(win32con.CF_UNICODETEXT, image_base64)
            # ctypes.windll.user32.MessageBoxW(0, "保存成功", "通知", 1)
            print("发送图片")
            self.write({
                "code": 0,
                "message": "ok",
                "data": image_base64,
            })
            return
        self.write({
            "code": -1,
            "message": "",
            "data": ""
        })

