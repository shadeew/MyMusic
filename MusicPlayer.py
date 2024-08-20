from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Music Player')
root.iconbitmap(None)
root.geometry("500x400")

#initialize Pygame mixer for sound
pygame.mixer.init()

# getting the song length
def play_time():
    # check for double timing
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000

    # throw up temp label to get data
    # slider_label.config(text=f'Slider: {int(my_slider.get()) }and Song Pos:{int(current_time)}')

    # converted time into time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))



    # grab song title from playlist
    song = song_box.get(ACTIVE)
    song = f'C:/Users/dell/Desktop/python project/chugh/songs/{song}.mp3'
    # get song length from mutagen
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length #it returns timr in second
    # converted time into time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    # to remove the off set time of the slider
    current_time += 1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: { converted_song_length} ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        # updating slider to the position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        # updating slider to the position
        slider_position = int(song_length)

        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')

        #     move this thing along with slider
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)




    # status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')
    # update slider position to current song position
    # my_slider.config( value=current_time)



    # updating time
    status_bar.after(1000,play_time)

# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir='C:/Users/dell/Desktop/python project/chugh/songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    # stripping out the directory info and extention from song name
    song= song.replace("C:/Users/dell/Desktop/python project/chugh/songs/","")
    song = song.replace(".mp3", "")
    # ad song to list box
    song_box.insert(END,song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/KD/gui/audio/', title="Choose A Song",
                                      filetypes=(("mp3 Files", "*.mp3"),))
    # loop throughing the list and replace directory
    for song in songs:
        song = song.replace("C:/Users/dell/Desktop/python project/chugh/songs/", "")
        song = song.replace(".mp3", "")
        # ad song to list box
        song_box.insert(END, song)



# plat selected song
def play():
    # set stopped variable to false so slider moves
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/dell/Desktop/python project/chugh/songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
#     call the play time function to run that all the time
    play_time()

    # #updating slider to the position
    slider_position = int(song_length)
    my_slider.config(to=slider_position,value=0)

global stopped
stopped = False

# stop playing song
def stop():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

#     clear the status bar
    status_bar.config(text='')
    #Set stop variable
    global stopped
    stopped = True
# pause/unpause song
# creatong a global variable for pause
global paused
paused = False
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # pause
        pygame.mixer.music.pause()
        paused = True
def forward():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # getting the correct song tupple number
    next_one = song_box.curselection()
    #     adding one to current song
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'C:/Users/dell/Desktop/python project/chugh/songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0,END)

    #changing  selection bar
    song_box.activate(next_one)
#     set activate bar to next
    song_box.select_set(next_one,last=None)




def back():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    # getting the correct song tupple number
    next_one = song_box.curselection()
    #     adding one to current song
    next_one = next_one[0] - 1
    song = song_box.get(next_one)
    song = f'C:/Users/dell/Desktop/python project/chugh/songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)

    # changing  selection bar
    song_box.activate(next_one)
    #     set activate bar to next
    song_box.select_set(next_one, last=None)



# delete a song from list
def delete_song():
    stop()
    # delete currently selected song
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# delete all songs
def delete_all_songs():
    stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()

# creating a slider function
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of{int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/dell/Desktop/python project/chugh/songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(my_slider.get()))

# create volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    # get current volume
    # current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_volume*100)

#create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# creating playlist box
song_box = Listbox(master_frame,bg="black",fg="yellow",width=60,selectbackground="gray",selectforeground="black")
song_box.grid(row=0,column=0)

# create player control button images
back_btn_img = PhotoImage(file="C:/Users/dell/Desktop/python project/chugh/icon/Rewind.png")
forward_btn_img = PhotoImage(file='C:/Users/dell/Desktop/python project/chugh/icon/Fast Forward.png')
play_btn_img = PhotoImage(file='C:/Users/dell/Desktop/python project/chugh/icon/Play.png')
pause_btn_img = PhotoImage(file='C:/Users/dell/Desktop/python project/chugh/icon/Pause.png')
stop_btn_img = PhotoImage(file='C:/Users/dell/Desktop/python project/chugh/icon/Stop.png')

# create player Control Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1,column=0,pady=20)

# create volume label frame
volume_frame = LabelFrame(master_frame,text='Volume')
volume_frame.grid(row=0,column=1,padx=20)

#player control buttons
back_btn = Button(controls_frame,image=back_btn_img,borderwidth=0,command=back)
forward_btn = Button(controls_frame,image=forward_btn_img,borderwidth=0,command =forward)
play_btn = Button(controls_frame,image=play_btn_img,borderwidth=0,command=play)
pause_btn = Button(controls_frame,image=pause_btn_img,borderwidth=0,command=lambda :pause(paused))
stop_btn = Button(controls_frame,image=stop_btn_img,borderwidth=0,command=stop)

back_btn.grid(row=0,column=0,padx=10)
forward_btn.grid(row=0,column=1,padx=10)
play_btn.grid(row=0,column=2,padx=10)
pause_btn.grid(row=0,column=3,padx=10)
stop_btn.grid(row=0,column=4,padx=10)

#create menu
my_menu = Menu(root)
root.config(menu = my_menu)

# add Add song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist",command=add_song)
# Add many songs to list
add_song_menu.add_command(label="Add Many Song To Playlist",command=add_many_songs)

# Create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist",command=delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist",command=delete_all_songs)

# creating a status bar
status_bar = Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

# creating a slider
my_slider = ttk.Scale(master_frame,from_=0,to=200,orient=HORIZONTAL,value=0,command = slide,length=360)
my_slider.grid(row=2,column=0,pady=10)

# create volume slider
volume_slider = ttk.Scale(volume_frame,from_=0,to=1,orient=VERTICAL,value=1,command = volume,length=125)
volume_slider.pack(pady=15)


# Crrate Temporary slider label
# slider_label = Label(root,text="0")
# slider_label.pack(pady=10)

root.mainloop()


