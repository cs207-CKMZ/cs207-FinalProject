from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import pandas as pd
sys.path.insert(0, 'C:/Users/1004p/Desktop/Harvard/Courses/2018-2019/CS 207/cs207-FinalProject/AutoDiff_CKMZ/AutoDiff_CKMZ/modules/')
import AutoDiff

class USimGUI(Frame): 
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self._x = AutoDiff.AutoDiff(0) #Somehow need range and such??
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
        ntbk.add(inPg,text='Drawing Board', padding=5)
        ntbk.add(credPg,text='Credits', padding=5)
        
        ntbk.pack(fill=BOTH)
        self.pack(fill=BOTH, expand=True)

    def loadmainPg(self,mainPg):
        #########################Front page#################################3
        
        #Insert personalized logo
        #pic = PhotoImage(file=self.resource_path('data/logo.gif'))
        #pic.zoom(10,10)
        #mainPg_l1 = Label(mainPg,image=pic)
        #mainPg_l1.image = pic
        #mainPg_l1.configure(image=pic)
        #mainPg_l1.grid(row=0, column=0,padx=5, sticky=E+W+S+N)

        mainPg_l2 = Label(mainPg,text='Welcome to USim, a roller coaster simulator that compares Automatic Differetiationn and numerical approximation methods for calculating derivatives. \n\nCS207\n\nVersion 1.0.0\n\nLast updated Dec 12, 2018.', font=('Helvetica', 12), wraplength=250)
        mainPg_l2.grid(row=0, column=1, padx=5, sticky=E+W+S+N)

    def loadinPg(self, inPg):
        ################################User Input Page############################
        #Fuction input      
        inPg_l1 = Label(inPg, text='Potential function for rollercoaster: Use the list below to input operations. Type variables or numbers.')   
        inPg_l1.grid(row=0, columnspan=2, column=0, padx=5, pady=5, sticky=W)

        inPg_func = Text(inPg, height=1)
        inPg_func.grid(row=1, column=0, sticky=E+W+S+N, padx=5, pady=5, columnspan=2)   
        
        #Function options list
        inPg_l2 = Label(inPg, text='(Type to search functions, click add to add to rollercoaster function)')
        inPg_l2.grid(row=2,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        #All available functions
        allfuncs=StringVar()
        flist = [f for f in dir(AutoDiff)[1:] if not f.startswith("__") and not f.startswith('np')]
        allfuncs.set(flist) #Put in that stuff from modules
        inPg_funcList = Listbox(inPg, listvariable=allfuncs, height=5) 
        inPg_funcList.grid(row=4,rowspan=5,column=0, columnspan=2, sticky=W+S+N+E,padx=5,pady=5)

        #Searchbar
        searchKW = StringVar()
        searchKW.trace('w', lambda name, index, mode: self.update_list(searchKW, inPg_funcList, flist))
        searchBar = Entry(inPg, textvariable=searchKW)
        searchBar.grid(row=3, columnspan=2, column=0, sticky=W+S+N+E, padx=5, pady=5)

        #Scrollbar
        yScrollfunc=Scrollbar(inPg)
        yScrollfunc.grid(row=4,column=0,columnspan=2,rowspan=5, sticky=E+N+S,pady=5)
        yScrollfunc.configure(command=inPg_funcList.yview)

        inPg_funcList.configure(yscrollcommand=yScrollfunc.set)

        #Other inputs
        inPg_l4 = Label(inPg, text='x0')
        inPg_l4.grid(row=9, column=0,padx=5,pady=5,sticky=W+N+S)

        inPg_x0 = Text(inPg, height=1, width=5)
        inPg_x0.grid(row=10,column=0,sticky=E+W+S+N,padx=5,pady=5)

        inPg_l5 = Label(inPg, text='v0')
        inPg_l5.grid(row=9, column=1, padx=5,pady=5,sticky=W+N+S)

        inPg_v0 = Text(inPg, height=1,width=5)
        inPg_v0.grid(row=10,column=1,sticky=E+W+S+N,padx=5,pady=5)

        inPg_l6 = Label(inPg, text='xmin')
        inPg_l6.grid(row=11, column=0, padx=5,pady=5,sticky=W+N+S)

        inPg_xmin = Text(inPg, height=1,width=5)
        inPg_xmin.grid(row=12,column=0,sticky=E+W+S+N,padx=5,pady=5)

        inPg_l7 = Label(inPg, text='xmax')
        inPg_l7.grid(row=11, column=1, padx=5,pady=5,sticky=W+N+S)

        inPg_xmax = Text(inPg, height=1,width=5)
        inPg_xmax.grid(row=12,column=1,sticky=E+W+S+N,padx=5,pady=5)

        inPg_l8 = Label(inPg, text='dx')
        inPg_l8.grid(row=13, column=0, padx=5,pady=5,sticky=W+N+S)

        inPg_dx = Text(inPg, height=1,width=5)
        inPg_dx.grid(row=14,column=0,sticky=E+W+S+N,padx=5,pady=5)

        #Running simulation buttons
        addButton=Button(inPg,text='Add', command = lambda: self.addtoAD(inPg_func, inPg_funcList, flist))
        ADButton = Button(inPg, text='Run with Automatic Differentiation', command= lambda: self.runAD(inPg_x0, inPg_v0, inPg_xmin, inPg_xmax, inPg_dx))
        numButton = Button(inPg, text='Run with numerical approximations', command= lambda: self.runNum(inPg_x0, inPg_v0, inPg_xmin, inPg_xmax, inPg_dx))
        addButton.grid(row=2, column=1, sticky=E+N+S, pady=5,padx=5)
        ADButton.grid(row=13, rowspan=2,column=1, sticky=W+N+S, pady=5,padx=5)                
        numButton.grid(row=13, rowspan =2, column=1, sticky=E+N+S, pady=5,padx=5)      

        #Clear buttons
        inPg_clrfunc=Button(inPg,text='Clear', command=lambda: inPg_func.delete('1.0', END))
        inPg_clrfunc.grid(row=0,column=1,sticky=E,padx=5,pady=5)


    def loadcredPg(self,credPg):
        ##########################Credits#################################        
        cred = Text(credPg,wrap=WORD)
        cred.insert(END, 'TEXT HERE\n\nCopyright 2018 CKMZ\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \'Software\'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \'AS IS\', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.')
        cred.grid(row=0, column=0, pady=5, sticky=E+W+S+N)
        
        yScrollCredits=Scrollbar(credPg)
        yScrollCredits.grid(row=0, column=1, pady=5, sticky=E+N+S)
        yScrollCredits.config(command=cred.yview)
        cred.config(state=DISABLED, yscrollcommand=yScrollCredits.set)  

    def addtoAD(self, tbox, lbox, flist):
        sel = lbox.get(0,END)[lbox.curselection()[0]]
        prev_text = tbox.get('1.0', END)
        new_text = str(sel) + '(' + prev_text
        tbox.delete('1.0', END)
        tbox.insert(END, new_text)
        tbox.insert(END, ')')
        self._x = 'IDK PLACEHOLDER'
            
    def update_list(self, searchKW, lbox, allfuncs):
        search_term = searchKW.get()
        lbox_list = allfuncs
         
        lbox.delete(0, END)
     
        for item in lbox_list:
            if search_term.lower() in item.lower():
                lbox.insert(END, item)

    def runAD(self, ufunc, x0, v0, xmin, xmax, xrange):
        if len(fileBox.get('1.0',END))>1:    
            fname=str(self.resource_path(fileBox.get('1.0',END)))
            fname=fname.strip()
            motif=str(motifBox.get('1.0',END)).strip()
            thresh=str(threshBox.get('1.0',END)).strip()
            if not len(motif)>0:
                motif=int(10)
            if not len(thresh)>0:
                thresh=int(3)
            try:
                msm.msm(fname,motif_length=motif,match_threshold=thresh)
            except UserWarning as errormsg:
                messagebox.showerror('Error', errormsg)
            ''' except Exception as e:
                print(e)
                messagebox.showerror('Error', 'There was an unexpected error. Please reference the documentation (link) or contact us at support@integratedsciences.org.') '''
        else:
            messagebox.showerror('Error','Fill out all required fields!')            

#Runs the program
def main():
    print("69 ayyyyy")
    root = Tk()
    root.geometry('350x300+300+300')
    
    app = USimGUI(root)
    
    root.protocol('WM_DELETE_WINDOW', app.quit)

    app.mainloop()


if __name__ == '__main__':
    main() 