from Tkinter import *
from window import *
import ImageTk, time

class Msg:
	def __init__(self, window):
		self.window = window
		self.msgCanvas = False
		self.msg_img = ImageTk.PhotoImage(file="player/gui/images/msg_bg.png");
		self.window.register("msg", self.keypressAction)
	
	def viewMsg(self, string):
		self.hideMsg();
		self.msgCanvas = self.window.get_bg().create_image(0, self.window.get_resolution()['height']/2-160, image=self.msg_img, anchor="nw");
		self.textCanvas = self.window.get_bg().create_text(self.window.get_resolution()["width"]/2, self.window.get_resolution()['height']/2-80, text=string, fill="white", anchor="center", font=("Helvectica", "24"), justify="center");
		self.window.get_bg().update()
		self.window.setFocus("msg")
	
	def hideMsg(self):
		if self.msgCanvas:
			self.window.get_bg().delete(self.msgCanvas)
			self.window.get_bg().delete(self.textCanvas)
			self.window.get_bg().update()
			self.window.restoreFocus()
	
	def keypressAction(self, event):
		if event.keycode == 2359309 or event.keycode == 36 or event.keycode == 3473435 or event.keycode == 9: # Enter or esc
			self.hideMsg()
