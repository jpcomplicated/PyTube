from __future__ import unicode_literals
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
import youtube_dl
import threading
import queue


class MyLogger(object):
	def debug(selg, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		download_button['state'] = NORMAL
		print(msg)


def my_hook(d):
	total_bytes = None
	global _queue
	if d['status'] == 'finished':
		download_button['state'] = NORMAL
		progressbar['value'] = 100
		print('Downloaing finished.')

	if d['status'] == 'downloading':
		if 'total_bytes' in d.keys():
			total_bytes = float(d['total_bytes'])
		elif 'total_bytes_estimate' in d.keys():
			total_bytes = float(d['total_bytes_estimate'])
			if total_bytes != None:
				percent = float(d['downloaded_bytes'])/total_bytes*100.0
				progressbar['value'] = percent

	if 'elapsed' in d.keys():
		if None != d['elapsed']:
			seconds = int(d['elapsed'])
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			if m == 0:
				var_ElapsedTime.set('%ds' % s)
			elif h == 0:
				var_ElapsedTime.set('%dm%ds' % (m, s))
			else:
				var_ElapsedTime.set('%dh%dm%ds' % (h, m, s))

	if 'eta' in d.keys():
		if None != d['eta']:
			seconds = d['eta']
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			str_time = ''
			if m == 0:
				var_RemainingTime.set('%ds' % s)
			elif h == 0:
				var_RemainingTime.set('%dm%ds' % (m, s))
			else:
				var_RemainingTime.set('%dh%dm%ds' % (h, m, s))

	if 'speed' in d.keys():
		if None != d['speed']:
			speed = d['speed']/1024
			if speed > 1024:
				speed = speed/1024
				var_Speed.set('%.2fmb/s' % speed)
			else:
				var_Speed.set('%.1fkb/s' % speed)


#主窗口
def main_window():
	global root
	global var_URL
	global var_Folder
	global var_Proxy
	global download_button
	global progressbar
	global var_ElapsedTime
	global var_RemainingTime
	global var_Speed
	global _queue

	root = Tk()
	root.title('Video Downloader')               
	root.geometry('400x240')  
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
	open_button.place(x=315, y=80, height=25, width=70)

	#download button
	download_button = Button(root, text='Download', command=create_download_thread)
	download_button.place(x=165, y=200, height=25)

	#下载进度条
	var_progress = StringVar()
	label_progress = Label(root, textvariable=var_progress)
	var_progress.set('Rate:')
	label_progress.place(x=10, y=122)
	progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=330, mode='determinate')
	progressbar.place(x=55, y=120)

	#显示已用时间
	var_elapsed_time = StringVar()
	label_elapsed_time = Label(root, textvariable=var_elapsed_time)
	var_elapsed_time.set('Elapsed:')
	label_elapsed_time.place(x=10, y=160)

	var_ElapsedTime = StringVar()
	label_ElapsedTime = Label(root, textvariable=var_ElapsedTime)
	label_ElapsedTime.place(x=63, y=160)

	#显示剩余时间
	var_remaining_time = StringVar()
	label_remaining_time = Label(root, textvariable=var_remaining_time)
	var_remaining_time.set('Remaining:')
	label_remaining_time.place(x=138, y=160)

	var_RemainingTime = StringVar()
	label_RemainingTime = Label(root, textvariable=var_RemainingTime)
	label_RemainingTime.place(x=208, y=160)

	#显示下载速度
	var_speed = StringVar()
	label_speed = Label(root, textvariable=var_speed)
	var_speed.set('Speed:')
	label_speed.place(x=270, y=160)

	var_Speed = StringVar()
	label_Speed = Label(root, textvariable=var_Speed)
	label_Speed.place(x=315, y=160)


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
var_ElapsedTime = None
var_RemainingTime = None
var_Speed = None
ydl_opts = {
	'logger': MyLogger(),
	'progress_hooks': [my_hook],
	'writesubtitles': True,
	'subtitleslangs': ['zh_CN'],
	'nocheckcertificate': True,
}


if __name__ == '__main__':
	main_window()