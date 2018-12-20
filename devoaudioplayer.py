from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer

# https://www.flaticon.com/

# Globals
file_name = ""
paused = False


root = Tk()

menuBar = Menu(root)

# root.config() is adding a configuration option to the root widget.
root.config(menu=menuBar)

# create the first sub menu
# tearoff=0 removes a dash line that shows up in the subMenu 
# (Used for poping out the subMenu I think)
subMenu = Menu(menuBar, tearoff=0)
# Add the submenu to the menuBar
menuBar.add_cascade(label="File", menu=subMenu)


def fileOpen():
    global file_name
    file_name = filedialog.askopenfilename()
    print(file_name)


# Add commands to the subMenu
subMenu.add_command(label="Open", command=fileOpen)
subMenu.add_command(label="Exit", command=root.destroy)


def about():
    tkinter.messagebox.showinfo(
        "Renewed Hope Devotional Archive Player", 
        "This app was made by Drew Crawford in 2018 to provide a way to listed "
        "to the entire devotional archive, right from your computer. You can "
        "contact me at renewedhopeguild@gmail.com with any thoughts or "
        "suggestions.")


# Create the second subMenu
subMenu2 = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=subMenu2)
subMenu2.add_command(label="About", command=about)

mixer.init()  # initilizing the mixer

root.title("Renewed Hope Devotional Archive Player")
root.iconbitmap('music.ico')


text = Label(root, text="Let's make some noise!")
text.pack(pady=10)


def play_music():
    global paused
    try:
        if paused:
            mixer.music.unpause()
            paused = False
            file_name_path = file_name.split('/')
            statusbar['text'] = "Playing : " + file_name_path[-1]
        else:
            mixer.music.load(file_name)
            mixer.music.play()
            file_name_path = file_name.split('/')
            statusbar['text'] = "Playing : " + file_name_path[-1]
    except:
        tkinter.messagebox.showerror(
            "Error", 
            'No file has been selected to play. Click the "File" button at '
            'the top and select "Open" to select a file to play from your '
            'computer.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Stopped"


def pause_music():
    global paused
    if paused:
        mixer.music.unpause()
        paused = False
        file_name_path = file_name.split('/')
        statusbar['text'] = "Playing : " + file_name_path[-1]
    else:
        mixer.music.pause()
        statusbar['text'] = "Paused"
        paused = True


def set_vol(vol):
    mixer.music.set_volume(int(vol) * .01)

middle_frame = Frame(root)
middle_frame.pack()

playPhoto = PhotoImage(file='play.png')
stopPhoto = PhotoImage(file='stop.png')
pausePhoto = PhotoImage(file='pause.png')
reloadPhoto = PhotoImage(file="reload.png")


playBtn = Button(middle_frame, image=playPhoto, command=play_music)
playBtn.pack(side=LEFT, padx=10)

stopBtn = Button(middle_frame, image=stopPhoto, command=stop_music)
stopBtn.pack(side=LEFT, padx=10)

pause_btn =Button(middle_frame, image=pausePhoto, command=pause_music)
pause_btn.pack(side=LEFT, padx=10)

scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)
mixer.music.set_volume(.5)
scale.pack(pady=10)

statusbar = Label(root, text="Welcome to the Renewed Hope Devotional Archive Player", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

root.mainloop()
