from tkinter import Tk, Button, Entry, StringVar, END, NSEW
from math import pi, e, sqrt
from re import sub

class Window(Tk):
    sup = [
        '\u2070', '\u00B9', '\u00B2', '\u00B3', '\u2074', '\u2075', '\u2076',
        '\u2077', '\u2078', '\u2079', '\u207B']
    supscript = False
    sq_root = False
    def __init__(self):
        super(Window, self).__init__()
        self.attributes("-alpha", .8)
        self.title("Calculator")
        self.config(bg = "black")
        self._input = StringVar()
        self.entry = Entry(
            self, textvariable = self._input, font = ("Courier", 36, "bold"),
            justify = "right",width = 12,relief = "flat", bg = "black", 
            fg = "white", selectbackground = "grey")
        self.entry.grid(row = 0, columnspan = 6)
        self.entry.bind("<Button-1>", lambda _: self.entry.select_range(0, END))
        self.entry.bind("<Return>", lambda _: self.buttonpress('='))
        key_table = [
            ['1','2','3','+','x\u207F',],
            ['4','5','6','-','\u221A'],
            ['7','8','9','\u00D7','\u03C0'],
            ['C','0','=','\u00F7','e']
        ]
        for x, keys in enumerate(key_table):
            for y, key in enumerate(keys):
                b_widget = Button(
                    self, text = key, font = ("Courier", 36), relief = "flat",
                    bg = "black", fg = "white", activebackground = "grey",
                    activeforeground = "black", overrelief = "sunken", bd = 0,
                    command = lambda x = key: self.buttonpress(x))
                b_widget.grid(row = x + 1,column = y , sticky = NSEW)
        self.resizable(False, False)
        self.entry.focus()
    
    def buttonpress(self, command):
        words = self._input.get()
        if command == 'x\u207F':
            self.supscript = not self.supscript
        elif command is "\u221A":
            self.sq_root = not self.sq_root
            if self.sq_root is True:
                self.entry.insert(END, '\u221A')
            else:
                self.entry.insert(END, ')')
        elif command is 'C':
            self._input.set('')
        elif command is '=':
            self.calc(words.translate({
                ord('\u00D7'): '*', ord('\u00F7'): '/',
                ord('\u03C0'): str(pi), ord('e'): str(e)
            }))
        elif self.supscript is True:
            if command is '-':
                self.entry.insert(END, self.sup[10])
            else:
                self.entry.insert(END, self.sup[int(command)])
                self.supscript = not self.supscript
        else:
            self.entry.insert(END,command)
    
    def script(self, equation):
        for x in self.sup:
            if x in equation:
                equation = equation.replace(x, f"**{self.sup.index(x)}")
        return equation
    
    def selfgroup(self, equation):
        if "\u221A" in equation:
            start, radicand = equation.split("\u221A")
            try:
                radicand, end = radicand.split(")")
            except ValueError:
                return f"{start}{int(radicand) ** .5}"
            return f"{start}{int(radicand) ** .5}{end}"
        return equation
    
    def calc(self, equation):
        try:
            equation = self.script(equation)
            equation = self.selfgroup(equation)
            self._input.set(eval(equation))
        except ZeroDivisionError:
            self._input.set('\u221E')
        except SyntaxError:
            return False

if __name__ == "__main__":
    window = Window()
    window.mainloop()
