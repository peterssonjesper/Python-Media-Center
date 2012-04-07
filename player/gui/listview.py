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
		self.leftTitle = False
		self.rightTitle = False
		self.detailedInfo = False
		self.poster = False
		self.posterData = False
		self.max_positions = int((self.window.get_resolution()['height']-70)/50.0-1)
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
		self.hl = self.window.get_bg().create_image(10, 110, image=self.hl_img, anchor="nw");
		self.printListItems();

	def setLeftTitle(self, title):
		if self.leftTitle:
			self.window.get_bg().delete(self.leftTitle)
		self.leftTitle = self.window.get_bg().create_text(35, 27, text=title, fill="white", anchor="nw", font=("Helvectica", "36"));

	def setRightTitle(self, title):
		if self.rightTitle:
			self.window.get_bg().delete(self.rightTitle)
		self.rightTitle = self.window.get_bg().create_text(self.window.get_resolution()['width']-35, 27, text=title, fill="white", anchor="ne", font=("Helvectica", "36"));

	def setDetailedInfo(self, info, posterData = False):
		self.unsetDetailedInfo()
		if posterData:
			try:
				self.posterData = ImageTk.PhotoImage(data=posterData)
				self.poster = self.window.get_bg().create_image(self.window.get_resolution()['width']-40, 110, image=self.posterData, anchor="ne");
			except:
				pass
		self.detailedInfo = self.window.get_bg().create_text(self.window.get_resolution()['width']-350, 600, text=info, fill="white", anchor="nw", font=("Helvectica", "16"), width=320);

	def unsetDetailedInfo(self):
		if self.detailedInfo:
			self.window.get_bg().delete(self.detailedInfo)
		if self.poster:
			self.window.get_bg().delete(self.poster)
	
	def printListItems(self):
		for l in self.labels:
			self.window.get_bg().delete(l)
		self.labels = []
		y_offset = 1
		for i in range(self.scope[0], self.scope[1]):
			f = self.listItems[i]
			self.labels.append(self.window.get_bg().create_text(25, 70+y_offset*50, text=f.get_label(), anchor="nw", fill="white", font=("Helvectica", "24"), width=800));
			y_offset += 1

	def keypressAction(self, event):
		if event.keycode == 8255233 or event.keycode == 116: # Arrow down
			if self.hlPos < self.max_positions-1 and self.hlPos < len(self.listItems)-1:
				self.hlPos += 1
				self.window.get_bg().move(self.hl, 0, 50);
				self.triggerHover();
			elif self.scope[1] < len(self.listItems):
				self.scope[0] += 1
				self.scope[1] += 1
				self.printListItems();
				self.triggerHover();

		elif event.keycode == 7993133 or event.keycode == 117: # Page down
			if self.hlPos < min(self.max_positions-1, len(self.listItems)-1): # The hl is not at the bottom
				self.window.get_bg().move(self.hl, 0, 50*(min(self.max_positions-self.hlPos-1, len(self.listItems)-1)));
				self.hlPos = min(self.max_positions-1, len(self.listItems)-1)
				self.triggerHover();
			elif self.hlPos == self.max_positions-1: # Hl at bottom
				self.scope[1] = min(self.max_positions+self.scope[1], len(self.listItems)-1)
				self.scope[0] = self.scope[1] - min(self.max_positions, self.listItems)
				self.printListItems();
				self.triggerHover();

		elif event.keycode == 7665452 or event.keycode == 112: # Page up
			if self.hlPos != 0: # The hl is not at the top
				self.window.get_bg().move(self.hl, 0, -50*self.hlPos);
				self.hlPos = 0;
				self.triggerHover();
			else: # Hl at top
				self.scope[0] = max(0, self.scope[0]-self.max_positions)
				self.scope[1] = min(self.max_positions+self.scope[0], len(self.listItems))
				self.printListItems();
				self.triggerHover();

		elif event.keycode == 8320768 or event.keycode == 111: # Arrow up
			if self.hlPos > 0:
				self.hlPos -= 1
				self.window.get_bg().move(self.hl, 0, -50);
				self.triggerHover();
			elif self.scope[0] > 0:
				self.scope[0] -= 1
				self.scope[1] -= 1
				self.printListItems();
				self.triggerHover();

		elif event.keycode == 2359309 or event.keycode == 36: # Enter
			selectedItem = self.scope[0]+self.hlPos
			self.onActionFn("enter", self.listItems[selectedItem])
			self.triggerHover();

		elif event.keycode == 3473435 or event.keycode == 9: # Esc
			selectedItem = self.scope[0]+self.hlPos
			if selectedItem < len(self.listItems):
				self.onActionFn("esc", self.listItems[selectedItem])
			else:
				self.onActionFn("esc", None)
			self.triggerHover();

		elif event.keycode == 6354696 or event.keycode == 71: # F5
			selectedItem = self.scope[0]+self.hlPos
			self.onActionFn("f5", self.listItems[selectedItem])

		else:
			print "Keypress: No match for key " + str(event.keycode)
	
	def triggerHover(self):
		currentItem = self.scope[0]+self.hlPos
		if len(self.listItems) > currentItem:
			self.onHoverFn(self.listItems[currentItem])
	
	def onAction(self, fn):
		self.onActionFn = fn

	def onHover(self, fn):
		self.onHoverFn = fn

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
