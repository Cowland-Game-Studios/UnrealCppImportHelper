import tkinter as tk
import os
from PIL import ImageTk, Image
import threading
import webbrowser

from Handlers.SettingsHandler import YamlParser
from Handlers.UIComponents import IncrementSlider, ToggleSwitch, TransitionalButton
from Handlers.UI import InfoPane, SettingsPane, MiscPane, BlueprintsPane, CPPPane, DashboardPane

class App():

  DirectoryAbove = "/".join(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").split("/")[:-1])
  
  def __init__(self, SplashRef, AllCPPClasses):

    self.AllCPPClasses = AllCPPClasses

    self.window = SplashRef
    self.Width = 720
    self.Height = 512
    self.AllWidgets = []
    self.IsAnimating = False

    #Setup window
    self.window.geometry(f"{self.Width}x{self.Height}")
    self.window["bg"] = "#121212"
    self.window.title("Unrealify by Cowland Game Studios")
    self.window.resizable(False, False)
    self.window.focus_force()
    self.window.iconphoto(False, ImageTk.PhotoImage(file = App.DirectoryAbove + "/Image/Logo/Icon.png"))

    #Load images
    self.CowImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/Logo/Logo.png").resize((100, 100), Image.ANTIALIAS))
    self.CPPImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Cpp.png").resize((125, 37), Image.ANTIALIAS))
    self.BlueprintImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Blueprint.png").resize((125, 37), Image.ANTIALIAS))
    self.MiscImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Misc.png").resize((125, 37), Image.ANTIALIAS))
    self.SettingImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Settings.png").resize((30, 30), Image.ANTIALIAS))
    self.InfoImage = ImageTk.PhotoImage(Image.open(App.DirectoryAbove + "/Image/SideBar/Info.png").resize((30, 30), Image.ANTIALIAS))

    #Handlers
    self.SettingsHandler = YamlParser(App.DirectoryAbove + "/Configuration.yaml")
    self.Settings = self.SettingsHandler.GetAllData()

    #Reset the Opened
    YamlParser(App.DirectoryAbove + "/Data/Projects.yaml").Write("Opened", "")

    #Startup windows & processes
    self.SetUpSideBar()
    self.__ContinueLastLeft()

    #Last
    self.window.focus_force()

    self.window.protocol("WM_DELETE_WINDOW", self.Destroy)

  def __ContinueLastLeft(self):
    if (self.Settings["App"]["LastLeft"] == "Blueprints"):
      self.SetUpBlueprintsMenu()
    elif (self.Settings["App"]["LastLeft"] == "C++"):
      self.SetUpCPPMenu()
    elif (self.Settings["App"]["LastLeft"] == "Settings"):
      self.SetUpSettingsMenu()
    elif (self.Settings["App"]["LastLeft"] == "Misc"):
      self.SetUpMiscMenu()
    elif (self.Settings["App"]["LastLeft"] == "Info"):
      self.SetUpInformationMenu()
    else:
      self.SetUpDashboardMenu()

  def Loop(self):
    self.window.mainloop()

  def Destroy(self):
    self.Clear(Exiting=True)
    self.window.destroy()
    
  def SetUpSideBar(self):
    self.SideBar = tk.Frame(width=125, height=self.Height, bg="#2D2D2D")
    self.SideBar.pack(side=tk.LEFT, fill="y")

    #using tklabels because buttons shift down
    self.CowButton = tk.Label(self.SideBar, image=self.CowImage, relief=tk.FLAT, borderwidth=0, background="#2D2D2D")
    self.CowButton.bind("<1>", lambda x: [self.SetUpDashboardMenu()])
    self.CowButton.pack(pady=10)

    self.CPPButton = TransitionalButton.TransitionalButton(self.SideBar, OnClickFuncRef=self.SetUpCPPMenu, OverlayImage=self.CPPImage)
    self.CPPButton.pack(pady=5)

    self.BlueprintButton = TransitionalButton.TransitionalButton(self.SideBar, OnClickFuncRef=self.SetUpBlueprintsMenu, OverlayImage=self.BlueprintImage)
    self.BlueprintButton.pack(pady=5)

    self.MiscButton = TransitionalButton.TransitionalButton(self.SideBar, OnClickFuncRef=self.SetUpMiscMenu, OverlayImage=self.MiscImage)
    self.MiscButton.pack(pady=5)

    self.SettingButton = TransitionalButton.TransitionalButton(self.SideBar, Mode="BL", OnClickFuncRef=self.SetUpSettingsMenu, OverlayImage=self.SettingImage)
    self.SettingButton.place(x=0, y=self.Height, anchor="sw")

    self.InfoButton = TransitionalButton.TransitionalButton(self.SideBar, Mode="BR", OnClickFuncRef=self.SetUpInformationMenu, OverlayImage=self.InfoImage)
    self.InfoButton.place(x=125, y=self.Height, anchor="se")

  def SetNotAnimating(self):
    self.IsAnimating = False
  
  def ResetSideBar(self, SkipAnimations=False):

    if self.IsAnimating:
      return

    self.IsAnimating = True
    
    self.CowButton["image"] = self.CowImage

    self.CPPButton.PlayAnimation(False, 0, self.SetNotAnimating)
    self.BlueprintButton.PlayAnimation(False, 0, self.SetNotAnimating)
    self.MiscButton.PlayAnimation(False, 0, self.SetNotAnimating)

    self.SettingButton.PlayAnimation(False, 0, self.SetNotAnimating)
    self.InfoButton.PlayAnimation(False, 0, self.SetNotAnimating)

  def Clear(self, SkipAnimations=False, Exiting=False):

    self.window.overrideredirect(False) #do we have to keep this here?

    for Widget in self.AllWidgets:
      if Widget is not None:
        if hasattr(Widget, "OnExit") and Exiting:
          Widget.OnExit()
        Widget.destroy()
    self.AllWidgets = []

    self.ResetSideBar(SkipAnimations)

  def __AddPadding(self, Parent, Size = 3):
    tk.Label(Parent, text="", font=("Yu Gothic", Size), bg="#121212").pack()

  def SetUpDashboardMenu(self):
    ContentPane = self.SetUpUI()
    self.SettingsHandler.Write("App/LastLeft", "Dashboard")

    DashboardMenu = DashboardPane.DashboardPane(ContentPane, self.SettingsHandler, 720-142, 512)
    DashboardMenu.place(x=0, y=0)

    self.AllWidgets.append(
      DashboardMenu
    )

  def SetUpCPPMenu(self):
    self.CPPButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()
    
    self.SettingsHandler.Write("App/LastLeft", "C++")

    CPPMenu = CPPPane.CPPPane(ContentPane, self.SettingsHandler, 720-142, 512, self.AllCPPClasses)
    CPPMenu.place(x=0, y=0)

    self.AllWidgets.append(
      CPPMenu
    )
  
  def SetUpBlueprintsMenu(self):
    self.BlueprintButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()
    
    self.SettingsHandler.Write("App/LastLeft", "Blueprints")

    BlueprintsMenu = BlueprintsPane.BlueprintsPane(ContentPane, self.SettingsHandler, 720-142, 512)
    BlueprintsMenu.place(x=0, y=0)

    self.AllWidgets.append(
      BlueprintsMenu
    )

  def SetUpMiscMenu(self):
    self.MiscButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()

    self.SettingsHandler.Write("App/LastLeft", "Misc")

    MiscBites = MiscPane.MiscPane(ContentPane, self.SettingsHandler, 720-142, 512)
    MiscBites.place(x=0, y=0)

    self.AllWidgets.append(
      MiscBites
    )

  def SetUpSettingsMenu(self):
    self.SettingButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()

    self.SettingsHandler.Write("App/LastLeft", "Settings")

    SettingsMenu = SettingsPane.SettingsPane(ContentPane, self.SettingsHandler, 720-142, 512)
    SettingsMenu.grid(row=1)

    self.AllWidgets.append(
      SettingsMenu
    )

  def SetUpInformationMenu(self):
    self.InfoButton.PlayAnimation(True, CallbackFuncRef=self.SetNotAnimating)
    ContentPane = self.SetUpUI()
    
    self.SettingsHandler.Write("App/LastLeft", "Info")

    InfoMenu = InfoPane.InfoPane(ContentPane, self.SettingsHandler, 720-125, 512)
    InfoMenu.grid(row=1)

  def SetUpUI(self):
    self.Clear()

    ContentPane = tk.Canvas(width=self.Width - 125, height=self.Height, bg="#121212", highlightthickness=0)
    ContentPane.place(x = 125, y = 0, anchor = "nw")

    self.AllWidgets.append(ContentPane)

    return ContentPane
