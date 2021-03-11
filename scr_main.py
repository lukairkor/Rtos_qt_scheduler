import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtWidgets
import random
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt 
import numpy as np
from collections import defaultdict

from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

path = os.path.dirname(__file__) #uic paths from itself, not the active dir, so path needed
qtCreatorFile = "/home/lukas/Programowanie_kod/Projekty_Studia_air/SCR_project/szablon_scr.ui" #Ui file name, from QtDesigner, assumes in same folder as this .py

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) #process through pyuic

class MyApp(QMainWindow, Ui_MainWindow): #gui class
    
    def __init__(self):
        #The following sets up the gui via Qt
        super(MyApp, self).__init__()
        self.initUI()


    def initUI(self): 
        '''initiates application UI'''
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.adding_rows() #losuje wypelnia tabelke
        
        self.ui.spinBox.valueChanged.connect(self.adding_rows_by_user)
        self.ui.tabele.itemChanged.connect(self.adding_rows_by_user)

        self.canvas_figure()

        self.ui.checkBox_PRIORYTET.toggled.connect(self.selection_algorithm)
        self.ui.checkBox_RMS.toggled.connect(self.selection_algorithm)
        self.ui.checkBox_EDF.toggled.connect(self.selection_algorithm)

        self.ui.pushButton.clicked.connect(self.close_programm)
        # self.ui.pushButton_2.clicked.connect(self.selection_algorithm)
        self.ui.pushButton_3.clicked.connect(self.adding_rows_test)
        

    def adding_rows_by_user(self):

        row_amount = self.ui.spinBox.value()        
        tabelerows = self.ui.tabele.setRowCount(row_amount)

        return row_amount
        

    def adding_rows_test(self):
        
        row_amount = self.ui.spinBox.value()        
        tabelerows = self.ui.tabele.setRowCount(row_amount)
        
        for x in range(0, row_amount):
            
            for y in range(0,3):

                tab = self.ui.tabele
                if x ==0:
                    if y ==0:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(1)))
                    elif y ==1:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(5)))
                    elif y ==2:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(0)))    
                elif x ==1:
                    if y ==0:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(1)))
                    elif y ==1:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(10)))
                    elif y ==2:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(1)))   
                elif x ==2:
                    if y ==0:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(2)))
                    elif y ==1:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(20)))
                    elif y ==2:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(2)))   
                elif x ==3:
                    if y ==0:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(10)))
                    elif y ==1:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(5)))
                    elif y ==2:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(3)))   
                else:
                    if y ==0:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(random.randint(1, 4))))
                    elif y ==1:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(random.randint(1, 15))))
                    elif y ==2:
                        tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(x)))   

        return row_amount

        
    # def adding_rows(self):
        
        row_amount = self.ui.spinBox.value()        
        tabelerows = self.ui.tabele.setRowCount(row_amount)
        
        for x in range(0, row_amount):
            
            for y in range(0,4):

                tab = self.ui.tabele
                tab.setItem(x,y, QtWidgets.QTableWidgetItem(str(random.randint(0, 10))))

        return row_amount


    def selection_algorithm(self):
        # self.ui.groupBox.addWidget(self.ui.checkBox_PRIORYTET)
        # self.ui.groupBox.addWidget(self.ui.checkBox_RMS)
        # self.ui.groupBox.addWidget(self.ui.checkBox_EDF)
        row_amount = self.adding_rows_by_user()
        row_amount = self.adding_rows_test()

        if self.ui.checkBox_PRIORYTET.isChecked():
            self.ui.pushButton_2.clicked.connect(self.wykres_pr)
        elif self.ui.checkBox_RMS.isChecked():
            self.ui.pushButton_2.clicked.connect(self.wykres_rms)
        elif self.ui.checkBox_EDF.isChecked():
            self.ui.pushButton_2.clicked.connect(self.wykres_edf)
           

    def data_from_tab_to_list(self):

        tab = self.ui.tabele #QtWidgets.QTableWidget
        l = []
        rows = tab.rowCount()
        columns = tab.columnCount()

        #writing data from tabele to list l
        for i in range(0, rows):
            
            for j in range(0, columns):
            
                itemm = tab.item(i, j)
                item_text = itemm.text()
                l.append(item_text)

        l = [int(n) for x in l for n in x.split(',')] #from str to int ['1','2'] to [1,2] l = [1 t.trwania, 2 okres/termin, 3 priorytet] 
        l1, l2 = (x[i::3] for x in [l] for i in (0,2)) #Split list elements by comma

        #map(function, iterables) 
        l1 = ' '.join(map(str, l1))  #list of czas przetwarzania 
        l2 = ' '.join(map(str, l2))  #list of prioritise                                            

        print("l",l,'\nl1',l1,'\nl2',l2)
        return  l1, l2


    def data_from_tab_to_dict(self):

        tab = self.ui.tabele #QtWidgets.QTableWidget
        my_dict = defaultdict(list)
        rows = tab.rowCount()
        columns = tab.columnCount()
        
        for i in range(0, rows):
            for j in range(0, columns):
                itemm = tab.item(i, j)
                item_text = itemm.text()
                my_dict[str(i)].append(item_text)
                mydict = my_dict
        return mydict


    def wykres_pr(self):
        
        tab = self.ui.tabele
        row_amount = self.adding_rows_by_user()
        data_in_list1, data_in_list2 = self.data_from_tab_to_list()

        # row_amount = nn
        str_okrs = ""
        str_priorytet = ""
        nr_proces = []

        
        #process from 1 not 0
        for i in range(0, row_amount):
            #list_name.insert(index, element)
            nr_proces.insert(i,i+1)

        bt = list(map(int, data_in_list1.split())) #czas_przetwarzania burst_time
        priority = list(map(int, data_in_list2.split()))
        print(bt,'\n',priority)
        end_time = []
        priority = []

        # Sorting processes burst time(czas_przetwarzania), on the basis of their priority(priorytet)
        for i in range(0, len(priority)-1):
            for j in range(0,len(priority)-i-1):
                if(priority[j]>priority[j+1]):
                    swap = priority[j]
                    priority[j] = priority[j+1]
                    priority[j+1] = swap
        
                    swap = bt[j]
                    bt[j] = bt[j+1]
                    bt[j+1] = swap

                    swap = nr_proces[j]
                    nr_proces[j] = nr_proces[j+1]
                    nr_proces[j+1] = swap
        
        priority.insert(0,0)
        end_time.insert(0,bt[0])
        
        #Calculating of waiting time(priorytet) and Turn Around Time(okres) of each process
        for i in range(1,len(nr_proces)):
            priority.insert(i,priority[i-1]+bt[i-1])
            end_time.insert(i,priority[i]+bt[i])
        priority.sort()   

        self.gan.clear()

        for i in range(row_amount):

            nr_proces_s= nr_proces[i] #proces
            bt_s = bt[i] #czas_przetwarzania
            priority_s= priority[i] #waiting time
            end_time_s = end_time[i] #turn around time 
            end_time_s1 = end_time[i-1]

            self.gan.broken_barh([(priority_s, bt_s)],  (nr_proces_s,0.7),
                        facecolors =('black'))
             

        self.canvas.draw()


    def data_from_tab_to_dict(self):

        tab = self.ui.tabele #QtWidgets.QTableWidget
        my_dict = defaultdict(list)
        rows = tab.rowCount()
        columns = tab.columnCount()
        
        for i in range(0, rows):
            for j in range(0, columns):
                itemm = tab.item(i, j)
                item_text = itemm.text()
                item_text = int(item_text)
                my_dict[str(i+1)].append(item_text)
                mydict = dict(my_dict)
        return mydict


    def wykres_rms(self):  

        self.gan.clear()

        processes = self.data_from_tab_to_dict()

        #obliczamy najmniejsza wspolna wielokrotnosc okresow np.lcm.reduce([3, 12, 20])60
        lcp = 1
        for period in processes.values(): 
            lcp = np.lcm(lcp, period[1]) 
            
        # print(lcp)
        #lista przechowujaca ilosc pojawien poszczegol nego okresu
        Scheme = [0 for n in range(len(processes))] 


        keyss = len(processes)
        keys = []
        keysorg = []
        for keyy in processes:
            # print('key\n',key)
            key = int(keyy)
            key = key+0.225
            keys.append(key)
        for keyy in processes:
            # print('key\n',key)
            keyy = 'P'+keyy
            keysorg.append(keyy)

        
        for time in range(0, lcp):
            for key in processes:

                if (time % processes.get(key)[1]) == 0:
                    Scheme[processes.get(key)[2]] = processes.get(key)[0] 
                    # print('scheme\n',Scheme)

            #wypisujemy poszczegolne wywolania procesow
            for exect in range(0, len(Scheme)): #przechodzimy przez liczbe procesow [0, 0, 0..]
                    if Scheme[exect] != 0:
                        
                        period_numb = exect + 1

                        # Setting Y-axis  
                        self.gan.set_ylim(0, keyss+1) 
                        self.gan.set_yticks(keys)
                        self.gan.set_yticklabels(keysorg)


                        self.gan.broken_barh([(time, 0.9)], ((period_numb),0.45), 
                                            facecolors =('black'))
                                            
                        for key in processes:
                            okres = processes.get(key)[1]
                            ilosc = lcp / okres
                            ilosc = int(ilosc)
                            for x in range(ilosc):
                                self.gan.broken_barh([(okres*x, 0.1)], ((int(key)),0.7), 
                                                facecolors =('blue'))

                        self.gan.broken_barh([(0, lcp)], ((period_numb),0.02), 
                                            facecolors =('orange'))
                           
                        Scheme[exect] = Scheme[exect] - 1
                        break

        self.canvas.draw()


    def wykres_edf(self): 

        self.gan.clear()
        
        processes = self.data_from_tab_to_dict()
            
        #obliczamy najmniejsza wspolna wielokrotnosc okresow np.lcm.reduce([3, 12, 20])60
        lcp = 1
        for period in processes.values():
            lcp = np.lcm(lcp, period[1])

        #kolejnosc na bazie nazwy procesu
        #ile czasu dla kazdego procesu aby zakonczyc w okresie
        Scheme = [0 for number in range(len(processes))]

        keyss = len(processes)
        keys = []
        keysorg = []
        for keyy in processes:
            # print('key\n',key)
            key = int(keyy)
            key = key+0.225
            keys.append(key)
        for keyy in processes:
            # print('key\n',key)
            keyy = 'P'+keyy
            keysorg.append(keyy)


        for time in range(0, lcp):
        # When the current time mod period is zero, it means a new task is arriving.
        # Thus we refresh the Scheme accordingly.
            for p in processes:
                if (time % processes.get(p)[1]) == 0:
                    Scheme[processes.get(p)[2]] = processes.get(p)[0]
        
            ToNextDeadline = [999 for number in range(len(processes))]
            no_task = 1
            for exect in range(0, len(Scheme)):
        # Jezeli jeszcz nie koniec rob dalej
                if Scheme[exect] != 0:
                    ToNextDeadline[exect] = processes.get(str(exect + 1))[1] - (time % processes.get(str(exect + 1))[1])
                                   
                                        
                    no_task = 0
        
            if no_task == 1:
                continue
        # Wykonujemy proces z najblizszym deadlin
            run_numb = ToNextDeadline.index(min(ToNextDeadline))

            # Setting Y-axis  
            self.gan.set_ylim(0, keyss+1) 
            self.gan.set_yticks(keys)
            self.gan.set_yticklabels(keysorg)

            period_numb = run_numb + 1

            self.gan.broken_barh([(time, 0.9)], ((period_numb),0.45), 
                                                    facecolors =('black'))

            for key in processes:
                okres = processes.get(key)[1]
                ilosc = lcp / okres
                ilosc = int(ilosc)
                for x in range(ilosc):
                    self.gan.broken_barh([(okres*x, 0.1)], ((int(key)),0.7), 
                                    facecolors =('blue'))

            self.gan.broken_barh([(0, lcp)], ((period_numb),0.02), 
                                facecolors =('orange'))


            Scheme[run_numb] = Scheme[run_numb] - 1

        self.canvas.draw()


    def canvas_figure(self):
       
        # a figure instance to plot on
        self.figure, self.gan = plt.subplots()
        
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # set the layout
        layout = self.ui.chart
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        # self.setLayout(layout)

        # Setting labels for x-axis and y-axis 
        self.gan.set_xlabel('seconds since start') 
        self.gan.set_ylabel('Processor') 
        # Setting graph attribute 
        self.gan.grid(True) 
    

    def close_programm(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv) #instantiate a QtGui (holder for the app)
    window = MyApp()
    window.show()
    # print('ddd')
    sys.exit(app.exec_())
