from __future__ import unicode_literals
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
import youtube_dl
import threading


class MyLogger(object):
	def debug(selg, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		download_button['state'] = NORMAL
		print(msg)


def hook_status(d):
	if d['status'] == 'finished':
		download_button['state'] = NORMAL
		print('Downloaing finished.')

def hook_progress(d):
	total_bytes = None
	if d['status'] == 'downloading':
		if 'total_bytes' in d.keys():
			total_bytes = float(d['total_bytes'])
		elif 'total_bytes_estimate' in d.keys():
			total_bytes = float(d['total_bytes_estimate'])
	if total_bytes != None:
		percent = float(d['downloaded_bytes'])/total_bytes*100.0
		progressbar['value'] = percent


#主窗口
def main_window():
	global root
	global var_URL
	global var_Folder
	global var_Proxy
	global download_button
	global progressbar

	root = Tk()
	root.title('Video Downloader')               
	root.geometry('400x200')  
	root.resizable(width=False, height=False)

	#url
	var_url = StringVar()
	label_url = Label(root, textvariable=var_url)
	var_url.set('URL:')
	label_url.place(x=10, y=15)

	#url text
	var_URL = StringVar()
	text_url = Entry(root, textvariable=var_URL)
	text_url.place(x=55, y=10, width=330, height=25)

	#folder
	var_folder = StringVar()
	label_folder = Label(root, textvariable=var_folder)
	var_folder.set('Folder:')
	label_folder.place(x=10, y=85)

	#folder text
	var_Folder = StringVar()
	text_url = Entry(root, state=DISABLED, textvariable=var_Folder)
	text_url.place(x=55, y=80, width=250, height=25)

	#proxy
	var_proxy = StringVar()
	label_proxy = Label(root, textvariable=var_proxy)
	var_proxy.set('Proxy:')
	label_proxy.place(x=10, y=50)

	#proxy text
	var_Proxy = StringVar()
	text_proxy = Entry(root, textvariable=var_Proxy)
	text_proxy.place(x=55, y=45, width=330, height=25)

	#open button
	open_button = Button(root, text='Open', command=c_save)
	open_button.place(x=320, y=80, height=25, width=65)

	#download button
	download_button = Button(root, text='Download', command=create_download_thread)
	download_button.place(x=165, y=160, height=25)

	#下载进度条
	#folder
	var_progress = StringVar()
	label_progress = Label(root, textvariable=var_progress)
	var_progress.set('Rate:')
	label_progress.place(x=10, y=122)
	progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=330, mode='determinate')
	progressbar.place(x=55, y=120)

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
	if var_Proxy.get() != '':
		ydl_opts['proxy'] = var_Proxy.get()
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([var_URL.get()])



#全局变量
root = None
var_URL = None
var_Folder = None
var_Proxy = None
download_button = None
progressbar = None
ydl_opts = {
	'logger': MyLogger(),
	'progress_hooks': [hook_status, hook_progress],
	'writesubtitles': True,
	'subtitleslangs': ['zh_CN'],
	'nocheckcertificate': True,
}


if __name__ == '__main__':
	main_window()