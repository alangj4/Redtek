# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinter import ttk
import math
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import xfoil as xf
from xfoil import *
from xfoil.model import Airfoil


##############################################################################

# WINDOW CONFIGURATION

##############################################################################

HEIGHT = 900
WIDTH = 1100

root = Tk()
root.title("Redtek propeller creator")
root.resizable(width=False, height=False)

canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

logo_Redtek = ImageTk.PhotoImage(Image.open("logo.jpg"))
logo = Label(canvas, image=logo_Redtek)
logo.place(relx=0.5, anchor='n')

upframe = Frame(root)
upframe.place(relx=0.5, rely=0.07, relwidth=0.95, relheight=0.3, anchor='n')

lowframe = ttk.Notebook(root)
lowframe.place(relx=0.5, rely=0.4, relwidth=0.99, relheight=0.6, anchor='n')

# TAB 1 CONFIGURATION
tab1 = ttk.Frame(lowframe)
lowframe.add(tab1, text='Airfoil analysis')

geometryframe = Frame(tab1, bd=1, relief=SUNKEN)
geometryframe.place(relx=0.258, rely=0.5, relwidth=0.47, relheight=0.46, anchor='n')

plotframe = ttk.Notebook(tab1)
plotframe.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=1, anchor='w')
cl_plot = ttk.Frame(plotframe)
plotframe.add(cl_plot, text='CL vs. alpha')
cd_plot = ttk.Frame(plotframe)
plotframe.add(cd_plot, text='CD vs. alpha')
cl_cd_plot = ttk.Frame(plotframe)
plotframe.add(cl_cd_plot, text='CL vs. CD')

# TAB 2 CONFIGURATION
tab2 = ttk.Frame(lowframe)
lowframe.add(tab2, text='Find optimum airfoil')

# TAB 3 CONFIGURATION
tab3 = ttk.Frame(lowframe)
lowframe.add(tab3, text='Airfoil comparison')

geometryframe31 = Frame(tab3, bd=1, relief=SUNKEN)
geometryframe31.place(relx=0.3655, rely=0.5, relwidth=0.235, relheight=0.22, anchor='n')

geometryframe32 = Frame(tab3, bd=1, relief=SUNKEN)
geometryframe32.place(relx=0.3655, rely=0.725, relwidth=0.234, relheight=0.22, anchor='n')

plotframe3 = ttk.Notebook(tab3)
plotframe3.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=1, anchor='w')
cl_plot3 = ttk.Frame(plotframe3)
plotframe3.add(cl_plot3, text='CL vs. alpha')
cd_plot3 = ttk.Frame(plotframe3)
plotframe3.add(cd_plot3, text='CD vs. alpha')
cl_cd_plot3 = ttk.Frame(plotframe3)
plotframe3.add(cl_cd_plot3, text='CL vs. CD')


##############################################################################

# DEFINITIONS

##############################################################################

def info():
    info_window = Toplevel()
    info_window.title('Info about program usage')
    titleinfo = Label(info_window, text='INFO ABOUT THE CORRECT USE OF THE PROGRAM', font='default 20 bold').pack()

def on_entry_click(event, variable, value):
    if variable.get() == value:
        variable.delete(0, END)
        variable.insert(0, '')
        variable.config(fg='black')

def on_focusout(event, variable, value):
    if variable.get() == '':
        variable.insert(0, value)
        variable.config(fg = 'grey')


################################
#  UPPER FRAME - DRONE SETTINGS
################################

def submit_drone():
    # Asegurar que lo introducido es un valor numérico correcto, habrá que
    # establecer límites de valores que se puedan introducir
    # VER CÓMO SE HACE
    global weight
    global radio
    global prop_num
    global blade_num
    global rpm
    global powerLabel
    global power_reqLabel

    if len(weight_entry.get()) == 0:
        messagebox.showwarning("Some values are missing", "The weight entry is empty")

    elif len(radio_entry.get()) == 0:
        messagebox.showwarning("Some values are missing", "The porpeller radio entry is empty")

    elif len(prop_num_entry.get()) == 0:
        messagebox.showwarning("Some values are missing", "The number of propellers entry is empty")

    elif len(blade_num_entry.get()) == 0:
        messagebox.showwarning("Some values are missing", "The number of blades entry is empty")

    elif len(rpm_entry.get()) == 0:
        messagebox.showwarning("Some values are missing", "The rpm entry is empty")

    else:
        weight = float(weight_entry.get())
        radio = float(radio_entry.get())
        prop_num = int(prop_num_entry.get())
        blade_num = int(blade_num_entry.get())
        rpm = float(rpm_entry.get())

        preview_img = config_list[(prop_num - 1) * 3 + (blade_num -2)]
        preview = Label(upframe, image=preview_img, bd=1, relief=SUNKEN)
        preview.place(relx=0.7, rely=0.04, anchor='n')
        previewLabel = Label(upframe, text="Drone configuration")
        previewLabel.place(relx=0.7, rely=1, anchor='s')

        # POWER REQUIREMENTS & SOME CALCULATIONS
        prop_omega = rpm * float(math.pi) / float(30)  #[rad/s]
        prop_area = prop_num * math.pi * radio ** 2  #[m^2]
        v_1 = math.sqrt((2 * weight *g_mars) / (rho_mars * prop_area))  #[m/s]
        power_req = 0.5 * rho_mars * prop_area * v_1 ** 3  #[W]

        powerLabel = Label(upframe, text="Power required [W]")
        powerLabel.place(relx=0.22, rely=0.9, anchor='w')
        power_reqLabel = Label(upframe, text=round(power_req, 3), width=9)
        power_reqLabel.place(relx=0.34, rely=0.9, anchor='w')

        clearButton_drone = Button(upframe, text="Clear", command=clear_drone)
        clearButton_drone.place(relx=0.31, rely=0.76, anchor='e')

