import sys
from turtle import color
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np
from pathlib import Path
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
import os
from scipy.stats import norm,poisson,cauchy,expon
import pyqtgraph as pg 
 
class TableModel(QtCore.QAbstractTableModel):
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#d8ffdb')
 
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, index):
        return self._data.shape[1]
 
    # Add Row and Column header
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.file_src = "img/"
        self.picName = os.listdir(self.file_src)

        uic.loadUi('work1.ui', self)
        self.setWindowTitle('Table View: the pandas version')
 
        self.table = self.tableView
 
        win = self.graphLayoutWidget
         
        self.plt1 = win.addPlot(title="p1")
        win.nextRow()
        self.plt2 = win.addPlot(title="p2")
        self.graphLayoutWidget.setBackground('w')

        self.plt4 = self.graphwidget_2.addPlot(title="Type II Error")
        self.graphwidget_2.setBackground('w')

        self.pltw3 = self.widget.addPlot(title="approximate")
        self.widget.setBackground('w')
        
        self.gView.setBackground('w')
        

    # ---------------------tab1

        self.pn = 0
        # Signals
        self.pushButton_first.clicked.connect(self.showfirstImg)
        self.pushButton_next.clicked.connect(self.shownextImg)
        self.pushButton_last.clicked.connect(self.showlastImg)
        self.pushButton_lastest.clicked.connect(self.showlastestImg)
        self.pushBtn_exit.clicked.connect(self.dialogBox)
        self.gView.scene().sigMouseMoved.connect(self.mouseMoved)
        self.verticalSlider.valueChanged.connect(self.slider_it)
        self.verticalSlider.setMinimum(-5)
        self.verticalSlider.setMaximum(5)
        self.verticalSlider_2.valueChanged.connect(self.slider_2_it)
        self.verticalSlider_2.setMinimum(1)
        self.verticalSlider_2.setMaximum(5)
        self.verticalSlider.valueChanged.connect(self.update_plot_w4)
        self.verticalSlider_2.valueChanged.connect(self.update_plot_w4)
        # self.verticalSlider.valueChanged.connect(self.pdfcdf_clicked)
        
