import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.image import Image
from kivy.graphics import RenderContext, Rectangle
import pygame

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class BackdropWidget(Widget):
  def __init__(self, width, height):
    Widget.__init__(self)
    self.width = width
    self.height = height

    # Load backdrop
    self.canvas = RenderContext()
    self.bg = Image('player/gui/images/bg.png')
    self.bg.texture.wrap = 'repeat'
    self.bg.texture.uvsize = (self.width/512.0, self.height/512.0)
    with self.canvas:
      Rectangle(texture=self.bg.texture, size=(2,2), pos=(-1,-1))



class RootWidget(Widget):
  def __init__(self, width, height):
    Widget.__init__(self)
    self.width = width
    self.height = height

    self.layout = FloatLayout(size=(width, height))
    self.layout.add_widget(Label(text="Hello World!", pos_hint={'top': 1.2, 'x': -0.45}))
    self.layout.add_widget(Label(text="Test"))

    self.add_widget(BackdropWidget(width, height))
    self.add_widget(self.layout)

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
