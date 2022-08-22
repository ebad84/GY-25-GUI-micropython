import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from pandas import DataFrame
import serial
import serial.tools.list_ports
from serial import Serial
import time
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
##########  button function #############
def start():
    global start_status, arduino_port, com_port, roll, pitch, yaw, count
    port = port_lists.get()
    if start_button.config('text')[-1] == 'Start':
        start_button.config(text='Stop')
        if port == com_port:
            start_status = True
            ani.event_source.start()
            roll, pitch, yaw = 0.0, 0.0, 0.0
            roll_array.clear()
            pitch_array.clear()
            yaw_array.clear()
            roll_count.clear()
            pitch_count.clear()
            yaw_count.clear()
            roll_csv.clear()
            pitch_csv.clear()
            yaw_csv.clear()
            roll_array.clear()
            pitch_array.clear()
            yaw_array.clear()

            roll_count.clear()
            pitch_count.clear()
            yaw_count.clear()

            ax1.clear()
            ax1.set_xlim(0, 10)
            ax1.set_ylim(roll_min_var, roll_max_var)
            ax1.grid()

            ax2.clear()
            ax2.set_xlim(0, 10)
            ax2.set_ylim(pitch_min_var, pitch_max_var)
            ax2.grid()

            ax3.clear()
            ax3.set_xlim(0, 10)
            ax3.set_ylim(yaw_min_var, yaw_max_var)
            ax3.grid()
            count=10

        else:
            try:
                com_port = port
                arduino_port = Serial(str(com_port), 9600, timeout=100)
                start_status = True
                ani.event_source.start()
                roll, pitch, yaw = 0.0, 0.0, 0.0
                roll_array.clear()
                pitch_array.clear()
                yaw_array.clear()
                roll_count.clear()
                pitch_count.clear()
                yaw_count.clear()
                roll_csv.clear()
                pitch_csv.clear()
                yaw_csv.clear()
                roll_array.clear()
                pitch_array.clear()
                yaw_array.clear()

                roll_count.clear()
                pitch_count.clear()
                yaw_count.clear()

                ax1.clear()
                ax1.set_xlim(0, 10)
                ax1.set_ylim(roll_min_var, roll_max_var)
                ax1.grid()

                ax2.clear()
                ax2.set_xlim(0, 10)
                ax2.set_ylim(pitch_min_var, pitch_max_var)
                ax2.grid()

                ax3.clear()
                ax3.set_xlim(0, 10)
                ax3.set_ylim(yaw_min_var, yaw_max_var)
                ax3.grid()
                count=10
            except ValueError:
                return
    else:
        start_button.config(text='Start')
        start_status = False

def print_text():
    global print_text_status
    if print_text_button.config('text')[-1] == 'Show Text Data':
        print_text_button.config(text='Stop Show Text Data')
        print_text_status = True
    else:
        print_text_button.config(text='Show Text Data')
        print_text_status = False

def arduino_reset():
    arduino_port.write(b'r')



def mode_change():
    label = mode_label.cget('text')
    print(type(label))
    if label == 'Manual Mode':
        arduino_port.write(b'2')
        mode_label['text'] = '2'
        print('2')

    elif label == 'Set Position 1':
        arduino_port.write(b'3')
        mode_label['text']='3'
        print('3')

    elif label == 'Set Position 2':
        arduino_port.write(b'4')
        mode_label['text']='4'
        print('4')

    else:
        arduino_port.write(b'1')
        mode_label['text'] = '1'
        print('1')

def record():
    global record_status
    if record_button.config('text')[-1] == 'Start Data Record':
        record_button.config(text='Stop Data Record')
        exportcsv_button['state'] = tk.DISABLED
        record_status = True
        ani.event_source.start()
        roll_csv.clear()
        pitch_csv.clear()
        yaw_csv.clear()
    else:
        record_button.config(text='Start Data Record')
        exportcsv_button['state'] = tk.NORMAL
        record_status = False

def export():
    global df
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv(export_file_path, index=False, header=True)

