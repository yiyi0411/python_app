import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox 
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from matplotlib.pyplot import get
import pandas as pd
import sqlite3
from sqlite3 import Error
from PyQt5.QtGui import QPixmap
import numpy as np
import pyqtgraph as pg 
from collections import Counter
# sys.setrecursionlimit(2000)
# print(sys.getrecursionlimit())
#########################################
class subplotWindow(QWidget):
    # create a customized signal 
    # submitted = QtCore.pyqtSignal(str) # "submitted" is like a component name 
 
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('work2_sub_plot.ui', self)
        self.setWindowTitle('Plot')
        self.widget.setBackground('w')
        win = self.widget
        self.plt1 = win.addPlot(title="p1")
        self.pBut_to_main.clicked.connect(self.on_submit)
        self.textBrowser.setText("   1:Poster / 2:Oral / 3:Spotlight")

    def passInfo(self, df):
        self.plt1.clear()
        # freq = df.groupby([df.columns[2]]).count()
        x = [1, 2, 3]
        # x0 = list(Counter(df[df.columns[2]]).keys())
        d = Counter(df[df.columns[2]])
        y = []
        if d.get('Poster') == None:
            y.append(0)
        else:
            y.append(d.get('Poster'))
        if d.get('Oral') == None:
            y.append(0)
        else:
            y.append(d.get('Oral'))
        if d.get('Spotlight') == None:
            y.append(0)
        else:
           y.append(d.get('Spotlight'))
        # y.append(d.get('Poster'))
        # y.append(d.get('Oral'))
        # y.append(d.get('Spotlight'))
        self.label.setText(str(y[0]))
        self.label_2.setText(str(y[1]))
        self.label_3.setText(str(y[2]))
        
        barItem = pg.BarGraphItem(x = x, height = y, width = 0.6, brush=(107,200,224))
        self.plt1.addItem(barItem )
        self.plt1.setTitle(df.columns[2])
        
 
          
    def on_submit(self):
        self.close()

