import os
import random
import customtkinter as ctk
import pygame
from tkinter import filedialog, messagebox
from mutagen.id3 import ID3

# Set initial appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ModernMusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Music Player")
        self.geometry("800x500")
        self.resizable(False, False)
        
        # Internal state
        self.songs = []          # List of song file names (relative paths)
        self.song_names = []     # List of displayed song titles
        self.current_index = 0
        self.paused = False
        self.current_appearance_mode = "Dark"  # Track current appearance mode
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Build UI components
        self.create_widgets()

    def create_widgets(self):
        # Left Panel: Song List and Open File Button
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        self.song_listbox = ctk.CTkTextbox(self.left_frame, width=280, height=400, corner_radius=10)
        self.song_listbox.configure(state="disabled")
        self.song_listbox.pack(padx=10, pady=10)
        
        self.open_button = ctk.CTkButton(self.left_frame, text="Open MP3 File", command=self.open_file)
        self.open_button.pack(pady=10)
        
        # Right Panel: Song Info, Appearance Toggle, and Controls
        self.right_frame = ctk.CTkFrame(self, width=480)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Appearance Mode Toggle Switch
        self.appearance_switch = ctk.CTkSwitch(
            self.right_frame,
            text=f"{self.current_appearance_mode} Mode",
            command=self.toggle_appearance
        )
        self.appearance_switch.pack(pady=10)
        
        # Song Title Label
        self.song_label = ctk.CTkLabel(self.right_frame, text="No Song Loaded", font=("Roboto", 20))
        self.song_label.pack(pady=20)
        
        # Control Buttons Frame
        self.controls_frame = ctk.CTkFrame(self.right_frame)
        self.controls_frame.pack(pady=10)
        
        # Create control buttons
        self.prev_button = ctk.CTkButton(self.controls_frame, text="Prev", command=self.previous_song, width=80)
        self.play_button = ctk.CTkButton(self.controls_frame, text="Play", command=self.play_song, width=80)
        self.pause_button = ctk.CTkButton(self.controls_frame, text="Pause/Resume", command=self.pause_song, width=100)
        self.next_button = ctk.CTkButton(self.controls_frame, text="Next", command=self.next_song, width=80)
        self.shuffle_button = ctk.CTkButton(self.controls_frame, text="Shuffle", command=self.shuffle_songs, width=80)
        self.stop_button = ctk.CTkButton(self.controls_frame, text="Stop", command=self.stop_song, width=80)
        
        self.prev_button.grid(row=0, column=0, padx=5, pady=5)
        self.play_button.grid(row=0, column=1, padx=5, pady=5)
        self.pause_button.grid(row=0, column=2, padx=5, pady=5)
        self.next_button.grid(row=0, column=3, padx=5, pady=5)
        self.shuffle_button.grid(row=0, column=4, padx=5, pady=5)
        self.stop_button.grid(row=0, column=5, padx=5, pady=5)
        
        # Volume Control
        self.volume_label = ctk.CTkLabel(self.right_frame, text="Volume")
        self.volume_label.pack(pady=(20, 5))
        self.volume_slider = ctk.CTkSlider(self.right_frame, from_=0, to=1, number_of_steps=100, command=self.change_volume)
        self.volume_slider.set(1)
        self.volume_slider.pack(padx=20)
        
    def toggle_appearance(self):
        # Toggle between Dark and Light modes
        if self.current_appearance_mode == "Dark":
            self.current_appearance_mode = "Light"
        else:
            self.current_appearance_mode = "Dark"
        ctk.set_appearance_mode(self.current_appearance_mode)
        self.appearance_switch.configure(text=f"{self.current_appearance_mode} Mode")
    
    def update_song_label(self):
        if self.song_names:
            self.song_label.configure(text=self.song_names[self.current_index])
        else:
            self.song_label.configure(text="No Song Loaded")
    
    def update_song_listbox(self):
        self.song_listbox.configure(state="normal")
        self.song_listbox.delete("1.0", "end")
        for name in self.song_names:
            self.song_listbox.insert("end", name + "\n")
        self.song_listbox.configure(state="disabled")
        
    def change_volume(self, value):
        try:
            pygame.mixer.music.set_volume(float(value))
        except Exception as e:
            print("Error setting volume:", e)
    
    def play_song(self):
        if not self.songs:
            return
        try:
            pygame.mixer.music.load(self.songs[self.current_index])
            pygame.mixer.music.play()
            self.paused = False
            self.update_song_label()
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play the song: {e}")
    
    def pause_song(self):
        if not self.songs:
            return
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.paused = not self.paused
        
    def stop_song(self):
        pygame.mixer.music.stop()
    
    def next_song(self):
        if not self.songs:
            return
        self.current_index = (self.current_index + 1) % len(self.songs)
        self.play_song()
    
    def previous_song(self):
        if not self.songs:
            return
        self.current_index = (self.current_index - 1) % len(self.songs)
        self.play_song()
    
    def shuffle_songs(self):
        if not self.songs:
            return
        combined = list(zip(self.songs, self.song_names))
        random.shuffle(combined)
        self.songs, self.song_names = zip(*combined)
        self.songs = list(self.songs)
        self.song_names = list(self.song_names)
        self.current_index = 0
        self.update_song_listbox()
        self.play_song()
    
    def open_file(self):
        # Ask for one MP3 file
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Audio Files", "*.mp3")])
        if not file_path:
            return
        
        directory = os.path.dirname(file_path)
        try:
            os.chdir(directory)
        except Exception as e:
            messagebox.showerror("Directory Error", f"Error changing directory: {e}")
            return
        
        # Gather all MP3 files from the directory
        self.songs.clear()
        self.song_names.clear()
        mp3_files = [f for f in os.listdir(directory) if f.lower().endswith('.mp3')]
        selected_file = os.path.basename(file_path)
        
        for file in mp3_files:
            full_path = os.path.realpath(file)
            try:
                audio = ID3(full_path)
                title = audio['TIT2'].text[0]
            except Exception:
                title = file
            self.song_names.append(title)
            self.songs.append(file)
        
        if not self.songs:
            if messagebox.askretrycancel("No Songs Found", "No songs found in this directory."):
                self.open_file()
            return
        
        # Set current index to the selected file
        try:
            self.current_index = self.songs.index(selected_file)
        except ValueError:
            self.current_index = 0
        
        self.update_song_listbox()
        self.play_song()

if __name__ == "__main__":
    app = ModernMusicPlayer()
    app.mainloop()