def clear_drone():
    global preview_img

    weight_entry.delete(0, END)
    radio_entry.delete(0, END)
    prop_num_entry.delete(0, END)
    blade_num_entry.delete(0, END)
    rpm_entry.delete(0, END)

    powerLabel.destroy()
    power_reqLabel.destroy()

    preview_img = ImageTk.PhotoImage(Image.open("pr.png"))
    preview = Label(upframe, image=preview_img, bd=1, relief=SUNKEN)
    preview.place(relx=0.7, rely=0.04, anchor='n')
    previewLabel = Label(upframe, text="Drone configuration")
    previewLabel.place(relx=0.7, rely=1, anchor='s')

    clearButton_drone = Button(upframe, text="Clear", command=clear_drone, state='disable')
    clearButton_drone.place(relx=0.31, rely=0.76, anchor='e')



#####################################
#  LOWER FRAME TAB 1 - XFOIL ANALYSIS
#####################################

def select_airfoil(frame_entry, frame_plot):
    # En un futuro estaría bien que el propio programa te mostrase una base de
    # dato con todos los perfiles NACA y Selig disponibles en la carpeta
    # airfoils-geom
    global plot_geom

    tab1.filename = filedialog.askopenfilename(initialdir="", title="Select an airfoil geometry", filetypes=((".dat files", "*.dat"),(".txt files", "*.txt")))
    airfoil_sel = Label(frame_entry, text=tab1.filename)
    airfoil_sel.place(relx=1, rely=0.5, anchor='e')

    coordinates = np.genfromtxt(tab1.filename, skip_header=1)
    x = coordinates[:,0]
    y = coordinates[:,1]

    plot_fig = plt.figure(figsize=(5.5,2.2), dpi=100)
    plot = plot_fig.add_subplot(111)
    plot.clear()
    plot.plot(x, y)
    plot.axis([0, 1, -0.2, 0.3])
    plot.tick_params(width=0, labelsize=0)
    plot.grid('True')
    for axis in ['top','bottom','left','right']:
        plot.spines[axis].set_linewidth(0.5)

    plot_geom = FigureCanvasTkAgg(plot_fig, master=frame_plot)
    plot_geom.get_tk_widget().pack_forget()
    plot_geom.get_tk_widget().pack() # side=TOP, fill=BOTH, expand=True

    #Printear el nombre del perfil sacado de tab1.filename
    geomLabel = Label(frame_plot, text="Airfoil geometry")
    geomLabel.place(relx=0.5, anchor='n')

    clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis)
    clearButton_analysis.place(relx=0.255, rely=0.43, anchor='e')

