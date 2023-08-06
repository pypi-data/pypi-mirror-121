import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter.constants import END
import tkinter.messagebox as msg


# frame = ttk.Frame()
 
class HomePage1(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.resizable(0,0)
        self.root.geometry('%dx%d' % (400, 300))  # 设置窗口大小

        self.style = ttk.Style()
        self.style.configure('W.TButton', font = ('calibri', 10, 'bold', 'underline'),foreground = 'Green')


        self.createPage()
 
    def createPage(self):
        self.page = ttk.Frame(self.root)  # 创建Frame
        self.page.pack()

        btn_up = ttk.Button(self.page, text='up',width=12, command=self.keyevent_up).grid(row=1, column=2, pady=5)
        btn_down= ttk.Button(self.page, text='down',width=12, command=self.keyevent_down).grid(row=3, column=2, pady=5)
        btn_left = ttk.Button(self.page, text='left',width=12, command=self.keyevent_left).grid(row=2, column=1, pady=5)
        btn_right = ttk.Button(self.page, text='right',width=12, command=self.keyevent_right).grid(row=2, column=3, pady=5)
        btn_enter = ttk.Button(self.page, text='Enter',width=12, command=self.keyevent_select).grid(row=2, column=2, pady=5)

        ttk.Button(self.page, text='Back',width=12, command=self.keyevent_back).grid(row=4, column=1, pady=5)
        ttk.Button(self.page, text='Home',width=12, command=self.keyevent_home).grid(row=4, column=2, pady=5)
        ttk.Button(self.page, text='Menu',width=12, command=self.keyevent_menu).grid(row=4, column=3, pady=5)

        ttk.Button(self.page, text='Play/Pause',width=12, command=self.keyevent_play).grid(row=5, column=2, pady=5)
        ttk.Button(self.page, text='Volumn_up',width=12, command=self.keyevent_vol_up).grid(row=5, column=1, pady=5)
        ttk.Button(self.page, text='Volumn_down',width=12, command=self.keyevent_vol_down).grid(row=5, column=3, pady=5)

        short_ble = ttk.Button(self.page, text='Bluetooth',width=12, command=self.shortcut_bluetooth, style = 'W.TButton').grid(row=6, column=1, pady=5)
        short_wifi = ttk.Button(self.page, text='Wifi',width=12, command=self.shortcut_wifi, style = 'W.TButton').grid(row=6, column=2, pady=5)
        short_mirror = ttk.Button(self.page, text='Mirror',width=12, command=self.shortcut_mirror, style = 'W.TButton').grid(row=6, column=3, pady=5)


        input_guide = ttk.Label(self.page, text="input your text:")
        input_guide.grid(column=1, row=7, padx=5, pady=5)

        self.text = tk.StringVar()
        self.text_entry = ttk.Entry(self.page, textvariable=self.text)
        self.text_entry.grid(column=2, row=7)

        ttk.Button(self.page, text="Input", command=self.input_text).grid(column=3, row=7)



    def keyevent_up(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 19')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口
 
    def keyevent_down(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 20')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_left(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 21')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_right(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 22')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_select(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 23')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_back(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 4')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_home(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 3')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_menu(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 82')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_play(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 85')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_vol_up(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 24')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_vol_down(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 25')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def shortcut_bluetooth(self):
        subprocess.getstatusoutput('adb shell input keyevent 4')
        out = subprocess.getstatusoutput('adb shell  am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.controllers_bluetooth_devices.ControllersAndBluetoothActivity')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def shortcut_wifi(self):
        subprocess.getstatusoutput('adb shell input keyevent 4')
        out = subprocess.getstatusoutput('adb shell  am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.network.NetworkActivity')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def shortcut_mirror(self):
        out = subprocess.getstatusoutput('adb shell am start -n com.amazon.cast.sink/.DisplayMirroringSinkActivity')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def input_text(self, *args):
        value = str(self.text.get())
        out = subprocess.getstatusoutput(f'adb shell input text {value}')
        self.text_entry.delete(0, END)
        if out[0]==0:
            pass
        else:
            pass

    def connectPhone(self):
        self.page.destroy()
 
    def sayTry(self):
        msg.showinfo("Message", "手机连接失败,请尝试重新连接")  # 弹出消息窗口

    def sayFail(self):
        msg.showinfo("Message", "手机连接失败，未知错误")  # 弹出消息窗口

    #没有安装adb判断
    def sayNoadb(self):
        msg.showinfo("Message", "没有安装adb或者未配置adb环境变量")  # 弹出消息窗口


if __name__ == '__main__':
    root = tk.Tk()
    root.title('pyadb_GUI')
    
    HomePage1(root)
    root.mainloop()

def main():
    root = tk.Tk()
    root.title('pyadb_GUI')
    
    HomePage1(root)
    root.mainloop()