def set_range():
    global  roll_slider, pitch_slider, yaw_slider, \
            roll_min, pitch_min, yaw_min, \
            roll_max, pitch_max, yaw_max, \
            roll_min_var, pitch_min_var, yaw_min_var, \
            roll_max_var, pitch_max_var, yaw_max_var

    roll_slider.place_forget()
    pitch_slider.place_forget()
    yaw_slider.place_forget()

    roll_min_var = int(roll_min.get())
    roll_max_var = int(roll_max.get())
    pitch_min_var = int(pitch_min.get())
    pitch_max_var = int(pitch_max.get())
    yaw_min_var = int(yaw_min.get())
    yaw_max_var = int(yaw_max.get())

    roll_slider = tk.Scale(position_frame, orient=tk.HORIZONTAL,
                           length=350,
                           width=20,
                           from_=roll_min_var,
                           to=roll_max_var,
                           sliderlength=20,
                           digit=5,
                           resolution=0.01)

    pitch_slider = tk.Scale(position_frame, orient=tk.HORIZONTAL,
                            length=350,
                            width=20,
                            from_=pitch_min_var,
                            to=pitch_max_var,
                            sliderlength=20,
                            digit=5,
                            resolution=0.01)

    yaw_slider = tk.Scale(position_frame, orient=tk.HORIZONTAL,
                          length=350,
                          width=20,
                          from_=yaw_min_var,
                          to=yaw_max_var,
                          sliderlength=20,
                          digit=5,
                          resolution=0.01)

    roll_slider.place(anchor='w', relx=0.45, rely=0.23)
    pitch_slider.place(anchor='w', relx=0.45, rely=0.38)
    yaw_slider.place(anchor='w', relx=0.45, rely=0.53)

def set_zero():
    global roll_origin, pitch_origin, yaw_origin
    roll_origin = num[0]
    pitch_origin = num[1]
    yaw_origin = num[2]

def toggle_3D():
    global enable_3D
    if toggle_3D_button.config('text')[-1] == 'Enable 3D':
        toggle_3D_button.config(text='Disable 3D')
        enable_3D = True
    else:
        toggle_3D_button.config(text='Enable 3D')
        enable_3D = False

def toggle_plot_all():
    global enable_plot, enable_roll, enable_pitch, enable_yaw

    if toggle_plot_all_button.config('text')[-1] == 'Enable All':
        toggle_plot_all_button.config(text='Disable All')
        toggle_plot_roll_button.config(text='Disable Roll')
        toggle_plot_pitch_button.config(text='Disable Pitch')
        toggle_plot_yaw_button.config(text='Disable Yaw')

        enable_plot = True
        enable_roll = True
        enable_pitch = True
        enable_yaw = True
    else:
        toggle_plot_all_button.config(text='Enable All')
        toggle_plot_roll_button.config(text='Enable Roll')
        toggle_plot_pitch_button.config(text='Enable Pitch')
        toggle_plot_yaw_button.config(text='Enable Yaw')
        enable_plot = False
        enable_roll = False
        enable_pitch = False
        enable_yaw = False

def toggle_plot_roll():
    global enable_roll, enable_plot
    if toggle_plot_roll_button.config('text')[-1] == 'Enable Roll':
        toggle_plot_roll_button.config(text='Disable Roll')
        toggle_plot_all_button.config(text='Disable All')
        enable_roll = True
        enable_plot = True
    else:
        toggle_plot_roll_button.config(text='Enable Roll')
        enable_roll = False

def toggle_plot_pitch():
    global enable_pitch, enable_plot
    if toggle_plot_pitch_button.config('text')[-1] == 'Enable Pitch':
        toggle_plot_pitch_button.config(text='Disable Pitch')
        toggle_plot_all_button.config(text='Disable All')
        enable_pitch = True
        enable_plot = True
    else:
        toggle_plot_pitch_button.config(text='Enable Pitch')
        enable_pitch = False

def toggle_plot_yaw():
    global enable_yaw, enable_plot
    if toggle_plot_yaw_button.config('text')[-1] == 'Enable Yaw':
        toggle_plot_yaw_button.config(text='Disable Yaw')
        toggle_plot_all_button.config(text='Disable All')
        enable_yaw = True
        enable_plot = True
    else:
        toggle_plot_yaw_button.config(text='Enable Yaw')
        enable_yaw = False

def on_closing():
    global stop_threads
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        ani.event_source.stop()
        gui.quit()
        gui.destroy()
        stop_threads = True

##########  backend function #############

