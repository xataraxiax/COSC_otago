'''
    Etude 6: Toothpicks
    File name: toothpicks.py
    Author: Stefan Pedersen 1427681
    Date created: 11/02/2017
    Date last modified: 14/02/2017
    Python Version: 2.7
'''
 
import sys, math
from Tkinter import *
generation = 0

#Toothpicks Frame
class Toothpicks(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
 
    def initUI(self):
        ratio = 1
        if len(sys.argv) == 3:
            order = int(sys.argv[1])
            ratio = float(sys.argv[2])
        else:
            order = int(sys.argv[1])
        generation = order 
        width = self.parent.winfo_screenheight()-80
        height = self.parent.winfo_screenheight()-80
        lineWidth = 2

        #calculate line-length based on order and ratio
        sum = 0
        for i in range(1, (order / 2) + 1):
            sum += pow(ratio, i*2)
        lineLength = (((width/2) / (1/1+sum))) -10
 
        self.parent.title("Toothpicks")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        draw(order, lineLength, lineWidth, width/2, height/2, canvas, ratio)

#Recursive draw function
def draw(n, lineLength, lineWidth, x, y, canvas, ratio): 
    x0 = x - lineLength*ratio
    x1 = x + lineLength*ratio
    y0 = y - lineLength*ratio
    y1 = y + lineLength*ratio
 
    if generation%2 == 0 and n == 0:
        canvas.create_line(x0, y, x1, y, width=lineWidth)
        canvas.pack(fill=BOTH, expand=1)
        return 
    if n == 0  or n == -1:
        return

    #create horizontal line
    canvas.create_line(x0, y, x1, y, width=lineWidth)

    #create vertical lines
    y0 = y - lineLength*ratio*ratio
    y1 = y + lineLength*ratio*ratio    
    canvas.create_line(x0, y0, x0, y1, width=lineWidth)
    canvas.create_line(x1, y0, x1, y1, width=lineWidth)
 
    draw(n-2, lineLength*ratio, lineWidth, x0, y0, canvas, ratio)
    draw(n-2, lineLength*ratio, lineWidth, x0, y1, canvas, ratio)
    draw(n-2, lineLength*ratio, lineWidth, x1, y0, canvas, ratio)
    draw(n-2, lineLength*ratio, lineWidth, x1, y1, canvas, ratio)
    
    canvas.pack(fill=BOTH, expand=1) 
 
def main():
    global width
    root = Tk()
    tp = Toothpicks(root) 
    width = root.winfo_screenheight()-80
    height = root.winfo_screenheight()-80
    root.geometry(str(width) + "x" + str(height))
    root.mainloop()
 
if __name__ == '__main__':
    main()
