import serial
import serial.tools.list_ports
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial import Serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

def SetRoll():

    Min = RollMin.get()
    Max = RollMax.get()
    XSlider = XSlider=tk.Scale(orient=tk.HORIZONTAL,
                     length=350,
                     width=25,
                     from_=Min,
                     to=Max,
                     sliderlength=20,
                     digit=5,
                     resolution=0.01)

def connect():

    global ArduinoPort
    #Get COM Port from Combo Box
    port_long = cb.get()
    port = port_long[0:4]
    #Reset Slider to 0.00
    XSlider.set(0.00)
    YSlider.set(0.00)
    ZSlider.set(0.00)
    #Reset Label to 0
    XLabel["text"] = 0
    ZLabel["text"] = 0
    YLabel["text"] = 0
    try:
            ArduinoPort = serial.Serial(str(port), 9600)
            # ArduinoPort = "test"
    except ValueError:
        print("Cannot Connecterd")
        return

def disconnect():
    try:
        ArduinoPort.close()
    except AttributeError:
        print
        "Closed without Using it "
    # gui.quit()

def serial_ports():
    return serial.tools.list_ports.comports()

def on_select(event=None):
    print("comboboxes: ", cb.get())

def update():
    global buffer
    while ArduinoPort.inWaiting():
        tmp = ArduinoPort.readline(1)
        if tmp == b'\n':
            pass
        elif tmp == b'\x00':
            try :
                num = [float(i) for i in buffer.decode().split()]
                XSlider.set(num[0])
                YSlider.set(num[1])
                ZSlider.set(num[2])
                XLabel["text"] = num[0]
                ZLabel["text"] = num[2]
                YLabel["text"] = num[1]
            except:
                # pass
                print(buffer)
            # reset
            buffer = b''
        else:
            buffer += tmp
    gui.after(1,update)

def update_var():
    global buffer, Roll, Pitch, Yaw
    while ArduinoPort.inWaiting():
        tmp = ArduinoPort.readline(1)
        if tmp == b'\n':
            pass
        elif tmp == b'\x00':
            try :
                num = [float(i) for i in buffer.decode().split()]
                Roll = num[0]
                Pitch = num[1]
                Yaw = num[2]
                return [Roll, Pitch, Yaw]
            except:
                # pass
                print()
            # reset
            buffer = b''
        else:
            buffer += tmp
    gui.after(1,update)

def animate(i, xs, Rolls):

    global cnt
    update_var()
    xs.append(cnt)
    Rolls.append(Roll)
    Pitchs.append(Pitch)
    Yaws.append(Yaw)

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, Rolls, label='Roll')
    ax.plot(xs, Pitchs, label='Pitch')
    ax.plot(xs, Yaws, label='Yaw')
    leg = ax.legend()
    plt.xlim(left=max(0, cnt - 20), right=cnt)
    plt.ylim(-60, 60)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('GY25-Plotting moitor')
    plt.ylabel('Degree')
    cnt +=0.5

# Set initial Arduino port
# ArduinoPort = Serial('COM4',9600,timeout=30)
ArduinoPort = Serial('/dev/tty',9600,timeout=30)
# ArduinoPort = "Test"
ArduinoPort.flushInput()
buffer = b''

# Declare Variable to collect data
Roll = 0.0
Pitch = 0.0
Yaw = 0.0

# Declare GUI initial
gui = tk.Tk()
gui.title("Gyroscope Monitor")
gui.geometry("{0}x{1}+0+0".format(
            gui.winfo_screenwidth()+5, gui.winfo_screenheight()-80))
gui.state('zoomed')

#GUI Font
TopicSize = tkFont.Font(family="Luida Grande", size=36)
TextSize = tkFont.Font(family="Luida", size=16)
TextSize2 = tkFont.Font(family="Luida", size=12)
TextSize3 = tkFont.Font(size=10)

#Plot Initail Setting
fig = plt.figure(figsize=(10, 5.5))
fig.patch.set_facecolor('#f0f0f0')
ax = fig.add_subplot(1, 1, 1)
# ax.set_facecolor()
line = FigureCanvasTkAgg(fig, gui)
line.get_tk_widget().place(anchor='s', relx=0.5, rely=1.1)
xs = []
Rolls = []
Pitchs = []
Yaws = []
cnt = 0