def submit_analysis():
    # Asegurar que lo introducido es un valor numérico correcto, habrá que
    # establecer límites de valores que se puedan introducir
    # VER CÓMO SE HACE
    global plot_cl_a
    global plot_cd_a
    global plot_cl_cd

    if len(re_entry.get()) == 0:
        messagebox.showwarning("Some values are missing", "The Reynolds number entry is empty")

    else:
        re = float(re_entry.get())
        mach = float(mach_entry.get())
        alpha_from = float(a_fromEntry.get())
        alpha_to = float(a_toEntry.get())
        a_step = float(a_stepEntry.get())

        clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis)
        clearButton_analysis.place(relx=0.255, rely=0.43, anchor='e')


        # XFOIL #######
        xf = XFoil ()

        #from xfoil.test import naca0012
        #xf.airfoil = naca0012

        xf.Re = re
        xf.M = mach
        xf.max_iter = 200
        coordinates = np.genfromtxt(tab1.filename, skip_header=1)
        xf.airfoil = Airfoil(x = np.array(coordinates[:,0]), y = np.array(coordinates[:,1]))
        xf.repanel(200)

        a, cl, cd, cm, cp = xf.aseq(alpha_from, alpha_to, a_step)

        title = 'naca0012' + ' ' + 'Re=' + str(round(re)) + '' + ' M' + str(mach)

        # PLOT CL VS. ALPHA
        cl_a_figure = plt.figure(figsize=(5,5), dpi=100)
        cl_a = cl_a_figure.add_subplot(111)
        cl_a.plot(a, cl)
        cl_a.set_xlim(alpha_from - 2, alpha_to + 2)
        cl_a.tick_params(width=0.5, labelsize=6)
        cl_a.set_title(title, fontsize=14)
        cl_a.set_xlabel('alpha')
        cl_a.set_ylabel('Cl')

        for axis in ['top','bottom','left','right']:
            cl_a.spines[axis].set_linewidth(0.5)

        plot_cl_a = FigureCanvasTkAgg(cl_a_figure, master=cl_plot)
        plot_cl_a.draw()
        plot_cl_a.get_tk_widget().pack()

        # PLOT CD VS. ALPHA
        cd_a_figure = plt.figure(figsize=(5,5), dpi=100)
        cd_a = cd_a_figure.add_subplot(111)
        cd_a.plot(a, cd)
        cd_a.set_xlim(alpha_from - 2, alpha_to + 2)
        cd_a.tick_params(width=0.5, labelsize=6)
        cd_a.set_title(title, fontsize=14)
        cd_a.set_xlabel('alpha')
        cd_a.set_ylabel('Cd')

        for axis in ['top','bottom','left','right']:
            cd_a.spines[axis].set_linewidth(0.5)

        plot_cd_a = FigureCanvasTkAgg(cd_a_figure, master=cd_plot)
        plot_cd_a.draw()
        plot_cd_a.get_tk_widget().pack()

        # PLOT CL VS. CD
        cl_cd_figure = plt.figure(figsize=(5,5), dpi=100)
        cl_cd = cl_cd_figure.add_subplot(111)
        cl_cd.plot(cd, cl)
        cl_cd.tick_params(width=0.5, labelsize=6)
        cl_cd.set_title(title, fontsize=14)
        cl_cd.set_xlabel('Cd')
        cl_cd.set_ylabel('Cl')

        for axis in ['top','bottom','left','right']:
            cl_cd.spines[axis].set_linewidth(0.5)

        plot_cl_cd = FigureCanvasTkAgg(cl_cd_figure, master=cl_cd_plot)
        plot_cl_cd.draw()
        plot_cl_cd.get_tk_widget().pack()

def clear_analysis():
    global plot_cl_a
    global plot_cd_a
    global plot_cl_cd
    global plot_geom

    re_entry.delete(0, END)
    re_entry.insert(END, '100000')
    re_entry.configure(fg='grey')
    mach_entry.delete(0, END)
    mach_entry.insert(END, '0')
    mach_entry.configure(fg='grey')
    a_fromEntry.delete(0, END)
    a_fromEntry.insert(END, '-20')
    a_fromEntry.configure(fg='grey')
    a_toEntry.delete(0, END)
    a_toEntry.insert(END, '20')
    a_toEntry.configure(fg='grey')

    airfoil_frame = LabelFrame(tab1, bd=1)
    airfoil_frame.configure(height=25, width=172)
    airfoil_frame.grid_propagate(0)
    airfoil_frame.place(relx=0.25, rely=0.36, anchor='w')
    airfoil_sel = Label(airfoil_frame, text="No airfoil selected", fg='grey', font='default 12')
    airfoil_sel.place(relx=0.5, anchor='n')

    plot_geom.get_tk_widget().pack_forget()
    plot_cl_a.get_tk_widget().pack_forget()
    plot_cd_a.get_tk_widget().pack_forget()
    plot_cl_cd.get_tk_widget().pack_forget()

    # PLOTEAR ALGO ENCIMA DE LOS PLOTS PARA TAPARLOS

    clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis, state='disable')
    clearButton_analysis.place(relx=0.255, rely=0.43, anchor='e')



###########################################
#  LOWER FRAME TAB 2 - FIND OPTIMUM AIRFOIL
###########################################








#########################################
#  LOWER FRAME TAB 3 - AIRFOIL COMPARISON
#########################################

def select_airfoil_tab31(frame_entry, frame_plot):
    # En un futuro estaría bien que el propio programa te mostrase una base de
    # dato con todos los perfiles NACA y Selig disponibles en la carpeta
    # airfoils-geom
    global airfoil_1

    tab3.filename = filedialog.askopenfilename(initialdir="", title="Select an airfoil geometry", filetypes=((".dat files", "*.dat"),(".txt files", "*.txt")))
    airfoil_sel = Label(frame_entry, text=tab3.filename)
    airfoil_sel.place(relx=1, rely=0.5, anchor='e')

    coordinates = np.genfromtxt(tab3.filename, skip_header=1)
    x = coordinates[:,0]
    y = coordinates[:,1]

    plot_fig = plt.figure(figsize=(2.75,1.1), dpi=100)
    plot = plot_fig.add_subplot(111)
    plot.clear()
    plot.plot(x, y)
    plot.axis([0, 1, -0.2, 0.3])
    plot.tick_params(width=0, labelsize=0)
    plot.grid('True')
    for axis in ['top','bottom','left','right']:
        plot.spines[axis].set_linewidth(0.5)

    plot_geom = FigureCanvasTkAgg(plot_fig, master=frame_plot)
    plot_geom.draw()
    plot_geom.get_tk_widget().place(relx=0.5, rely=-0.02, anchor='n')

    #Printear el nombre del perfil sacado de tab3.filename
    geomLabel = Label(frame_plot, text="Airfoil geometry")
    geomLabel.place(relx=0.5, anchor='n')

    airfoil_1 = tab3.filename

