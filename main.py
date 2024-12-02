import tkinter as tk  
from tkinter import filedialog, messagebox
import pygame
from PIL import Image, ImageOps

        

class MazeApp:
    def __init__(self,root): # constructor method< initialzies class , is automatically called>
         #everything in the GUI is in between this :start
        self.root = root #creates the main GUI window
        self.root.title("Maze Solver")
        self.canvas_width= 600 
        self.canvas_height= 400 
        self.grid_size = 20
        
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        button_frame.pack(side="bottom", pady=10)

        #buttons
        tk.Button(button_frame, text="Upload Maze", command=self.upload_maze).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Draw Maze", command=self.draw_maze).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Solve Maze", command=self.solve_maze).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_canvas).grid(row=0, column=3, padx=5)
        
        #Canvas to displaying mazes
        self.canvas = tk.Canvas(root, width= self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=10)
        
        
        # Initialize pygame for interactive grid
        self.pygame_initialized = False
        
        
        
        
    def upload_maze(self):
         filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
         if filepath:
            self.process_image(filepath)
    
    def draw_maze(self):
        if not self.pygame_initialized:
            self.init_pygame()
        self.run_pygame()

    def solve_maze(self):
        pass

    def clear_canvas(self):
        self.canvas.delete("all")
        
    def process_image(self, filepath):
        #convert image to grayscale and binary
        image = Image.open(filepath)
        gray_image = ImageOps.grayscale(image)
        binary_image = gray_image.point(lambda p: 255 if p> 128 else 0, '1')
        binary_image.save("processed_maze.png")
        self.show_image("processed_maze.png")
        
    def show_image(self, filepath):
        img= tk.PhotoImage(file=filepath)
        self.canvas.create_image(0,0, anchor= tk.NW, image= img)
        self.root.mainloop()        
    
    def init_pygame(self):
        pygame.init()
        self.pygame_initialized = True
    
    def run_pygame(self):
        pygame.display.set_caption('maze solver') 
        screen= pygame.display.set_mode((self.canvas_width,self.canvas_height))
        screen.fill((255,255,255))  
        
        #grid logic
        for x in range(0, self.canvas_width,self.grid_size):
            for y in range(0, self.canvas_height, self.grid_size):
                rect= pygame.Rect(x,y, self.grid_size,self.grid_size)
                pygame.draw.rect(screen,(200,200,200),rect,1)
                
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running= False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    rect_x = (x // self.grid_size)*self.grid_size
                    rect_y = (y // self.grid_size)*self.grid_size
                    pygame.draw.rect(screen, (0,0,0), (rect_x,rect_y,self.grid_size,self.grid_size))
            
            pygame.display.flip()
        pygame.quit()
        
        
        
    
    

if __name__ =="__main__": #ensures the following code runs only if the script is executed directly (not imported as module)
    root = tk.Tk()
    app= MazeApp(root)
    root.mainloop() 