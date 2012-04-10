import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.graphics import RenderContext, Rectangle
import pygame

class RootWidget(Widget):
  def __init__(self, width, height):
    Widget.__init__(self)
    self.canvas = RenderContext()
    self.bg = Image('player/gui/images/bg.png')
    self.bg.texture.wrap = 'repeat'
    self.bg.texture.uvsize = (width/512.0, height/512.0)
    with self.canvas:
      Rectangle(texture=self.bg.texture, size=(2,2), pos=(-1,-1))

class Window(App):
  def __init__(self):
    App.__init__(self)
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
    self.root = RootWidget(disp.current_w, disp.current_h)
    return self.root

  def render(self):
    self.run()