def select_airfoil_tab32(frame_entry, frame_plot):
    # En un futuro estaría bien que el propio programa te mostrase una base de
    # dato con todos los perfiles NACA y Selig disponibles en la carpeta
    # airfoils-geom
    global airfoil_2

    tab3.filename = filedialog.askopenfilename(initialdir="", title="Select an airfoil geometry", filetypes=((".dat files", "*.dat"),(".txt files", "*.txt")))
    airfoil_sel = Label(frame_entry, text=tab3.filename)
    airfoil_sel.place(relx=1, rely=0.5, anchor='e')

    coordinates = np.genfromtxt(tab3.filename, skip_header=1)
    x = coordinates[:,0]
    y = coordinates[:,1]

    plot_fig = plt.figure(figsize=(2.75,1.1), dpi=100)
    plot = plot_fig.add_subplot(111)
    plot.clear()
    plot.plot(x, y)
    plot.axis([0, 1, -0.2, 0.3])
    plot.tick_params(width=0, labelsize=0)
    plot.grid('True')
    for axis in ['top','bottom','left','right']:
        plot.spines[axis].set_linewidth(0.5)

    plot_geom = FigureCanvasTkAgg(plot_fig, master=frame_plot)
    plot_geom.draw()
    plot_geom.get_tk_widget().place(relx=0.5, rely=-0.02, anchor='n')

    #Printear el nombre del perfil sacado de tab3.filename
    geomLabel = Label(frame_plot, text="Airfoil geometry")
    geomLabel.place(relx=0.5, anchor='n')

    airfoil_2 = tab3.filename

def submit_comparison(re, mach, alpha_from, alpha_to, a_step):
    # Asegurar que lo introducido es un valor numérico correcto, habrá que
    # establecer límites de valores que se puedan introducir
    # VER CÓMO SE HACE
    global plot_cl_a1
    global plot_cd_a1
    global plot_cl_cd1

    re = float(re_entry.get())
    mach = float(mach_entry.get())
    alpha_from = float(a_fromEntry.get())
    alpha_to = float(a_toEntry.get())
    a_step = float(a_stepEntry.get())

    clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis)
    clearButton_analysis.place(relx=0.255, rely=0.43, anchor='e')


    # XFOIL #######
    xf = XFoil ()

    #from xfoil.test import naca0012
    #xf.airfoil = naca0012

    xf.Re = re
    xf.M = mach
    xf.max_iter = 200

    coordinates_1 = np.genfromtxt(airfoil_1, skip_header=1)
    coordinates_2 = np.genfromtxt(airfoil_2, skip_header=1)

    xf.airfoil = Airfoil(x = np.array(coordinates_1[:,0]), y = np.array(coordinates_1[:,1]))
    xf.repanel(200)

    a_1, cl_1, cd_1, cm_1, cp_1 = xf.aseq(alpha_from, alpha_to, a_step)

    xf.airfoil = Airfoil(x = np.array(coordinates_2[:,0]), y = np.array(coordinates_2[:,1]))
    xf.repanel(200)

    a_2, cl_2, cd_2, cm_2, cp_2 = xf.aseq(alpha_from, alpha_to, a_step)

    title = 'Airfoil 1 vs. Airfoil 2' + ' ' + 'Re=' + str(round(re)) + '' + ' M' + str(mach)

    # PLOT CL VS. ALPHA
    cl_a1_figure = plt.figure(figsize=(5,5), dpi=100)
    cl_a1 = cl_a1_figure.add_subplot(111)
    cl_a1.cla()
    cl_a1.plot(a_1, cl_1)
    cl_a1.plot(a_2, cl_2)
    cl_a1.set_xlim(alpha_from - 2, alpha_to + 2)
    cl_a1.tick_params(width=0.5, labelsize=6)
    cl_a1.set_title(title, fontsize=14)
    cl_a1.set_xlabel('alpha')
    cl_a1.set_ylabel('Cl')

    for axis in ['top','bottom','left','right']:
        cl_a1.spines[axis].set_linewidth(0.5)

    plot_cl_a1 = FigureCanvasTkAgg(cl_a1_figure, master=cl_plot3)
    plot_cl_a1.draw()
    plot_cl_a1.get_tk_widget().pack()

    # PLOT CD VS. ALPHA
    cd_a1_figure = plt.figure(figsize=(5,5), dpi=100)
    cd_a1 = cd_a1_figure.add_subplot(111)
    cd_a1.cla()
    cd_a1.plot(a_1, cd_1)
    cd_a1.plot(a_2, cd_2)
    cd_a1.set_xlim(alpha_from - 2, alpha_to + 2)
    cd_a1.tick_params(width=0.5, labelsize=6)
    cd_a1.set_title(title, fontsize=14)
    cd_a1.set_xlabel('alpha')
    cd_a1.set_ylabel('Cd')

    for axis in ['top','bottom','left','right']:
        cd_a1.spines[axis].set_linewidth(0.5)

    plot_cd_a1 = FigureCanvasTkAgg(cd_a1_figure, master=cd_plot3)
    plot_cd_a1.draw()
    plot_cd_a1.get_tk_widget().pack()

    # PLOT CL VS. CD
    cl_cd1_figure = plt.figure(figsize=(5,5), dpi=100)
    cl_cd1 = cl_cd1_figure.add_subplot(111)
    cl_cd1.cla()
    cl_cd1.plot(cd_1, cl_1)
    cl_cd1.plot(cd_2, cl_2)
    cl_cd1.tick_params(width=0.5, labelsize=6)
    cl_cd1.set_title(title, fontsize=14)
    cl_cd1.set_xlabel('Cd')
    cl_cd1.set_ylabel('Cl')

    for axis in ['top','bottom','left','right']:
        cl_cd1.spines[axis].set_linewidth(0.5)

    plot_cl_cd1 = FigureCanvasTkAgg(cl_cd1_figure, master=cl_cd_plot3)
    plot_cl_cd1.draw()
    plot_cl_cd1.get_tk_widget().pack()