if __name__ == "__main__":

    #Topic Label
    Topic = tk.Label(text="Gyroscope Monitor",font=TopicSize)
    Topic.place(anchor='n', relx=0.5, rely=0.05)

    #COM Port Selector
    tk.Label(text="Choose COM Port", font=TextSize).place(anchor='n', relx=0.40, rely=0.2)
    gui.option_add("*TCombobox*Font", TextSize)
    cb = ttk.Combobox(gui, values=serial_ports())
    cb.set('COM1 - Communications Port (COM1)')
    cb.place(anchor='n', relx=0.6, rely=0.2)
    cb.bind('<<ComboboxSelected>>', on_select)
    gui.option_add("*Button*Font", TextSize2)
    connect = tk.Button(text="Connect", command=connect).place(anchor='n', relx=0.45, rely=0.275)
    disconnect = tk.Button(text="Disconnect", command=disconnect).place(anchor='n', relx=0.55, rely=0.275)

    #Angle Axis
    tk.Label(text="   Roll :", font=TextSize).place(anchor='w', relx=0.3, rely=0.40)
    tk.Label(text="   Pitch :", font=TextSize).place(anchor='w', relx=0.3, rely=0.48)
    tk.Label(text="   Yaw :", font=TextSize).place(anchor='w', relx=0.3, rely=0.56)

    #Roll_Scale
    XLabel = tk.Label(text=0, font=TextSize).place(anchor='w', relx=0.36, rely=0.40)

    RollMin_Var = tk.StringVar(gui, '-25')
    RollMax_Var = tk.StringVar(gui, '35')
    RollMin = tk.Entry(width=5, bd=5, textvariable=RollMin_Var)
    RollMin.place(anchor='w', relx=0.42, rely=0.40)
    RollMax = tk.Entry(width=5, bd=5, textvariable=RollMax_Var)
    RollMax.place(anchor='w', relx=0.60, rely=0.40)

    RollSet = tk.Button(text='Set', command=SetRoll).pack()

    XSlider=tk.Scale(orient=tk.HORIZONTAL,
                     length=350,
                     width=25,
                     from_=RollMin.get(),
                     to=RollMax.get(),
                     sliderlength=20,
                     digit=5,
                     resolution=0.01)
    XSlider.place(anchor='w', relx=0.45, rely=0.39)

    #Pitch_Scale
    YLabel = tk.Label(text=0, font=TextSize).place(anchor='w', relx=0.36, rely=0.48)

    DefPitchMin = tk.StringVar(gui, '-40')
    DefPitchMax = tk.StringVar(gui, '15')
    PitchMin = tk.Entry(width=5, bd=5, textvariable=DefPitchMin)
    PitchMin.place(anchor='w', relx=0.42, rely=0.48)
    PitchMax = tk.Entry(width=5, bd=5, textvariable=DefPitchMax)
    PitchMax.place(anchor='w', relx=0.60, rely=0.48)

    YSlider=tk.Scale(orient=tk.HORIZONTAL,
                     length=350,
                     width=25,
                     from_=PitchMin.get(),
                     to=PitchMax.get(),
                     sliderlength=20,
                     digit=5,
                     resolution=0.01)
    YSlider.place(anchor='w', relx=0.45, rely=0.47)

    #Yaw_Scale
    ZLabel = tk.Label(text=0, font=TextSize).place(anchor='w', relx=0.36, rely=0.56)

    DefYawMin = tk.StringVar(gui, '-30')
    DefYawMax = tk.StringVar(gui, '30')
    YawMin = tk.Entry(width=5, bd=5, textvariable=DefYawMin)
    YawMin.place(anchor='w', relx=0.42, rely=0.56)
    YawMax = tk.Entry(width=5, bd=5, textvariable=DefYawMax)
    YawMax.place(anchor='w', relx=0.60, rely=0.56)

    ZSlider=tk.Scale(orient=tk.HORIZONTAL,
                     length=350,
                     width=25,
                     from_=YawMin.get(),
                     to=YawMax.get(),
                     sliderlength=20,
                     digit=5,
                     resolution=0.01)
    ZSlider.place(anchor='w', relx=0.45, rely=0.55)

    #update angle
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, Rolls), interval=500)
    gui.after(1,update)
    gui.mainloop()