import cqh_image
from typing import ContextManager
import click
import win32clipboard
import win32con
import base64
import os
from PIL import ImageGrab
import io

import ctypes
#ctypes.windll.user32.MessageBoxW(0, msg, title, 1)

from contextlib import contextmanager

@contextmanager
def clipboard_context():
    try:
        win32clipboard.OpenClipboard()
        yield win32clipboard
    finally:
        win32clipboard.CloseClipboard()




@click.group()
def cli():
    pass


@click.command()
def image_to_base64():
    """
    把版粘贴的图片转成base64然后写到粘贴板里面
    """
    # https://www.cnblogs.com/liuwei0824/p/9547108.html
    # pillow的image 转成bytes

    pass
    image = ImageGrab.grabclipboard()
    if not image:
        raise ValueError("粘贴板里面不是图片")
    if isinstance(image, str):
        import sys
        print("iamge:{}".format(image), file=sys.stderr)
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
        win.SetClipboardData(win32con.CF_UNICODETEXT, image_base64)
        ctypes.windll.user32.MessageBoxW(0, "保存成功", "通知", 1)
        # toaster = ToastNotifier()
        # toaster.show_toast('cqh image',"图片转成base64成功D",   duration=10)
        # toaster.show_toast(title="This is a title", msg="This is a message",
        # icon_path=r"C:\Program Files\Internet Explorer\images\bing.ico", duration=10)






@click.command()
def base64_save():
    """
    把base64保存成图片
    """
    with clipboard_context() as win:
        try:
            data = win.GetClipboardData(win32con.CF_UNICODETEXT)
            start_text = "base64/"
            if not data.startswith(start_text):
                raise ValueError("粘贴板不是base64字符串, {}".format(data[:100]))
            data = data[len(start_text):]
            data_binary = base64.b64decode(data)
            pwd = os.getcwd()
            tmp_path = os.path.join(pwd, "tmp.png")
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            with open(tmp_path, "wb") as f:
                f.write(data_binary)

        except TypeError as e:
            print("格式错误,粘贴板里面可能是文本")
            raise
@click.command()
@click.option("--port", default=8082)
def serve(port):
    click.echo("port:{}".format(port))
    from cqh_image import __version__
    # print("dir:{}".format(vars(cqh_image)['__version__']))
    print("version: {}".format(__version__))
    from cqh_image.handler_image import HandlerImage
    from tornado import web, ioloop
    app = web.Application(handlers=[
        ("/image", HandlerImage),
    ])
    server = app.listen(port, xheaders=True)
    loop: ioloop.IOLoop = ioloop.IOLoop.current()
    loop.start()

cli.add_command(image_to_base64)
cli.add_command(base64_save)
cli.add_command(serve)


if __name__ == "__main__":
    cli()
