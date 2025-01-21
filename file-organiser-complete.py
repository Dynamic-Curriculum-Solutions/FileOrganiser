import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import shutil
import logging
from datetime import datetime
import sys
from pathlib import Path

class DisclaimerDialog:
    def __init__(self, parent):
        self.accepted = False
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Terms of Use - Dynamic Curriculum Solutions")
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # Add disclaimer text
        disclaimer_frame = ttk.Frame(self.dialog, padding="20")
        disclaimer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Company name header
        company_label = ttk.Label(
            disclaimer_frame, 
            text="Dynamic Curriculum Solutions",
            font=('Helvetica', 14, 'bold')
        )
        company_label.pack(pady=(0, 20))
        
        # Disclaimer text
        disclaimer_text = tk.Text(disclaimer_frame, wrap=tk.WORD, height=12, width=60)
        disclaimer_text.pack(pady=(0, 20))
        disclaimer_text.insert(tk.END, """
DISCLAIMER AND LIMITED LIABILITY

By using this software, you acknowledge and agree that:

1. This software is provided "AS IS" without warranty of any kind, either express or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose.

2. Dynamic Curriculum Solutions shall not be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services, loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software.

3. You assume all responsibility for file selection, backup, security, and data integrity. It is strongly recommended to maintain backups of all files before using this software.

4. This software may modify, move, or reorganize files based on your instructions. You accept full responsibility for the results of using this software.
        """)
        disclaimer_text.configure(state='disabled')
        
        # Buttons
        button_frame = ttk.Frame(disclaimer_frame)
        button_frame.pack(pady=(0, 10))
        
        accept_button = ttk.Button(button_frame, text="Accept", command=self.on_accept)
        accept_button.pack(side=tk.LEFT, padx=5)
        
        decline_button = ttk.Button(button_frame, text="Decline", command=self.on_cancel)
        decline_button.pack(side=tk.LEFT, padx=5)
        
        # Center the dialog on screen
        self.dialog.update_idletasks()
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - self.dialog.winfo_width()) // 2
        y = (screen_height - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")

    def on_accept(self):
        self.accepted = True
        self.dialog.destroy()

    def on_cancel(self):
        self.accepted = False
        self.dialog.destroy()

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Curriculum Solutions - File Organizer")
        self.root.geometry("800x600")
        
        # Show disclaimer first
        disclaimer = DisclaimerDialog(root)
        root.wait_window(disclaimer.dialog)
        if not disclaimer.accepted:
            root.quit()
            return
        
        # Add company branding
        branding_frame = ttk.Frame(root)
        branding_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        company_label = ttk.Label(
            branding_frame, 
            text="Dynamic Curriculum Solutions",
            font=('Helvetica', 14, 'bold')
        )
        company_label.pack()
        
        subtitle_label = ttk.Label(
            branding_frame,
            text="File Organization Tool",
            font=('Helvetica', 10)
        )
        subtitle_label.pack()

        # Configure logging
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"file_organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Source folder selection
        ttk.Label(self.main_frame, text="Source Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.source_var, width=60).grid(row=0, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_source).grid(row=0, column=2)

        # Destination folder selection
        ttk.Label(self.main_frame, text="Destination Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dest_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.dest_var, width=60).grid(row=1, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_dest).grid(row=1, column=2)

        # File pattern entry
        ttk.Label(self.main_frame, text="File Pattern:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pattern_var = tk.StringVar(value="*.*")
        ttk.Entry(self.main_frame, textvariable=self.pattern_var).grid(row=2, column=1, sticky=tk.W, padx=5)

        # Delimiter entry
        ttk.Label(self.main_frame, text="Filename Delimiter:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.delimiter_var = tk.StringVar(value="_")
        ttk.Entry(self.main_frame, textvariable=self.delimiter_var).grid(row=3, column=1, sticky=tk.W, padx=5)

        # Conflict handling options
        ttk.Label(self.main_frame, text="File Conflict Handling:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.conflict_var = tk.StringVar(value="ask")
        conflict_frame = ttk.Frame(self.main_frame)
        conflict_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(conflict_frame, text="Ask", value="ask", variable=self.conflict_var).pack(side=tk.LEFT)
        ttk.Radiobutton(conflict_frame, text="Skip", value="skip", variable=self.conflict_var).pack(side=tk.LEFT)
        ttk.Radiobutton(conflict_frame, text="Rename", value="rename", variable=self.conflict_var).pack(side=tk.LEFT)
        ttk.Radiobutton(conflict_frame, text="Overwrite", value="overwrite", variable=self.conflict_var).pack(side=tk.LEFT)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.main_frame, length=300, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

        # Status text
        self.status_text = tk.Text(self.main_frame, height=15, width=70, wrap=tk.WORD)
        self.status_text.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=6, column=3, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)

        # Start button
        ttk.Button(self.main_frame, text="Start Organization", command=self.organize_files).grid(row=7, column=0, columnspan=3, pady=10)

    def browse_source(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_var.set(folder)

    def browse_dest(self):
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_var.set(folder)

    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

    def handle_file_conflict(self, dest_file):
        conflict_action = self.conflict_var.get()
        
        if conflict_action == "ask":
            response = messagebox.askyesnocancel(
                "File Exists",
                f"File already exists:\n{dest_file}\n\nYes = Overwrite\nNo = Skip\nCancel = Rename",
                icon="warning"
            )
            if response is None:  # Cancel/Rename
                return "rename"
            elif response:  # Yes/Overwrite
                return "overwrite"
            else:  # No/Skip
                return "skip"
        
        return conflict_action

    def get_unique_filename(self, dest_file):
        counter = 1
        base_path = Path(dest_file)
        while Path(dest_file).exists():
            dest_file = str(base_path.parent / f"{base_path.stem}_{counter}{base_path.suffix}")
            counter += 1
        return dest_file

    def organize_files(self):
        source = self.source_var.get()
        destination = self.dest_var.get()
        pattern = self.pattern_var.get()
        delimiter = self.delimiter_var.get()

        if not source or not destination:
            self.update_status("Please select both source and destination folders.")
            return

        try:
            # Clear status text
            self.status_text.delete(1.0, tk.END)
            self.update_status("Starting file organization...")
            
            # Get list of files
            files = list(Path(source).rglob(pattern))
            total_files = len(files)
            
            if total_files == 0:
                self.update_status("No files found matching the pattern.")
                return

            # Reset progress bar
            self.progress_var.set(0)
            
            for index, file in enumerate(files):
                try:
                    # Create folder structure based on filename
                    file_parts = file.stem.split(delimiter)
                    relative_path = os.path.join(*file_parts[:-1]) if len(file_parts) > 1 else ""
                    dest_folder = os.path.join(destination, relative_path)
                    
                    # Create destination folder if it doesn't exist
                    os.makedirs(dest_folder, exist_ok=True)
                    
                    # Construct destination file path
                    dest_file = os.path.join(dest_folder, file.name)
                    
                    # Handle existing files
                    if os.path.exists(dest_file):
                        action = self.handle_file_conflict(dest_file)
                        
                        if action == "skip":
                            self.update_status(f"Skipped: {file.name} (already exists)")
                            continue
                        elif action == "rename":
                            dest_file = self.get_unique_filename(dest_file)
                    
                    # Copy file
                    shutil.copy2(file, dest_file)
                    
                    # Update status and progress
                    self.update_status(f"Copied: {file.name} -> {dest_file}")
                    self.progress_var.set((index + 1) / total_files * 100)
                    
                    # Log success
                    logging.info(f"Successfully copied {file} to {dest_file}")
                    
                except Exception as e:
                    error_msg = f"Error processing {file}: {str(e)}"
                    self.update_status(error_msg)
                    logging.error(error_msg)

            self.update_status("\nFile organization complete!")
            logging.info("File organization process completed")

        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.update_status(error_msg)
            logging.error(error_msg)

def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