### get COM port ###
def set_port(set):
    ports = list(serial.tools.list_ports.comports())
    if set == 1:
        for p in ports:
            if "Arduino" or "USB" or "usb" in p.description:
                return str(p)[0:4]
    else:
        ports_list = []
        for p in ports:
            if "COM" in p.description:
                ports_list.append(str(p)[0:4])
    return ports_list

### read from arduino ###
def read_arduino():
    global roll, pitch, yaw, num, mode
    while True:
        time.sleep(0.1)
        if start_status == True:
            while arduino_port.inWaiting():
                tmp = arduino_port.read_until(b'\n')
                try:
                    num = [float(i) for i in tmp.decode('ascii').split()]
                    tmp = b''
                    if print_text_status == True:
                        print(num)
                    roll = round(-(roll_origin - num[0]), 2)
                    pitch = round(-(pitch_origin - num[1]), 2)
                    yaw = round(-(yaw_origin - num[2]), 2)
                    mode = num[3]

                except:
                    pass
        if stop_threads:
            break

def set_mode(mode_num):
    if mode_num == 1:
        mode_label['text'] = 'Manual Mode'
    elif mode_num == 2:
        mode_label['text'] = 'Set Position 1'
    elif mode_num == 3:
        mode_label['text'] = 'Set Position 2'
    else:
        mode_label['text'] = 'Auto Mode'

### set slider ###
def slider_loop(i):
    global count
    if start_status == True:
        roll_slider.set(roll)
        pitch_slider.set(pitch)
        yaw_slider.set(yaw)
        set_mode(int(mode))

        if enable_3D == True:
            plot_3D(roll, pitch, yaw)

### realtime plot ###
def plot():
    global count, roll_array, roll_count
    while True:
        time.sleep(0.1)
        if start_status == True:
            if record_status == True:
                roll_csv.append(roll)
                pitch_csv.append(pitch)
                yaw_csv.append(yaw)
                save_to_frame(roll_csv, pitch_csv, yaw_csv)

            if count >= 10:
                roll_array.clear()
                pitch_array.clear()
                yaw_array.clear()

                roll_count.clear()
                pitch_count.clear()
                yaw_count.clear()

                ax1.clear()
                ax1.set_xlim(0, 10)
                ax1.set_ylim(roll_min_var, roll_max_var)
                ax1.grid()

                ax2.clear()
                ax2.set_xlim(0, 10)
                ax2.set_ylim(pitch_min_var, pitch_max_var)
                ax2.grid()

                ax3.clear()
                ax3.set_xlim(0, 10)
                ax3.set_ylim(yaw_min_var, yaw_max_var)
                ax3.grid()
                count = 0

            # # Draw x and y lists
            if enable_plot == True:
                if enable_roll == True:
                    roll_array.append(roll)
                    roll_count.append(count)
                    ax1.plot(roll_count, roll_array, label='Roll', color='C0')
                    ax1.set_xlim(0, 10)
                    ax1.set_ylim(roll_min_var, roll_max_var)

                if enable_pitch == True:
                    pitch_array.append(pitch)
                    pitch_count.append(count)
                    ax2.set_ylabel('Degree')
                    ax2.plot(pitch_count, pitch_array, label='Pitch', color='C1')
                    ax2.set_xlim(0, 10)
                    ax2.set_ylim(pitch_min_var, pitch_max_var)

                if enable_yaw == True:
                    yaw_array.append(yaw)
                    yaw_count.append(count)
                    ax3.plot(yaw_count, yaw_array, label='Yaw', color='C2')
                    ax3.set_xlim(0, 10)
                    ax3.set_ylim(yaw_min_var, yaw_max_var)

                count += 0.1

        if stop_threads:
            break

### set 3D moving plane ###
def plot_plane(p):
    return ax.plot_trisurf(p[0], p[1], p[2], color='C0', shade=False)

### plot 3D ###
def plot_3D(Roll, Pitch, Yaw):
    global PLANE, plane
    R = Rzyx(Yaw * np.pi / 180, -Pitch * np.pi / 180, Roll * np.pi / 180)
    rotated_plane = np.dot(R, plane)
    PLANE.remove()
    PLANE = plot_plane(rotated_plane)
    fig3d.canvas.draw()
    fig3d.canvas.flush_events()