def clear_comparison():
    global airfoil_sel31
    global airfoil_sel32
    global plot_cl_a1
    global plot_cd_a1
    global plot_cl_cd1

    re3Entry.delete(0, END)
    mach3Entry.delete(0, END)
    mach3Entry.insert(END, '0.7')
    mach3Entry.configure(fg='grey')
    a_from3Entry.delete(0, END)
    a_from3Entry.insert(END, '-20')
    a_from3Entry.configure(fg='grey')
    a_to3Entry.delete(0, END)
    a_to3Entry.insert(END, '20')
    a_to3Entry.configure(fg='grey')

    airfoil_frame31 = LabelFrame(tab3, bd=1)
    airfoil_frame31.configure(height=25, width=172)
    airfoil_frame31.grid_propagate(0)
    airfoil_frame31.place(relx=0.25, rely=0.36, anchor='w')
    airfoil_sel31 = Label(airfoil_frame31, text="No airfoil selected")
    airfoil_sel31.place(relx=0.5, anchor='n')

    airfoil_frame32 = LabelFrame(tab3, bd=1)
    airfoil_frame32.configure(height=25, width=172)
    airfoil_frame32.grid_propagate(0)
    airfoil_frame32.place(relx=0.25, rely=0.36, anchor='w')
    airfoil_sel32 = Label(airfoil_frame32, text="No airfoil selected")
    airfoil_sel32.place(relx=0.5, anchor='n')

    plot_cl_a1.get_tk_widget().pack_forget()
    plot_cd_a1.get_tk_widget().pack_forget()
    plot_cl_cd1.get_tk_widget().pack_forget()

    # PLOTEAR ALGO ENCIMA DE LOS PLOTS PARA TAPARLOS

    clearButton_comparison = Button(tab3, text="Clear", command=clear_comparison, state='disable')
    clearButton_comparison.place(relx=0.225, rely=0.41, anchor='n')

##############################################################################

# UPPER FRAME ###########

##############################################################################

# DRONE SETTINGS
titleDroneLabel = Label(upframe, text="Drone characteristics", font='default 16 bold')
titleDroneLabel.place(relx=0.31, rely=0.1, anchor='s')

weightLabel = Label(upframe, text="Drone weight [kg]")
weightLabel.place(relx=0.15, rely=0.2, anchor='w')
weight_entry = Entry(upframe, width=18)
weight_entry.place(relx=0.3, rely=0.2, anchor='w')

radioLabel = Label(upframe, text="Propeller radio [m]")
radioLabel.place(relx=0.15, rely=0.3, anchor='w')
radio_entry = Entry(upframe, width=18)
radio_entry.place(relx=0.3, rely=0.3, anchor='w')

prop_numLabel = Label(upframe, text="Number of propellers")
prop_numLabel.place(relx=0.15, rely=0.4, anchor='w')
prop_num_entry = Spinbox(upframe, from_=1, to=6, state = 'readonly', width=18)
prop_num_entry.place(relx=0.3, rely=0.4, anchor='w')

blade_numLabel = Label(upframe, text="Number of blades")
blade_numLabel.place(relx=0.15, rely=0.5, anchor='w')
blade_num_entry = Spinbox(upframe, from_=2, to=4, state = 'readonly', width=18)
blade_num_entry.place(relx=0.3, rely=0.5, anchor='w')

rpmLabel = Label(upframe, text="RPM [rpm]")
rpmLabel.place(relx=0.15, rely=0.6, anchor='w')
rpm_entry = Entry(upframe, width=18)
rpm_entry.place(relx=0.3, rely=0.6, anchor='w')

