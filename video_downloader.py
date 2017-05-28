from __future__ import unicode_literals
from tkinter import *
from tkinter.filedialog import *
import youtube_dl
import threading


class MyLogger(object):
	def debug(selg, msg):
		pass

	def waring(self, msg):
		pass

	def error(self, msg):
		download_button['state'] = NORMAL
		print(msg)


def my_hook(d):
	if d['status'] == 'finished':
		download_button['state'] = NORMAL
		print('Downloaing finished.')


#主窗口
def main_window():
	global root
	global var_URL
	global var_Folder
	global download_button

	root = Tk()                     
	root.geometry('400x140')  
	root.resizable(width=False, height=False)

	#url
	var_url = StringVar()
	label_url = Label(root, textvariable=var_url)
	var_url.set('URL:')
	label_url.place(x=10, y=15)

	#url text
	var_URL = StringVar()
	text_url = Entry(root, textvariable=var_URL)
	text_url.place(x=55, y=10, width=250, height=25)

	#checkbox
	var_to_mp3 = IntVar()
	checkbox_to_mp3 = Checkbutton(root, text = "To Mp3", variable = var_to_mp3, onvalue = 1, offvalue = 0)
	checkbox_to_mp3.place(x=315, y=8)

	#folder
	var_folder = StringVar()
	label_folder = Label(root, textvariable=var_folder)
	var_folder.set('Folder:')
	label_folder.place(x=10, y=50)

	#folder text
	var_Folder = StringVar()
	text_url = Entry(root, state=DISABLED, textvariable=var_Folder)
	text_url.place(x=55, y=45, width=250, height=25)

	#open button
	open_button = Button(root, text='Open', command=c_save)
	open_button.place(x=320, y=45, height=25, width=65)

	#download button
	download_button = Button(root, text='Download', command=create_download_thread)
	download_button.place(x=150, y=90, height=25, width=70)

	#进入消息循环
	root.mainloop()      


#选择保存路径
def c_save():
	rep = askdirectory()
	var_Folder.set(rep)


#创建下载线程
def create_download_thread():
	download_button['state'] = DISABLED
	t = threading.Thread(target=video_download, name='DownloadThread')
	t.start()


#下载函数
def video_download():
	ydl_opts['outtmpl'] = var_Folder.get() + '/%(title)s.%(ext)s'
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([var_URL.get()])



#全局变量
root = None
var_URL = None
var_Folder = None
open_button = None
ydl_opts = {
	#'proxy': '127.0.0.1:8085',
	'outtmpl': 'video/%(title)s.%(ext)s',
	'logger': MyLogger(),
	'progress_hooks': [my_hook],
}


if __name__ == '__main__':
	main_window()