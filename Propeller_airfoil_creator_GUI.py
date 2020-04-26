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
from matplotlib.figure import Figure
import xfoil as xf
from xfoil import XFoil
from xfoil.model import Airfoil


##############################################################################

# WINDOW CONFIGURATION

##############################################################################

HEIGHT = 900
WIDTH = 1100

root = Tk()
root.title("Redtek propeller creator")
#root.resizable(width=False, height=False)

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
geometryframe.place(relx=0.257, rely=0.5, relwidth=0.45, relheight=0.46, anchor='n')

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


##############################################################################

# DEFINITIONS

##############################################################################

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
        clearButton_drone.place(relx=0.278, rely=0.7, anchor='n')

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
    clearButton_drone.place(relx=0.278, rely=0.7, anchor='n')


def select_airfoil():

    # En un futuro estaría bien que el propio programa te mostrase una base de
    # dato con todos los perfiles NACA y Selig disponibles en la carpeta
    # airfoils-geom

    root.filename = filedialog.askopenfilename(initialdir="", title="Select an airfoil geometry", filetypes=((".dat files", "*.dat"),(".txt files", "*.txt")))
    airfoil_sel = Label(airfoil_frame, text=root.filename)
    airfoil_sel.place(relx=1, rely=0.5, anchor='e')

    coordinates = np.genfromtxt(root.filename, skip_header=2)
    x1 = coordinates[:,0]
    y1 = coordinates[:,1]
    plot_figure = Figure(figsize=(5.5,2.2), dpi=100)
    plot = plot_figure.add_subplot(111)
    plot.cla()
    plot.plot(x1, y1)
    plot.axis([0, 1, -0.2, 0.3])
    plot.tick_params(width=0.5, labelsize=7)

    for axis in ['top','bottom','left','right']:
        plot.spines[axis].set_linewidth(0.5)

    plot_geom = FigureCanvasTkAgg(plot_figure, master=geometryframe)
    plot_geom.draw()
    plot_geom.get_tk_widget().pack()

    #Printear el nombre del perfil sacado de root.filename
    geomLabel = Label(geometryframe, text="Airfoil geometry")
    geomLabel.place(relx=0.5, anchor='n')

#def findMiddle(input_list):
#    middle = float(len(input_list))/2
#    if middle % 2 != 0:
#        return input_list[int(middle - .5)]
#    else:
#        return (input_list[int(middle)], input_list[int(middle-1)])

def submit_analysis():
    # Asegurar que lo introducido es un valor numérico correcto, habrá que
    # establecer límites de valores que se puedan introducir
    # VER CÓMO SE HACE

    global re
    global mach
    global alpha_from
    global alpha_to
    global alpha_steps

    if len(re_entry.get()) == 0:
        messagebox.showwarning("Some values are missing", "The Reynolds number entry is empty")

    else:
        re = float(re_entry.get())
        mach = float(mach_entry.get())
        alpha_from = float(alpha_from_entry.get())
        alpha_to = float(alpha_to_entry.get())
        alpha_steps = float(alpha_steps_entry.get())

        clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis)
        clearButton_analysis.place(relx=0.225, rely=0.41, anchor='n')


        # XFOIL #######
        xf = XFoil ()


        #from xfoil.test import naca0012
        #xf.airfoil = naca0012

        xf.Re = re
        xf.M = mach
        xf.max_iter = 200
        coordinates = np.genfromtxt(root.filename, skip_header=2) #, skip_header=2
        xf.airfoil = Airfoil(x = np.array(coordinates[:,0]), y = np.array(coordinates[:,1]))

        a, cl, cd, cm, cp = xf.aseq(alpha_from, alpha_to, alpha_steps)

        title = 'naca0012' + ' ' + 'Re=' + str(round(re)) + '' + ' M' + str(mach)

        # PLOT CL VS. ALPHA
        plot_figure = Figure(figsize=(5,5), dpi=100)
        plot = plot_figure.add_subplot(111)
        plot.cla()
        plot.plot(a, cl)
        plot.tick_params(width=0.5, labelsize=6)
        plot.set_title(title, fontsize=14)
        plot.set_xlabel('alpha')
        plot.set_ylabel('Cl')

        for axis in ['top','bottom','left','right']:
            plot.spines[axis].set_linewidth(0.5)

        plot_cl = FigureCanvasTkAgg(plot_figure, master=cl_plot)
        plot_cl.draw()
        plot_cl.get_tk_widget().pack()

        # PLOT CD VS. ALPHA
        plot_figure = Figure(figsize=(5,5), dpi=100)
        plot = plot_figure.add_subplot(111)
        plot.cla()
        plot.plot(a, cd)
        plot.tick_params(width=0.5, labelsize=6)
        plot.set_title(title, fontsize=14)
        plot.set_xlabel('alpha')
        plot.set_ylabel('Cd')

        for axis in ['top','bottom','left','right']:
            plot.spines[axis].set_linewidth(0.5)

        plot_cl = FigureCanvasTkAgg(plot_figure, master=cd_plot)
        plot_cl.draw()
        plot_cl.get_tk_widget().pack()

        # PLOT CL VS. CD
        plot_figure = Figure(figsize=(5,5), dpi=100)
        plot = plot_figure.add_subplot(111)
        plot.cla()
        plot.plot(cd, cl)
        plot.tick_params(width=0.5, labelsize=6)
        plot.set_title(title, fontsize=14)
        plot.set_xlabel('Cd')
        plot.set_ylabel('Cl')

        for axis in ['top','bottom','left','right']:
            plot.spines[axis].set_linewidth(0.5)

        plot_cl = FigureCanvasTkAgg(plot_figure, master=cl_cd_plot)
        plot_cl.draw()
        plot_cl.get_tk_widget().pack()

        #number = np.arange(0, 80, 1)
        #num = np.arange(0, 4, 1)

        #for i in number:
            #for n in num:
                #print('lista de a', a[n,i])
            #for n in num:
                #print('lista de cl', cl[n,i])


