# -*- coding: utf-8 -*-

from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import ttk
import matplotlib as mpl
import matplotlib.pylab as plt
import math


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

upframe = Frame(root, bg='grey')
upframe.place(relx=0.5, rely=0.07, relwidth=0.95, relheight=0.3, anchor='n')

lowframe = ttk.Notebook(root)
lowframe.place(relx=0.5, rely=0.4, relwidth=0.99, relheight=0.575, anchor='n')

tab1 = ttk.Frame(lowframe)
lowframe.add(tab1, text='Airfoil analysis')

tab2 = ttk.Frame(lowframe)
lowframe.add(tab2, text='Find optimum airfoil')

# DEFINITIONS
def submit_drone():
    # Asegurar que lo introducido es un valor correcto
    # VER COMO SE HACE
    global weight
    global radio
    global prop_num
    global blade_num
    global rpm

    weight = float(weight_entry.get())
    radio = float(radio_entry.get())
    prop_num = int(prop_num_entry.get())
    blade_num = int(blade_num_entry.get())
    rpm = float(rpm_entry.get())

    preview_img = config_list[(prop_num - 1) * 3 + (blade_num -2)]
    preview = Label(upframe, image=preview_img, bd=1, relief=SUNKEN)
    preview.place(relx=0.5, rely=0.04, anchor='n')
    previewLabel = Label(upframe, text="Drone configuration")
    previewLabel.place(relx=0.5, rely=1, anchor='s')

    # POWER REQUIREMENTS & SOME CALCULATIONS
    prop_omega = rpm * float(math.pi) / float(30)  #[rad/s]
    prop_area = prop_num * math.pi * radio ** 2  #[m^2]
    v_1 = math.sqrt((2 * weight *g_mars) / (rho_mars * prop_area))  #[m/s]
    power_req = 0.5 * rho_mars * prop_area * v_1 ** 3  #[W]

    powerLabel = Label(upframe, text="Power required [W]")
    powerLabel.place(relx=0.65, rely=0.2, anchor='w')
    power_reqLabel = Label(upframe, text=round(power_req, 3), width=9)
    power_reqLabel.place(relx=0.77, rely=0.2, anchor='w')

def clear_drone():

    weight_entry.delete(0, END)
    radio_entry.delete(0, END)
    prop_num_entry.delete(0, END)
    blade_num_entry.delete(0, END)
    rpm_entry.delete(0, END)

    power_reqLabel = Label(upframe, text='', width=9)
    power_reqLabel.place(relx=0.77, rely=0.2, anchor='w')

    preview_img = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/pr.png"))
    preview = Label(upframe, image=preview_img, bd=1, relief=SUNKEN)
    preview.place(relx=0.5, rely=0.04, anchor='n')
    previewLabel = Label(upframe, text="Drone configuration")
    previewLabel.place(relx=0.5, rely=1, anchor='s')

def select_airfoil():
    root.filename = filedialog.askopenfilename(initialdir="/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/", title="Select an airfoil geometry",)
    airfoil_sel = Label(airfoil_frame, text=root.filename)
    airfoil_sel.grid(row=16, column=1, pady=1)

def submit_analysis():
    # Asegurar que lo introducido es un valor correcto
    # VER COMO SE HACE
    re = float(re_entry.get())
    mach = float(mach_entry.get())
    alpha_i_from = float(alpha_i_from_entry.get())
    alpha_i_to = float(alpha_i_to_entry.get())

def clear_analysis():

    re_entry.delete(0, END)
    mach_entry.delete(0, END)
    alpha_i_from_entry.delete(0, END)
    alpha_i_to_entry.delete(0, END)


# UPPER FRAME ###########
# DRONE SETTINGS
titleDroneLabel = Label(upframe, text="Drone characteristics", font='Helvetica 16 bold')
titleDroneLabel.place(relx=0.17, rely=0.1, anchor='s')

weightLabel = Label(upframe, text="Drone weight [kg]")
weightLabel.place(relx=0, rely=0.2, anchor='w')
weight_entry = Entry(upframe)
weight_entry.place(relx=0.15, rely=0.2, anchor='w')

