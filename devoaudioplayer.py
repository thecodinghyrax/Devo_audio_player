import os
import configparser
import time
from tkinter import *
import threading
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from pathlib import Path
from functools import partial
from mutagen.mp3 import MP3


# https://icons8.com/

# Current state
state = {
"file_name" : '', 
'paused' : False,
'playing' : False,
"muted" : False,
"previous_vol" : 50,
"play_list" : [],
'frequency' : 44100
}

# Available themes as counted by each seperate directory in the themes directory
themes_list = []
themes_dir_list = [x[0] for x in os.walk('themes')]
for theme in themes_dir_list:
    if '\\' in theme:
        theme = theme.split(os.sep)
        themes_list.append(theme[1])

# User preferences
def pick_theme(theme):
    config = configparser.ConfigParser()
    config.read('pref.ini')
    config['DEFAULT']['Theme'] = theme
    print("The new theme should be : ", theme)
    with open('pref.ini', 'w') as pref:
        config.write(pref)
    tkinter.messagebox.showwarning("Theme now set", "The new theme is now set. "
                                    "Please close this application and reopen "
                                    "it to apply the new style!")

def set_frequency(rate):
    state['frequency'] = rate
    print("The new frecuency should be : ", rate)
    mixer.quit()
    mixer.pre_init(frequency=state['frequency'])
    mixer.init()  # initilizing the mixer
    

config = configparser.ConfigParser()
config.read('pref.ini')
chosen_theme = config['DEFAULT']['Theme']
chosen_frequency = state['frequency']
file_path = Path.cwd() / 'themes' / chosen_theme


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
    add_to_playlist(state['file_name'])


def add_to_playlist(file):
    file_name = os.path.basename(file)
    song_list_box.insert(0, file_name)
    song_list_box.selection_clear(1)
    song_list_box.selection_set(0)
    state['play_list'].insert(0, file)

def delete_song():
    selected_song = song_list_box.curselection()
    selected_song_index = int(selected_song[0])
    state['play_list'].remove(state['play_list'][selected_song_index])
    song_list_box.delete(selected_song_index)

# Add commands to the subMenu
subMenu.add_command(label="Open", command=fileOpen)
subMenu.add_command(label="Exit", command=root.destroy)

def about():
    tkinter.messagebox.showinfo(
        "Renewed Hope Devotional Archive Player", 
        "This app was made by Drew Crawford in 2018 to provide a way to listed "
        "to the entire devotional archive, right from your computer. You can "
        "contact me at renewedhopeguild@gmail.com with any thoughts or "
        "suggestions.\nVersion : 1.0")


# Create the second subMenu
subMenu2 = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Theme", menu=subMenu2)
for theme in themes_list:
    print("Adding %s to subMenu2" % theme)
    subMenu2.add_command(label=theme, command=partial(pick_theme, theme))


# Create the third subMenu
subMenu3 = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Sample Rate", menu=subMenu3)
subMenu3.add_command(label="22.05 kHz", command=partial(set_frequency, 22050))
subMenu3.add_command(label="44.1 kHz", command=partial(set_frequency, 44100))
subMenu3.add_command(label="48 kHz", command=partial(set_frequency, 48000))
subMenu3.add_command(label="96 kHz", command=partial(set_frequency, 96000))

# Create the fourth subMenu
subMenu4 = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=subMenu4)
subMenu4.add_command(label="About", command=about)

mixer.pre_init(frequency=chosen_frequency)
mixer.init()  # initilizing the mixer

root.title("Renewed Hope Devotional Archive Player")
root.iconbitmap('music.ico')

left_frame = Frame(root)
left_frame.grid(column=0, row=0)

song_list_box = Listbox(left_frame)
song_list_box.grid(columnspan=2, row=0, padx=30)

add_btn = Button(left_frame, text="Add", command=fileOpen)
add_btn.grid(column= 0, row=1)

del_btn = Button(left_frame, text="Delete", command=delete_song)
del_btn.grid(column=1, row=1)

right_frame = Frame(root)
right_frame.grid(column=1, row=0)

