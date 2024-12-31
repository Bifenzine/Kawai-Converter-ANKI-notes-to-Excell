import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from pathlib import Path
from tkinter import ttk

# develop branch

def convert_text_to_excel(text_content: str, output_file: str):
    # Split the text into lines and skip the header lines
    lines = [line for line in text_content.split('\n') if line and not line.startswith('#')]
    
    # Process each line into a dictionary
    data = []
    for line in lines:
        if '\t' in line:
            # Split by tab and clean up quotes
            parts = [part.strip().strip('"') for part in line.split('\t')]
            
            # Ensure we have at least 2 parts
            if len(parts) >= 2:
                row_data = {
                    'Arabic': parts[0],
                    'Translation': parts[1],
                }
                data.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel writer with xlsxwriter engine
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Translations', index=False)
        
        # Get workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Translations']
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'bg_color': '#D9E1F2',
            'border': 1,
            'align': 'center'
        })
        
        rtl_format = workbook.add_format({
            'text_wrap': True,
            'reading_order': 2,  # RTL reading order
            'align': 'right'
        })
        
        ltr_format = workbook.add_format({
            'text_wrap': True,
            'reading_order': 1,  # LTR reading order
            'align': 'left'
        })
        
        # Format headers
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Format columns
        worksheet.set_column('A:A', 30, rtl_format)  # Arabic column
        worksheet.set_column('B:B', 30, ltr_format)  # Translation column
        worksheet.set_column('C:C', 20, ltr_format)  # Tags column
        
        # Set RTL format for Arabic cells
        for row_num in range(1, len(df) + 1):
            worksheet.write(row_num, 0, df['Arabic'].iloc[row_num-1], rtl_format)
            worksheet.write(row_num, 1, df['Translation'].iloc[row_num-1], ltr_format)
            if 'Tags' in df.columns:
                worksheet.write(row_num, 2, df['Tags'].iloc[row_num-1], ltr_format)

class KawaiiTextToExcelConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Kawaii Text to Excel Converter ✨")
        
        # Set kawaii color scheme
        self.colors = {
            'bg': '#FFF0F5',  # Soft pink background
            'button_bg': '#FFB6C1',  # Light pink
            'button_fg': '#FF69B4',  # Hot pink
            'text_bg': '#FFFFFF',  # White
            'accent': '#FF1493'  # Deep pink
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        self.root.minsize(500, 400)
        
        # Create style for widgets
        self.style = ttk.Style()
        self.style.configure('Kawaii.TButton',
                           background=self.colors['button_bg'],
                           foreground=self.colors['button_fg'],
                           font=('Helvetica', 12, 'bold'),
                           padding=10)
        
        # Create main container with padding
        self.main_container = tk.Frame(root, bg=self.colors['bg'], padx=20, pady=20)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create title label with cute emojis
        self.title_label = tk.Label(
            self.main_container,
            text="(づ｡◕‿‿◕｡)づ Text to Excel Converter ˎ₍•ʚ•₎ˏ",
            font=('Helvetica', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.title_label.pack(pady=(0, 20))


         # sparkles conversion label
        self.title_label = tk.Label(
            self.main_container,
            text="(ˎ₍•ʚ•₎ˏ Convert with sparkles ˎ₍•ʚ•₎ˏ",
            font=('Helvetica', 10, 'italic'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.title_label.pack(pady=(0, 20))
        
        # File selection frame
        self.file_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.file_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_label = tk.Label(
            self.file_frame,
            text="✧ Selected File: None ✧",
            font=('Helvetica', 10),
            bg=self.colors['bg'],
            wraplength=400
        )
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Create cute browse button
        self.browse_button = tk.Button(
            self.file_frame,
            text="✿ Browse ✿",
            command=self.browse_file,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            relief=tk.RAISED,
            font=('Helvetica', 10, 'bold'),
            cursor='heart'
        )
        self.browse_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Preview section
        self.preview_label = tk.Label(
            self.main_container,
            text="♡ File Preview ♡",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.preview_label.pack(anchor=tk.W, pady=(10, 5))
        
        # Create preview text area with cute border
        self.preview_frame = tk.Frame(
            self.main_container,
            bg=self.colors['accent'],
            padx=2,
            pady=2
        )
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.preview_text = tk.Text(
            self.preview_frame,
            height=15,
            wrap=tk.WORD,
            font=('Helvetica', 10),
            bg=self.colors['text_bg'],
            relief=tk.FLAT
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Convert button with kawaii styling
        self.convert_button = tk.Button(
            self.main_container,
            text="✧･ﾟ: Convert to Excel :･ﾟ✧",
            command=self.convert_file,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            relief=tk.RAISED,
            font=('Helvetica', 12, 'bold'),
            cursor='heart',
            padx=20,
            pady=10
        )
        self.convert_button.pack(pady=(0, 20))
        
        # Add a cute footer
        self.footer_label = tk.Label(
            self.main_container,
            text="ᓚᘏᗢ Made with love ᓚᘏᗢ",
            font=('Helvetica', 8),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.footer_label.pack()
        
        self.selected_file = None
        
        # Make the window responsive
        self.main_container.grid_columnconfigure(0, weight=1)
        self.root.bind('<Configure>', self.on_resize)
    
    def on_resize(self, event):
        # Update wraplength of file label based on window size
        new_wraplength = max(300, event.width - 200)
        self.file_label.configure(wraplength=new_wraplength)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"✧ Selected File: {os.path.basename(file_path)} ✧")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.preview_text.delete(1.0, tk.END)
                    preview_content = content[:1000] + ("\n..." if len(content) > 1000 else "")
                    self.preview_text.insert(tk.END, preview_content)
            except Exception as e:
                messagebox.showerror("(｡•́︿•̀｡)", f"Error reading file: {str(e)}")
    
    def convert_file(self):
        if not self.selected_file:
            messagebox.showwarning("(｡•́︿•̀｡)", "Please select a text file first!")
            return
        
        try:
            # Get desktop path
            desktop_path = str(Path.home() / "Desktop")
            
            # Get original filename without extension
            original_filename = os.path.splitext(os.path.basename(self.selected_file))[0]
            
            # Create new filename with kawaii prefix
            output_filename = f"Kawaii_conversion_{original_filename}.xlsx"
            
            # Join with desktop path
            output_file = os.path.join(desktop_path, output_filename)
            
            # Check if file already exists and add number if needed
            counter = 1
            while os.path.exists(output_file):
                output_filename = f"Kawaii_conversion_{original_filename}_{counter}.xlsx"
                output_file = os.path.join(desktop_path, output_filename)
                counter += 1
            
            # Read and convert the file
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                text_content = file.read()
            
            convert_text_to_excel(text_content, output_file)
            
            messagebox.showinfo("(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", 
                              f"Excel file created successfully!\n\n✨ Saved as: {output_filename}\n📍 Location: {desktop_path}")
        except Exception as e:
            messagebox.showerror("(｡•́︿•̀｡)", f"Error converting file: {str(e)}")

def main():
    root = tk.Tk()
    app = KawaiiTextToExcelConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()