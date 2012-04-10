import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
import pygame

class RootWidget(Widget):
  pass

class Window(App):
  def __init__(self):
    App.__init__(self)
    print dir(self)
    self.root = None;
    self.bg = None;

  def build(self):
    # get native screen resolution from pygame
    pygame.display.init()
    disp = pygame.display.Info()
    pygame.display.quit()

    # override config with fullscreen and our resolution
    Config.set('graphics', 'width', str(disp.current_w))
    Config.set('graphics', 'height', str(disp.current_h))
    Config.set('graphics', 'fullscreen', 'true')
    self.root = RootWidget()
    return self.root

  def setBackgroundImage(self):
    self.bg = Canvas(self.root, width=self.resolution['width'], height=self.resolution['height'], bg="black", highlightthickness=0);
    self.bg.img = ImageTk.PhotoImage(file="player/gui/images/bg.png");
    self.bg.create_image(self.resolution['width']/2, self.resolution['height']/2, image=self.bg.img);
  
    self.content = Canvas(self.frame, width=self.resolution['width'], height=self.resolution['height']);
    self.content.pack();
    self.content.create_window(0, 0, anchor="nw", window=self.bg, width=self.resolution['width'], height=self.resolution['height']);

  def render(self):
    self.run()
  
  def register(self, windowId, fn):
    pass
    self.keyPressRegisters.append((windowId, fn))

  #def get_bg(self):
  # return self.bg

  #def get_resolution(self):
  # return self.resolution;
