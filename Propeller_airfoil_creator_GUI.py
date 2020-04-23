# -*- coding: utf-8 -*-

from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter import messagebox
import ttk
import math
from aeropy import *

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

logo_Redtek = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/logo.jpg"))
logo = Label(canvas, image=logo_Redtek)
logo.place(relx=0.5, anchor='n')

upframe = Frame(root)
upframe.place(relx=0.5, rely=0.07, relwidth=0.95, relheight=0.3, anchor='n')

lowframe = ttk.Notebook(root)
lowframe.place(relx=0.5, rely=0.4, relwidth=0.99, relheight=0.575, anchor='n')

# TAB 1 CONFIGURATION
tab1 = ttk.Frame(lowframe)
lowframe.add(tab1, text='Airfoil analysis')

geometryframe = Frame(tab1, bd=1, relief=SUNKEN)
geometryframe.place(relx=0.265, rely=0.5, relwidth=0.5, relheight=0.46, anchor='n')

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


##############################################################################

# DEFINITIONS

##############################################################################

def submit_drone():
    # Asegurar que lo introducido es un valor correcto
    # VER COMO SE HACE
    # Checkear que se han introducido todos los datos
    global weight
    global radio
    global prop_num
    global blade_num
    global rpm

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
        preview.place(relx=0.75, rely=0.04, anchor='n')
        previewLabel = Label(upframe, text="Drone configuration")
        previewLabel.place(relx=0.75, rely=1, anchor='s')

        # POWER REQUIREMENTS & SOME CALCULATIONS
        prop_omega = rpm * float(math.pi) / float(30)  #[rad/s]
        prop_area = prop_num * math.pi * radio ** 2  #[m^2]
        v_1 = math.sqrt((2 * weight *g_mars) / (rho_mars * prop_area))  #[m/s]
        power_req = 0.5 * rho_mars * prop_area * v_1 ** 3  #[W]

        powerLabel = Label(upframe, text="Power required [W]")
        powerLabel.place(relx=0.28, rely=0.9, anchor='w')
        power_reqLabel = Label(upframe, text=round(power_req, 3), width=9)
        power_reqLabel.place(relx=0.4, rely=0.9, anchor='w')

        clearButton_drone = Button(upframe, text="Clear", command=clear_drone)
        clearButton_drone.place(relx=0.338, rely=0.7, anchor='n')

def clear_drone():

    weight_entry.delete(0, END)
    radio_entry.delete(0, END)
    prop_num_entry.delete(0, END)
    blade_num_entry.delete(0, END)
    rpm_entry.delete(0, END)

    powerLabel = Label(upframe, text="                                       ")
    powerLabel.place(relx=0.08, rely=0.9, anchor='w')
    power_reqLabel = Label(upframe, text='', width=9)
    power_reqLabel.place(relx=0.2, rely=0.9, anchor='w')

    preview_img = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/pr.png"))
    preview = Label(upframe, image=preview_img, bd=1, relief=SUNKEN)
    preview.place(relx=0.75, rely=0.04, anchor='n')
    previewLabel = Label(upframe, text="Drone configuration")
    previewLabel.place(relx=0.75, rely=1, anchor='s')

    clearButton_drone = Button(upframe, text="Clear", command=clear_drone, state='disable')
    clearButton_drone.place(relx=0.338, rely=0.7, anchor='n')

def select_airfoil():
    root.filename = filedialog.askopenfilename(initialdir="/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/", title="Select an airfoil geometry", filetypes=((".dat files", "*.dat"),(".txt files", "*.txt")))
    airfoil_sel = Label(airfoil_frame, text=root.filename)
    airfoil_sel.place(relx=1, rely=0.5, anchor='e')

