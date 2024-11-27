import tkinter  as tk  #tk as alias
from tkinter import ttk  #ttk themed tkinter widgets
import pygame

        

class MazeApp:
    def __init__(self): # constructor method< initialzies class , is automatically called>
         #everything in the GUI is in between this :start
        self.root = tk.Tk() #creates the main GUI window
        
        
        
        
        #and this :end 
        self.root.mainloop() # keeps the GUI open until the user closes it 
        
    
    

if __name__ =="__main__": #ensures the following code runs only if the script is executed directly (not imported as module)
    MazeApp() 