from tkinter import Tk, Button, Entry, StringVar, END, NSEW
from math import pi, e, sqrt

class Window(object):
    sup = ["\u2070","\u00B9","\u00B2","\u00B3",
            "\u2074","\u2075","\u2076","\u2077",
            "\u2078","\u2079","\u207B"]
    supscript=False
    root=False
    def __init__(self):
        root = Tk()
        root.attributes('-alpha', 0.8)
        title = root.title("Calculator")
        root.config(bg='black')
        self.input=StringVar()
        self.entry=Entry(root,textvariable=self.input,
                        font=("Courier",36,'bold'),
                        justify="right",width=12,relief="flat",
                        bg='black',fg='white',selectbackground="grey")
        self.entry.grid(row=0,columnspan=6)
        self.entry.bind("<Button-1>",lambda x: self.entry.select_range(0,END))
        self.entry.bind("<Return>",lambda x: self.buttonpress("="))
        buts = [["1","2","3","+","x\u207F",],
                ["4","5","6","-","\u221A"],
                ["7","8","9","\u00D7","\u03C0"],
                ["C","0","=","\u00F7","e"]]
        for x in range(len(buts)):
            for y in range(len(buts[x])):
                sym = buts[x][y]
                Button(root,text=sym,font=("Courier",36),
                        command=lambda x=sym: self.buttonpress(x),
                        relief="flat",bg='black',fg='white',
                        activebackground="grey",activeforeground="black",
                        overrelief="sunken",bd=0
                        ).grid(row=x+1,column=y,sticky=NSEW)
        root.resizable(False,False)
        self.entry.focus()
        root.mainloop()

    def buttonpress(self,command):
        words = self.input.get()
        if command == "x\u207F":
            self.supscript = not self.supscript
        elif command == "\u221A":
            self.root = not self.root
            if self.root==True:
                self.entry.insert(END,"\u221A")
            else:
                self.entry.insert(END,")")
        elif command == "C":
            self.input.set("")
        elif command == "=":
            equation=words.replace("\u00D7","*").replace("\u00F7","/").replace("\u03C0",str(pi)).replace("e",str(e))
            self.calc(equation)
        elif self.supscript == True:
            if command == "-":
                self.entry.insert(END,self.sup[10])
            else:
                self.entry.insert(END,self.sup[int(command)])
                self.supscript = not self.supscript
        else:
            self.entry.insert(END,command)

    def script(self,equation):
        for x in self.sup:
            if x in equation:
                equation = equation.replace(x,
                            "**"+str(self.sup.index(x)))
        return equation

    def rootgroup(self,equation):
        if "\u221A" in equation:
            start, rt = equation.split("\u221A")
            try:
                rt, end = rt.split(")")
            except ValueError:
                return start+str(sqrt(int(rt)))
            return start+str(sqrt(int(rt)))+end
        else:
            return equation

    def calc(self,equation):
        try:
            equation = self.script(equation)
            equation = self.rootgroup(equation)
            answer = eval(equation)
            self.input.set(answer)
        except ZeroDivisionError:
            self.input.set('\u221E')
        except SyntaxError:
            return

Window()
