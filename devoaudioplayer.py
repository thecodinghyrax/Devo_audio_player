import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from pathlib import Path


# https://www.flaticon.com/
# https://icons8.com/

# Current state
state = {
"file_name" : '', 
'paused' : False,
'playing' : False,
"muted" : False,
"previous_vol" : 50,
"theme" : ["default", "dark"] # The theme list represents folders that contain the differently styled elements TODO
}


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
    state['file_name'] = filedialog.askopenfilename()
    play_music()
    print(state['file_name'])


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
    try:
        if state['paused']:
            # mixer.music.unpause()
            state['paused'] = False
            state['playing'] = True
            mixer.music.play()
            load_middle_buttons(state['playing'])
            statusbar['text'] = "Playing : " + os.path.basename(state['file_name'])
        else:
            mixer.music.load(state['file_name'])
            mixer.music.play()
            statusbar['text'] = "Playing : " + os.path.basename(state['file_name'])
            state['playing'] = True
            load_middle_buttons(state['playing'])

    except:
        tkinter.messagebox.showerror(
            "Error", 
            'No file has been selected to play. Click the "File" button at '
            'the top and select "Open" to select a file to play from your '
            'computer.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Stopped"
    state['playing'] = False
    load_middle_buttons(state['playing'])


def pause_music():
    if not state['playing']:
        pass
    elif state['paused']:
        mixer.music.unpause()
        state['paused'] = False
        statusbar['text'] = "Playing : " + os.path.basename(state['file_name'])
    else:
        mixer.music.pause()
        statusbar['text'] = "Paused"
        state['paused'] = True


def set_vol(vol):
    mixer.music.set_volume(int(vol) * .01)
    if not state['muted']:
        state['previous_vol'] = (int(vol) * .01) 

    if mixer.music.get_volume() == 0:
        vol_btn.configure(image=mutePhoto)
    elif  mixer.music.get_volume() <= .33:
        vol_btn.configure(image=softPhoto)
    elif  mixer.music.get_volume() <= .66:
        vol_btn.configure(image=mediumPhoto)
    else:
        vol_btn.configure(image=loudPhoto)
    print("state.previous_vol is being set to : ", state['previous_vol'])
    print("The state['muted'] is now: ", state['muted'])
  
    




# Still flaky when muting. Sorta works now. 
def mute():
    if state['muted']:
        mixer.music.set_volume(state['previous_vol'])
        scale.set((state['previous_vol'] * 100))
        state['muted'] = False
        if state['previous_vol'] <= .33:
            vol_btn.configure(image=softPhoto)
        elif state['previous_vol'] <= .66:
            vol_btn.configure(image=mediumPhoto)
        else:
            vol_btn.configure(image=loudPhoto)
       
            
    else:
        mixer.music.set_volume(0)
        state['muted'] = True
        print("state of previous vol is : ", state['previous_vol'])
        scale.set(0)
        print("state of previous vol after scale.set is : ", state['previous_vol'])
        vol_btn.configure(image=mutePhoto)




middle_frame = Frame(root)
middle_frame.pack(pady=15)

playPhoto = PhotoImage(file='play.png')
stopPhoto = PhotoImage(file='stop.png')
pausePhoto = PhotoImage(file='pause.png')
backPhoto = PhotoImage(file='back.png')
mutePhoto = PhotoImage(file='mute.png')
softPhoto = PhotoImage(file='soft.png')
mediumPhoto = PhotoImage(file="medium.png")
loudPhoto = PhotoImage(file='loud.png')


def load_middle_buttons(playing):
    if playing:
        backBtn = Button(middle_frame, image=backPhoto, command=play_music)
        backBtn.grid(row=0, column=0, padx=18)
    else:
        playBtn = Button(middle_frame, image=playPhoto, command=play_music)
        playBtn.grid(row=0, column=0, padx=18)

    stopBtn = Button(middle_frame, image=stopPhoto, command=stop_music)
    stopBtn.grid(row=0, column=1, padx=18)

    pause_btn =Button(middle_frame, image=pausePhoto, command=pause_music)
    pause_btn.grid(row=0, column=2, padx=18)

load_middle_buttons(state['playing'])

bottom_frame = Frame(root)
bottom_frame.pack(pady=15)


vol_btn = Button(bottom_frame, image=mediumPhoto, command=mute)
vol_btn.grid(row=0, column=0, padx=30)

scale = Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)
mixer.music.set_volume(.5)
scale.grid(row=0, column=1, pady=10)


statusbar = Label(root, text="Welcome to the Renewed Hope Devotional Archive Player", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

root.mainloop()
