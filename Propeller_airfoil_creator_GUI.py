from tkinter import *
from PIL import ImageTk,Image

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
upframe.place(relx=0.5, rely=0.07, relwidth=0.95, relheight=0.3,anchor='n')

lowframe = Frame(root)
lowframe.place(relx=0.5, rely=0.4, relwidth=0.95, relheight=0.575,anchor='n')

# DEFINITIONS
def submit_drone():
    # Asegurar que lo introducido es un valor correcto
    # VER COMO SE HACE
    int(weight.get())
    int(radio.get())
    int(prop_num.get())
    int(blade_num.get())
    int(rpm.get())

    preview_img = config_list[int(prop_num.get()) - 1]
    preview = Label(image=preview_img, bd=1, relief=SUNKEN)
    preview.place(relx=0.6, rely=0.07, relwidth=0.4, relheight=0.3)

def select_airfoil():
    root.filename = filedialog.askopenfilename(initialdir="/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/", title="Select an airfoil geometry",)
    airfoil_sel = Label(airfoil_frame, text=root.filename)
    airfoil_sel.grid(row=16, column=1, pady=1)

def submit_analysis():
    # Asegurar que lo introducido es un valor correcto
    # VER COMO SE HACE
    int(re.get())
    int(mach.get())
    int(a_i.get())
    int(a_step.get())


# UPPER FRAME ###########
# DRONE SETTINGS
titleDroneLabel = Label(upframe, text="Drone characteristics", font='Helvetica 16 bold')
titleDroneLabel.place(relx=0.17, rely=0.1, anchor='s')

weightLabel = Label(upframe, text="Drone weight [kg]")
weightLabel.place(relx=0, rely=0.2, anchor='w')
weight = Entry(upframe)
weight.place(relx=0.15, rely=0.2, anchor='w')

radioLabel = Label(upframe, text="Propeller radio [m]")
radioLabel.place(relx=0, rely=0.3, anchor='w')
radio = Entry(upframe)
radio.place(relx=0.15, rely=0.3, anchor='w')

prop_numLabel = Label(upframe, text="Number of propellers")
prop_numLabel.place(relx=0, rely=0.4, anchor='w')
prop_num = Spinbox(upframe, from_=1, to=6)
prop_num.place(relx=0.15, rely=0.4, anchor='w')

blade_numLabel = Label(upframe, text="Number of blades")
blade_numLabel.place(relx=0, rely=0.5, anchor='w')
blade_num = Spinbox(upframe, from_=1, to=4)
blade_num.place(relx=0.15, rely=0.5, anchor='w')

rpmLabel = Label(upframe, text="RPM [rpm]")
rpmLabel.place(relx=0, rely=0.6, anchor='w')
rpm = Entry(upframe)
rpm.place(relx=0.15, rely=0.6, anchor='w')

# DRONE CONFIGURATIONS IMAGES
config_1 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/config-1.png"))
config_2 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/config-2.png"))
config_3 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/config-3.png"))
config_4 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/config-4.png"))
config_5 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/config-5.png"))
config_6 = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/config-6.png"))

config_list = [config_1, config_2, config_3, config_4, config_5, config_6]

# INITIAL IMAGE
preview_img = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/pr.png"))
preview = Label(upframe, image=preview_img, bd=1, relief=SUNKEN)
preview.place(relx=0.5, rely=0.04, anchor='n')

previewLabel = Label(upframe, text="Drone configuration")
previewLabel.place(relx=0.5, rely=1, anchor='s')


submitButton_drone = Button(upframe, text="Submit", command=submit_drone)
submitButton_drone.place(relx=0.17, rely=0.75, anchor='n')


# LOWER FRAME ###########

# XFOIL ANALYSIS SETTINGS
titleXfoilLabel = Label(lowframe, text="Airfoil analysis", font='Helvetica 16 bold')
titleXfoilLabel.place(relx=0.17, rely=0.052, anchor='s')

reLabel = Label(lowframe, text="Reynolds number")
reLabel.place(relx=0, rely=0.1, anchor='w')
re = Entry(lowframe)
re.place(relx=0.15, rely=0.1, anchor='w')

machLabel = Label(lowframe, text="Mach number")
machLabel.place(relx=0, rely=0.152, anchor='w')
mach = Entry(lowframe)
mach.place(relx=0.15, rely=0.152, anchor='w')

a_iLabel = Label(lowframe, text="Intital a")
a_iLabel.place(relx=0, rely=0.204, anchor='w')
a_i = Entry(lowframe)
a_i.place(relx=0.15, rely=0.204, anchor='w')

a_stepLabel = Label(lowframe, text="Steps a")
a_stepLabel.place(relx=0, rely=0.256, anchor='w')
a_step = Entry(lowframe)
a_step.place(relx=0.15, rely=0.256, anchor='w')

airfoilButton_analysis = Button(lowframe, text="Select an airofil", command=select_airfoil)
airfoilButton_analysis.place(relx=0, rely=0.308, anchor='w')
airfoil_frame = LabelFrame(lowframe, bd=1)
airfoil_frame.configure(height=25, width=172)
airfoil_frame.grid_propagate(0)
airfoil_frame.place(relx=0.15, rely=0.308, anchor='w')
airfoil_sel = Label(airfoil_frame, text="No airfoil selected")
airfoil_sel.place(relx=0.15, rely=0.5, anchor='w')

submitButton_analysis = Button(lowframe, text="Submit", command=submit_analysis)
submitButton_analysis.place(relx=0.17, rely=0.386, anchor='n')




# QUIT PROGRAM
button_quit = Button (canvas, text="Close", command=root.quit)
button_quit.place(relx=0.975, rely=0.035, anchor='e')

root.mainloop()