def submit_analysis():
    # Asegurar que lo introducido es un valor correcto
    # VER COMO SE HACE
    # Checkear que se han introducido todos los datos
    global re
    global mach
    global alpha_from
    global alpha_to

    if len(re_entry.get()) == 0:
        messagebox.showwarning("Some values are missing", "The Reynolds number entry is empty")

    else:
        re = float(re_entry.get())
        mach = float(mach_entry.get())
        alpha_from = float(alpha_from_entry.get())
        alpha_to = float(alpha_to_entry.get())

        clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis)
        clearButton_analysis.place(relx=0.235, rely=0.4, anchor='n')

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
    airfoil_frame.place(relx=0.25, rely=0.34, anchor='w')
    airfoil_sel = Label(airfoil_frame, text="No airfoil selected")
    airfoil_sel.place(relx=0.5, anchor='n')

    clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis, state='disable')
    clearButton_analysis.place(relx=0.235, rely=0.4, anchor='n')

def on_entry_click_mach(event):
    if mach_entry.get() == '0.7':
        mach_entry.delete(0, END)
        mach_entry.insert(0, '')
        mach_entry.config(fg='black')

def on_focusout_mach(event):
    if mach_entry.get() == '':
        mach_entry.insert(0, '0.7')
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


##############################################################################

# UPPER FRAME ###########

##############################################################################

# DRONE SETTINGS
titleDroneLabel = Label(upframe, text="Drone characteristics", font='Helvetica 16 bold')
titleDroneLabel.place(relx=0.37, rely=0.1, anchor='s')

weightLabel = Label(upframe, text="Drone weight [kg]")
weightLabel.place(relx=0.2, rely=0.2, anchor='w')
weight_entry = Entry(upframe)
weight_entry.place(relx=0.35, rely=0.2, anchor='w')

radioLabel = Label(upframe, text="Propeller radio [m]")
radioLabel.place(relx=0.2, rely=0.3, anchor='w')
radio_entry = Entry(upframe)
radio_entry.place(relx=0.35, rely=0.3, anchor='w')

prop_numLabel = Label(upframe, text="Number of propellers")
prop_numLabel.place(relx=0.2, rely=0.4, anchor='w')
prop_num_entry = Spinbox(upframe, from_=1, to=6, state = 'readonly')
prop_num_entry.place(relx=0.35, rely=0.4, anchor='w')

blade_numLabel = Label(upframe, text="Number of blades")
blade_numLabel.place(relx=0.2, rely=0.5, anchor='w')
blade_num_entry = Spinbox(upframe, from_=2, to=4, state = 'readonly')
blade_num_entry.place(relx=0.35, rely=0.5, anchor='w')

rpmLabel = Label(upframe, text="RPM [rpm]")
rpmLabel.place(relx=0.2, rely=0.6, anchor='w')
rpm_entry = Entry(upframe)
rpm_entry.place(relx=0.35, rely=0.6, anchor='w')

# DRONE CONFIGURATIONS IMAGES
config_12 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-1.2.png"))
config_13 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-1.3.png"))
config_14 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-1.4.png"))
config_22 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-2.2.png"))
config_23 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-2.3.png"))
config_24 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-2.4.png"))
config_32 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-3.2.png"))
config_33 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-3.3.png"))
config_34 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-3.4.png"))
config_42 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-4.2.png"))
config_43 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-4.3.png"))
config_44 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-4.4.png"))
config_52 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-5.2.png"))
config_53 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-5.3.png"))
config_54 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-5.4.png"))
config_62 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-6.2.png"))
config_63 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-6.3.png"))
config_64 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/drone_config/config-6.4.png"))

config_list = [config_12, config_13, config_14,
    config_22, config_23, config_24,
    config_32, config_33, config_34,
    config_42, config_43, config_44,
    config_52, config_53, config_54,
    config_62, config_63, config_64]

# INITIAL IMAGE
preview_img = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/pr.png"))
preview = Label(upframe, image=preview_img, bd=1, relief=SUNKEN)
preview.place(relx=0.75, rely=0.04, anchor='n')

previewLabel = Label(upframe, text="Drone configuration")
previewLabel.place(relx=0.75, rely=1, anchor='s')


submitButton_drone = Button(upframe, text="Submit", command=submit_drone)
submitButton_drone.place(relx=0.402, rely=0.7, anchor='n')