# DRONE CONFIGURATIONS IMAGES
config_12 = ImageTk.PhotoImage(Image.open("drone_config/config-1.2.png"))
config_13 = ImageTk.PhotoImage(Image.open("drone_config/config-1.3.png"))
config_14 = ImageTk.PhotoImage(Image.open("drone_config/config-1.4.png"))
config_22 = ImageTk.PhotoImage(Image.open("drone_config/config-2.2.png"))
config_23 = ImageTk.PhotoImage(Image.open("drone_config/config-2.3.png"))
config_24 = ImageTk.PhotoImage(Image.open("drone_config/config-2.4.png"))
config_32 = ImageTk.PhotoImage(Image.open("drone_config/config-3.2.png"))
config_33 = ImageTk.PhotoImage(Image.open("drone_config/config-3.3.png"))
config_34 = ImageTk.PhotoImage(Image.open("drone_config/config-3.4.png"))
config_42 = ImageTk.PhotoImage(Image.open("drone_config/config-4.2.png"))
config_43 = ImageTk.PhotoImage(Image.open("drone_config/config-4.3.png"))
config_44 = ImageTk.PhotoImage(Image.open("drone_config/config-4.4.png"))
config_52 = ImageTk.PhotoImage(Image.open("drone_config/config-5.2.png"))
config_53 = ImageTk.PhotoImage(Image.open("drone_config/config-5.3.png"))
config_54 = ImageTk.PhotoImage(Image.open("drone_config/config-5.4.png"))
config_62 = ImageTk.PhotoImage(Image.open("drone_config/config-6.2.png"))
config_63 = ImageTk.PhotoImage(Image.open("drone_config/config-6.3.png"))
config_64 = ImageTk.PhotoImage(Image.open("drone_config/config-6.4.png"))

config_list = [config_12, config_13, config_14,
    config_22, config_23, config_24,
    config_32, config_33, config_34,
    config_42, config_43, config_44,
    config_52, config_53, config_54,
    config_62, config_63, config_64]

# INITIAL IMAGE
preview_img = ImageTk.PhotoImage(Image.open("pr.png"))
preview = Label(upframe, image=preview_img, bd=1, relief=SUNKEN)
preview.place(relx=0.7, rely=0.04, anchor='n')

previewLabel = Label(upframe, text="Drone configuration")
previewLabel.place(relx=0.7, rely=1, anchor='s')


submitButton_drone = Button(upframe, text="Submit", command=submit_drone)
submitButton_drone.place(relx=0.31, rely=0.76, anchor='w')

clearButton_drone = Button(upframe, text="Clear", command=clear_drone, state='disable')
clearButton_drone.place(relx=0.31, rely=0.76, anchor='e')



##############################################################################

# LOWER FRAME ###########

##############################################################################

#########################################
# TAB 1 CONTENT - XFOIL ANALYSIS SETTINGS
#########################################
title1Label = Label(tab1, text="Analysis parameters", font='default 16 bold')
title1Label.place(relx=0.26, rely=0.07, anchor='s')

re_default = '100000'
reLabel = Label(tab1, text="Reynolds number")
reLabel.place(relx=0.1, rely=0.12, anchor='w')
re_entry = Entry(tab1, width=18)
re_entry.place(relx=0.25, rely=0.12, anchor='w')
re_entry.insert(END, re_default)
re_entry.bind('<FocusIn>', lambda event: on_entry_click(event, re_entry, re_default))
re_entry.bind('<FocusOut>', lambda event: on_focusout(event, re_entry, re_default))
re_entry.configure(fg='grey')

mach_default = '0'
machLabel = Label(tab1, text="Mach number")
machLabel.place(relx=0.1, rely=0.18, anchor='w')
mach_entry = Entry(tab1, width=18)
mach_entry.place(relx=0.25, rely=0.18, anchor='w')
mach_entry.insert(END, '0')
mach_entry.bind('<FocusIn>', lambda event: on_entry_click(event, mach_entry, mach_default))
mach_entry.bind('<FocusOut>', lambda event: on_focusout(event, mach_entry, mach_default))
mach_entry.configure(fg='grey')

alphaLabel = Label(tab1, text="Angle of attack α")
alphaLabel.place(relx=0.1, rely=0.24, anchor='w')

a_from_default = '-20'
a_fromLabel = Label(tab1, text="from")
a_fromLabel.place(relx=0.25, rely=0.24, anchor='w')
a_fromEntry = Entry(tab1, width=5)
a_fromEntry.place(relx=0.285, rely=0.24, anchor='w')
a_fromEntry.insert(END, a_from_default)
a_fromEntry.bind('<FocusIn>', lambda event: on_entry_click(event, a_fromEntry, a_from_default))
a_fromEntry.bind('<FocusOut>', lambda event: on_focusout(event, a_fromEntry, a_from_default))
a_fromEntry.configure(fg='grey')