def Rx(a):  # Roll
    c = np.cos(a)
    s = np.sin(a)
    return np.array([[1, 0, 0],
                     [0, c, -s],
                     [0, s, c]])

def Ry(a):  # Pitch
    c = np.cos(a)
    s = np.sin(a)
    return np.array([[c, 0, s],
                     [0, 1, 0],
                     [-s, 0, c]])

def Rz(a):  # Yaw
    c = np.cos(a)
    s = np.sin(a)
    return np.array([[c, -s, 0],
                     [s, c, 0],
                     [0, 0, 1]])

def Rzyx(a, b, c):
    return np.dot(Rz(a), np.dot(Ry(b), Rx(c)))

def save_to_frame(A, B, C):
    global df
    df = DataFrame(data={"Roll": A, "Pitchs": B, "Yaws": C})

########## Variable Declare #############

### button value ###
start_status = False
enable_3D = False
enable_plot = False
enable_roll = False
enable_pitch = False
enable_yaw = False
record_status = False
stop_threads = False
print_text_status = False

### read value ###
roll, pitch, yaw, mode = 0.0, 0.0, 0.0, 1
roll_origin, pitch_origin, yaw_origin = 0.0, 0.0, 0.0

### Slider Value ###
roll_min_var = -25
roll_max_var = 35
pitch_min_var = -25
pitch_max_var = 35
yaw_min_var = -25
yaw_max_var = 35

### plot value ###
roll_array, pitch_array, yaw_array = [], [], []
roll_count, pitch_count, yaw_count = [], [], []
count = 0

### export csv
roll_csv, pitch_csv, yaw_csv = [], [], []

### 3D Variable ###
a = 1.0  # length
b = 0.5  # width
lim = 1.5  # axis limit
plane = np.array([[a, -a, a, -a],
                  [b, 0, -b, 0],
                  [0, 0, 0, 0]])

########### Start GUI #############

### set arduino port ###
#############################################################################
com_port = set_port(1)
arduino_port = Serial(str(com_port), 9600, timeout=100)
time.sleep(1)
#############################################################################

### start threading ###
t1 = threading.Thread(target=plot) #start plot loop
t1.start()
t2 = threading.Thread(target=read_arduino) #start read loop
t2.start()

gui = tk.Tk()
gui.state('zoomed')
gui.title("Ankle Movement Monitor")
gui.protocol("WM_DELETE_WINDOW", on_closing)
H = gui.winfo_screenheight() - 80
W = gui.winfo_screenwidth() + 5
canvas = tk.Canvas(gui, height=H, width=W)

### Font ###
topic_size = tkFont.Font(size=26)
text_size = tkFont.Font(size=16)
text_size2 = tkFont.Font(size=12)
gui.option_add("*TCombobox*Font", text_size2)
gui.option_add("*Button*Font", text_size2)

### Header ###
topic = tk.Label(text='Ankle Movement Monitoring', font=topic_size)
topic.place(anchor='n', relx=0.5, rely=0.01, relwidth=0.4, relheight=0.1)

### COMPort Frame ###
comport_frame = tk.LabelFrame(gui, text='COM Port Setup')
comport_frame.place(anchor='n', relx=0.13, rely=0.15, relwidth=0.2, relheight=0.2)
tk.Label(comport_frame, text="COM Port", font=text_size2).place(anchor='w', relx=0.15, rely=0.15)

port_lists = ttk.Combobox(comport_frame, values=set_port(0))
port_lists.set(str(com_port))
port_lists.place(anchor='w', relx=0.5, rely=0.15, relwidth=0.35, relheight=0.22)

start_button = tk.Button(comport_frame, command=start, text="Start")
start_button.place(anchor='w', relx=0.18, rely=0.4, relwidth=0.3, relheight=0.18)

print_text_button = tk.Button(comport_frame, command=print_text, text="Show Text Data")
print_text_button.place(anchor='w', relx=0.18, rely=0.62, relwidth=0.62, relheight=0.2)

arduino_reset_button = tk.Button(comport_frame, command=arduino_reset, text="Reset")
arduino_reset_button.place(anchor='w', relx=0.5, rely=0.4, relwidth=0.3, relheight=0.18)

