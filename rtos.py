#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RTOS - Real Time Operating System Process scheduler
"""
import sys
import os
import random
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from collections import defaultdict
from PyQt5 import QtWidgets, uic


matplotlib.use('QT5Agg')


# uic paths from itself, not the active dir, so path needed
path = os.path.dirname(__file__)
# Ui file name, from QtDesigner, assumes in same folder as this .py
QT_CREATOR_FILE = "/home/lukas/Programowanie_kod/Projekty_Studia_air/SCR_project/szablon_scr.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(
    QT_CREATOR_FILE)  # process through pyuic


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    """GUI class"""

    def __init__(self):
        """Constructor of the MyApp class"""
        super().__init__()
        # set ups gui
        self.init_ui()
        # create canvas
        self.canvas_figure()

    def init_ui(self):
        '''Sets up the user interface of the application'''
        # create ui
        self.use_inter = Ui_MainWindow()
        self.use_inter.setupUi(self)
        # random file the table
        self.adding_rows()
        # Connects the spinBox widget's valueChanged signal to the adding_rows_by_user
        self.use_inter.spinBox.valueChanged.connect(self.adding_rows_by_user)
        # Connects the tabele widget's itemChanged signal to the adding_rows_by_user
        self.use_inter.tabele.itemChanged.connect(self.adding_rows_by_user)

        self.use_inter.checkBox_PRIORYTET.toggled.connect(
            self.selection_algorithm)
        self.use_inter.checkBox_RMS.toggled.connect(self.selection_algorithm)
        self.use_inter.checkBox_EDF.toggled.connect(self.selection_algorithm)

        self.use_inter.pushButton.clicked.connect(self.close_programm)
        # self.use_inter.pushButton_2.clicked.connect(self.selection_algorithm)
        self.use_inter.pushButton_3.clicked.connect(self.adding_rows_test)

    def adding_rows_by_user(self):
        """Add rows to the table as specified by the user input."""
        row_amount = self.use_inter.spinBox.value()
        tabelerows = self.use_inter.tabele.setRowCount(row_amount)

        return row_amount

    def adding_rows_test(self):
        """This function adds rows to the table with fixed values for
        the first 4 rows and random values for the rest.

        Returns:
            int: The number of rows added to the table.
        """
        row_amount = self.use_inter.spinBox.value()
        self.use_inter.tabele.setRowCount(row_amount)

        for row in range(row_amount):
            for col in range(3):
                tab = self.use_inter.tabele
                if row < 4:
                    if col == 0:
                        tab.setItem(
                            row, col, QtWidgets.QTableWidgetItem(str(row + 1)))
                    elif col == 1:
                        tab.setItem(
                            row, col, QtWidgets.QTableWidgetItem(str(5 * (row + 1))))
                    elif col == 2:
                        tab.setItem(
                            row, col, QtWidgets.QTableWidgetItem(str(row)))
                else:
                    if col == 0:
                        tab.setItem(row, col, QtWidgets.QTableWidgetItem(
                            str(random.randint(1, 4))))
                    elif col == 1:
                        tab.setItem(row, col, QtWidgets.QTableWidgetItem(
                            str(random.randint(1, 15))))
                    elif col == 2:
                        tab.setItem(
                            row, col, QtWidgets.QTableWidgetItem(str(row)))

        return row_amount

    def adding_rows(self):
        """Add a specified number of rows to the table widget.

        The number of rows to add is determined by the value set in the spinBox widget.
        The table widget will have random integer values (0-10) in each cell.

        Returns:
            int: The number of rows added to the table widget.
        """
        row_amount = self.use_inter.spinBox.value()
        self.use_inter.tabele.setRowCount(row_amount)

        for row in range(row_amount):
            for col in range(4):
                item = QtWidgets.QTableWidgetItem(str(random.randint(0, 10)))
                self.use_inter.tabele.setItem(row, col, item)

        return row_amount

    def selection_algorithm(self):
        """Determines which scheduling algorithm to use based on user selection"""
        row_amount = self.adding_rows_by_user() + self.adding_rows_test()

        if self.use_inter.checkBox_PRIORYTET.isChecked():
            self.use_inter.pushButton_2.clicked.connect(self.wykres_pr)
        elif self.use_inter.checkBox_RMS.isChecked():
            self.use_inter.pushButton_2.clicked.connect(self.wykres_rms)
        elif self.use_inter.checkBox_EDF.isChecked():
            self.use_inter.pushButton_2.clicked.connect(self.wykres_edf)

    def data_from_tab_to_dict(self):
        """Converts data from a QtWidgets.QTableWidget to a dictionary"""
        tab = self.use_inter.tabele
        rows, columns = tab.rowCount(), tab.columnCount()
        my_dict = defaultdict(list)

        for i in range(rows):
            for j in range(columns):
                item = tab.item(i, j)
                if item:
                    if j == 0:
                        my_dict[str(i)].append(float(item.text()))
                    else:
                        my_dict[str(i)].append(float(item.text()))

        return my_dict

    def data_from_tab_to_list(self):
        """Converts data from a QtWidgets.QTableWidget to two separate lists"""
        tab = self.use_inter.tabele
        rows, columns = tab.rowCount(), tab.columnCount()
        list_t = []

        for i in range(rows):
            for j in range(columns):
                item = tab.item(i, j)
                if item:
                    list_t.append(int(item.text().replace(',', '')))

        list_t1, list_t2 = list_t[::3], list_t[2::3]
        list_t1 = ' '.join(map(str, list_t1))
        list_t2 = ' '.join(map(str, list_t2))

        return list_t1, list_t2

    def multifunction(self):
        """
        Returns:
            processes:, a dictionary of the data from the user's table
            lcm: the least common multiple of the periods of each process in the table
            scheme: a list of zeros with a length equal to the number of processes in the table.
        """
        self.gan.clear()

        processes = self.data_from_tab_to_dict()

        lcm = 1
        for process_period in processes.values():
            lcm = int(np.lcm(lcm, int(process_period[1])))

        # how often specific peroid occurs
        scheme = [0 for i in range(len(processes))]

        keys = [int(key) + 0.225 for key in processes]
        key_labels = ['P' + key for key in processes]

        # Setting Y-axis
        self.gan.set_ylim(0, len(processes) + 1)
        self.gan.set_yticks(keys)
        self.gan.set_yticklabels(key_labels)

        return processes, lcm, scheme

    def wykres_pr(self):
        """Priority algorithm"""
        processes, lcm, scheme = self.multifunction()

        # Calculate end times and sort processes based on priority
        burst_times, priorities = zip(
            *[(processes[key][0], processes[key][1]) for key in processes])
        end_times = []
        processes = list(zip(burst_times, priorities,
                         range(1, len(processes) + 1)))
        processes.sort(key=lambda x: x[1])

        end_times.append(processes[0][0])

        for i in range(1, len(processes)):
            end_time = end_times[i - 1] + processes[i][0]
            end_times.append(end_time)

            for burst_time, priority, process_num in processes:
                self.gan.broken_barh([(burst_time, 0.9)],
                                     ((process_num -1) , 0.45), facecolors=('black'))
                self.gan.broken_barh([(0, max(end_times))], ((process_num-1), 0.02),
                                     facecolors=('orange'))
    
                # self.gan.broken_barh([(burst_time * process_num, 0.1)], (i-1, 0.7),
                #                      facecolors=('blue'))
        self.canvas.draw()

    def wykres_rms(self):
        """Real-Time Scheduling (RMS) algorithm """
        processes, lcp, scheme = self.multifunction()

        for time in range(lcp):
            for process_key in processes:
                if (time % int(processes[process_key][1])) == 0:
                    scheme[int(processes[process_key][2])] = int(
                        processes[process_key][0])

            for exect in range(len(scheme)):
                # wypisujemy poszczegolne wywolania procesow
                # przechodzimy przez liczbe procesow [0, 0, 0..]
                if scheme[exect] != 0:
                    period_numb = exect + 1
                    self.gan.broken_barh([(time, 0.9)], ((period_numb - 1), 0.45),
                                         facecolors=('black'))
                    for key in processes:
                        period = processes.get(key)[1]
                        ilosc = lcp // period
                        for i in range(int(ilosc)):
                            self.gan.broken_barh([(period * i, 0.1)], ((int(key)), 0.7),
                                                 facecolors=('blue'))
                    self.gan.broken_barh([(0, lcp)], ((period_numb - 1), 0.02),
                                         facecolors=('orange'))
                    scheme[exect] -= 1
                    break

        self.canvas.draw()

    def wykres_edf(self):
        """Earliest Deadline First (EDF) algorithm"""
        processes, lcp, scheme = self.multifunction()

        for time in range(lcp):
            # When the current time mod period is zero, it means a new task is arriving.
            # Thus we refresh the scheme accordingly.
            for process_key in processes:
                if (time % int(processes.get(process_key)[1])) == 0:
                    scheme[int(processes.get(process_key)[2])] = int(
                        processes.get(process_key)[0])
            to_next_dead_line = [999 for number in range(len(processes))]
            no_task = 1

            for exect in range(len(scheme)):
                value = processes.get(str(exect + 1))

                if value is not None:
                    to_next_dead_line[exect] = value[1] - (time % value[1])
                    no_task = 0

            if no_task == 1:
                continue
            # execute proscess with nearest deadlin
            run_numb = int(to_next_dead_line.index(min(to_next_dead_line)))
            period_numb = run_numb + 1
            self.gan.broken_barh([(time, 0.9)], ((period_numb - 1), 0.45),
                                 facecolors=('black'))

            for key in processes:
                period = processes.get(key)[1]
                ilosc = lcp // period
                for i in range(int(ilosc)):
                    self.gan.broken_barh([(period * i, 0.1)], ((int(key)), 0.7),
                                         facecolors=('blue'))

            self.gan.broken_barh([(0, lcp)], ((period_numb), 0.02),
                                 facecolors=('orange'))

            scheme[exect] -= 1

        self.canvas.draw()

    def canvas_figure(self):
        """Drawing everything"""
        # a figure instance to plot on
        self.figure, self.gan = plt.subplots()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas)

        # set the layout
        layout = self.use_inter.chart
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        # self.setLayout(layout)

        # Setting labels for x-axis and y-axis
        self.gan.set_xlabel('seconds since start')
        self.gan.set_ylabel('Processor')
        # Setting graph attribute
        self.gan.grid(True)

    def close_programm(self):
        """Closing application"""
        matplotlib.pyplot.close()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # instantiate a QtGui (holder for the app)
    window = MyApp()
    window.show()
