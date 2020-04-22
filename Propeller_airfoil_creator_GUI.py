from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog

root = Tk()
root.title("Anacardo propeller creator")
root.resizable(width=False, height=False)



# LOGO AND TITLE
logo_Redtek = ImageTk.PhotoImage(Image.open("/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/logo.jpg"))
logo = Label(image=logo_Redtek, anchor=N)
logo.grid(row=0, column= 0, columnspan=10, pady=20, sticky=N)

mainLabel = Label(root, text="ANACARDO PROPELLER CREATOR", font='Helvetica 16 bold')
mainLabel.grid(row=1, column=0, columnspan=10, pady=5)



# DEFINITIONS
def submit_drone():
    weight.get()
    radio.get()
    prop_num.get()
    blade_num.get()
    rpm.get()

    preview_img = config_list[int(prop_num.get()) - 1]
    preview = Label(image=preview_img, bd=1, relief=SUNKEN)
    preview.grid(row=3, rowspan=6, column= 3, columnspan=6, padx= 30)

def select_airfoil():
    root.filename = filedialog.askopenfilename(initialdir="/Users/alangarcia/Desktop/REDTEK/Mechanics/Propeller code/Repo/Redtek/", title="Select an airfoil geometry",)
    airfoil_sel = Label(airfoil_frame, text=root.filename)
    airfoil_sel.grid(row=16, column=1, pady=1)


def submit_analysis():
    re.get()
    mach.get()
    a_i.get()
    a_step.get()



# DRONE SETTINGS
titleLabel = Label(root, text="Drone characteristics", font='Helvetica 14 bold')
titleLabel.grid(row=2, column=0, pady=10)

weightLabel = Label(root, text="Drone weight [kg]")
weightLabel.grid(row=3, column=0, pady=1)
weight = Entry(root)
weight.grid(row=3, column=1, pady=1)

radioLabel = Label(root, text="Propeller radio [m]")
radioLabel.grid(row=4, column=0, pady=1)
radio = Entry(root)
radio.grid(row=4, column=1, pady=1)

prop_numLabel = Label(root, text="Number of propellers")
prop_numLabel.grid(row=5, column=0, pady=1)
prop_num = Spinbox(root, from_=1, to=6)
prop_num.grid(row=5, column=1, pady=1)

blade_numLabel = Label(root, text="Number of blades")
blade_numLabel.grid(row=6, column=0, pady=1)
blade_num = Entry(root)
blade_num.grid(row=6, column=1, pady=1)

rpmLabel = Label(root, text="RPM [rpm]")
rpmLabel.grid(row=7, column=0, pady=1)
rpm = Entry(root)
rpm.grid(row=7, column=1, pady=1)

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
preview = Label(image=preview_img, bd=1, relief=SUNKEN)
preview.grid(row=3, rowspan=6, column= 3, columnspan=6, padx= 30)

previewLabel = Label(root, text="Drone configuration")
previewLabel.grid(row=10, column=3, columnspan=6)


submitButton_drone = Button(root, text="Submit", command=submit_drone)
submitButton_drone.grid(row=8, column=0, columnspan=2, pady=40)



# XFOIL ANALYSIS SETTINGS
titleLabel = Label(root, text="Airfoil analysis", font='Helvetica 14 bold')
titleLabel.grid(row=11, column=0, pady=10)

reLabel = Label(root, text="Reynolds number")
reLabel.grid(row=12, column=0, pady=1)
re = Entry(root)
re.grid(row=12, column=1, pady=1)

machLabel = Label(root, text="Mach number")
machLabel.grid(row=13, column=0, pady=1)
mach = Entry(root)
mach.grid(row=13, column=1, pady=1)

a_iLabel = Label(root, text="Intital a")
a_iLabel.grid(row=14, column=0, pady=1)
a_i = Entry(root)
a_i.grid(row=14, column=1, pady=1)

a_stepLabel = Label(root, text="Steps a")
a_stepLabel.grid(row=15, column=0, pady=1)
a_step = Entry(root)
a_step.grid(row=15, column=1, pady=1)

airfoilButton_analysis = Button(root, text="Select an airofil", command=select_airfoil)
airfoilButton_analysis.grid(row=16, column=0, pady=1)
airfoil_frame = LabelFrame(root, bd=1)
airfoil_frame.configure(height=25, width=168)
airfoil_frame.grid_propagate(0)
airfoil_frame.grid(row=16, column=1, pady=1)
airfoil_sel = Label(airfoil_frame, text="No airfoil selected")
airfoil_sel.grid(row=16, column=1, pady=1)

submitButton_analysis = Button(root, text="Submit", command=submit_analysis)
submitButton_analysis.grid(row=17, column=0, columnspan=2, pady=40)




# QUIT PROGRAM
button_quit = Button (root, text="Close", command=root.quit)
button_quit.grid(row=30, column=9)

root.mainloop()
