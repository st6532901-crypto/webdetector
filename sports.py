import tkinter as tk
from tkinter import messagebox, filedialog
import cv2  # Placeholder for video recording/analyzing (install with `pip install opencv-python`)
import os

class SportsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Performance App")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Red and black theme
        self.bg_color = "black"
        self.fg_color = "red"
        self.button_bg = "red"
        self.button_fg = "black"

        # Create main container
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill="both", expand=True)

        # Navigation bar
        self.nav_frame = tk.Frame(self.main_frame, bg="#333333")
        self.nav_frame.pack(fill="x")
        nav_buttons = [
            ("Sign In/Register", self.show_signin),
            ("Profile", self.show_profile),
            ("Record Video", self.show_record),
            ("Analyze Video", self.show_analyze),
            ("Post Video", self.show_post),
            ("Leaderboard", self.show_leaderboard)
        ]
        for text, command in nav_buttons:
            btn = tk.Button(self.nav_frame, text=text, bg=self.button_bg, fg=self.button_fg,
                            font=("Arial", 12, "bold"), command=command)
            btn.pack(side="left", padx=10, pady=5)

        # Content frames (hidden initially)
        self.frames = {}
        self.create_signin_frame()
        self.create_profile_frame()
        self.create_record_frame()
        self.create_analyze_frame()
        self.create_post_frame()
        self.create_leaderboard_frame()

        # Show sign-in frame by default
        self.show_signin()

    def clear_frame(self):
        for frame in self.frames.values():
            frame.pack_forget()

    def create_signin_frame(self):
        frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.frames["signin"] = frame

        tk.Label(frame, text="Sign In or Register", bg=self.bg_color, fg=self.fg_color,
                 font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(frame, text="Email", bg=self.bg_color, fg=self.fg_color).pack()
        self.email_entry = tk.Entry(frame, bg="#333333", fg=self.fg_color, insertbackground=self.fg_color)
        self.email_entry.pack(pady=5)

        tk.Label(frame, text="Password", bg=self.bg_color, fg=self.fg_color).pack()
        self.password_entry = tk.Entry(frame, show="*", bg="#333333", fg=self.fg_color, insertbackground=self.fg_color)
        self.password_entry.pack(pady=5)

        tk.Button(frame, text="Sign In", bg=self.button_bg, fg=self.button_fg,
                  command=lambda: self.handle_auth("signin")).pack(pady=5)
        tk.Button(frame, text="Register", bg=self.button_bg, fg=self.button_fg,
                  command=lambda: self.handle_auth("register")).pack(pady=5)

        self.auth_message = tk.Label(frame, text="", bg=self.bg_color, fg=self.fg_color)
        self.auth_message.pack(pady=10)

    def create_profile_frame(self):
        frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.frames["profile"] = frame

        tk.Label(frame, text="Player Profile", bg=self.bg_color, fg=self.fg_color,
                 font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(frame, text="Name", bg=self.bg_color, fg=self.fg_color).pack()
        self.name_entry = tk.Entry(frame, bg="#333333", fg=self.fg_color, insertbackground=self.fg_color)
        self.name_entry.insert(0, "John Doe")
        self.name_entry.pack(pady=5)

        tk.Label(frame, text="Sport", bg=self.bg_color, fg=self.fg_color).pack()
        self.sport_entry = tk.Entry(frame, bg="#333333", fg=self.fg_color, insertbackground=self.fg_color)
        self.sport_entry.insert(0, "Basketball")
        self.sport_entry.pack(pady=5)

        tk.Label(frame, text="Age", bg=self.bg_color, fg=self.fg_color).pack()
        self.age_entry = tk.Entry(frame, bg="#333333", fg=self.fg_color, insertbackground=self.fg_color)
        self.age_entry.insert(0, "25")
        self.age_entry.pack(pady=5)

        tk.Label(frame, text="Bio", bg=self.bg_color, fg=self.fg_color).pack()
        self.bio_text = tk.Text(frame, height=5, width=30, bg="#333333", fg=self.fg_color, insertbackground=self.fg_color)
        self.bio_text.insert("1.0", "Professional athlete...")
        self.bio_text.pack(pady=5)

        tk.Button(frame, text="Update Profile", bg=self.button_bg, fg=self.button_fg,
                  command=self.update_profile).pack(pady=10)

        self.profile_message = tk.Label(frame, text="", bg=self.bg_color, fg=self.fg_color)
        self.profile_message.pack(pady=10)

    def create_record_frame(self):
        frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.frames["record"] = frame

        tk.Label(frame, text="Record Video", bg=self.bg_color, fg=self.fg_color,
                 font=("Arial", 16, "bold")).pack(pady=20)

        self.video_label = tk.Label(frame, text="Video Preview (Webcam)", bg="#333333", fg=self.fg_color, width=40, height=15)
        self.video_label.pack(pady=10)

        self.start_record_btn = tk.Button(frame, text="Start Recording", bg=self.button_bg, fg=self.button_fg,
                                          command=self.start_recording)
        self.start_record_btn.pack(pady=5)

        self.stop_record_btn = tk.Button(frame, text="Stop Recording", bg=self.button_bg, fg=self.button_fg,
                                         command=self.stop_recording, state="disabled")
        self.stop_record_btn.pack(pady=5)

        self.download_btn = tk.Button(frame, text="Download Video", bg=self.button_bg, fg=self.button_fg,
                                      command=self.download_video, state="disabled")
        self.download_btn.pack(pady=5)

        self.record_message = tk.Label(frame, text="", bg=self.bg_color, fg=self.fg_color)
        self.record_message.pack(pady=10)

    def create_analyze_frame(self):
        frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.frames["analyze"] = frame

        tk.Label(frame, text="Analyze Video", bg=self.bg_color, fg=self.fg_color,
                 font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(frame, text="Upload Video", bg=self.button_bg, fg=self.button_fg,
                  command=self.upload_video).pack(pady=10)

        self.analyze_btn = tk.Button(frame, text="Analyze", bg=self.button_bg, fg=self.button_fg,
                                     command=self.analyze_video, state="disabled")
        self.analyze_btn.pack(pady=5)

        self.analysis_result = tk.Label(frame, text="Analysis Result: None", bg=self.bg_color, fg=self.fg_color)
        self.analysis_result.pack(pady=10)

    def create_post_frame(self):
        frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.frames["post"] = frame

        tk.Label(frame, text="Post Video", bg=self.bg_color, fg=self.fg_color,
                 font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(frame, text="Upload Video", bg=self.button_bg, fg=self.button_fg,
                  command=self.upload_post_video).pack(pady=10)

        tk.Label(frame, text="Caption", bg=self.bg_color, fg=self.fg_color).pack()
        self.caption_text = tk.Text(frame, height=5, width=30, bg="#333333", fg=self.fg_color, insertbackground=self.fg_color)
        self.caption_text.pack(pady=5)

        tk.Button(frame, text="Post", bg=self.button_bg, fg=self.button_fg,
                  command=self.post_video).pack(pady=10)

        self.post_message = tk.Label(frame, text="", bg=self.bg_color, fg=self.fg_color)
        self.post_message.pack(pady=10)

    def create_leaderboard_frame(self):
        frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.frames["leaderboard"] = frame

        tk.Label(frame, text="Player Performance Leaderboard", bg=self.bg_color, fg=self.fg_color,
                 font=("Arial", 16, "bold")).pack(pady=20)

        # Simple leaderboard table using labels
        leaderboard_data = [
            ("1", "John Doe", "95", "Basketball"),
            ("2", "Jane Smith", "90", "Soccer")
        ]
        headers = ["Rank", "Player", "Score", "Sport"]
        for col, header in enumerate(headers):
            tk.Label(frame, text=header, bg="red", fg="black", font=("Arial", 12, "bold"),
                     width=15, relief="solid", borderwidth=1).grid(row=0, column=col, padx=1, pady=1)
        for row, data in enumerate(leaderboard_data, 1):
            for col, value in enumerate(data):
                tk.Label(frame, text=value, bg=self.bg_color, fg=self.fg_color,
                         width=15, relief="solid", borderwidth=1).grid(row=row, column=col, padx=1, pady=1)

    def show_signin(self):
        self.clear_frame()
        self.frames["signin"].pack(fill="both", expand=True)

    def show_profile(self):
        self.clear_frame()
        self.frames["profile"].pack(fill="both", expand=True)

    def show_record(self):
        self.clear_frame()
        self.frames["record"].pack(fill="both", expand=True)

    def show_analyze(self):
        self.clear_frame()
        self.frames["analyze"].pack(fill="both", expand=True)

    def show_post(self):
        self.clear_frame()
        self.frames["post"].pack(fill="both", expand=True)

    def show_leaderboard(self):
        self.clear_frame()
        self.frames["leaderboard"].pack(fill="both", expand=True)

    def handle_auth(self, auth_type):
        # Placeholder for authentication logic (connect to backend in production)
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            self.auth_message.config(text=f"{auth_type.capitalize()} successful!")
        else:
            self.auth_message.config(text="Please enter email and password")

    def update_profile(self):
        # Placeholder for profile update (connect to backend in production)
        self.profile_message.config(text="Profile updated!")

    def start_recording(self):
        # Placeholder for video recording with OpenCV
        self.record_message.config(text="Recording started (Webcam simulation)")
        self.start_record_btn.config(state="disabled")
        self.stop_record_btn.config(state="normal")
        # Example OpenCV code (uncomment and install opencv-python to use):
        """
        self.cap = cv2.VideoCapture(0)  # Open webcam
        self.out = cv2.VideoWriter('recorded_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
        def update_frame():
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)
                self.root.after(50, update_frame)
        update_frame()
        """

    def stop_recording(self):
        # Placeholder for stopping video recording
        self.record_message.config(text="Recording stopped")
        self.stop_record_btn.config(state="disabled")
        self.download_btn.config(state="normal")
        # Example OpenCV code (uncomment to use):
        """
        self.cap.release()
        self.out.release()
        """

    def download_video(self):
        # Placeholder for downloading video
        messagebox.showinfo("Download", "Video downloaded as recorded_video.avi")
        self.download_btn.config(state="disabled")
        self.start_record_btn.config(state="normal")

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])
        if file_path:
            self.analyze_btn.config(state="normal")
            self.analysis_result.config(text=f"Selected video: {os.path.basename(file_path)}")

    def analyze_video(self):
        # Placeholder for video analysis (integrate with ML model or backend)
        self.analysis_result.config(text="Analysis: Speed - 20 mph, Accuracy - 85%")
        self.analyze_btn.config(state="disabled")

    def upload_post_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])
        if file_path:
            self.post_message.config(text=f"Selected video: {os.path.basename(file_path)}")

    def post_video(self):
        # Placeholder for posting video (connect to backend in production)
        caption = self.caption_text.get("1.0", "end-1c")
        if caption.strip():
            self.post_message.config(text="Video posted successfully!")
        else:
            self.post_message.config(text="Please add a caption")

if __name__ == "__main__":
    root = tk.Tk()
    app = SportsApp(root)
    root.mainloop()