import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UIComponents.Usefuls import Usefuls

class Slider(tk.Canvas):
    def __init__(self, Root, Bounds, StartValue = 0, OnChangeFuncRef = None, SnapTo = [], SnapThreashold = 1, bg=Usefuls.LightGrey):
        self.bg = bg

        super().__init__(Root, width=400, height=30, bg=self.bg, borderwidth=0, highlightthickness=0)

        self.BackgroundImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Slider/SliderBackground.png").resize((250, 4), Image.ANTIALIAS))
        self.DotButtonImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/Slider/SliderButton.png").resize((15, 15), Image.ANTIALIAS))
        
        self.OnChangeFuncRef = OnChangeFuncRef

        self.Value = StartValue
        self.Bounds = Bounds
        self.SnapTo = SnapTo + [self.Bounds[0], self.Bounds[1]]
        self.SnapThreashold = SnapThreashold

        self.SetUpUI()

    def SetUpUI(self):
        self.Background = self.create_image(7, 15, image=self.BackgroundImage, anchor="w")
        self.Button = self.create_image((self.Value + abs(self.Bounds[0])) / (abs(self.Bounds[0]) + self.Bounds[1]) * 250 + 7, 7, image=self.DotButtonImage, anchor="n")
        self.BackgroundOverlay = self.create_rectangle(0, 0, 0, 0, outline="", fill=Usefuls.Mint)
        self.HitDetector = self.create_rectangle(0, 0, 400, 30, outline="")
        self.tag_bind(self.HitDetector, "<B1-Motion>", lambda x: [self.OnClicked(x)])
        self.tag_bind(self.HitDetector, "<ButtonRelease>", lambda x: [self.OnClicked(x), self.OnChanged()])
        
        self.UpdateButtonPos()

    def UpdateButtonPos(self):
        self.coords(self.BackgroundOverlay, 0, 13, (self.Value + abs(self.Bounds[0])) / (abs(self.Bounds[0]) + self.Bounds[1]) * 250 + 1, 17)
        self.moveto(self.Button, ((self.Value + abs(self.Bounds[0])) / (abs(self.Bounds[0]) + self.Bounds[1]) * 250), 7)

    def OnChanged(self):
        if self.OnChangeFuncRef:
            self.OnChangeFuncRef(self.Value)

        print(self.Value)

    def OnClicked(self, Event, ValueOverride = None):
        NewValue = (((Event.x - 7) / 250) * (abs(self.Bounds[0]) + self.Bounds[1]) - abs(self.Bounds[0])) if ValueOverride is None else ValueOverride
        NewValue = round(NewValue * 1e3) / 1e3

        if NewValue >= self.Bounds[0] and NewValue <= self.Bounds[1]:
            self.Value = NewValue
        elif NewValue > self.Bounds[1]:
            self.Value = self.Bounds[1]
        elif NewValue < self.Bounds[0]:
            self.Value = self.Bounds[0]

        if (ValueOverride is None):
          Lowest = 10e9
          Snap = 0
          for Point in self.SnapTo:
              if (abs(self.Value - Point) < Lowest):
                  Lowest = abs(self.Value - Point)
                  Snap = Point
  
          if Lowest < self.SnapThreashold:
              self.Value = Snap

        self.UpdateButtonPos()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg=Usefuls.LightGrey

    # create canvas
    myCanvas = Slider(root, (-20, 30), 0, SnapTo=[ -10, 5, 10, 15], SnapThreashold=2)

    # add to window and show
    myCanvas.place(x=10, y=0, width=375, height=30, anchor="nw")
    root.mainloop()