#         self.comboBox_ImgName.currentIndexChanged.connect(self.showImg)
#         self.pBut_exit.clicked.connect(self.close)
    #----------------------tab2
        self.update_plot_w4('PDF')
        self.update_plot()
        self.update_plot_w3()

    #------------------------w1

        #Signals
        self.actionexit.triggered.connect(self.fileExit)
        self.actionOpen.triggered.connect(self.fileOpen)
        self.comboBox_col.currentIndexChanged.connect(self.showcol)
        self.comboBox_col_2.currentIndexChanged.connect(self.showcol_1)
        # self.comboBox.currentIndexChanged.connect(self.showcol)
        #w1
        self.lineEdit_sd.returnPressed.connect(self.update_plot)
        self.lineEdit_n.returnPressed.connect(self.update_plot)
        self.lineEdit_mu.returnPressed.connect(self.update_plot)
        self.lineEdit_mua.returnPressed.connect(self.update_plot)
        self.lineEdit_beta.returnPressed.connect(self.update_n)
        self.comboBox_alpha.currentIndexChanged.connect(self.update_plot)
        self.checkBox_Grid.stateChanged.connect(self.gridon)
        #w3
        self.lineEdit_w3_n.returnPressed.connect(self.update_plot_w3)
        self.lineEdit_w3_p.returnPressed.connect(self.update_plot_w3)
        self.lineEdit_w3_prob.returnPressed.connect(self.update_plot_w3)
        self.lineEdit_w3_N.returnPressed.connect(self.update_plot_w3)
        self.comboBox_2.currentIndexChanged.connect(self.update_plot_w3)
        #pdf/cdf
        
        self.radioBut_PDF.toggled.connect(self.pdfcdf_clicked)
        self.radioBut_cdf.toggled.connect(self.pdfcdf_clicked)
        self.comboBox.currentIndexChanged.connect(self.update_plot_w4)
        self.lineEdit_5.returnPressed.connect(self.update_plot_w4)
        self.lineEdit_13.returnPressed.connect(self.update_plot_w4)
        self.checkBox_Grid_2.stateChanged.connect(self.gridon_2)
        self.radioBut_PDF.setChecked(True)
 
    # Slots:    
    def slider_it(self,value,s=0):
        s = self.comboBox.currentIndex()
        if s == 2:
            self.verticalSlider.setMinimum(0)
        else:
            self.verticalSlider.setMinimum(-5)
        self.lineEdit_5.setText(str(value))

    def slider_2_it(self,value):
        self.lineEdit_13.setText(str(value))


    def update_plot_w4(self, str = 'CDF' , s = 0):
        str = self.groupBox.title()
        # print(str)
        s = self.comboBox.currentIndex()
        x = np.linspace(-5, 5, 1000)
        mu = np.double(self.lineEdit_5.text())
        sd = np.double(self.lineEdit_13.text())
        self.gView.clear()
        if s == 0:
            if str == 'PDF':
                y = norm.pdf(x,mu,sd)
                title = 'Normal\'s PDF'
            else:
                y = norm.cdf(x,mu,sd)
                title = "Normal\'s CDF"
        elif s == 1:
            if str == 'PDF':
                y = cauchy.pdf(x,mu,sd)
                title = 'Cauchy\'s PDF'
            else:
                y = cauchy.cdf(x,mu,sd)
                title = "Cauchy\'s CDF"
        else:
            x = np.linspace(0, 5, 1000)
            self.lineEdit_6.setText("0")
            if str == 'PDF':
                y = expon.pdf(x,mu,sd)
                title = 'Exponential\'s PDF'
            else:
                y =expon.cdf(x,mu,sd)
                title = "Exponential\'s CDF"
            self.gView.setYRange(0, 1)


        self.gView.plot(x, y,pen='r')
        self.vLine = pg.InfiniteLine(pos = 1, angle=90, movable=False)
        self.hLine = pg.InfiniteLine(pos = 0.2, angle=0, movable=False)
        self.vLine2 = pg.InfiniteLine(pos = mu, angle=90, movable=False,pen='r')
        self.gView.addItem(self.vLine) # add PlotDataItem in PlotWidget 
        self.gView.addItem(self.hLine)
        self.gView.addItem(self.vLine2)
        self.gView.setTitle(title)
    
    def pdfcdf_clicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.groupBox.setTitle(radioBtn.text())
            self.update_plot_w4(radioBtn.text())
            # print(radioBtn.text())

    def mouseMoved(self, point, s = 0): # returns the coordinates in pixels with respect to the PlotWidget
        s = self.comboBox.currentIndex()
        p = self.gView.plotItem.vb.mapSceneToView(point) # convert to the coordinate of the plot
        mu = np.double(self.lineEdit_5.text())
        sd = np.double(self.lineEdit_13.text())
        self.vLine.setPos(p.x()) # set position of the verticle line
        self.hLine.setPos(p.y()) # set position of the horizontal line
        self.lineEdit_14.setText(str(round(p.x(), 4))) 
        if s == 0:
            self.lineEdit.setText(str(round(norm.pdf(p.x(),mu,sd), 4)))
            self.lineEdit_3.setText(str(round(norm.cdf(p.x(),mu,sd), 4)))
        elif s == 1:
            self.lineEdit.setText(str(round(cauchy.pdf(p.x(),mu,sd), 4)))
            self.lineEdit_3.setText(str(round(cauchy.cdf(p.x(),mu,sd), 4)))
        else:
            self.lineEdit.setText(str(round(expon.pdf(p.x(),mu,sd), 4)))
            self.lineEdit_3.setText(str(round(expon.cdf(p.x(),mu,sd), 4)))


    def dialogBox(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Wang's Class Demo")
        dlg.setText("確定要離開這個 App")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        buttonY = dlg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('確定')
        buttonY = dlg.button(QMessageBox.StandardButton.No)
        buttonY.setText('取消')
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
 
        if button == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            print("No!")    

    def update_plot_w3(self,s=0):
        s = self.comboBox_2.currentIndex()
        self.pltw3.clear()
        N = int(self.lineEdit_w3_N.text())
        n = int(self.lineEdit_w3_n.text())
        p = np.double(self.lineEdit_w3_p.text())
        prob = np.double(self.lineEdit_w3_prob.text())
        bin = np.random.binomial(n,p,N)
        y, x = np.histogram(bin,density = True)
        # self.plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/(len(x)*1.1), brush=(107,200,224))
        self.pltw3.addItem(barItem)
        self.pltw3.setYRange(0, y.max())
        if not n*p < 5:
            mu = n * p
            q = 1 - p
            sd = np.sqrt(n*p*q) 
            x = np.linspace(mu - 3 * sd,mu + 3 * sd, N)
            y = norm.pdf(x,mu,sd)
            pen = pg.mkPen(color=(255, 0, 0), width = 2)
            pen1 = pg.mkPen(color="r", width = 2)
            self.pltw3.plot(x,y,name='Normal',pen=pen)
            # self.pltw3.setYRange(0, y.max())
            self.label_w3_dis.setText("Normal")
            if s == 0:
                tv = sum(bin >= prob)/N
                av = norm.sf(prob,mu,sd)
                xa = np.linspace(prob,mu + 3 * sd, N)
                ya = norm.pdf(xa,mu,sd)
                cur1 = self.pltw3.plot(xa, ya,pen=pen)
                cur2 = self.pltw3.plot(xa, np.zeros(len(ya)))
                self.pltw3.plot([prob]*2,[0,norm.pdf(prob,mu,sd)],pen=pen1)
            elif s == 1:
                tv = sum(bin == prob)/N
                av = norm.cdf(prob+0.5,mu,sd) - norm.cdf(prob-0.5,mu,sd)
                xa = np.linspace(prob-0.5,prob+0.5, N)
                ya = norm.pdf(xa,mu,sd)
                cur1 = self.pltw3.plot(xa, ya,pen=pen)
                cur2 = self.pltw3.plot(xa, np.zeros(len(ya)))
                self.pltw3.plot([prob-0.5]*2,[0,norm.pdf(prob-0.5,mu,sd)],pen=pen1)
                self.pltw3.plot([prob+0.5]*2,[0,norm.pdf(prob+0.5,mu,sd)],pen=pen1)
            else:
                tv = sum(bin <= prob)/N
                av = norm.cdf(prob,mu,sd)
                xa = np.linspace(mu - 3 * sd,prob, N)
                ya = norm.pdf(xa,mu,sd)
                cur1 = self.pltw3.plot(xa, ya,pen=pen)
                cur2 = self.pltw3.plot(xa, np.zeros(len(ya)))
                self.pltw3.plot([prob]*2,[0,norm.pdf(prob,mu,sd)],pen=pen1)
            patchcur = pg.FillBetweenItem(curve1 = cur1, curve2 = cur2, brush = (255, 204, 153))
            self.pltw3.addItem(patchcur)
        else:
            lambda_ = n * p
            x = np.arange(n + 1)
            y = poisson.pmf(x,lambda_)
            pen = pg.mkPen(color=(255, 0, 0), width = 2)
            self.pltw3.plot(x,y,name='Possion',pen=pen, symbol='o', symbolSize=5)
            # self.pltw3.setYRange(0, y.max())
            self.label_w3_dis.setText("Possion")
            if s == 0:
                tv = sum(bin > prob)/N
                av = poisson.sf(prob,lambda_)
                xa = np.linspace(prob,n , N)
                ya = poisson.pmf(xa,lambda_)
                cur1 = self.pltw3.plot(xa, ya,pen=pen)
                cur2 = self.pltw3.plot(xa, np.zeros(len(ya)))
                
            elif s == 1:
                tv = sum(bin == prob)/N
                av = poisson.pmf(prob,lambda_)
                xa = np.linspace(prob,n , N)
                ya = poisson.pmf(xa,lambda_)
            else:
                tv = sum(bin <= prob)/N
                av = poisson.cdf(prob,lambda_)
                xa = np.linspace(0,prob, N)
                ya = poisson.pmf(xa,lambda_)
                cur1 = self.pltw3.plot(xa, ya,pen=pen)
                cur2 = self.pltw3.plot(xa, np.zeros(len(ya)))
                # self.pltw3.plot([prob]*2,[0,poisson.pmf(prob,lambda_)],pen=pen1)
        self.lineEdit_w3_tv.setText(str(round(tv,4)))
        self.lineEdit_w3_av.setText(str(round(av,4)))
        # add color patch under curve
        patchcur = pg.FillBetweenItem(curve1 = cur1, curve2 = cur2, brush = (255, 204, 153))
        self.pltw3.addItem(patchcur)
        
        


    def fileExit(self):
        self.close()
 
    def fileOpen(self):
        home_dir = str(Path.home())
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            "", "EXCEL files (*.xlsx *.xls);;Text files (*.txt);;Images (*.png *.xpm *.jpg)")
        # print(fname[0])
        if fname[0]:
            self.df = pd.read_excel(fname[0], index_col = None, header = 0)
            self.model = TableModel(self.df)
            self.table.setModel(self.model)
 
            self.label_variable.setText(str(self.df.shape[1]))
            self.label_size.setText(str(self.df.shape[0]))
            self.comboBox_col.clear()
            self.comboBox_col.addItems(self.df.columns)
            self.comboBox_col_2.addItems(self.df.columns)
 
            self.update_plt1()
            self.update_plt2()
    
    def showcol(self,s):
        self.plt1.clear()
        s = self.comboBox_col.currentIndex()
        s1 = self.comboBox_col_2.currentIndex()
        y, x = np.histogram(self.df[self.df.columns[s]])
        # self.plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/len(x), brush=(107,200,224))
        self.plt1.addItem(barItem)
        self.plt1.setTitle(self.df.columns[s])
        a = np.array(self.df[self.df.columns[s]]).reshape(1, -1)
        b = np.array(self.df[self.df.columns[s1]]).reshape(1, -1)
        a_b = np.r_[a, b]
        c_a_b = round(np.corrcoef(a_b)[0, 1], 4)
        self.label_r_2.setText(str(c_a_b))

        self.plt2.clear()
        if isinstance(self.df[self.df.columns[0]][0], str) or isinstance(self.df[self.df.columns[1]][0], str) :
            self.plt2.setLabel('bottom',"")   
            self.plt2.setLabel('left',"")
            return
        else :
        # if self.df[self.df.columns[0]][0]== float and self.df[self.df.columns[1]][0]== float :
            self.plt2.plot(self.df[self.df.columns[s]], self.df[self.df.columns[s1]], pen=None, symbol='o', symbolSize=5)
            self.plt2.setLabel('bottom',self.df.columns[s])   
            self.plt2.setLabel('left',self.df.columns[s1])

    def showcol_1(self,s):
        self.plt1.clear()
        s1 = self.comboBox_col.currentIndex()
        s = self.comboBox_col_2.currentIndex()
        y, x = np.histogram(self.df[self.df.columns[s1]])
        # self.plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/len(x), brush=(107,200,224))
        self.plt1.addItem(barItem)
        self.plt1.setTitle(self.df.columns[s1])
        a = np.array(self.df[self.df.columns[s]]).reshape(1, -1)
        b = np.array(self.df[self.df.columns[s1]]).reshape(1, -1)
        a_b = np.r_[a, b]
        c_a_b = round(np.corrcoef(a_b)[0, 1], 4)
        self.label_r_2.setText(str(c_a_b))

        self.plt2.clear()
        if isinstance(self.df[self.df.columns[0]][0], str) or isinstance(self.df[self.df.columns[1]][0], str) :
            self.plt2.setLabel('bottom',"")   
            self.plt2.setLabel('left',"")
            return
        else :
        # if self.df[self.df.columns[0]][0]== float and self.df[self.df.columns[1]][0]== float :
            self.plt2.plot(self.df[self.df.columns[s1]], self.df[self.df.columns[s]], pen=None, symbol='o', symbolSize=5)
            self.plt2.setLabel('bottom',self.df.columns[s1])   
            self.plt2.setLabel('left',self.df.columns[s])

     

             
    def update_plt1(self):
        self.plt1.clear()
        y, x = np.histogram(self.df[self.df.columns[0]])
        # self.plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/len(x), brush=(107,200,224))
        self.plt1.addItem(barItem)
        self.plt1.setTitle(self.df.columns[0])
 
    def update_plt2(self):
        self.plt2.clear()
        if isinstance(self.df[self.df.columns[0]][0], str) or isinstance(self.df[self.df.columns[1]][0], str) :
            self.plt2.setLabel('bottom',"")   
            self.plt2.setLabel('left',"")
            return
        else :
        # if self.df[self.df.columns[0]][0]== float and self.df[self.df.columns[1]][0]== float :
            self.plt2.plot(self.df[self.df.columns[1]], self.df[self.df.columns[1]], pen=None, symbol='o', symbolSize=5)
            self.plt2.setLabel('bottom',self.df.columns[1])   
            self.plt2.setLabel('left',self.df.columns[1])  

    def showfirstImg(self):
        if self.pn == 0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Wang's Class Demo")
            dlg.setText("已到第一頁")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('確定')
            buttonY = dlg.button(QMessageBox.StandardButton.No)
            buttonY.setText('取消')
            dlg.setIcon(QMessageBox.Icon.Question)
            button = dlg.exec()
        else:
            self.pn = 0
            self.label_img.setPixmap(QPixmap(self.file_src + self.picName[self.pn]))
            self.label_title.setText("第" + str(self.pn + 1) + "頁") 

    def shownextImg(self):
        if self.pn < len(self.picName) - 1:
            self.pn += 1
            self.label_img.setPixmap(QPixmap(self.file_src + self.picName[self.pn]))
            self.label_title.setText("第" + str(self.pn + 1) + "頁") # set Label text
            # self.label_cap.setText(self.comboBox_ImgName.currentText())
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Wang's Class Demo")
            dlg.setText("已到最後一頁")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('確定')
            buttonY = dlg.button(QMessageBox.StandardButton.No)
            buttonY.setText('取消')
            dlg.setIcon(QMessageBox.Icon.Question)
            button = dlg.exec()


    def showlastImg(self):
        if self.pn > 0:
            self.pn -= 1
            self.label_img.setPixmap(QPixmap(self.file_src + self.picName[self.pn]))
            self.label_title.setText("第" + str(self.pn + 1) + "頁") # set Label text
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Wang's Class Demo")
            dlg.setText("已到第一頁")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('確定')
            buttonY = dlg.button(QMessageBox.StandardButton.No)
            buttonY.setText('取消')
            dlg.setIcon(QMessageBox.Icon.Question)
            button = dlg.exec()

    def showlastestImg(self):
        if self.pn == len(self.picName) - 1:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Wang's Class Demo")
            dlg.setText("已到最後一頁")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('確定')
            buttonY = dlg.button(QMessageBox.StandardButton.No)
            buttonY.setText('取消')
            dlg.setIcon(QMessageBox.Icon.Question)
            button = dlg.exec()

        else:
            self.pn = len(self.picName) - 1
            self.label_img.setPixmap(QPixmap(self.file_src + self.picName[self.pn]))
            self.label_title.setText("第" + str(self.pn + 1) + "頁") 
    #-------------------w1
    def update_n(self,s=0):
        s = self.comboBox_alpha.currentIndex()
        self.plt4.clear()
        self.plt4.addLegend()
        self.alpha = [0.01, 0.05, 0.1] 
        n = int(self.lineEdit_n.text())
        sd = np.double(self.lineEdit_sd.text()) / np.sqrt(n)
        mu = np.double(self.lineEdit_mu.text())
        mua = np.double(self.lineEdit_mua.text())
        beta = np.double(self.lineEdit_beta.text())
        if mu <= mua:
            cv = norm.ppf(1-(self.alpha[s]/2),mu,sd)
        else:
            cv = norm.ppf((self.alpha[s]/2),mu,sd)
        if mu <= mua:
            zalpha = norm.ppf(1-(self.alpha[s]/2))
        else:
            zalpha = norm.ppf((self.alpha[s]/2))

        if beta >= 0.5:
            zbeta = norm.ppf(beta)
        else :
            zbeta = norm.ppf(1 -beta)
        std = np.double(self.lineEdit_sd.text())
        n = round((((abs(zalpha) + abs(zbeta)) ** 2)*(std ** 2))/((mu-mua)**2))
        self.lineEdit_n.setText(str(n))
        # if mua >= mu:
        #     beta = round(norm.cdf(cv,mua,sd), 4)
        # else:
        #     beta = round(norm.sf(cv,mua,sd), 4)
        self.lineEdit_beta.setText(str(beta))
        x1 = np.linspace(mu - 5 * sd,mu + 5 * sd, n)
        x2 = np.linspace(mua - 5 * sd,mua + 5 * sd, n)
        self.label_nmu.setText(self.lineEdit_mu.text())
        y1 = norm.pdf(x1,loc = mu, scale = sd)
        y2 = norm.pdf(x2,loc = mua, scale = sd)
        pen = pg.mkPen(color=(255, 0, 0), width = 3)
        pen2 = pg.mkPen(color=(107,200,224), width = 3)
        self.plt4.plot(x1, y1,name = 'H0',pen = pen2)
        self.plt4.plot(x2, y2, pen=pen,name = 'Ha')
        x = np.linspace(norm.ppf(1-self.alpha[s],mu,sd),5 * sd + mu, 200)
        y = norm.pdf(x,mu,sd)
        xa1 = np.linspace(-5 * sd + mu,norm.ppf(self.alpha[s],mu,sd), 200)
        ya1 = norm.pdf(xa1,mu,sd)
        # pen = pg.mkPen(color=(255, 0, 0), width = 10) # Qt.DotLine, Qt.DashDotLine and Qt.DashDotDotLine
        if mu <= mua:
            xa = np.linspace(-5 * sd + mua,cv , 200)
            ya = norm.pdf(xa,mua,sd)
        else:
            xa = np.linspace(cv,5 * sd + mua , 200)
            ya = norm.pdf(xa,mua,sd)
        print(cv)
        cur1 = self.plt4.plot(x, y)
        cur2 = self.plt4.plot(x, np.zeros(len(y)))
        cur11 = self.plt4.plot(xa1, ya1)
        cur21 = self.plt4.plot(xa1, np.zeros(len(ya1)))
        cur3 = self.plt4.plot(xa, ya,pen='r')
        cur4 = self.plt4.plot(xa, np.zeros(len(ya)))
        # add color patch under curve
        patchcur = pg.FillBetweenItem(curve1 = cur1, curve2 = cur2, brush = (107,200,224))
        patchcur1 = pg.FillBetweenItem(curve1 = cur11, curve2 = cur21, brush = (107,200,224))
        patchcura = pg.FillBetweenItem(curve1 = cur3, curve2 = cur4, brush = 'r')
        self.plt4.addItem(patchcur)
        self.plt4.addItem(patchcur1)
        self.plt4.addItem(patchcura)
        pencv = pg.mkPen(color=(0, 204, 153), width=2, style=QtCore.Qt.DashLine) # DotLine
        self.plt4.plot([cv]*2, [0,y1.max()],pen=pencv,name='critical value')
    
    def update_plot(self,s=0):
        s = self.comboBox_alpha.currentIndex()
        self.plt4.clear()
        self.plt4.addLegend()
        self.alpha = [0.01, 0.05, 0.1] 
        n = int(self.lineEdit_n.text())
        sd = np.double(self.lineEdit_sd.text())/np.sqrt(n)
        mu = np.double(self.lineEdit_mu.text())
        mua = np.double(self.lineEdit_mua.text())
        if mu <= mua:
            cv = norm.ppf(1-(self.alpha[s]/2),mu,sd)
        else:
            cv = norm.ppf((self.alpha[s]/2),mu,sd)
        if mua >= mu:
            beta = round(norm.cdf(cv,mua,sd), 4)
        else:
            beta = round(norm.sf(cv,mua,sd), 4)
        self.lineEdit_beta.setText(str(beta))
        x1 = np.linspace(mu - 5 * sd,mu + 5 * sd, n)
        x2 = np.linspace(mua - 5 * sd,mua + 5 * sd, n)
        self.label_nmu.setText(self.lineEdit_mu.text())
        y1 = norm.pdf(x1,loc = mu, scale = sd)
        y2 = norm.pdf(x2,loc = mua, scale = sd)
        pen = pg.mkPen(color=(255, 0, 0), width = 3)
        pen2 = pg.mkPen(color=(107,200,224), width = 3)
        self.plt4.plot(x1, y1,name = 'H0',pen = pen2)
        self.plt4.plot(x2, y2, pen=pen,name = 'Ha')
        x = np.linspace(norm.ppf(1-self.alpha[s],mu,sd),5 * sd + mu, 200)
        y = norm.pdf(x,mu,sd)
        xa1 = np.linspace(-5 * sd + mu,norm.ppf(self.alpha[s],mu,sd), 200)
        ya1 = norm.pdf(xa1,mu,sd)
        # pen = pg.mkPen(color=(255, 0, 0), width = 10) # Qt.DotLine, Qt.DashDotLine and Qt.DashDotDotLine
        if mu <= mua:
            xa = np.linspace(-5 * sd + mua,cv , 200)
            ya = norm.pdf(xa,mua,sd)
        else:
            xa = np.linspace(cv,5 * sd + mua , 200)
            ya = norm.pdf(xa,mua,sd)
        print(cv)
        cur1 = self.plt4.plot(x, y)
        cur2 = self.plt4.plot(x, np.zeros(len(y)))
        cur11 = self.plt4.plot(xa1, ya1)
        cur21 = self.plt4.plot(xa1, np.zeros(len(ya1)))
        cur3 = self.plt4.plot(xa, ya,pen='r')
        cur4 = self.plt4.plot(xa, np.zeros(len(ya)))
        # add color patch under curve
        patchcur = pg.FillBetweenItem(curve1 = cur1, curve2 = cur2, brush = (107,200,224))
        patchcur1 = pg.FillBetweenItem(curve1 = cur11, curve2 = cur21, brush =(107,200,224))
        patchcura = pg.FillBetweenItem(curve1 = cur3, curve2 = cur4, brush = 'r')
        self.plt4.addItem(patchcur)
        self.plt4.addItem(patchcur1)
        self.plt4.addItem(patchcura)
        pencv = pg.mkPen(color=(0, 204, 153), width=2, style=QtCore.Qt.DashLine) # DotLine
        self.plt4.plot([cv]*2, [0,y1.max()],pen=pencv,name='critical value')

    def gridon(self, s):
            # print(self.checkBox_Grid.checkState())
            if s == 2: # 0 : unchecked; 2 : checked
                self.plt4.showGrid(x = True, y = True)   
            else:
                self.plt4.showGrid(x = False, y = False) 
    def gridon_2(self, s):
            # print(self.checkBox_Grid.checkState())
            if s == 2: # 0 : unchecked; 2 : checked
                self.gView.showGrid(x = True, y = True)   
            else:
                self.gView.showGrid(x = False, y = False)

         
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()