class AnotherWindow(QWidget):
    # create a customized signal 
    # submitted = QtCore.pyqtSignal(str) # "submitted" is like a component name 
 
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('work2_sub.ui', self)
        self.setWindowTitle('Papers Detail')
        self.pBut_to_main.clicked.connect(self.on_submit)
         
    
    def on_submit(self):
        self.close()
 
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
            return QtGui.QColor('#ffcccc')
 
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
        uic.loadUi('work2_main.ui', self)
        self.table = self.tableView    
        database = r"Database/test.sqlite"
        self.setWindowTitle('Paper Query System')
        # create a database connect
        self.conn = create_connection(database)
        self.cur = self.conn.cursor()
        self.p = 0
        self.item_page = 15
        with self.conn: # with can handle the exceptions, like resources released, cleaning...
            select_table(self)
        # Signals
        # self.select_table.currentIndexChanged.connect(self.queryTable)
        self.upper = self.df.shape[0] - (self.df.shape[0] % self.item_page)
        self.pBut_exit.clicked.connect(self.appEXIT)
        self.next_page.clicked.connect(self.nextpage)
        self.pre_page.clicked.connect(self.prepage)
        self.first_page.clicked.connect(self.firstpage)
        self.last_page.clicked.connect(self.lastpage)
        self.lineEdit.returnPressed.connect(self.select_table_2)
        self.lineEdit.returnPressed.connect(self.combobox)
        # self.comboBox.clear()
        for i in range(int(self.upper / self.item_page) + 1):
            self.comboBox.addItem(str(i + 1))
        self.comboBox.currentIndexChanged.connect(self.selectpage)
        self.pushButton.clicked.connect(self.select_table_2)
        self.pushButton.clicked.connect(self.combobox)
         # Signal
        self.table.doubleClicked.connect(self.call_subWin)
        self.table.doubleClicked.connect(self.rowSelected)
        self.table.clicked.connect(self.rowSelected_main)
        self.comboBox_3.currentIndexChanged.connect(self.select_table_2)
        self.comboBox_3.currentIndexChanged.connect(self.combobox)
        self.pBut_papers.clicked.connect(self.call_subplotWin)
        self.actionsave_file.triggered.connect(self.saveData)
         
    # Slots
    def call_subplotWin(self):
        # create a sub-window
        self.subplotiwndow = subplotWindow()
        # pass information to sub-window
        self.subplotiwndow.passInfo(self.df) 
        self.subplotiwndow.show()

    def rowSelected_main(self, mi):
        print([mi.row()+ self.p , mi.column()])
        if 'Abstract' in self.df.columns:
            col_list = list(self.df.columns)
        else:
            print('No Abstract from the Query')
            return
        # display Abstract on TextBrowser, then go fetch author names
        self.textBrowser_2.setText(self.df.iloc[mi.row()+ self.p, col_list.index('Title')])
        show_authors(self, self.df.iloc[mi.row()+ self.p, 0])

    def rowSelected(self, mi):
        # print([mi.row()+ self.p, mi.column()])
        if 'Abstract' in self.df.columns:
            col_list = list(self.df.columns)
        else:
            print('No Abstract from the Query')
            return
        # display Abstract on TextBrowser, then go fetch author names
        self.anotherwindow.textBrowser_abstract.setText(self.df.iloc[mi.row()+ self.p, col_list.index('Abstract')])
        self.anotherwindow.textBrowser_title.setText(self.df.iloc[mi.row()+ self.p, col_list.index('Title')])
        self.textBrowser_2.setText(self.df.iloc[mi.row()+ self.p, col_list.index('Title')])
        self.anotherwindow.textBrowser_papertext.setText(self.df.iloc[mi.row()+ self.p, col_list.index('PaperText')])
        self.anotherwindow.label_type.setText(self.df.iloc[mi.row()+ self.p, col_list.index('EventType')])
        self.anotherwindow.label_Img.setPixmap(QPixmap(u"Database/NIP2015_Images/" + self.df.iloc[mi.row()+ self.p, col_list.index('imgfile')]))
        show_authors(self, self.df.iloc[mi.row()+ self.p, 0])
        names = show_authors(self, self.df.iloc[mi.row()+ self.p, 0])
        self.anotherwindow.textBrowser_ators.setText(names.replace(";", "/"))
    
    def call_subWin(self):
        # create a sub-window
        self.anotherwindow = AnotherWindow()
        self.anotherwindow.show()
        
        
    
    # Slots
    def combobox(self):
        # select_table(self)
        if len(self.rows_) !=0:
            self.upper = self.df.shape[0] - (self.df.shape[0] % self.item_page)
            self.comboBox.clear()
            if self.df.shape[0] % self.item_page != 0 or self.upper < self.item_page:
                for i in range(int(self.upper / self.item_page) + 1):
                        self.comboBox.addItem(str(i + 1))
            else:
                self.upper = self.upper - self.item_page
                for i in range(int(self.upper / self.item_page)+ 1):
                        self.comboBox.addItem(str(i + 1))
        
        
    def selectpage(self):
        self.p = self.comboBox.currentIndex() * self.item_page 
        select_table(self)
        self.label_p.setText(str(int(self.p / self.item_page) + 1))

    def select_table_2(self,s=0):
        s = self.comboBox_2.currentIndex()
        s1 = self.comboBox_3.currentIndex()
        w = self.lineEdit.text()
        if s1 == 0:
            eventtype = ""
            eventtype0 = ""
        elif s1 == 1:
            eventtype = "eventtype = \'Poster' and "
            eventtype0 = " where eventtype = \'Poster'"
        elif s1 == 2:
            eventtype = "eventtype = \'Oral' and "
            eventtype0 = " where eventtype = \'Oral'"
        elif s1 == 3:
            eventtype = "eventtype = \'Spotlight' and "
            eventtype0 = " where eventtype = \'Spotlight'"
        
        if s == 0 and self.lineEdit.isModified() == False:
            sql = "select * from papers" + eventtype0
        elif s == 0 and self.lineEdit.isModified() == True:
            sql = "select * from papers where " + eventtype + "  (id like '%{}%' or pdfname like '%{}%'\
                or Abstract like '%{}%' or PaperText like '%{}%' or id in (select distinct(paperid) \
            from paperauthors A, authors B \
                where B.name like '%{}%' and A.authorid = B.id))".format(w,w,w,w,w)
        elif s == 1:
            sql = "select * from papers where " + eventtype + " id in (select distinct(paperid) \
            from paperauthors A, authors B \
                where B.name like '%{}%' and A.authorid = B.id)".format(w)
        elif s == 2:
            sql = "select * from papers where " + eventtype + " title like '%{}%'".format(w)
        elif s == 3:
            sql = "select * from papers where id == {}".format(w)
        elif s == 4:
            sql = "select * from papers where " + eventtype + " pdfname like '%{}%'".format(w)
        elif s == 5:
            sql = "select * from papers where" + eventtype + " Abstract like '%{}%'".format(w)
        elif s == 6:
            sql = "select * from papers where " + eventtype + " PaperText like '%{}%'".format(w)
        SQLExecute(self, sql)
        rows,p = SQLExecute(self, sql)
        self.pBut_papers.setText(str(len(rows)))
        if len(rows) == 0: # nothing found
        # raise a messageBox here
            dlg = QMessageBox(self)
            dlg.setWindowTitle("SQL Information: ")
            dlg.setText("Nothing Found !!!")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('OK')
            dlg.setIcon(QMessageBox.Icon.Information)
            button = dlg.exec()
        else:totabl(self, rows, p)
        
    def saveData(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 
            "", "EXCEL files (*.xlsx)")
        if len(fname) != 0:
            self.df.to_excel(fname)
        
    def appEXIT(self):
        self.conn.close() # close database
        self.close() # close app

    def nextpage(self):
        if self.p < self.upper:
            self.p = self.p + self.item_page
            select_table(self)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Page Information: ")
            dlg.setText("已經是最後一頁 !!!")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('OK')
            dlg.setIcon(QMessageBox.Icon.Information)
            button = dlg.exec()    
        self.label_p.setText(str(int(self.p / self.item_page) + 1))
        self.comboBox.setCurrentIndex(int(self.p / self.item_page))
        
    
    def prepage(self):
        if self.p > 0:
            self.p = self.p - self.item_page
            select_table(self)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Page Information: ")
            dlg.setText("已經是第一頁 !!!")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('OK')
            dlg.setIcon(QMessageBox.Icon.Information)
            button = dlg.exec()
        self.label_p.setText(str(int(self.p / self.item_page) + 1))
        self.comboBox.setCurrentIndex(int(self.p / self.item_page))

    def firstpage(self):
        if self.p == 0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Page Information: ")
            dlg.setText("已經是第一頁 !!!")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('OK')
            dlg.setIcon(QMessageBox.Icon.Information)
            button = dlg.exec()
        else:
            self.p = 0
            select_table(self)
        self.label_p.setText(str(int(self.p / self.item_page) + 1))
        self.comboBox.setCurrentIndex(int(self.p / self.item_page))

    def lastpage(self):
        if self.p == self.upper:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Page Information: ")
            dlg.setText("已經是最後一頁 !!!")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('OK')
            dlg.setIcon(QMessageBox.Icon.Information)
            button = dlg.exec()
        else:
            self.p = self.upper
            select_table(self)
        self.label_p.setText(str(int(self.p / self.item_page) + 1))
        self.comboBox.setCurrentIndex(int(self.p / self.item_page))
     
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
def select_table(self,s = 0, s1 =0):
        s = self.comboBox_2.currentIndex()
        s1 = self.comboBox_3.currentIndex()
        w = self.lineEdit.text()
        if s1 == 0:
            eventtype = ""
            eventtype0 = ""
        elif s1 == 1:
            eventtype = "eventtype = \'Poster' and "
            eventtype0 = " where eventtype = \'Poster'"
        elif s1 == 2:
            eventtype = "eventtype = \'Oral' and "
            eventtype0 = " where eventtype = \'Oral'"
        elif s1 == 3:
            eventtype = "eventtype = \'Spotlight' and "
            eventtype0 = " where eventtype = \'Spotlight'"
        
        if s == 0 and self.lineEdit.isModified() == False:
            sql = "select * from papers" + eventtype0
        elif s == 0 and self.lineEdit.isModified() == True:
           sql = "select * from papers where " + eventtype + "  (id like '%{}%' or pdfname like '%{}%'\
                or Abstract like '%{}%' or PaperText like '%{}%' or id in (select distinct(paperid) \
            from paperauthors A, authors B \
                where B.name like '%{}%' and A.authorid = B.id))".format(w,w,w,w,w)
        elif s == 1:
            sql = "select * from papers where " + eventtype + " id in (select distinct(paperid) \
            from paperauthors A, authors B \
                where B.name like '%{}%' and A.authorid = B.id)".format(w)
        elif s == 2:
            sql = "select * from papers where " + eventtype + " title like '%{}%'".format(w)
        elif s == 3:
            sql = "select * from papers where id == {}".format(w)
        elif s == 4:
            sql = "select * from papers where " + eventtype + " pdfname like '%{}%'".format(w)
        elif s == 5:
            sql = "select * from papers where" + eventtype + " Abstract like '%{}%'".format(w)
        elif s == 6:
            sql = "select * from papers where " + eventtype + " PaperText like '%{}%'".format(w)
        SQLExecute(self, sql)
        rows,p = SQLExecute(self, sql)
        self.pBut_papers.setText(str(len(rows)))
        if len(rows) == 0: # nothing found
        # raise a messageBox here
            dlg = QMessageBox(self)
            dlg.setWindowTitle("SQL Information: ")
            dlg.setText("Nothing Found !!!")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
            buttonY = dlg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('OK')
            dlg.setIcon(QMessageBox.Icon.Information)
            button = dlg.exec()
        else:totabl(self, rows, p)
        # self.upper = self.df.shape[0] - (self.df.shape[0] % 10)
        # self.comboBox.clear()
        # for i in range(int(self.upper / self.item_page) + 1):
        #         self.comboBox.addItem(str(i + 1))