def clear_analysis():
    global airfoil_sel

    re_entry.delete(0, END)
    mach_entry.delete(0, END)
    mach_entry.insert(END, '0.7')
    mach_entry.configure(fg='grey')
    alpha_from_entry.delete(0, END)
    alpha_from_entry.insert(END, '-20')
    alpha_from_entry.configure(fg='grey')
    alpha_to_entry.delete(0, END)
    alpha_to_entry.insert(END, '20')
    alpha_to_entry.configure(fg='grey')

    airfoil_frame = LabelFrame(tab1, bd=1)
    airfoil_frame.configure(height=25, width=172)
    airfoil_frame.grid_propagate(0)
    airfoil_frame.place(relx=0.25, rely=0.36, anchor='w')
    airfoil_sel = Label(airfoil_frame, text="No airfoil selected")
    airfoil_sel.place(relx=0.5, anchor='n')

    clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis, state='disable')
    clearButton_analysis.place(relx=0.225, rely=0.41, anchor='n')

def on_entry_click_re(event):
    if re_entry.get() == '100000':
        re_entry.delete(0, END)
        re_entry.insert(0, '')
        re_entry.config(fg='black')

def on_focusout_re(event):
    if re_entry.get() == '':
        re_entry.insert(0, '100000')
        re_entry.config(fg = 'grey')

def on_entry_click_mach(event):
    if mach_entry.get() == '0.7':
        mach_entry.delete(0, END)
        mach_entry.insert(0, '')
        mach_entry.config(fg='black')

def on_focusout_mach(event):
    if mach_entry.get() == '':
        mach_entry.insert(0, '0')
        mach_entry.config(fg = 'grey')

def on_entry_click_afrom(event):
    if alpha_from_entry.get() == '-20':
        alpha_from_entry.delete(0, END)
        alpha_from_entry.insert(0, '')
        alpha_from_entry.config(fg='black')

def on_focusout_afrom(event):
    if alpha_from_entry.get() == '':
        alpha_from_entry.insert(0, '-20')
        alpha_from_entry.config(fg = 'grey')

def on_entry_click_ato(event):
    if alpha_to_entry.get() == '20':
        alpha_to_entry.delete(0, END)
        alpha_to_entry.insert(0, '')
        alpha_to_entry.config(fg='black')

def on_focusout_ato(event):
    if alpha_to_entry.get() == '':
        alpha_to_entry.insert(0, '20')
        alpha_to_entry.config(fg = 'grey')

def on_entry_click_astep(event):
    if alpha_steps_entry.get() == '0.5':
        alpha_steps_entry.delete(0, END)
        alpha_steps_entry.insert(0, '')
        alpha_steps_entry.config(fg='black')

def on_focusout_astep(event):
    if alpha_steps_entry.get() == '':
        alpha_steps_entry.insert(0, '0.5')
        alpha_steps_entry.config(fg = 'grey')

def info():
    info_window = Toplevel()
    info_window.title('Info about program usage')
    titleinfo = Label(info_window, text='INFO ABOUT THE CORRECT USE OF THE PROGRAM', font='default 20 bold').pack()




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
submitButton_drone.place(relx=0.342, rely=0.7, anchor='n')