top_frame = Frame(right_frame)
top_frame.grid(row=0)

song_length_label = Label(top_frame, text="Total length --:--")
song_length_label.grid(pady=10, row=0)

song_current_time = Label(top_frame, text="Current time --:--")
song_current_time.grid(row=1)


def show_details():
    if state['file_name'].endswith('mp3'):
        mp3_file_info = MP3(state['file_name'])
        total_length = mp3_file_info.info.length
        
    else:
        sound_obj = mixer.Sound(state['file_name'])
        total_length = sound_obj.get_length()
        
    time_format = change_time_format(total_length)
    song_length_label['text'] = "Total length " + time_format
    
    thread_one = threading.Thread(target=partial(start_count, total_length))
    thread_one.start()

def change_time_format(time):
    '''Converts the supplied time in miliseconds to a min:sec format'''
    mins, secs = divmod(time, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    return time_format

def start_count(count):
    current_time = 0
    # get_busy will return False when the music stops playing
    while current_time <= count and mixer.music.get_busy():
        if state['paused']:
            continue
        else:
            if current_time >= (count - 1):
                print("The current_time is == count")
                try:
                    print("Trying to go to the next song")
                    current_time = 0
                    selected_song = song_list_box.curselection()
                    song_list_box.selection_clear(int(selected_song[0]))
                    song_list_box.selection_set(int(selected_song[0]) + 1)
                    print("Just before play, select_song is : ", (int(selected_song[0]) + 1))
                    play_music()
                except:
                    stop_music()

            else:
                time_format = change_time_format(current_time)
                song_current_time['text'] = 'Current time ' + time_format
                time.sleep(1)
                current_time += 1

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
            stop_music()
            time.sleep(1)
            selected_song = song_list_box.curselection()
            selected_song_index = int(selected_song[0])
            mixer.music.load(state['play_list'][selected_song_index])
            state['file_name'] = state['play_list'][selected_song_index]

            if state['file_name'].endswith('mp3'):
                mp3_file_info = MP3(state['file_name'])
                sample_rate = mp3_file_info.info.sample_rate
                if sample_rate == state['frequency']:
                    pass
                else:
                    set_frequency(sample_rate)
                    mixer.music.load(state['play_list'][selected_song_index])
                    
            mixer.music.play()
            statusbar['text'] = "Playing : " + os.path.basename(state['play_list'][selected_song_index])
            state['playing'] = True
            load_middle_buttons(state['playing'])
            show_details()

    except Exception as e:
        tkinter.messagebox.showerror(
            "Error", 
            'No file has been selected to play. Click the "File" button at '
            'the top and select "Open" to select a file to play from your '
            'computer.')
        print(e)


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


middle_frame = Frame(right_frame)
middle_frame.grid(pady=15, row=1)

# Assign all images
playPhoto = PhotoImage(file=(file_path.joinpath('play.png')))
stopPhoto = PhotoImage(file=(file_path.joinpath('stop.png')))
pausePhoto = PhotoImage(file=(file_path.joinpath('pause.png')))
backPhoto = PhotoImage(file=(file_path.joinpath('back.png')))
mutePhoto = PhotoImage(file=(file_path.joinpath('mute.png')))
softPhoto = PhotoImage(file=(file_path.joinpath('soft.png')))
mediumPhoto = PhotoImage(file=(file_path.joinpath('medium.png')))
loudPhoto = PhotoImage(file=(file_path.joinpath('loud.png')))


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

bottom_frame = Frame(right_frame)
bottom_frame.grid(pady=15, row=2)


vol_btn = Button(bottom_frame, image=mediumPhoto, command=mute)
vol_btn.grid(row=0, column=0, padx=30)

scale = Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)
mixer.music.set_volume(.5)
scale.grid(row=0, column=1, pady=10)


statusbar = Label(root, text="Welcome to the Renewed Hope Devotional Archive Player", relief=SUNKEN)
statusbar.grid(columnspan=2, sticky=EW)

def on_closing():
    stop_music()
    root.destroy()



root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
