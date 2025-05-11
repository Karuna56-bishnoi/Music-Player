import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

# Initialize an empty playlist
playlist = []


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.pack()
        pygame.init()
        
        pygame.mixer.init()
        self.current_song_index = -1  # Keep track of the current song index
        self.current_volume = 0.5  # Default volume (50%)
        self.is_playing = False  # Track whether music is playing
        pygame.mixer.music.set_volume(self.current_volume)

    def create_widgets(self):
        # Playlist Listbox
        self.playlistbox = tk.Listbox(self, width=60, height=15, selectmode=tk.SINGLE)
        self.playlistbox.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Buttons Row 1
        

        self.previousButton = tk.Button(self, text="Previous", width=12, command=self.previous_song)
        self.previousButton.grid(row=1, column=1, padx=5, pady=5)
        
        self.playButton = tk.Button(self, text="▶", width=12, command=self.play_pause)
        self.playButton.grid(row=1, column=0, padx=5, pady=5)


        self.nextButton = tk.Button(self, text="Next", width=12, command=self.next_song)
        self.nextButton.grid(row=1, column=2, padx=5, pady=5)

        self.volumeUpButton = tk.Button(self, text="Volume Up", width=12, command=self.volume_up)
        self.volumeUpButton.grid(row=1, column=3, padx=5, pady=5)

        self.volumeDownButton = tk.Button(self, text="Volume Down", width=12, command=self.volume_down)
        self.volumeDownButton.grid(row=1, column=4, padx=5, pady=5)

        # Buttons Row 2
        self.loopButton = tk.Button(self, text="Loop", width=12, command=self.loop)
        self.loopButton.grid(row=2, column=0, padx=5, pady=5)

        self.addButton = tk.Button(self, text="Add", width=12, command=self.add)
        self.addButton.grid(row=2, column=1, padx=5, pady=5)

        self.saveButton = tk.Button(self, text="Save Playlist", width=12, command=self.save_playlist)
        self.saveButton.grid(row=2, column=2, padx=5, pady=5)

        self.loadButton = tk.Button(self, text="Load Playlist", width=12, command=self.load_playlist)
        self.loadButton.grid(row=2, column=3, padx=5, pady=5)

        self.quitButton = tk.Button(self, text="Quit", width=12, command=self.master.quit)
        self.quitButton.grid(row=2, column=4, padx=5, pady=5)

    def play_pause(self):
        """Toggle between Play and Pause."""
        if not self.is_playing:  # If music is not playing, start or resume playing
            if len(playlist) == 0:
                messagebox.showinfo("Notice", "No songs in your playlist!\nClick 'Add' to add songs.")
                return

            if self.current_song_index == -1:  # If no song has been played yet
                selected_songs = self.playlistbox.curselection()
                if not selected_songs:
                    messagebox.showinfo("Notice", "Please select a song to play.")
                    return
                self.current_song_index = selected_songs[0]
                self.play_song(self.current_song_index)  # Play the song for the first time
            else:
                pygame.mixer.music.unpause()  # Resume playback
            self.playButton.config(text="||")
            self.is_playing = True
        else:  # If music is playing, pause it
            pygame.mixer.music.pause()
            self.playButton.config(text="▶")
            self.is_playing = False

    def play_song(self, index):
        """Play the song at the specified index."""
        pygame.mixer.music.stop()
        play_it = playlist[index]
        pygame.mixer.music.load(play_it)
        pygame.mixer.music.play(0, 0.0)
        self.playlistbox.select_clear(0, tk.END)  # Clear previous selection
        self.playlistbox.select_set(index)  # Highlight the current song
        self.is_playing = True
        self.playButton.config(text="||")

    def loop(self):
        """Loop the currently playing song."""
        if len(playlist) == 0:
            messagebox.showinfo("Notice", "No songs to loop!\nClick 'Add' to add songs.")
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1, 0.0)

    def add(self):
        """Add songs to the playlist."""
        files = filedialog.askopenfilenames(title="Select Songs",
                                            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if not files:
            return

        for file in files:
            playlist.append(file)
            song_short = file.split("/")[-1]  # Extract the file name
            self.playlistbox.insert(tk.END, song_short)

    def save_playlist(self):
        """Save the playlist to a file."""
        if not playlist:
            messagebox.showinfo("Notice", "No songs in the playlist to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")],
                                                 title="Save Playlist")
        if file_path:
            with open(file_path, "w") as f:
                for song in playlist:
                    f.write(song + "\n")
            messagebox.showinfo("Success", f"Playlist saved to {file_path}")

    def load_playlist(self):
        """Load a playlist from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")],
                                               title="Load Playlist")
        if file_path:
            with open(file_path, "r") as f:
                songs = f.readlines()

            # Clear the current playlist and listbox
            playlist.clear()
            self.playlistbox.delete(0, tk.END)

            # Add loaded songs to the playlist
            for song in songs:
                song = song.strip()  # Remove newline characters
                playlist.append(song)
                song_short = song.split("/")[-1]  # Extract the file name
                self.playlistbox.insert(tk.END, song_short)
            messagebox.showinfo("Success", f"Playlist loaded from {file_path}")

    def previous_song(self):
        """Play the previous song in the playlist."""
        if len(playlist) == 0:
            messagebox.showinfo("Notice", "No songs in your playlist!\nClick 'Add' to add songs.")
            return

        if self.current_song_index <= 0:
            messagebox.showinfo("Notice", "This is the first song in the playlist.")
            return

        self.current_song_index -= 1
        self.play_song(self.current_song_index)

    def next_song(self):
        """Play the next song in the playlist."""
        if len(playlist) == 0:
            messagebox.showinfo("Notice", "No songs in your playlist!\nClick 'Add' to add songs.")
            return

        if self.current_song_index >= len(playlist) - 1:
            messagebox.showinfo("Notice", "This is the last song in the playlist.")
            return

        self.current_song_index += 1
        self.play_song(self.current_song_index)

    def volume_up(self):
        """Increase the volume."""
        if self.current_volume < 1.0:
            self.current_volume += 0.1
            self.current_volume = round(self.current_volume, 1)  # Limit to 1 decimal
            pygame.mixer.music.set_volume(self.current_volume)
            print(f"Volume increased to: {self.current_volume * 100}%")

    def volume_down(self):
        """Decrease the volume."""
        if self.current_volume > 0.0:
            self.current_volume -= 0.1
            self.current_volume = round(self.current_volume, 1)  # Limit to 1 decimal
            pygame.mixer.music.set_volume(self.current_volume)
            print(f"Volume decreased to: {self.current_volume * 100}%")


# Main Execution
root = tk.Tk()
root.title("Python Music Player")
root.geometry("700x400")  # Adjusted size to fit new layout
app = Application(root)
root.mainloop()