clearButton_drone = Button(upframe, text="Clear", command=clear_drone, state='disable')
clearButton_drone.place(relx=0.278, rely=0.7, anchor='n')



##############################################################################

# LOWER FRAME ###########

##############################################################################

#########################################
# TAB 1 CONTENT - XFOIL ANALYSIS SETTINGS
#########################################
title1Label = Label(tab1, text="Analysis parameters", font='default 16 bold')
title1Label.place(relx=0.26, rely=0.07, anchor='s')

reLabel = Label(tab1, text="Reynolds number")
reLabel.place(relx=0.1, rely=0.12, anchor='w')
re_entry = Entry(tab1, width=18)
re_entry.place(relx=0.25, rely=0.12, anchor='w')
re_entry.insert(END, '100000')
re_entry.bind('<FocusIn>', on_entry_click_re)
re_entry.bind('<FocusOut>', on_focusout_re)
re_entry.configure(fg='grey')

machLabel = Label(tab1, text="Mach number")
machLabel.place(relx=0.1, rely=0.18, anchor='w')
mach_entry = Entry(tab1, width=18)
mach_entry.place(relx=0.25, rely=0.18, anchor='w')
mach_entry.insert(END, '0')
mach_entry.bind('<FocusIn>', on_entry_click_mach)
mach_entry.bind('<FocusOut>', on_focusout_mach)
mach_entry.configure(fg='grey')

alphaLabel = Label(tab1, text="Angle of attack α")
alphaLabel.place(relx=0.1, rely=0.24, anchor='w')
alphaFromLabel = Label(tab1, text="from")
alphaFromLabel.place(relx=0.25, rely=0.24, anchor='w')
alpha_from_entry = Entry(tab1, width=5)
alpha_from_entry.place(relx=0.285, rely=0.24, anchor='w')
alpha_from_entry.insert(END, '-20')
alpha_from_entry.bind('<FocusIn>', on_entry_click_afrom)
alpha_from_entry.bind('<FocusOut>', on_focusout_afrom)
alpha_from_entry.configure(fg='grey')
alphaToLabel = Label(tab1, text="to")
alphaToLabel.place(relx=0.342, rely=0.24, anchor='w')
alpha_to_entry = Entry(tab1, width=5)
alpha_to_entry.place(relx=0.362, rely=0.24, anchor='w')
alpha_to_entry.insert(END, '20')
alpha_to_entry.bind('<FocusIn>', on_entry_click_ato)
alpha_to_entry.bind('<FocusOut>', on_focusout_ato)
alpha_to_entry.configure(fg='grey')

alpha_stepsLabel = Label(tab1, text="α increment")
alpha_stepsLabel.place(relx=0.1, rely=0.3, anchor='w')
alpha_steps_entry = Entry(tab1, width=18)
alpha_steps_entry.place(relx=0.25, rely=0.3, anchor='w')
alpha_steps_entry.insert(END, '0.5')
alpha_steps_entry.bind('<FocusIn>', on_entry_click_astep)
alpha_steps_entry.bind('<FocusOut>', on_focusout_astep)
alpha_steps_entry.configure(fg='grey')


airfoilButton = Button(tab1, text="Select an airfoil", command=select_airfoil)
airfoilButton.place(relx=0.1, rely=0.36, anchor='w')

airfoil_frame = LabelFrame(tab1, bd=1)
airfoil_frame.configure(height=25, width=172)
airfoil_frame.grid_propagate(0)
airfoil_frame.place(relx=0.25, rely=0.36, anchor='w')
airfoil_sel = Label(airfoil_frame, text="No airfoil selected", fg='grey', font='default 12')
airfoil_sel.place(relx=0.5, anchor='n')

submitButton_analysis = Button(tab1, text="Submit", command=submit_analysis)
submitButton_analysis.place(relx=0.29, rely=0.41, anchor='n')

clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis, state='disable')
clearButton_analysis.place(relx=0.225, rely=0.41, anchor='n')

geomLabel = Label(geometryframe, text="Airfoil geometry")
geomLabel.place(relx=0.5, anchor='n')




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








# PROGRAM INFO
button_info = Button (canvas, text="Info about", command=info)
button_info.place(relx=0.025, rely=0.035, anchor='w')


# QUIT PROGRAM
button_quit = Button (canvas, text="Close", command=root.quit)
button_quit.place(relx=0.975, rely=0.035, anchor='e')

root.mainloop()
