import tkinter as tk
from PIL import ImageTk, Image
import os

from Handlers.UI.TemplatePane import TemplatePane
from Handlers.UI.BitesTemplatePane import BitesTemplatePane

class MiscPane(TemplatePane):

    DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-2])

    def __init__(self, Root, SettingsHandler, width=400, height=50):
        super().__init__(Root, SettingsHandler, width, height)

        self.Root = Root
        self.Settings = SettingsHandler.GetAllData()

        self.SetUpMiscUI()

    def SetUpMiscUI(self):

        self.BitesPane = tk.Canvas(self.Root, width=720-142, height=50, bg="#121212", highlightthickness=0)

        self.BackgroundText = tk.Label(self.BitesPane, text="Bites", font=("Yu Gothic Bold", 30), bg="#121212", foreground="#FFF")
        self.BackgroundText.grid()

        self.MiscBites = BitesTemplatePane(self.BitesPane, "C++", self.SettingsHandler, Width=720-142, Height=300)
        self.MiscBites.grid()

        self.Add(self.BitesPane)

        self.AllWidgets = [self.BitesPane]

        #self.PlayAnimation()