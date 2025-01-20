from tkinter import Label,Entry,Tk,Button,filedialog,messagebox, Frame, Canvas, Scrollbar, WORD, Text, END
from shamir import Shamir

exported_shares = []
recovered_points = []
recovered_prime = []
shamir_instance = Shamir()

# Create icons (buttons with images)
def create_icon_button(icon_text, value, prime_number, row, column):
    # Create a button with text acting as an icon
    button = Button(left_frame, text=icon_text, width=10, height=2, command=lambda: download_file(value, prime_number))
    button.grid(row=row, column=column, padx=10, pady=10)
    return button

def update_scrollregion():
    """Update the scroll region of the canvas."""
    left_canvas.update_idletasks()  # Ensure all changes are reflected
    left_canvas.configure(scrollregion=left_canvas.bbox("all"))

def delete_points():
    global exported_shares
    # Clear existing buttons
    for button in exported_shares:
        if button:
            button.destroy()
    exported_shares.clear()

def clear_values():
    global recovered_points
    global recovered_prime
    # Clear existing buttons
    recovered_points = []
    recovered_prime = []
    exported_shares.clear()
    l_secret.config(text="")
    text_widget.delete(1.0, END)

def calculate_share_secret():
    try:
        # Read input from the Entry widgets
        secret_number = el1.get()
        n_elements = el2.get()
        k_number = el3.get()
        shamir_instance.get_values(secret=secret_number,n_parts=n_elements, k_parts=k_number)
        delete_points()
        for i, part in enumerate(shamir_instance.points):
            print(part)
            button = create_icon_button(f"Part {i+1}",part, shamir_instance.prime_number,i+5,0)
            exported_shares.append(button)  # Track the new button
        update_scrollregion()
    except TypeError:
        # Handle invalid input
        messagebox.showerror("Invalid Input", "Please enter valid integers!")

def recover_secret():
    try:
        # Read input from the Entry widgets
        prime = list(set(recovered_prime))
        if(len(prime) > 1):
            raise TypeError("The prime number should be the same for all values to recover")
        secret = shamir_instance.reconstruct_secret_shamir(recovered_points, prime[0])
        l_secret.config(text=secret)
        text_widget.delete(1.0, END)
    except TypeError:
        # Handle invalid input
        messagebox.showerror("Invalid Input", "The secret could not be recovered")

def upload_file():
    # Open a file dialog for the user to select a file
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        try:
            content = []
            # Read the file content (optional)
            with open(file_path, "r") as file:
                for line in file:
                    content.append(line.strip())
            recovered_points.append((int(content[0]),int(content[1])))
            recovered_prime.append(int(content[2]))
            # Optionally, display the file content in the GUI
            text_widget.insert(END, content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {str(e)}")

def download_file(value, prime_number):
    # Ask the user where to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if file_path:
        try:
            # Write the value to the file
            with open(file_path, "w") as file:
                file.write(str(value[0])+"\n")
                file.write(str(value[1])+"\n")
                file.write(str(prime_number)+"\n")
            messagebox.showinfo("Success", f"File saved successfully at {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def gui_share_secret():
    master = Tk()
    master.title('Shamir Secret Sharing')
    Label(master, text='Secret number: ').grid(row=0)
    Label(master, text='Number of shared elements: ').grid(row=1)
    Label(master, text='Minimum number of elements: ').grid(row=2)
    e1 = Entry(master)
    e2 = Entry(master)
    e3 = Entry(master)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    Button(master, text='Generate numbers', width=25, command=calculate_share_secret).grid(row=3)

    # Label to display the result
    master.mainloop()

# Create the main window
root = Tk()
root.title("Shamir Sharing Secret")
root.geometry("800x600")

# Configure the grid layout for the main window
root.columnconfigure(0, weight=1, uniform="section")  # Left section
root.columnconfigure(1, weight=1, uniform="section")  # Right section
root.rowconfigure(0, weight=1)

# Create the left section as a scrollable canvas
left_canvas = Canvas(root, bg="lightblue")
left_canvas.grid(row=0, column=0, sticky="nsew")

# Add a scrollbar to the left canvas
left_scrollbar = Scrollbar(root, orient="vertical", command=left_canvas.yview)
left_scrollbar.grid(row=0, column=0, sticky="nse")

# Configure the canvas to work with the scrollbar
left_canvas.configure(yscrollcommand=left_scrollbar.set)
left_canvas.bind("<Configure>",lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))

# Create a frame inside the canvas for content
left_frame = Frame(left_canvas, bg="lightblue")
left_canvas.create_window((0, 0), window=left_frame, anchor="nw")

# Add widgets to the left section
Label(left_frame, text="Share the secret", bg="lightblue", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
Label(left_frame, text=" Secret number: ", bg="lightblue").grid(row=1, column=0, sticky="w", padx=5, pady=5)
el1 = Entry(left_frame)
el1.grid(row=1, column=1, padx=5, pady=5)

Label(left_frame, text=" Number of shared elements: ", bg="lightblue").grid(row=2, column=0, sticky="w", padx=5, pady=5)
el2 = Entry(left_frame)
el2.grid(row=2, column=1, padx=5, pady=5)

Label(left_frame, text=" Minimum number of elements: ", bg="lightblue").grid(row=3, column=0, sticky="w", padx=5, pady=5)
el3 = Entry(left_frame)
el3.grid(row=3, column=1, padx=5, pady=5)

Button(left_frame, text="Generate points", command=calculate_share_secret,  width=20, height=2).grid(row=4, column=0, columnspan=2, pady=10)

# Create the right section
right_frame = Frame(root, bg="lightgreen")
right_frame.grid(row=0, column=1, sticky="nsew")

# Configure the grid layout inside the right frame
right_frame.columnconfigure([0, 1], weight=1)

# Add widgets to the right section
Label(right_frame, text="Recover the secret", bg="lightgreen", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

# Create a button for uploading a file
upload_button = Button(right_frame, text="Upload File", command=upload_file, width=20, height=2)
upload_button.grid(row=1, column=0, columnspan=2, pady=10)

# Text widget to display the file content
text_widget = Text(right_frame, wrap=WORD, height=15, width=40)
text_widget.grid(row=2, column=0, columnspan=2, pady=10)
l_secret = Label(right_frame, text="", bg="lightgreen", font=("Arial", 16))
l_secret.grid(row=5, column=0, columnspan=2, pady=10)
Label(right_frame, text="Secret: ", bg="lightgreen", font=("Arial", 16)).grid(row=4, column=0, columnspan=2, pady=10)
upload_button = Button(right_frame, text="Recover secret", command=recover_secret, width=20, height=2)
upload_button.grid(row=3, column=0, columnspan=1, pady=10)
upload_button = Button(right_frame, text="Clear values", command=clear_values, width=20, height=2)
upload_button.grid(row=3, column=1, columnspan=1, pady=10)

# Start the main loop
root.mainloop()