a_to_default = '20'
a_toLabel = Label(tab1, text="to")
a_toLabel.place(relx=0.342, rely=0.24, anchor='w')
a_toEntry = Entry(tab1, width=5)
a_toEntry.place(relx=0.362, rely=0.24, anchor='w')
a_toEntry.insert(END, a_to_default)
a_toEntry.bind('<FocusIn>', lambda event: on_entry_click(event, a_toEntry, a_to_default))
a_toEntry.bind('<FocusOut>', lambda event: on_focusout(event, a_toEntry, a_to_default))
a_toEntry.configure(fg='grey')

a_step_default = '0.5'
a_stepLabel = Label(tab1, text="α increment")
a_stepLabel.place(relx=0.1, rely=0.3, anchor='w')
a_stepEntry = Entry(tab1, width=18)
a_stepEntry.place(relx=0.25, rely=0.3, anchor='w')
a_stepEntry.insert(END, a_step_default)
a_stepEntry.bind('<FocusIn>', lambda event: on_entry_click(event, a_stepEntry, a_step_default))
a_stepEntry.bind('<FocusOut>', lambda event: on_focusout(event, a_stepEntry, a_step_default))
a_stepEntry.configure(fg='grey')

airfoil_frame = LabelFrame(tab1, bd=1)
airfoil_frame.configure(height=25, width=172)
airfoil_frame.grid_propagate(0)
airfoil_frame.place(relx=0.25, rely=0.36, anchor='w')
airfoil_sel = Label(airfoil_frame, text="No airfoil selected", fg='grey', font='default 12')
airfoil_sel.place(relx=0.5, anchor='n')

airfoilButton = Button(tab1, text="Select an airfoil", command=lambda: select_airfoil(airfoil_frame, geometryframe))
airfoilButton.place(relx=0.1, rely=0.36, anchor='w')

geomLabel = Label(geometryframe, text="Airfoil geometry")
geomLabel.place(relx=0.5, anchor='n')


submitButton_analysis = Button(tab1, text="Submit", command=submit_analysis)
submitButton_analysis.place(relx=0.255, rely=0.43, anchor='w')

clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis, state='disable')
clearButton_analysis.place(relx=0.255, rely=0.43, anchor='e')





######################################
# TAB 2 CONTENT - FIND OPTIMUM AIRFOIL
######################################

# CALCULATIONS
# REFERENCE VALUES
# The mars atmosphere values has been approximated to the values of the carbon dioxide (95%)

g_mars = 3.711  #[m/s^2]
mu_mars = 13.695  #[microPa*s]
rho_mars = 0.0198  #[kg/m^3]
nu_mars = mu_mars * (10 ** (- 6)) / rho_mars  #[m^2/s]

# ANALYSIS PARAMETERS
a_i = 0.01  # By default
a_step = 0.01  # By default
cl_i = 1   # By default
#diff_r = radio / 10  # By default


# PROPELLER AIRFOIL CHARACTERIZATION #######
#for diff_r <= radio:
#    r = diff_r
#    a = a_i
#    a_a = 0
#    a_max = 0
#    a_p_a = 0
#    a_p_max =
#    G = 0
#    G_a = 0
#    G_max = 0
#
#    while G = G_a:
#      tan_phi = (1 - math.sqrt(1 + 4 * (v_1 / prop_omega * r) ** 2 * a * (a - a))) / (2 * a * v_1 / (prop_omega * r))
#      phi = math.atan(tan_phi)
#      a_p = (v_1 * (1 - a)) / (prop_omega * r * tan_phi) + 1
#      f = (blades_num * (radio - r)) / (2 * radio * math.sin(phi))
#      F = 2 / math.pi * math.acos( exp( - f ))
#      G = F * (1 - a) * a_p
#      if G < G_a:
#        G_max = G_a
#        a_max = a_a
#        a_p_max = a_p_a
#        break
#      else:
#        a = a + a_step
#        G_a = G
#        a_a = a
#        a_p_a = a_p

#v_r = math.sqrt(v_1 ** 2 * (1 - a_max) ** 2 + prop_omega ** 2 * r ** 2 * (a_p_max - 1) ** 2)

# ITERATION & CALL TO XFOIL
#c_l = cl_i
#if
#    c = (a_max * 8 * math.pi * r * math.sin(phi) ** 2) / ((1 - a_max) * blades_num * c_l * math.cos(phi))
#    re = (v_r * c) / (nu_mars)
#

#########################################
# TAB 3 CONTENT - AIRFOIL COMPARISON
#########################################
title3Label = Label(tab3, text="Airfoil comparison", font='default 16 bold')
title3Label.place(relx=0.26, rely=0.07, anchor='s')

re3_default = '100000'
re3Label = Label(tab3, text="Reynolds number")
re3Label.place(relx=0.1, rely=0.12, anchor='w')
re3Entry = Entry(tab3, width=18)
re3Entry.place(relx=0.25, rely=0.12, anchor='w')
re3Entry.insert(END, re3_default)
re3Entry.bind('<FocusIn>', lambda event: on_entry_click(event, re3Entry, re3_default))
re3Entry.bind('<FocusOut>', lambda event: on_focusout(event, re3Entry, re3_default))
re3Entry.configure(fg='grey')