clearButton_drone = Button(upframe, text="Clear", command=clear_drone, state='disable')
clearButton_drone.place(relx=0.338, rely=0.7, anchor='n')



##############################################################################

# LOWER FRAME ###########

##############################################################################

#########################################
# TAB 1 CONTENT - XFOIL ANALYSIS SETTINGS
#########################################
title1Label = Label(tab1, text="Analysis parameters", font='Helvetica 16 bold')
title1Label.place(relx=0.26, rely=0.1, anchor='s')

reLabel = Label(tab1, text="Reynolds number")
reLabel.place(relx=0.1, rely=0.16, anchor='w')
re_entry = Entry(tab1)
re_entry.place(relx=0.25, rely=0.16, anchor='w')

machLabel = Label(tab1, text="Mach number")
machLabel.place(relx=0.1, rely=0.22, anchor='w')
mach_entry = Entry(tab1)
mach_entry.place(relx=0.25, rely=0.22, anchor='w')
mach_entry.insert(END, '0.7')
mach_entry.bind('<FocusIn>', on_entry_click_mach)
mach_entry.bind('<FocusOut>', on_focusout_mach)
mach_entry.configure(fg='grey')

alphaLabel = Label(tab1, text="Angle of attack α")
alphaLabel.place(relx=0.1, rely=0.28, anchor='w')
alphaFromLabel = Label(tab1, text="from")
alphaFromLabel.place(relx=0.25, rely=0.28, anchor='w')
alpha_from_entry = Entry(tab1, width=5)
alpha_from_entry.place(relx=0.285, rely=0.28, anchor='w')
alpha_from_entry.insert(END, '-20')
alpha_from_entry.bind('<FocusIn>', on_entry_click_afrom)
alpha_from_entry.bind('<FocusOut>', on_focusout_afrom)
alpha_from_entry.configure(fg='grey')
alphaToLabel = Label(tab1, text="to")
alphaToLabel.place(relx=0.345, rely=0.28, anchor='w')
alpha_to_entry = Entry(tab1, width=5)
alpha_to_entry.place(relx=0.365, rely=0.28, anchor='w')
alpha_to_entry.insert(END, '20')
alpha_to_entry.bind('<FocusIn>', on_entry_click_ato)
alpha_to_entry.bind('<FocusOut>', on_focusout_ato)
alpha_to_entry.configure(fg='grey')

airfoilButton_analysis = Button(tab1, text="Select an airfoil", command=select_airfoil)
airfoilButton_analysis.place(relx=0.1, rely=0.34, anchor='w')

airfoil_frame = LabelFrame(tab1, bd=1)
airfoil_frame.configure(height=25, width=172)
airfoil_frame.grid_propagate(0)
airfoil_frame.place(relx=0.25, rely=0.34, anchor='w')
airfoil_sel = Label(airfoil_frame, text="No airfoil selected")
airfoil_sel.place(relx=0.5, anchor='n')

submitButton_analysis = Button(tab1, text="Submit", command=submit_analysis)
submitButton_analysis.place(relx=0.3, rely=0.4, anchor='n')

clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis, state='disable')
clearButton_analysis.place(relx=0.235, rely=0.4, anchor='n')

geomLabel = Label(geometryframe, text="Airfoil geometry")
geomLabel.place(relx=0.5, anchor='n')


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
#    # XFOIL #######
#    from xfoil import XFoil
#    xf = XFoil()
#
#    # Import an airfoil
#    from xfoil.test import XXXXX
#    xf.airfoil = XXXXX

#    # Setting up the analysis parameters
#    xf.Re = re
#    xf.max_iter = 100
#    xf.M = 0.7
#
#    # Obtaining the angle of attack, lift coefficient, drag coefficient and momentum coefficient of the airfoil
#    a, cl, cd, cm = xf.aseq(0, 30, 0.5)


######################################
# TAB 2 CONTENT - FIND OPTIMUM AIRFOIL
######################################











# QUIT PROGRAM
button_quit = Button (canvas, text="Close", command=root.quit)
button_quit.place(relx=0.975, rely=0.035, anchor='e')

root.mainloop()
