from Tkinter import *
import tkFileDialog
from PIL import ImageTk, Image
from tkColorChooser import askcolor
from fourNeigborsLabeling import *
import copy
from PIL import ImageGrab

class GUI:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.file_adress = None
        self.img = None
        self.out = None
        self.input_label = None
        self.output_label = None
        self.imheight = 512
        self.imwidth = 512
        self.hActual = 0
        self.wActual = 0
        self.currentColor = (255, 255, 255)
        self.image_count = 0
        self.labels = None
        self.imgHistory = []
        self.output_img = None
        self.final_image = None
        self.currentState = int(0)
        self.point1 = None
        self.point2 = None
        self.rect = None

        self.iFrame = Canvas(frame, height=self.imheight, width=self.imwidth, borderwidth=1, relief=RIDGE)
        self.iFrame.pack(side=RIGHT)
        self.iFrame.bind("<Button-1>", self.labiling)
        self.iFrame.pack_propagate(False)

        self.cFrame = Frame(frame, height=self.imheight, width=max(256, self.imwidth / 4))
        self.cFrame.pack(side=TOP)

        self.Buttonn = Button(self.cFrame, text="Pick Color", command=self.pickColor)
        self.Buttonn.pack(side=LEFT)

        self.Buttonn = Button(self.cFrame, text="Eraser", command=self.create_earser)
        self.Buttonn.pack(side=RIGHT)

        self.oFrame = Canvas(frame, height=self.hActual, width=self.wActual, borderwidth=1, relief=RIDGE)
        self.oFrame.pack(side=RIGHT)
        self.oFrame.pack_propagate(False)

    def openFile(self):

        self.file_address = tkFileDialog.askopenfilename(initialdir=".", title="Select Image",
                                                         filetypes=(("JPG Files", "*.jpg"),("PNG Files", "*.png")))
        self.img = Image.open(self.file_address).resize((self.imheight, self.imwidth), Image.ANTIALIAS)
        self.img = self.img.point(lambda p: p > 190 and 255)
        self.img = self.img.convert('1')
        pix = self.img.load()
        rowSize, columnSize = self.img.size
        pixelValues = [[0 for x in range(columnSize)] for y in range(rowSize)]

        for i in range(rowSize):
            for j in range(columnSize):
                pix[i, j] = converToBinaryValue(pix[i, j])
                pixelValues[i][j] = pix[i, j]
        (labels, output_img) = fourConnectedLabeling(self.img)
        self.labels = labels
        self.output_img = output_img
        image_for_append =  copy.deepcopy(output_img)
        self.imgHistory.append(image_for_append)
        self.final_image = ImageTk.PhotoImage(self.imgHistory[self.currentState])

        if self.input_label is None:
            self.input_label = self.iFrame.create_image(self.imwidth / 2 + 1, self.imheight / 2 + 1,
                                                             image=self.final_image)
        else:
            self.iFrame.itemconfig(self.input_label, image=self.final_image)

    def labiling(self, event):
        global final_image
        x, y = int(self.iFrame.canvasx(event.x)), int(self.iFrame.canvasy(event.y))
        imageTest = self.output_img
        self.currentState = (self.currentState + 1)
        pix = imageTest.load()
        clicked_Label = self.labels[x][y]
        for i in range(self.imheight):
            for j in range(self.imwidth):
                if clicked_Label is not 1:
                    if clicked_Label is self.labels[i][j]:
                        pix[i, j] = self.currentColor
        self.imgHistory.append(imageTest)
        print("label number", self.imgHistory.index(imageTest))
        self.final_image = ImageTk.PhotoImage(self.imgHistory[self.currentState])
        self.iFrame.itemconfig(self.input_label, image=self.final_image)

    def undo(self):
        pass

    def save(self):

        ImageGrab.grab().crop(box).save("NewEditPhoto.png", "png")

    def redo(self):
        pass

    def clear(self):
        pass

    def pickColor(self):

        color = askcolor()
        color = str(color)
        start = color.index("((")
        stop = color.index("),")
        color = color[(start):stop]
        color = color[2:len(color)]
        r, g, b = color.split(",")
        global choosenColor
        choosenColor = int(r), int(g), int(b)
        self.currentColor = choosenColor

    def create_earser(self):

        global choosenColor
        choosenColor = (255, 255, 255)
        self.currentColor = choosenColor

def main():

    global box
    root = Tk()
    root.title(" The Paint ")
    gui = GUI(root)
    box = (root.winfo_x() + 1, root.winfo_y() + 1, 1000, 500)
    menu = Menu(root)
    root.config(menu=menu)

    subMenu = Menu(menu)
    menu.add_cascade(label="File", menu=subMenu)

    subMenu.add_command(label="Open File", command=gui.openFile)
    subMenu.add_command(label="Exit", command=root.destroy)
    editMenu = Menu(menu)

    menu.add_cascade(label="Edit", menu=editMenu)
    editMenu.add_command(label="Undo", command=gui.undo)
    editMenu.add_command(label="Redo", command=gui.redo)
    editMenu.add_command(label="Clear", command=gui.clear)
    editMenu.add_command(label="Save File", command=gui.save)

    root.mainloop()
if __name__ == '__main__':
    main()