mach3_default = '0'
mach3Label = Label(tab3, text="Mach number")
mach3Label.place(relx=0.1, rely=0.18, anchor='w')
mach3Entry = Entry(tab3, width=18)
mach3Entry.place(relx=0.25, rely=0.18, anchor='w')
mach3Entry.insert(END, mach3_default)
mach3Entry.bind('<FocusIn>', lambda event: on_entry_click(event, mach3Entry, mach3_default))
mach3Entry.bind('<FocusOut>', lambda event: on_focusout(event, mach3Entry, mach3_default))
mach3Entry.configure(fg='grey')

alpha3Label = Label(tab3, text="Angle of attack α")
alpha3Label.place(relx=0.1, rely=0.24, anchor='w')

a_from3_default = '-20'
a_from3Label = Label(tab3, text="from")
a_from3Label.place(relx=0.25, rely=0.24, anchor='w')
a_from3Entry = Entry(tab3, width=5)
a_from3Entry.place(relx=0.285, rely=0.24, anchor='w')
a_from3Entry.insert(END, a_from3_default)
a_from3Entry.bind('<FocusIn>', lambda event: on_entry_click(event, a_from3Entry, a_from3_default))
a_from3Entry.bind('<FocusOut>', lambda event: on_focusout(event, a_from3Entry, a_from3_default))
a_from3Entry.configure(fg='grey')

a_to3_default = '20'
a_to3Label = Label(tab3, text="to")
a_to3Label.place(relx=0.342, rely=0.24, anchor='w')
a_to3Entry = Entry(tab3, width=5)
a_to3Entry.place(relx=0.362, rely=0.24, anchor='w')
a_to3Entry.insert(END, a_to3_default)
a_to3Entry.bind('<FocusIn>', lambda event: on_entry_click(event, a_to3Entry, a_to3_default))
a_to3Entry.bind('<FocusOut>', lambda event: on_focusout(event, a_to3Entry, a_to3_default))
a_to3Entry.configure(fg='grey')

a_step3_default = '0.5'
a_step3Label = Label(tab3, text="α increment")
a_step3Label.place(relx=0.1, rely=0.3, anchor='w')
a_step3Entry = Entry(tab3, width=18)
a_step3Entry.place(relx=0.25, rely=0.3, anchor='w')
a_step3Entry.insert(END, a_step3_default)
a_step3Entry.bind('<FocusIn>', lambda event: on_entry_click(event, a_step3Entry, a_step3_default))
a_step3Entry.bind('<FocusOut>', lambda event: on_focusout(event, a_step3Entry, a_step3_default))
a_step3Entry.configure(fg='grey')

airfoil_frame31 = LabelFrame(tab3, bd=1)
airfoil_frame31.configure(height=25, width=172)
airfoil_frame31.grid_propagate(0)
airfoil_frame31.place(relx=0.04, rely=0.635, anchor='w')
airfoil_sel31 = Label(airfoil_frame31, text="No airfoil selected", fg='grey', font='default 12')
airfoil_sel31.place(relx=0.5, anchor='n')

airfoil_frame32 = LabelFrame(tab3, bd=1)
airfoil_frame32.configure(height=25, width=172)
airfoil_frame32.grid_propagate(0)
airfoil_frame32.place(relx=0.04, rely=0.86, anchor='w')
airfoil_sel32 = Label(airfoil_frame32, text="No airfoil selected", fg='grey', font='default 12')
airfoil_sel32.place(relx=0.5, anchor='n')

airfoilButton31 = Button(tab3, text="Select an airfoil", command=lambda: select_airfoil_tab31(airfoil_frame31, geometryframe31))
airfoilButton31.place(relx=0.075, rely=0.57, anchor='w')

airfoilButton32 = Button(tab3, text="Select an airfoil", command=lambda: select_airfoil_tab32(airfoil_frame32, geometryframe32))
airfoilButton32.place(relx=0.075, rely=0.8, anchor='w')

submitButton_comparison = Button(tab3, text="Submit", command=lambda: submit_comparison(re3Entry.get(), mach3Entry.get(), a_from3Entry.get(), a_to3Entry.get(), a_step3Entry.get()))
submitButton_comparison.place(relx=0.255, rely=0.38, anchor='w')

clearButton_comparison = Button(tab3, text="Clear", command=clear_comparison, state='disable')
clearButton_comparison.place(relx=0.255, rely=0.38, anchor='e')





# PROGRAM INFO
button_info = Button (canvas, text="Info about", command=info)
button_info.place(relx=0.025, rely=0.035, anchor='w')


# QUIT PROGRAM
button_quit = Button (canvas, text="Close", command=root.quit)
button_quit.place(relx=0.975, rely=0.035, anchor='e')

root.mainloop()