mode_change_button = tk.Button(comport_frame, command=mode_change, text="Select Mode")
mode_change_button.place(anchor='w', relx=0.18, rely=0.85, relwidth=0.4, relheight=0.2)
mode_label = tk.Label(comport_frame, text='1', font=text_size2)
mode_label.place(anchor='w', relx=0.6, rely=0.85)

### Record Frame ###
record_frame = tk.LabelFrame(gui, text="Data Record")
record_frame.place(relx=0.13, rely=0.35, relwidth=0.2, relheight=0.2, anchor='n')

record_button = tk.Button(record_frame, command=record, text="Start Data Record")
record_button.place(anchor='w', relx=0.15, rely=0.25, relwidth=0.7, relheight=0.35)

exportcsv_button = tk.Button(record_frame, command=export, text="Export Data to CSV File")
exportcsv_button.place(anchor='w', relx=0.15, rely=0.65, relwidth=0.7, relheight=0.35)

### Position Slider Frame ###
position_frame = tk.LabelFrame(gui, text="Position Monitoring")
position_frame.place(anchor='n', relx=0.28, rely=0.55, relwidth=0.5, relheight=0.43)

tk.Label(position_frame, text="   Inversion - Eversion             (Roll)  :",
         font=text_size2).place(anchor='w', relx=0.01, rely=0.25)
tk.Label(position_frame, text="   Plantarflexion - Dorsiflexion (Pitch) :",
         font=text_size2).place(anchor='w', relx=0.01, rely=0.4)
tk.Label(position_frame, text="   Abduction - Adduction         (Yaw) :",
         font=text_size2).place(anchor='w', relx=0.01, rely=0.55)

init_min_var = tk.StringVar(gui, '-25')
init_max_var = tk.StringVar(gui, '35')

min_frame = tk.LabelFrame(position_frame, text="Min")
min_frame.place(anchor='w', relx=0.37, rely=0.375, relwidth=0.07, relheight=0.54)
roll_min = tk.Entry(min_frame, bd=2, textvariable=tk.StringVar(gui, '-25'))
roll_min.place(anchor='w', relx=0.15, rely=0.17, relwidth=0.65, relheight=0.13)
pitch_min = tk.Entry(min_frame, bd=2, textvariable=tk.StringVar(gui, '-25'))
pitch_min.place(anchor='w', relx=0.15, rely=0.5, relwidth=0.65, relheight=0.13)
yaw_min = tk.Entry(min_frame, bd=2, textvariable=tk.StringVar(gui, '-25'))
yaw_min.place(anchor='w', relx=0.15, rely=0.83, relwidth=0.65, relheight=0.13)

max_frame = tk.LabelFrame(position_frame, text="Max")
max_frame.place(anchor='w', relx=0.83, rely=0.375, relwidth=0.07, relheight=0.54)
roll_max = tk.Entry(max_frame, bd=2, textvariable=tk.StringVar(gui, '35'))
roll_max.place(anchor='w', relx=0.15, rely=0.17, relwidth=0.65, relheight=0.13)
pitch_max = tk.Entry(max_frame, bd=2, textvariable=tk.StringVar(gui, '35'))
pitch_max.place(anchor='w', relx=0.15, rely=0.5, relwidth=0.65, relheight=0.13)
yaw_max = tk.Entry(max_frame, bd=2, textvariable=tk.StringVar(gui, '35'))
yaw_max.place(anchor='w', relx=0.15, rely=0.83, relwidth=0.65, relheight=0.13)

roll_slider = tk.Scale(position_frame, orient=tk.HORIZONTAL,
                       length=350,
                       width=20,
                       from_=init_min_var.get(),
                       to=init_max_var.get(),
                       sliderlength=20,
                       digit=5,
                       resolution=0.01)
roll_slider.place(anchor='w', relx=0.45, rely=0.23)
pitch_slider = tk.Scale(position_frame, orient=tk.HORIZONTAL,
                        length=350,
                        width=20,
                        from_=init_min_var.get(),
                        to=init_max_var.get(),
                        sliderlength=20,
                        digit=5,
                        resolution=0.01)
pitch_slider.place(anchor='w', relx=0.45, rely=0.38)
yaw_slider = tk.Scale(position_frame, orient=tk.HORIZONTAL,
                      length=350,
                      width=20,
                      from_=init_min_var.get(),
                      to=init_max_var.get(),
                      sliderlength=20,
                      digit=5,
                      resolution=0.01)