def SQLExecute(self, SQL):
    """
    Execute a SQL command and display the requested items on the QTableView
    :param conn: SQL command
    :return: None
    """
    # cur = self.conn.cursor()
    try:
        self.cur.execute(SQL)
    except Error as e:
        display_message(str(e))
        return None
   
    rows = self.cur.fetchall()
    self.rows_ = rows
    p = self.p
    return rows,p
    # Process fetched output

def totabl(self, rows, p):
    names = [description[0] for description in self.cur.description]# extract column names
    self.df = pd.DataFrame(rows)
    self.df.index = self.df.index + 1
    self.df.columns = names
    self.model = TableModel(self.df[p:p +  self.item_page])
    self.table.setModel(self.model)
    self.table.resizeColumnToContents(0) # resize the width of the 1st column

def display_message(message):
    dlg = QMessageBox()
    dlg.setWindowTitle("SQL Information: ")
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
    buttonY = dlg.button(QMessageBox.StandardButton.Yes)
    buttonY.setText('OK')
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.exec()

def show_authors(self, paperid):
    sql = "select name from authors A, paperauthors B where B.paperid="+str(paperid)+" and A.id=B.authorid"
    with self.conn:
        self.rows = SQLExecute(self, sql)[0]
        names =""
        for row in self.rows:
            names = names + row[0] +"; "
        self.textBrowser_authors.setText(names)
        self.pBut_authors.setText(str(names.count(";")))
        return names
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()