radioLabel = Label(upframe, text="Propeller radio [m]")
radioLabel.place(relx=0, rely=0.3, anchor='w')
radio_entry = Entry(upframe)
radio_entry.place(relx=0.15, rely=0.3, anchor='w')

prop_numLabel = Label(upframe, text="Number of propellers")
prop_numLabel.place(relx=0, rely=0.4, anchor='w')
prop_num_entry = Spinbox(upframe, from_=1, to=6)
prop_num_entry.place(relx=0.15, rely=0.4, anchor='w')

blade_numLabel = Label(upframe, text="Number of blades")
blade_numLabel.place(relx=0, rely=0.5, anchor='w')
blade_num_entry = Spinbox(upframe, from_=2, to=4)
blade_num_entry.place(relx=0.15, rely=0.5, anchor='w')

rpmLabel = Label(upframe, text="RPM [rpm]")
rpmLabel.place(relx=0, rely=0.6, anchor='w')
rpm_entry = Entry(upframe)
rpm_entry.place(relx=0.15, rely=0.6, anchor='w')

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
preview.place(relx=0.5, rely=0.04, anchor='n')

previewLabel = Label(upframe, text="Drone configuration")
previewLabel.place(relx=0.5, rely=1, anchor='s')


submitButton_drone = Button(upframe, text="Submit", command=submit_drone)
submitButton_drone.place(relx=0.202, rely=0.75, anchor='n')

clearButton_drone = Button(upframe, text="Clear", command=clear_drone)
clearButton_drone.place(relx=0.138, rely=0.75, anchor='n')




# LOWER FRAME ###########

# XFOIL ANALYSIS SETTINGS
titleXfoilLabel = Label(tab1, text="Analysis parameters", font='Helvetica 16 bold')
titleXfoilLabel.place(relx=0.17, rely=0.055, anchor='s')

reLabel = Label(tab1, text="Reynolds number")
reLabel.place(relx=0, rely=0.1, anchor='w')
re_entry = Entry(tab1)
re_entry.place(relx=0.15, rely=0.1, anchor='w')

machLabel = Label(tab1, text="Mach number")
machLabel.place(relx=0, rely=0.16, anchor='w')
mach_entry = Entry(tab1)
mach_entry.place(relx=0.15, rely=0.16, anchor='w')

alpha_iLabel = Label(tab1, text="Angle of attack α")
alpha_iLabel.place(relx=0, rely=0.22, anchor='w')
alpha_iFromLabel = Label(tab1, text="from")
alpha_iFromLabel.place(relx=0.15, rely=0.22, anchor='w')
alpha_i_from_entry = Entry(tab1, width=5)
alpha_i_from_entry.place(relx=0.185, rely=0.22, anchor='w')
alpha_iToLabel = Label(tab1, text="to")
alpha_iToLabel.place(relx=0.245, rely=0.22, anchor='w')
alpha_i_to_entry = Entry(tab1, width=5)
alpha_i_to_entry.place(relx=0.265, rely=0.22, anchor='w')


airfoilButton_analysis = Button(tab1, text="Select an airofil", command=select_airfoil)
airfoilButton_analysis.place(relx=0, rely=0.28, anchor='w')
airfoil_frame = LabelFrame(tab1, bd=1)
airfoil_frame.configure(height=25, width=172)
airfoil_frame.grid_propagate(0)
airfoil_frame.place(relx=0.15, rely=0.28, anchor='w')
airfoil_sel = Label(airfoil_frame, text="No airfoil selected")
airfoil_sel.place(relx=0.15, rely=0.5, anchor='w')

submitButton_analysis = Button(tab1, text="Submit", command=submit_analysis)
submitButton_analysis.place(relx=0.2, rely=0.37, anchor='n')

clearButton_analysis = Button(tab1, text="Clear", command=clear_analysis)
clearButton_analysis.place(relx=0.135, rely=0.37, anchor='n')





# CALCULATIONS ###########


# REFERENCE VALUES #######
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















# QUIT PROGRAM
button_quit = Button (canvas, text="Close", command=root.quit)
button_quit.place(relx=0.975, rely=0.035, anchor='e')

root.mainloop()
