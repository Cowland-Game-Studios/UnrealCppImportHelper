'''

Efficiency Bottleneck is this file. 
If anyone has a more optomized solution file a PR. Thanks

'''

from bs4 import BeautifulSoup #to process page
import requests #to get page
import re #to replace html stuff
import math
import threading

def RemoveHTML(ListOfHTML) -> dict: #nested fucntion tsk tsk

    MapOfClassToLink = {}

    for i in range(len(ListOfHTML)):
        try:
            
            Elem = str(ListOfHTML[i])

            if "#idx_" in Elem: #remove table of contents tags
                continue

            Key = re.sub("<[^>]*>", "", Elem) #removes <a> tags
            UnprocessedLink = re.search("href=\".*\"", Elem).group(0) #extracts stuff between href="here"
            Value = re.sub("(href=|\")", "", UnprocessedLink).replace("id=content_link", "").replace("../", "https://docs.unrealengine.com/5.0/en-US/API/") #idk why id=contentlink has to be replaced, but im coding this at 10pm so just file a PR to remvoe this pls :)
            MapOfClassToLink[Key.lower()] = Value #adds new array elemetn thing
            
        except Exception as e:
            print(e)
            continue #need try except in case .group(0) doesn't work
        
        #regex from https://stackoverflow.com/questions/11229831/regular-expression-to-remove-html-tags-from-a-string/11230103
    
    return MapOfClassToLink

def GetAllCPPClasses(ProgressBar = None) -> dict:

    #Get stuff in url
    PageURL = "https://docs.unrealengine.com/en-US/API/Classes/index.html"
    PageToParse = requests.get(PageURL)

    Soup = BeautifulSoup(PageToParse.content, "html.parser")

    DictOfClasses = RemoveHTML(Soup.find_all("a",{"id":"content_link"}))

    return DictOfClasses 

def GetClassInclude(PageURL) -> str: #sends in URL of the class
    try:
        PageToParse = requests.get(PageURL.replace(" ", ""))
        Soup = BeautifulSoup(PageToParse.content, "html.parser")

        for PossibleHeaderLocations in Soup.find_all("td",{"class":"desc-cell"}):
            PossibleHeaderLocations = str(PossibleHeaderLocations)
            if "#include" in PossibleHeaderLocations:
                IncludeHeader = PossibleHeaderLocations
                break

        IncludeHeader = re.sub("<[^>]*>", "", IncludeHeader).strip()

        return IncludeHeader
    except:
        return f"Error, \"{PageURL}\" not found!"

if __name__ == "__main__":
  with open("text.txt", "w+") as f:
    f.write(str(GetAllCPPClasses()))
    #print(GetClassInclude("https://docs.unrealengine.com/en-US/API/Editor/GraphEditor/FZoomLevelsContainer/index.html"))