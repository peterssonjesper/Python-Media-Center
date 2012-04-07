from Tkinter import *
from window import *
import ImageTk

class ListView:
	def __init__(self, window):
		self.window = window
		self.listItems = []
		self.labels = []
		self.scope = [0, 0]
		self.hlPos = -1
		self.title = False
		self.max_positions = int((self.window.get_resolution()['height']-80)/50.0-1)
		self.hl_img = ImageTk.PhotoImage(file="gui/images/highlighter.png");
		self.window.register("listview", self.keypressAction)
	
	def setListItems(self, new_items):
		self.listItems = new_items;
		self.scope = [0, min(self.max_positions, len(self.listItems))]
		self.hlPos = 0
		try:
			self.window.get_bg().delete(self.hl)
		except:
			pass
		self.hl = self.window.get_bg().create_image(self.window.get_resolution()['width']/2, 80, image=self.hl_img);
		self.printListItems();

	def setTitle(self, title):
		if self.title:
			self.window.get_bg().delete(self.title)
		self.title = self.window.get_bg().create_text(40, 50, text=title, fill="white", anchor="nw", font=("Helvectica", "24"));
	
	def printListItems(self):
		for l in self.labels:
			self.window.get_bg().delete(l)
		self.labels = []
		y_offset = 1
		for i in range(self.scope[0], self.scope[1]):
			f = self.listItems[i]
			self.labels.append(self.window.get_bg().create_text(self.window.get_resolution()["width"]/2-385, 15+y_offset*50, text=f.get_label(), anchor="nw", fill="white", font=("Helvectica", "24"), width=800));
			y_offset += 1

	def keypressAction(self, event):
		if event.keycode == 8255233 or event.keycode == 116: # Arrow down
			if self.hlPos < self.max_positions-1 and self.hlPos < len(self.listItems)-1:
				self.hlPos += 1
				self.window.get_bg().move(self.hl, 0, 50);
			elif self.scope[1] < len(self.listItems):
				self.scope[0] += 1
				self.scope[1] += 1
				self.printListItems();

		elif event.keycode == 7993133 or event.keycode == 117: # Page down
			if self.hlPos < min(self.max_positions-1, len(self.listItems)-1): # The hl is not at the bottom
				self.window.get_bg().move(self.hl, 0, 50*(min(self.max_positions-self.hlPos-1, len(self.listItems)-1)));
				self.hlPos = min(self.max_positions-1, len(self.listItems)-1)
			elif self.hlPos == self.max_positions-1: # Hl at bottom
				self.scope[1] = min(self.max_positions+self.scope[1], len(self.listItems)-1)
				self.scope[0] = self.scope[1] - min(self.max_positions, self.listItems)
				self.printListItems();

		elif event.keycode == 7665452 or event.keycode == 112: # Page up
			if self.hlPos != 0: # The hl is not at the top
				self.window.get_bg().move(self.hl, 0, -50*self.hlPos);
				self.hlPos = 0;
			else: # Hl at top
				self.scope[0] = max(0, self.scope[0]-self.max_positions)
				self.scope[1] = min(self.max_positions+self.scope[0], len(self.listItems))
				self.printListItems();

		elif event.keycode == 8320768 or event.keycode == 111: # Arrow up
			if self.hlPos > 0:
				self.hlPos -= 1
				self.window.get_bg().move(self.hl, 0, -50);
			elif self.scope[0] > 0:
				self.scope[0] -= 1
				self.scope[1] -= 1
				self.printListItems();

		elif event.keycode == 2359309 or event.keycode == 36: # Enter
			selectedItem = self.scope[0]+self.hlPos
			self.onActionFn("enter", self.listItems[selectedItem])

		elif event.keycode == 3473435 or event.keycode == 9: # Esc
			selectedItem = self.scope[0]+self.hlPos
			self.onActionFn("esc", self.listItems[selectedItem])

		elif event.keycode == 6354696 or event.keycode == 71: # F5
			selectedItem = self.scope[0]+self.hlPos
			self.onActionFn("f5", self.listItems[selectedItem])

		else:
			print "Keypress: No match for key " + str(event.keycode)
	
	def onAction(self, fn):
		self.onActionFn = fn

class ListItem:
	def __init__(self, label):
		self.label = label
		self.attrs = {}

	def get_label(self):
		return self.label;

	def setAttr(self, attr, val):
		self.attrs[attr] = val
	
	def getAttr(self, attr):
		try:
			return self.attrs[attr]
		except:
			return False
