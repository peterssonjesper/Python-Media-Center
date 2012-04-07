from Tkinter import *
from window import *
import ImageTk

class Msg:
	def __init__(self, window):
		self.window = window
		self.msgCanvas = False
		self.msg_img = ImageTk.PhotoImage(file="gui/images/msg_bg.png");
		self.window.register("msg", self.keypressAction)
	
	def viewMsg(self, string):
		if self.msgCanvas: # Remove old msg
			self.window.get_bg().delete(self.msgCanvas)
			self.window.get_bg().delete(self.textCanvas)
		self.msgCanvas = self.window.get_bg().create_image(self.window.get_resolution()['width']/2, self.window.get_resolution()['height']/2-150, image=self.msg_img);
		self.textCanvas = self.window.get_bg().create_text(self.window.get_resolution()["width"]/2, self.window.get_resolution()['height']/2-190, text=string, fill="white", anchor="center", font=("Helvectica", "24"), width=780);
		self.window.setFocus("msg")
	
	def hideMsg(self):
		if self.msgCanvas:
			self.window.get_bg().delete(self.msgCanvas)
			self.window.get_bg().delete(self.textCanvas)
			self.window.restoreFocus()
	
	def keypressAction(self, event):
		if event.keycode == 2359309 or event.keycode == 36 or event.keycode == 3473435 or event.keycode == 9: # Enter or esc
			self.hideMsg()
