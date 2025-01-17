import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UIComponents.Usefuls import Usefuls

class TransitionalButton(tk.Canvas):
    def __init__(self, Root, OnClickFuncRef = None, bg=Usefuls.LightGrey, Mode="Side", OverlayImage = None, TwoTapToReverse=False, AutoPlay=True):

        self.Width = 125 if (Mode == "Side") else 30
        self.Height = 37 if (Mode == "Side") else 30

        super().__init__(Root, width=self.Width, height=self.Height, bg=bg, borderwidth=0, highlightthickness=0)

        self.AutoPlay = AutoPlay

        self.Mode = Mode
        self.TwoTapToReverse = TwoTapToReverse

        self.SideBarImage = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/TransitionalButton/SideBar.png").resize((125, 37), Image.ANTIALIAS))
        self.BottomBarImageR = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/TransitionalButton/BottomBarR.png").resize((30, 30), Image.ANTIALIAS))
        self.BottomBarImageL = ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/TransitionalButton/BottomBarL.png").resize((30, 30), Image.ANTIALIAS))

        self.OverlayImage = OverlayImage
        self.OnClickFuncRef = OnClickFuncRef

        self.IsHighlighted = False
        self.Cooldown = False

        self.SetUpUI()

    def OnClick(self):

        if (self.Cooldown):
            return

        if (self.OnClickFuncRef):
            self.OnClickFuncRef()

        if self.AutoPlay:
            self.Cooldown = True
            self.PlayAnimation(not self.IsHighlighted)

    def SetUpUI(self):
        self.SlideImage = self.create_image(self.Width, 0, image=self.SideBarImage if self.Mode == "Side" else self.BottomBarImageL if self.Mode == "BL" else self.BottomBarImageR, anchor="nw")
        self.ButtonID = self.create_image(0, 0, image=self.OverlayImage, anchor="nw")
        self.tag_bind(self.ButtonID, "<1>", lambda x :[self.OnClick()])
    
    def PlayAnimation(self, Reversed = False, Lerp = 0, CallbackFuncRef=None):

        if (Reversed == self.IsHighlighted): return

        if Lerp > 1:
            self.IsHighlighted = Reversed
            
            if self.IsHighlighted:
                self.Cooldown = not self.TwoTapToReverse
            else:
                self.Cooldown = False

            if (CallbackFuncRef):
                CallbackFuncRef()
            return

        LerpFlipped = Lerp * (-1 if Reversed else 1)

        self.moveto(self.SlideImage, ((LerpFlipped * self.Width) + (self.Width if Reversed else 0)) if self.Mode == "Side" else 0, ((LerpFlipped * self.Height) + (self.Height if Reversed else 0)) if self.Mode != "Side" else 0)

        self.after(10, lambda: [self.PlayAnimation(Reversed, Lerp = Lerp + 0.1 * (1 - Lerp + 0.01), CallbackFuncRef=CallbackFuncRef)])

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x150")
    root["bg"] = bg=Usefuls.LightGrey

    # create canvas
    myCanvas = TransitionalButton(root, Mode="Bottom", OverlayImage=ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/TransitionalButton/Info.png").resize((50, 50), Image.ANTIALIAS)))
    myCanvas.pack()
    
    myCanvas = TransitionalButton(root, Mode="Side", OverlayImage=ImageTk.PhotoImage(Image.open(Usefuls.DirectoryAbove + "/Image/TransitionalButton/CPP.png").resize((125, 37), Image.ANTIALIAS)))
    myCanvas.pack()
    # add to window and show
    root.mainloop()