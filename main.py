import tkinter  as tk  #tk as alias
from tkinter import filedialog, messagebox
from tkinter import ttk  #ttk themed tkinter widgets
import pygame

        

class MazeApp:
    def __init__(self,root): # constructor method< initialzies class , is automatically called>
         #everything in the GUI is in between this :start
        self.root = root #creates the main GUI window
        self.root.title("Maze Solver")
        self.canvas_width= 600  
        self.canvas_height= 400 
        self.gridsize = 20
        
        #buttons
        tk.Button(root, text="Upload Maze", command= self.upload_maze).pack(pady=5)
        
        
        
    def upload_maze(self):
         filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
         if filepath:
            self.process_image(filepath)
        
        
        #and this :end 
            self.root.mainloop() # keeps the GUI open until the user closes it 
        
    
    

if __name__ =="__main__": #ensures the following code runs only if the script is executed directly (not imported as module)
    root = tk.Tk()
    app= MazeApp(root)
    root.mainloop() 