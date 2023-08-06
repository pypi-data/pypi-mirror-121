import os
from configparser import ConfigParser
from tkinter import *
from simba.roi_tools.ROI_define import ROI_definitions


class ROI_menu:
    def __init__(self, config_path, new_roi=True):
        self.config_path = config_path
        config = ConfigParser()
        config.read(config_path)
        self.project_path = config.get('General settings', 'project_path')
        self.measures_dir = os.path.join(self.project_path, 'logs', 'measures')
        self.video_dir = os.path.join(self.project_path, 'videos')
        if new_roi is True:
            try:
                os.remove(os.path.join(self.measures_dir, 'ROI_definitions.h5'))
                os.remove(os.path.join(self.measures_dir, 'ROI_index.h5'))
            except:
                pass

        self.roi_table_menu()

    def roi_table_menu(self):
        self.filesFound = []
        self.row = []
        for i in os.listdir(self.video_dir):
            if i.endswith(('.avi', '.mp4', '.mov', 'flv')):
                self.filesFound.append(i)

        maxname = max(self.filesFound, key=len)
        roimenu = Tk()
        roimenu.minsize(500, 400)
        roimenu.wm_title("ROI Table")

        tableframe = LabelFrame(roimenu, text='Video Name', labelanchor=NW)

        for i in range(len(self.filesFound)):
            self.row.append(roitableRow(tableframe, self.video_dir, str(self.filesFound[i]), str(len(maxname)), str(i + 1) + '.', projectini=self.config_path))
            self.row[i].grid(row=i + 1, sticky=W)
        tableframe.grid(row=0)


class roitableRow(Frame):
    def __init__(self, parent =None ,dirname='',filename = '',widths = "" ,indexs='',projectini=''):
        self.projectini = projectini
        self.filename = os.path.join(dirname,filename)
        Frame.__init__(self,master=parent)
        var=StringVar()
        self.index = Entry(self,textvariable=var,width=4)
        var.set(indexs)
        self.index.grid(row=0,column=0)
        self.lblName = Label(self,text=filename,width =widths,anchor=W)
        self.lblName.grid(row=0,column=1,sticky=W)
        self.btnset = Button(self,text='Draw',command=self.draw)
        self.btnset.grid(row=0,column=2)
        self.btnreset = Button(self,text='Reset',command =self.reset)
        self.btnreset.grid(row=0,column=3)
        self.btnapplyall = Button(self, text='Apply to all', command=self.applyall)
        self.btnapplyall.grid(row=0, column=4)

    def draw(self):
        ROI_definitions(self.projectini,self.filename)

    def reset(self):
        ROI_reset(self.projectini, self.filename)

    def applyall(self):
        multiplyFreeHand(self.projectini, self.filename)