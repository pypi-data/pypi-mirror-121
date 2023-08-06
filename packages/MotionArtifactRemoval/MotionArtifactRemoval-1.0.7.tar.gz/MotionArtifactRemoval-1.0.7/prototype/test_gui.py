# Copyright The Jackson Laboratory, 2021
# authors: Jim Peterson, Abed Ghanbari

import os
import sys
import tifffile as tiff
import pandas as pd
import itertools
import csv
import numpy as np
import matplotlib
from skimage.transform import resize
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QSlider, QLabel, QPushButton, QListWidget, QGridLayout, QMessageBox, QSizePolicy, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import mplcursors

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mmar'))
import process_slice
from create_mask import create_mask

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ssUNET'))
import generate_output

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'MRI Motion Artifact Removal'
        self.show_unet = True
        # coordinated for the UI
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 1000
        self.initUI()

    def initUI(self):
        '''
        initialize the UI
        we use a grid structure for the app
        '''
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # slider widget for the frames
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged[int].connect(self.changeValue_frame) # by each change in slider the changeValue_frame function is called

        self.prntfldr_textbox = QLineEdit(self)
        self.prntfldr_textbox.setText("/Users/ghanba/Documents/ssif_data_jax")
        self.prntfldr_textbox.returnPressed.connect(self.set_parentfldr)

        self.prntfldr_button = QPushButton('Set parent folder')
        self.prntfldr_button.clicked.connect(self.set_parentfldr)


        self.label_frame = QLabel(self) # by each change in slider frame number label will change
        self.label_frame.setText('Frame Number: '+'0')
        self.label_frame.setMinimumWidth(150)

        self.mouse_list_lbl = QLabel(self) # label for list of mouse names
        self.mouse_list_lbl.setText('Mouse Names:')
        self.mouse_list_lbl.setAlignment(Qt.AlignBottom)

        # list of folders found
        self.mouselistbox = QListWidget()
        self.mouselistbox.setMinimumWidth(215)
        self.mouselistbox.setSortingEnabled(True)
        
        self.mouselistbox.itemSelectionChanged.connect(self.updateImageList)

        self.label_z = QLabel(self)
        self.label_z.setText('Slice Number: ')

        # ComboBox
        self.cb = QComboBox()
        self.cb.currentIndexChanged.connect(self.z_selectionchange)

        self.mask_cb = QComboBox()
        self.mask_cb.addItem('UNET')
        self.mask_cb.addItem('Background')
        self.mask_cb.currentIndexChanged.connect(self.set_masks)

        self.image_or_mask = QCheckBox("Mask",self)
        self.image_or_mask.stateChanged.connect(lambda:self.changeValue_frame(self.slider.value()))

        self.label_bg_MAD = QLabel(self)
        self.label_bg_MAD.setText('Background Thr:')
        self.label_bg_MAD.setAlignment(Qt.AlignRight)

        self.bg_MAD = QLineEdit(self)
        self.bg_MAD.setText("3.5")
        self.bg_MAD.setMaximumWidth(30)
        self.bg_MAD.returnPressed.connect(self.updateImageList)

        self.label_fg_MAD = QLabel(self)
        self.label_fg_MAD.setText('Foreground Thr:')

        self.fg_MAD = QLineEdit(self)
        self.fg_MAD.setText("5.5")
        self.fg_MAD.setMaximumWidth(30)
        self.fg_MAD.returnPressed.connect(self.updateImageList)

        # Figure canvas and toolbar
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setMaximumHeight(30)

        # list of accepted frames
        self.framelist_accepted = QListWidget()
        self.framelist_accepted.setMaximumWidth(60)
        self.framelist_accepted.setSortingEnabled(True)
        self.framelist_accepted.itemDoubleClicked.connect(self.framelist_accepted_double_clicked)
        self.framelist_accepted.itemSelectionChanged.connect(self.framelist_accepted_clicked)

        # list of rejected frames
        self.framelist_rejected = QListWidget()
        self.framelist_rejected.setMaximumWidth(60)
        self.framelist_rejected.setSortingEnabled(True)
        self.framelist_rejected.itemDoubleClicked.connect(self.framelist_rejected_double_clicked)
        self.framelist_rejected.itemSelectionChanged.connect(self.framelist_rejected_clicked)

        # adding labels at the top of the lists
        self.label_list1 = QLabel(self)
        self.label_list1.setText('Accepted')
        self.label_list2 = QLabel(self)
        self.label_list2.setText('Rejected')

        # button for saving the list of rejected frames
        self.save_button = QPushButton('Save list')
        self.save_button.setMaximumWidth(75)
        self.save_button.clicked.connect(self.save_onclick)

        # button for loading rejected frames list 
        self.load_button = QPushButton('Load list')
        self.load_button.setMaximumWidth(75)
        self.load_button.clicked.connect(self.load_onclick)

        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(self.exitapp)

        ################## Layout ##################
        layout = QGridLayout()
        layout.addWidget(self.prntfldr_textbox,0,1,1,4)
        layout.addWidget(self.prntfldr_button,0,5,1,1)
        layout.addWidget(self.mouse_list_lbl,1,0,1,1)
        layout.addWidget(self.mouselistbox, 2, 0, 22,1)
        layout.addWidget(self.toolbar,21,1,1,5)
        layout.addWidget(self.canvas,2,1,19,5)
        layout.addWidget(self.label_z,22,1,1,1)
        layout.addWidget(self.cb,22,2,1,1)
        layout.addWidget(self.mask_cb,22,5,1,1)
        layout.addWidget(self.image_or_mask,22,4,1,1)
        layout.addWidget(self.label_frame,23,1,1,1)
        layout.addWidget(self.slider,23,2,1,4)
        layout.addWidget(self.label_list1,1, 6,1,1)
        layout.addWidget(self.label_list2,1, 7,1,1)
        layout.addWidget(self.framelist_accepted, 2, 6,21,1)
        layout.addWidget(self.framelist_rejected, 2, 7,21,1)
        layout.addWidget(self.load_button, 23, 6,1,1)
        layout.addWidget(self.save_button, 23, 7,1,1)
        layout.addWidget(self.label_bg_MAD, 24,1,1,1)
        layout.addWidget(self.bg_MAD, 24,2,1,1)
        layout.addWidget(self.label_fg_MAD, 24,3,1,1)
        layout.addWidget(self.fg_MAD, 24,4,1,1)

        self.setLayout(layout)

        self.show()
    def get_filename(self):
        return os.path.join(self.parent_folder, self.mouse_name, 'dti_large_0.tif')

    def set_parentfldr(self):
        if os.path.isdir(self.prntfldr_textbox.text()):
            self.parent_folder = self.prntfldr_textbox.text()
            self.mouse_folders = [f for f in os.listdir(self.parent_folder) if not f.startswith('.')] # lists all folders in the parent folder except the ones starting with "."
            self.mouse_name = self.mouse_folders[0]  # default to first in the list of folders
            self.file_name = self.get_filename()
            self.mouselistbox.clear()
            for i, fldr in enumerate(self.mouse_folders):
                self.mouselistbox.insertItem(i, fldr)
            self.mouselistbox.setCurrentRow(0)
            self.updateImageInit()
            for i in range(self.nz):
                self.cb.addItem(str(i))
            self.cb.setCurrentIndex(0)
            self.slider.setMaximum(self.data.shape[0]-1)
            self.changeValue_frame(0)
        else:
            self.showDialog(msg='Folder does not exist:\n'+self.prntfldr_textbox.text())

    def updateImageInit(self):
        '''
        in first pass of the app loads the first folder's data and creates the mask
        '''
        if os.path.isfile(self.file_name):
            self.data_all = tiff.imread(self.file_name) # reads image data 
            self.nz = self.data_all.shape[1] # sets number of slices
            self.data = self.data_all[:,0,:,:] # sets the current slice data to slice 0
            self.set_masks()
            self.rejected_frames = [set() for i in range(self.nz)] # should be a set of rejected frames data structures
        else:
            msg='File does\'nt exist:\n'+self.file_name
            print('warning:'+msg)
            self.showDialog(msg=msg)

    def updateImageList(self):
        '''
        by selecting mouse updates the app
        '''
        self.mouse_name = self.mouselistbox.currentItem().text() # gets what has been selected in mice list
        self.file_name = self.get_filename()
        self.updateImageInit() # gets the data for the current mouse
        self.changeValue_frame(0) # goes to frame 0
        self.slider.setValue(0) # set the slider value to 0
        self.plot_intensity_profile() # plots the intensity plots for slice 0 and frame 0
        self.update_textboxs() # updates the rejected and accepted frames
        self.cb.setCurrentIndex(0)

    def changeValue_frame(self, value):
        if hasattr(self,'data'):
            self.label_frame.setText('Frame Number: '+str(value))
            
            if self.image_or_mask.isChecked():
                if self.mask_cb.currentText()=='UNET':
                    data_show=self.maskunet
                else:
                    data_show=self.maskdata

            else:
                data_show = self.data[value, :, :]
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            if value==0 or self.image_or_mask.isChecked():
                ax.imshow(data_show, cmap='gray')
            else:
                # for frames (except the frame 0) we keep the range the same so imshow doesn't adjust contrast automatically
                ax.imshow(data_show, cmap='gray', vmin=np.min(self.data[1:,:,:]), vmax=np.max(self.data[1:,:,:]))
            plt.axis('off')
            self.figure.tight_layout()
            self.canvas.draw()

    def framelist_accepted_double_clicked(self):
        item = self.framelist_accepted.currentItem()
        self.framelist_rejected.addItem(item.text())
        self.framelist_accepted.takeItem(self.framelist_accepted.row(item))
        # if a frame in accepted frames was double clicked add it to set of rejected frames
        self.rejected_frames[self.cb.currentIndex()].add(int(item.text()))

    def framelist_rejected_double_clicked(self):
        item = self.framelist_rejected.currentItem()
        self.framelist_accepted.addItem(item.text())
        self.framelist_rejected.takeItem(self.framelist_rejected.row(item))
        self.rejected_frames[self.cb.currentIndex()].remove(int(item.text()))

    def framelist_accepted_clicked(self, item=None):
        if not item:
            item = self.framelist_accepted.currentItem()
        self.slider.setValue(int(item.text()))

    def framelist_rejected_clicked(self, item=None):
        if not item:
            item = self.framelist_rejected.currentItem()
        if item:
            self.slider.setValue(int(item.text()))

    def z_selectionchange(self):
        self.data = self.data_all[:,self.cb.currentIndex(),:,:]
        self.set_masks()
        self.changeValue_frame(0)
        self.slider.setValue(0)
        self.plot_intensity_profile()
        self.update_textboxs()

    def update_textboxs(self):
        self.framelist_accepted.clear()
        self.framelist_rejected.clear()
        for i in range(self.data.shape[0]):
            if i in self.rejected_frames[self.cb.currentIndex()]:
                self.framelist_rejected.insertItem(i, str(i).zfill(2))
            else:
                self.framelist_accepted.insertItem(i, str(i).zfill(2))

    def save_onclick(self):
        if hasattr(self,'file_name'):
            dict = {}
            for i in range(self.nz):
                dict[str(i)] = list(self.rejected_frames[i])
            with open(os.path.join(os.path.dirname(self.file_name), 'frame_list.csv'), "w") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(dict.keys())
                writer.writerows(itertools.zip_longest(*dict.values()))
    def set_masks(self):
        if hasattr(self,'data'):
            mask_output = generate_output.output_mask(self.data[0, :, :]) # mask is estimated for the slice 0 and frame 0 since the non directional DTI image is stored in frame 0
            self.maskunet = resize(mask_output, (self.data_all.shape[2], self.data_all.shape[3]), anti_aliasing=True)
            self.maskdata = process_slice.create_mask(self.data[0,:,:], fg=False)[0] # mask is estimated for the slice 0 and frame 0 since the non directional DTI image is stored in frame 0
            self.changeValue_frame(0)

    def load_onclick(self):
        if hasattr(self,'file_name'):
            csv_file_path = os.path.join(os.path.dirname(self.file_name), 'frame_list.csv')
            if os.path.isfile(csv_file_path):
                df = pd.read_csv(csv_file_path)
                self.rejected_frames = [set() for i in range(self.nz)]
                # recreate rejected_frames dictionary from csv file
                for i in range(self.nz):
                    for frame in list(df.to_dict()[str(i)].values()):
                        if not pd.isna(frame):
                            self.rejected_frames[i].add(int(frame))
                self.update_textboxs()
            else:
                self.showDialog(msg='There is no csv file for this mouse ...')
    
    def calculate_profiles(self):
        '''
        Calculates the profiles of the foreground and background.
        
        Returns
        -------
        profile_foreground : numpy.ndarray
            The profile of the foreground.
        profile_background : numpy.ndarray
            The profile of the background.
        
        Notes
        -----
        The profile of the foreground is calculated by summing the data over the
        pixels in mask, and dividing by the number of pixels in the mask.
        '''
        nz = self.data.shape[0]
        profile_foreground = np.zeros(nz)
        profile_background = np.zeros(nz)
        for iz in range(nz):
            profile_foreground[iz] = np.sum(self.data[iz,:,:] * (self.maskdata)) / np.sum((self.maskdata))
            profile_background[iz] = np.sum(self.data[iz,:,:] * (1-self.maskdata)) / np.sum((1-self.maskdata))
        for i in self.get_outliers(profile_background, mode='MAD', MAD_thr=float(self.bg_MAD.text())):
            self.rejected_frames[self.cb.currentIndex()].add(i)
        for i in self.get_outliers(profile_foreground, mode='MAD', MAD_thr=float(self.fg_MAD.text())):
            self.rejected_frames[self.cb.currentIndex()].add(i)
        return profile_foreground, profile_background

    def get_outliers(self, data, mode='MAD', r=None, MAD_thr=None):
        '''
        This function identifies outliers in a given dataset.
    
        Parameters
        ----------
        data : list
            A list of numbers.
        mode : str, optional
            The method used to identify outliers.
            'std' uses standard deviation method.
            'MAD' uses median absolute deviation method.
            The default is 'MAD'.
        r : float, optional
            The ratio used to identify outliers.
            The default is None.
        MAD_thr : float, optional
            The threshold used to identify outliers using median absolute deviation method.
            The default is None, however in [https://www.sciencedirect.com/science/article/abs/pii/S0022103113000668]
            it has been suggested to use 2.5
        
        Returns
        -------
        outliers : list
            A list of indices of outliers in the given dataset.
        
        '''
        if mode=='std':
            mean = np.mean(data)
            std = np.std(data)
            outliers = []
            for i in range(1,len(data)):
                if data[i] > mean + r*std or data[i] < mean - r*std:
                    outliers.append(i)
        elif mode=='MAD':
            # calculate median and median absolute deviation
            # ref: https://www.sciencedirect.com/science/article/abs/pii/S0022103113000668
            data_median = np.median(data)
            data_mad = np.median([np.abs(data - data_median)])
            # identify outliers
            cut_off = data_mad * MAD_thr
            lower, upper = data_median - cut_off, data_median + cut_off
            outliers = []
            for i in range(1,len(data)):
                if data[i] < lower or data[i] > upper:
                    outliers.append(i)
        return outliers

    def plot_intensity_profile(self):
        '''
        Plots the intensity profile of the current slice.
    
        This function is triggered whenever the current folder is updated or the slice number is changed
        The profile is calclulated using "calculate_profiles" and plotted on separate window

        '''
        if not hasattr(self,'profile_plot'):
            self.profile_plot = BgProfileWindow()
        self.profile_plot.fig.clear()
        profile_foreground, profile_background = self.calculate_profiles()
        self.profile_plot.updatefig(    
                foreground=profile_foreground[1:], 
                background=profile_background[1:], 
                mouse=self.mouse_name, 
                z_idx =self.cb.currentIndex(),
                sig=self.slider

                )
        self.profile_plot.draw()


    def showDialog(self,msg=''):
        '''
        This is a function that shows a dialog box.
        It takes a single argument, which is the message to be displayed.
        '''
        msgBox = QMessageBox()
        msgBox.setText(msg)
        msgBox.setWindowTitle("MMAR Warning!")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def exitapp(self):
        self.mask_fig.close()
        self.profile_plot.close()
        QCoreApplication.instance().quit()


class BgProfileWindow(FigureCanvas):
    def __init__(self, width=6, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def updatefig(self, foreground, background, mouse=None, z_idx=None, sig=None):
        self.sig = sig
        xx = np.arange(1, len(foreground)+1)
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.plot(xx, foreground, marker='o', color='dodgerblue', label='Foreground')
        self.axes.title.set_text(mouse+' Slice #'+str(z_idx))
        self.axes.title.set_fontsize(10)
        self.axes.set_xlabel('Slice Number')
        self.axes.set_ylabel('Foreground Intensity', color='dodgerblue')
        self.axes2 = self.axes.twinx()

        self.axes2.plot(xx, background, marker='o', color='darkorange', label='Background')
        self.axes2.set_ylabel('Background Intensity', color='darkorange')
        self.show()

        self.crs = mplcursors.cursor([self.axes, self.axes2],hover=True)
        self.crs.connect("add", lambda sel: sel.annotation.set_text(
            '{:.0f} : {:.2f}'.format(sel.target[0], sel.target[1])))
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        ix, iy = event.xdata, event.ydata
        self.sig.setValue(round(ix))

def run_gui():
    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'icon.png')
    app.setWindowIcon(QIcon(path))
    ex = App()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_gui()
