from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
from USim.USim.modules import animation as Anim

class USimGUI(Frame): 
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
        with open(self.resource_path('USim/USim/modules/functions.txt'), 'r') as f:
            self.funcs = f.read().splitlines()
        self.parent = parent
        self.initUI()
                
    def initUI(self):
        self.parent.title('USim: Rollercoaster simulator')
        self.style = Style()
        self.style.theme_use('default')  

        self.pack(fill=BOTH, expand=1)
        
        mlabel = Label(self, text='USim: Rollercoaster simulator with Automatic Differetiation\n\nDo NOT close this window.', font=('Helvetica', 16), justify=CENTER, wraplength=350)
        mlabel.grid(row=0, column=0, pady=15, padx=10, sticky=S+N+E+W)

        #Navigation
        sButton = Button(self, text='Start',command=self.nav)
        sButton.grid(row=1, column=0, padx=15, pady=5)

        qButton=Button(self, text='Quit', command=self.quit)
        qButton.grid(row=2, column=0, padx=15, pady=5)

    # Needed for PyInstaller to read files: filepath = resource_path()

    def resource_path(self, relative_path):
        ''' Get absolute path to resource, works for dev and for PyInstaller '''
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)

    def quit(self):
        quit()

    def nav(self):
        top=Toplevel()
        top.title('USim')

        #######################ALL Page Declarations###################

        ntbk = Notebook(top)
        mainPg = Frame(ntbk)
        inPg = Frame(ntbk)
        credPg = Frame(ntbk)

        #############################Compile notebook############
        self.loadmainPg(mainPg)
        self.loadinPg(inPg)
        self.loadcredPg(credPg)

        ntbk.add(mainPg, compound=LEFT, text='Welcome', padding=5)
        ntbk.add(inPg,text='Simulations', padding=5)
        ntbk.add(credPg,text='Credits', padding=5)
        
        ntbk.pack(fill=BOTH)
        self.pack(fill=BOTH, expand=True)

    def loadmainPg(self,mainPg):
        #########################Front page#################################3
        mainPg_l2 = Label(mainPg,text='Welcome to USim, a roller coaster simulator that compares Automatic Differetiationn and numerical approximation methods for calculating derivatives. \n\nCS207\n\nVersion 1.0.0\n\nLast updated Dec 12, 2018.', font=('Helvetica', 12), wraplength=250)
        mainPg_l2.grid(row=0, column=1, padx=5, sticky=E+W+S+N)

    def loadinPg(self, inPg):
        ################################User Input Page############################
        #Fuction input      
        inPg_l1 = Label(inPg, text='Potential function for rollercoaster: choose from the list below.')   
        inPg_l1.grid(row=0, columnspan=2, column=0, padx=5, pady=5, sticky=W)

        inPg_func = Text(inPg, height=1, state='disabled')
        inPg_func.grid(row=1, column=0, sticky=E+W+S+N, padx=5, pady=5, columnspan=2)   
        
        #Function options list
        inPg_l2 = Label(inPg, text='(Type to search functions, click select to select)')
        inPg_l2.grid(row=2,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        #All available functions
        allfuncs=StringVar()
        allfuncs.set(self.funcs) 
        inPg_funcList = Listbox(inPg, listvariable=allfuncs, height=5) 
        inPg_funcList.grid(row=4,rowspan=5,column=0, columnspan=2, sticky=W+S+N+E,padx=5,pady=5)

        #Searchbar
        searchKW = StringVar()
        searchKW.trace('w', lambda name, index, mode: self.update_list(searchKW, inPg_funcList))
        searchBar = Entry(inPg, textvariable=searchKW)
        searchBar.grid(row=3, columnspan=2, column=0, sticky=W+S+N+E, padx=5, pady=5)

        #Scrollbar
        yScrollfunc=Scrollbar(inPg)
        yScrollfunc.grid(row=4,column=0,columnspan=2,rowspan=5, sticky=E+N+S,pady=5)
        yScrollfunc.configure(command=inPg_funcList.yview)

        inPg_funcList.configure(yscrollcommand=yScrollfunc.set)

        #Other inputs
        inPg_l4 = Label(inPg, text='x0, initial position of the ball')
        inPg_l4.grid(row=9, column=0,padx=5,pady=5,sticky=W+N+S)

        inPg_x0 = Text(inPg, height=1, width=5)
        inPg_x0.grid(row=10,column=0,sticky=E+W+S+N,padx=5,pady=5)

        inPg_l5 = Label(inPg, text='v0, initial velocity of the ball along the rollercoaster. Specify +/-')
        inPg_l5.grid(row=9, column=1, padx=5,pady=5,sticky=W+N+S)

        inPg_v0 = Text(inPg, height=1,width=5)
        inPg_v0.grid(row=10,column=1,sticky=E+W+S+N,padx=5,pady=5)

        inPg_l6 = Label(inPg, text='xmin, minimum position')
        inPg_l6.grid(row=11, column=0, padx=5,pady=5,sticky=W+N+S)

        inPg_xmin = Text(inPg, height=1,width=5)
        inPg_xmin.grid(row=12,column=0,sticky=E+W+S+N,padx=5,pady=5)

        inPg_l7 = Label(inPg, text='xmax, maximum position')
        inPg_l7.grid(row=11, column=1, padx=5,pady=5,sticky=W+N+S)

        inPg_xmax = Text(inPg, height=1,width=5)
        inPg_xmax.grid(row=12,column=1,sticky=E+W+S+N,padx=5,pady=5)

        #Running simulation buttons
        addButton = Button(inPg,text='Select', command = lambda: self.addtoAD(inPg_func, inPg_funcList))
        ADButton = Button(inPg, text='Run with Automatic Differentiation', command= lambda: self.runSim(inPg_func, inPg_x0, inPg_v0, inPg_xmin, inPg_xmax, 1))
        numButton = Button(inPg, text='Run with Numerical Approximation', command= lambda: self.runSim(inPg_func, inPg_x0, inPg_v0, inPg_xmin, inPg_xmax, 2))
        addButton.grid(row=2, column=1, sticky=E+N+S, pady=5,padx=5)
        ADButton.grid(row=13,column=0, sticky=W+N+S, pady=5,padx=5)                
        numButton.grid(row=13, column=1, sticky=E+N+S, pady=5,padx=5)      

        #Clear buttons
        inPg_clrfunc=Button(inPg,text='Clear', command=lambda: self.delfunc(inPg_func))
        inPg_clrfunc.grid(row=0,column=1,sticky=E,padx=5,pady=5)

    def loadcredPg(self,credPg):
        ##########################Credits#################################        
        cred = Text(credPg,wrap=WORD)
        cred.insert(END, 'USim is an educational tool meant to demonstrate the applications of automatic differentiation and the ways in which automatic differentiation can outperform other methods of taking derivatives, like numerical approximations. The commbination of technical knowledge and tangible visualization of a ball rolling on a rollercoaster helps students more easily understand physics, math, and computer science.\n\nCopyright 2018 CKMZ\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \'Software\'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \'AS IS\', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.')
        cred.grid(row=0, column=0, pady=5, sticky=E+W+S+N)
        
        yScrollCredits=Scrollbar(credPg)
        yScrollCredits.grid(row=0, column=1, pady=5, sticky=E+N+S)
        yScrollCredits.config(command=cred.yview)
        cred.config(state=DISABLED, yscrollcommand=yScrollCredits.set)  

    def delfunc(self, tbox):
        tbox.configure(state = 'normal')
        tbox.delete('1.0', END)
        tbox.configure(state='disabled')

    def addtoAD(self, tbox, lbox):
        try:
            sel = lbox.get(0,END)[lbox.curselection()[0]]
            tbox.configure(state='normal')
            tbox.delete('1.0', END)
            tbox.insert(END, sel)
            tbox.configure(state='disabled')
        except:
            messagebox.showwarning('Warning', 'Please select a function from the list below.')
            
    def update_list(self, searchKW, lbox):
        search_term = searchKW.get()
        lbox_list = self.funcs
        lbox.delete(0, END)     
        for item in lbox_list:
            if search_term.lower() in item.lower():
                lbox.insert(END, item)

    def runSim(self, ufuncbox, x0box, v0box, xminbox, xmaxbox, simtype):
        ufunc = ufuncbox.get('1.0', END).strip()
        x0 = x0box.get('1.0', END).strip()
        v0 = v0box.get('1.0', END).strip()
        xmin = xminbox.get('1.0', END).strip()
        xmax = xmaxbox.get('1.0', END).strip()

        if len(ufunc) > 0 and len(x0) > 0 and len(v0) > 0 and len(xmin) > 0 and len(xmax) > 0:
            try:
                #AD function
                try:
                    ufunc = self.funcs.index(ufunc) #CHANGE AND ALSO ADD FOR AD
                    x0 = float(x0)
                    v0 = float(v0)
                    xmin = float(xmin)
                    xmax = float(xmax)
                except:
                    raise UserWarning('x0, v0, xmin, and xmax must all be numbers.')
                if x0 < xmin or x0 > xmax:
                    raise UserWarning('x0 must be between xmin and xmax!')
                try:
                    anim = Anim.Animation(function_index=ufunc, init_status=(x0, v0), 
                        x_range=(xmin, xmax), option=simtype)
                    anim.run_animation()
                except:
                    raise UserWarning('Invalid bounds/parameters. Try changing the inputs.')
            except UserWarning as errormsg:
                messagebox.showerror('Error', errormsg)
        else:
            messagebox.showerror('Error','Fill out all required fields!')            

#Runs the program
def main():
    root = Tk()
    root.geometry('350x300+300+300')
    
    app = USimGUI(root)
    
    root.protocol('WM_DELETE_WINDOW', app.quit)

    app.mainloop()


if __name__ == '__main__':
    main() 