#dangerous code below, can be modified easily to a keylogger!!!

from pynput.keyboard import Key, Listener
import re

Keys = []
UnrealClassesDict = {}

def IsNotCharacter(Key):
  if "key" in Key.lower(): #to rid key.space, key.backspace
    return True
  return False

def ProcessStrokes(Key):
  
  global Keys, UnrealClassesDict
  
  Key = str(Key)
  
  if IsNotCharacter(Key): #on space pressed flush characters
    Keys = []
    return
  
  Keys.append(Key.replace("\'", "")) #add character into Keys
  
  if "".join(Keys) in list(UnrealClassesDict.keys()): #code if in statement
    print(UnrealClassesDict["".join(Keys)])
    Keys = []
  
  print(Keys)
  

if __name__ == "__main__":
  
  import BeautifulSoupHandler
  
  UnrealClassesDict = BeautifulSoupHandler.GetAllClasses()
  
  print("Classes loaded \n\n")
  
  with Listener(on_press = ProcessStrokes) as listener:   
      listener.join()