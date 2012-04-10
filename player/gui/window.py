from Tkinter import *
import ImageTk

class Window:
	def __init__(self):
		self.root = Tk()
		self.bg = None;
		self.resolution = { "width" : 1920, "height" : 1080 };
		self.frame = Frame(self.root, width=self.resolution['width'], height=self.resolution['height']);
		self.root.bind("<Key>", self.keypressAction);
		self.frame.pack()
		self.setFullscreen();
		self.setBackgroundImage();
		self.keyPressRegisters = []
		self.focusedWindow = False

		self.focusStack = []

	def setBackgroundImage(self):
		self.bg = Canvas(self.root, width=self.resolution['width'], height=self.resolution['height'], bg="black", highlightthickness=0);
		self.bg.img = ImageTk.PhotoImage(file="player/gui/images/bg.png");
		self.bg.create_image(self.resolution['width']/2, self.resolution['height']/2, image=self.bg.img);
	
		self.content = Canvas(self.frame, width=self.resolution['width'], height=self.resolution['height']);
		self.content.pack();
		self.content.create_window(0, 0, anchor="nw", window=self.bg, width=self.resolution['width'], height=self.resolution['height']);

	def setFullscreen(self):
		self.root.geometry(str(self.resolution["width"]) + "x" + str(self.resolution["height"]) + "+0+0");
		self.root.focus_set()

	def onSelection(self, fn):
		self.onSelectionFunction = fn

	def onEscape(self, fn):
		self.onEscapeFunction = fn
	
	def render(self):
		self.root.mainloop()
	
	def register(self, windowId, fn):
		self.keyPressRegisters.append((windowId, fn))

	def get_bg(self):
		return self.bg

	def get_resolution(self):
		return self.resolution;

	def keypressAction(self, event):
		for registers in self.keyPressRegisters:
			if registers[0] == self.focusedWindow:
				registers[1](event)
				break
	
	def setFocus(self, windowId):
		self.focusStack = self.focusStack + [self.focusedWindow]
		self.focusedWindow = windowId
	
	def restoreFocus(self):
		self.focusedWindow = self.focusStack[-1]
		self.focusStack = self.focusStack[:-1]