yaw_slider.place(anchor='w', relx=0.45, rely=0.53)

set_range_button = tk.Button(position_frame, command=set_range, text="Set Range", width=10, height=2)
set_range_button.place(anchor='w', relx=0.48, rely=0.8)

set_zero_button = tk.Button(position_frame, command=set_zero, text="Set Zero", width=10, height=2)
set_zero_button.place(anchor='w', relx=0.65, rely=0.8)

### plot frame ###
plot_frame = tk.LabelFrame(gui, text="Respone Graph")
plot_frame.place(anchor='n', relx=0.753, rely=0.15, relwidth=0.435, relheight=0.83)
fig = plt.figure(2, figsize=(8, 7))
fig.patch.set_facecolor('#f0f0f0')

ax1 = fig.add_subplot(3, 1, 1)
ax1.set_xlim(0, 10)
ax1.set_ylim(roll_min_var, roll_max_var)
ax1.grid()

ax2 = fig.add_subplot(3, 1, 2)
ax2.set_ylabel('Degree')
ax2.set_xlim(0, 10)
ax2.set_ylim(pitch_min_var, pitch_max_var)
ax2.grid()

ax3 = fig.add_subplot(3, 1, 3)
ax3.set_xlim(0, 10)
ax3.set_ylim(yaw_min_var, yaw_max_var)
ax3.grid()

fig.tight_layout(h_pad=3.5)

plot_canvas = FigureCanvasTkAgg(fig, plot_frame)
plot_canvas.get_tk_widget().place(anchor='w', relx=0.025, rely=0.5, relwidth=0.95, relheight=0.85)

toggle_plot_all_button = tk.Button(plot_frame, command=toggle_plot_all, text="Enable All")
toggle_plot_all_button.place(anchor='w', relx=0.285, rely=0.95, relwidth=0.482)

toggle_plot_roll_button = tk.Button(plot_frame, command=toggle_plot_roll, text="Enable Roll")
toggle_plot_roll_button.place(anchor='w', relx=0.45, rely=0.07, relwidth=0.15)

toggle_plot_pitch_button = tk.Button(plot_frame, command=toggle_plot_pitch, text="Enable Pitch")
toggle_plot_pitch_button.place(anchor='w', relx=0.45, rely=0.36, relwidth=0.15)

toggle_plot_yaw_button = tk.Button(plot_frame, command=toggle_plot_yaw, text="Enable Yaw")
toggle_plot_yaw_button.place(anchor='w', relx=0.45, rely=0.65, relwidth=0.15)

### 3D Frame ###
plane3D_frame = tk.LabelFrame(gui, text="3D-Simulation")
plane3D_frame.place(anchor='n', relx=0.382, rely=0.15, relwidth=0.295, relheight=0.40)
frame_3D = tk.LabelFrame(plane3D_frame)
frame_3D.place(anchor='n', relx=0.5, rely=0.05, relwidth=0.8, relheight=0.8)

fig3d = plt.figure(1, figsize=(6, 6))
ax = fig3d.gca(projection='3d')

ax.set_xlabel('Roll')
ax.set_ylabel('Pitch')
ax.set_zlabel('Yaw')

ax.set_xticks([0])
ax.set_yticks([0])
ax.set_zticks([0])
ax.view_init(15, 30)  # initial view (elevation, azimuth)

ax.plot([-lim, lim], [0, 0], [0, 0], 'r')  # x-axis
ax.plot([0, 0], [-lim, lim], [0, 0], 'g')  # y-axis
ax.plot([0, 0], [0, 0], [-lim, lim], 'b')  # z-axis

PLANE = plot_plane(plane)
plt.subplots_adjust(bottom=0.30)

plot_canvas_3D = FigureCanvasTkAgg(fig3d, frame_3D)
plot_canvas_3D.get_tk_widget().place(anchor='n', relx=0.5, rely=-0.38, relwidth=1.2, relheight=2)

toggle_3D_button = tk.Button(plane3D_frame, command=toggle_3D, text="Enable 3D", width=10)
toggle_3D_button.place(anchor='w', relx=0.09, rely=0.92, relwidth=0.82)

ani = animation.FuncAnimation(fig, slider_loop, fargs=(), interval=10)
gui.mainloop()
########### End GUI #############