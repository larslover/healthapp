"""
def clean_up_period_difficulties():
    conn = sqlite3.connect("gracehealth.db")
    cursor = conn.cursor()

    try:
        # Update regularity_period_difficulties to "N/A" where Gender is "male"
        cursor.execute("""
            UPDATE student 
            SET E5_regularity_period_difficulties = 'N/A' 
            WHERE Gender = 'male'
        """)

        conn.commit()
        print("Database cleaned: Set 'N/A' for males in E5_regularity_period_difficulties.")

    except Exception as e:
        print(f"Error updating database: {e}")

    finally:
        conn.close()

# Run the function to clean up the database
clean_up_period_difficulties()



def update_length_age_category():
    conn = sqlite3.connect("gracehealth.db")
    cursor = conn.cursor()

    # Female height thresholds
    female_thresholds = {
        24: (76.0, 79.3),
        25: (76.8, 80.0),
        26: (77.5, 80.8),
        27: (78.1, 81.5),
        28: (78.8, 82.2),
        29: (79.5, 82.9),
        30: (80.1, 83.6),
        31: (80.7, 84.3),
        32: (81.3, 84.9),
        33: (81.9, 85.6),
        34: (82.5, 86.2),
        35: (83.1, 86.8),
        36: (83.6, 87.4),
        37: (84.2, 88.0),
        38: (84.7, 88.6),
        39: (85.3, 89.2),
        40: (85.8, 89.8),
        41: (86.3, 90.4),
        42: (86.8, 90.9),
        43: (87.4, 91.5),
        44: (87.9, 92.0),
        45: (88.4, 92.5),
        46: (88.9, 93.1),
        47: (89.3, 93.6),
        48: (89.8, 94.1),
        49: (90.3, 94.6),
        50: (90.7, 95.1),
        51: (91.2, 95.6),
        52: (91.7, 96.1),
        53: (92.1, 96.6),
        54: (92.6, 97.1),
        55: (93.0, 97.6),
        56: (93.4, 98.1),
        57: (93.9, 98.5),
        58: (94.3, 99.0),
        59: (94.7, 99.5),
        60: (95.2, 99.9),
    }

    # Male height thresholds
    male_thresholds = {
        24: (78.0, 81.0),
        25: (78.6, 81.7),
        26: (79.3, 82.5),
        27: (79.9, 83.1),
        28: (80.5, 83.8),
        29: (81.1, 84.5),
        30: (81.7, 85.1),
        31: (82.3, 85.7),
        32: (82.8, 86.4),
        33: (83.4, 86.9),
        34: (83.9, 87.5),
        35: (84.4, 88.1),
        36: (85.0, 88.7),
        37: (85.5, 89.2),
        38: (86.0, 89.8),
        39: (86.5, 90.3),
        40: (87.0, 90.9),
        41: (87.5, 91.4),
        42: (88.0, 91.9),
        43: (88.4, 92.4),
        44: (88.9, 93.0),
        45: (89.4, 93.5),
        46: (89.8, 94.0),
        47: (90.3, 94.4),
        48: (90.7, 94.9),
        49: (91.2, 95.4),
        50: (91.6, 95.9),
        51: (92.1, 96.4),
        52: (92.5, 96.9),
        53: (93.0, 97.4),
        54: (93.4, 97.8),
        55: (93.9, 98.3),
        56: (94.3, 98.8),
        57: (94.7, 99.3),
        58: (95.3, 99.7),
        59: (95.6, 100.2),
        60: (96.1, 100.7),
    }

    cursor.execute("SELECT id, age_in_month, height, gender FROM student")
    rows = cursor.fetchall()

    for row in rows:
        student_id, age, height, gender = row

        if height is None or height == "":
            continue  # Skip invalid height entries

        try:
            height = float(height)
        except ValueError:
            continue  # Skip invalid height values

        # Select the correct thresholds
        if gender == "female":
            height_thresholds = female_thresholds
        elif gender == "male":
            height_thresholds = male_thresholds
        else:
            continue  # Skip invalid gender entries

        # Determine category (now stored in lowercase)
        category = "n/a"
        if age in height_thresholds:
            lower_threshold, upper_threshold = height_thresholds[age]
            if height < lower_threshold:
                category = "severe stunting"
            elif height < upper_threshold:
                category = "moderate stunting"
            else:
                category = "normal"

        # Update database with the correct category in lowercase
        cursor.execute("UPDATE student SET length_age = ? WHERE id = ?", (category, student_id))

    conn.commit()
    conn.close()

    print("Database records updated successfully with lowercase categories.")

# Run the function once to update the existing records
update_length_age_category()

def add_status_column():
    """
    Alter the 'student' table to add a 'status' column if it doesn't already exist.
    """
    try:
        # Check if the 'status' column already exists
        cursor.execute("PRAGMA table_info(student);")
        columns = cursor.fetchall()

        # Look for the 'status' column
        column_names = [column[1] for column in columns]

        if 'status' not in column_names:
            # Alter the table to add the 'status' column
            cursor.execute("""
                ALTER TABLE student
                ADD COLUMN status TEXT DEFAULT 'active';
            """)

            # Commit the changes to the database
            conn.commit()




    except Exception as e:
        # Handle any errors during the table alteration process
        messagebox.showerror("Error", f"Failed to add 'status' column: {e}")
        conn.rollback()


# Call the function to add the status column
add_status_column()

def add_muac_column():
    """
    Alter the 'student' table to add a 'status' column if it doesn't already exist.
    """
    try:
        # Check if the 'status' column already exists
        cursor.execute("PRAGMA table_info(student);")
        columns = cursor.fetchall()

        # Look for the 'status' column
        column_names = [column[1] for column in columns]

        if 'muac' not in column_names:
            # Alter the table to add the 'status' column
            cursor.execute("""
                ALTER TABLE student
                ADD COLUMN muac INTEGER
            """)

            # Commit the changes to the database
            conn.commit()




    except Exception as e:
        # Handle any errors during the table alteration process
        messagebox.showerror("Error", f"Failed to add 'muac' column: {e}")
        conn.rollback()


# Call the function to add the status column
add_muac_column()


def add_muac_sam_column():
    """
    Alter the 'student' table to add a 'status' column if it doesn't already exist.
    """
    try:
        # Check if the 'status' column already exists
        cursor.execute("PRAGMA table_info(student);")
        columns = cursor.fetchall()

        # Look for the 'status' column
        column_names = [column[1] for column in columns]

        if 'muac_sam' not in column_names:
            # Alter the table to add the 'status' column
            cursor.execute("""
                ALTER TABLE student
                ADD COLUMN muac_sam TEXT
            """)

            # Commit the changes to the database
            conn.commit()




    except Exception as e:
        # Handle any errors during the table alteration process
        messagebox.showerror("Error", f"Failed to add 'muac_sam' column: {e}")
        conn.rollback()


# Call the function to add the status column
add_muac_sam_column()




def fetch_data_by_id(id_value):
    """
    Fetches all screening records for a given student ID, sorted by screen_date descending.

    Args:
        id_entry_widget (tk.Entry): The Tkinter Entry widget containing the student ID.

    Returns:
        List[Dict]: A list of dictionaries, each representing a screening record.
    """


    conn = sqlite3.connect('gracehealth.db')  # Connect to the database
    cursor = conn.cursor()

    query = """
    SELECT
        name, date_of_birth, Gender, Class_section, Roll_no, Aadhaar_No,
        Father_or_guardian_name, mother_name, contact_number, Address,
        email, Name_teacher, school_name, last_school_name, place_of_birth,
        known_earlier_disease,
        weight, height,muac, muac_sam, BMI, Vision_both, VISON_left, VISON_right, VISION_problem,
        B1_severe_anemia, B2_Vita_A_deficiency, B3_Vit_D_deficiency, B4_Goitre,
        B5_Oedema, C1_convulsive_dis, C2_otitis_media, C3_dental_condition,
        C4_skin_condition, C5_rheumatic_heart_disease, C6_others_TB_asthma,
        D1_difficulty_seeing, D2_delay_in_walking, D3_stiffness_floppiness,
        D5_reading_writing_calculatory_difficulty, D6_speaking_difficulty,
        D7_hearing_problems, D8_learning, D9_attention, E3_depression_sleep,
        E4_Menarke, E5_regularity_period_difficulties, E6_UTI_STI, E7,
        E8_menstrual_pain, E9_remarks, BMI_category, weight_age, length_age,
        weight_height, age_in_month, deworming, vaccination, tea_garden,
        screen_date, age_screening
    FROM student
    WHERE id = ?
    ORDER BY strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) DESC

    """

    cursor.execute(query, (id_value,))
    rows = cursor.fetchall()  # Fetch all matching rows
    conn.close()  # Always close the connection

    if rows:
        # Get column names from cursor description
        column_names = [description[0] for description in cursor.description]

        # Convert each row to a dictionary
        data_list = [dict(zip(column_names, row)) for row in rows]
        print(f"Number of screenings fetched: {len(data_list)}")
        return data_list
    else:
        print("No data found for the given ID")
        return []




import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Toplevel
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def save_text_as_pdf(text_widget):
    """
    Saves the content of a Tkinter Text widget as a PDF file.

    Args:
        text_widget (tk.Text): The Tkinter Text widget containing the journal content.
    """
    # Ask the user to choose a file location and name
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

    if not file_path:
        return  # Exit the function if the user cancels the save dialog

    # Get the content from the Text widget
    text_content = text_widget.get("1.0", tk.END).strip()

    # Create a PDF file
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Set the initial y-position for the text
    y_position = height - 40  # Start near the top with some margin
    line_height = 14  # Line spacing for each line

    # Split text into lines and write each line to the PDF
    for line in text_content.split("\n"):
        if y_position <= 40:  # If there's not enough space, create a new page
            c.showPage()
            y_position = height - 40  # Reset y-position for the new page

        c.drawString(40, y_position, line)
        y_position -= line_height

    # Save the PDF file
    c.save()
    print(f"PDF saved as {file_path}")

def display_journal(id_value, summary_frame):
    data_list = fetch_data_by_id(id_value)
    if not data_list:
        return

    clear_frame(summary_frame)
    journal_text = create_text_widget(summary_frame)
    add_pdf_button(summary_frame, journal_text)

    total_screenings = len(data_list)
    for index, data in enumerate(data_list):
        screening_number = total_screenings - index
        insert_screening_header(journal_text, screening_number)
        insert_bio(journal_text, data)
        insert_physical_measurements(journal_text, data)
        insert_physical_categories(journal_text, data)
        insert_eye_section(journal_text, data)
        insert_general_health(journal_text, data)
        journal_text.insert(tk.END, "-" * 40 + "\n")
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_text_widget(frame):
    journal_text = tk.Text(frame, wrap=tk.WORD, height=10, width=45)
    scroll = tk.Scrollbar(frame, command=journal_text.yview)
    journal_text.config(yscrollcommand=scroll.set)
    journal_text.tag_configure("highlight", foreground="red", font=("Arial", 10, "bold"))
    journal_text.grid(row=0, column=0, sticky="nsew")
    scroll.grid(row=0, column=1, sticky="ns")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    return journal_text

def add_pdf_button(frame, text_widget):
    save_pdf_button = ttk.Button(frame, text="Save as PDF", command=lambda: save_text_as_pdf(text_widget))
    save_pdf_button.grid(row=1, column=0, pady=10, sticky="ew")

def insert_screening_header(widget, number):
    widget.insert(tk.END, f"=== SCREENING {number} ===\n")
def insert_bio(widget, data):
    widget.insert(tk.END, f"Screen Date: {data.get('screen_date', 'N/A')}\n")
    widget.insert(tk.END, f"Age Screening: {data.get('age_screening', 'N/A')}\n")
    widget.insert(tk.END, "-" * 40 + "\n=== BIO ===\n")
    keys = [
        ('name', 'Name'), ('date_of_birth', 'Date of Birth'), ('Gender', 'Gender'),
        ('Class_section', 'Class Section'), ('Roll_no', 'Roll No'), ('Aadhaar_No', 'Aadhaar No'),
        ('Father_or_guardian_name', 'Father/Guardian Name'), ('mother_name', "Mother's Name"),
        ('contact_number', 'Contact Number'), ('Address', 'Address'),
        ('tea_garden', 'Tea Garden'), ('email', 'Email'),
        ('Name_teacher', 'Name of Teacher'), ('school_name', 'School Name'),
        ('last_school_name', 'Last School Name'), ('place_of_birth', 'Place of Birth'),
    ]
    for key, label in keys:
        widget.insert(tk.END, f"{label}: {data.get(key, 'N/A')}\n")
    widget.insert(tk.END, "-" * 40 + "\n")
def insert_physical_measurements(widget, data):
    widget.insert(tk.END, "=== PHYSICAL MEASUREMENTS ===\n")
    widget.insert(tk.END, f"Weight: {data.get('weight', 'N/A')}\n")
    widget.insert(tk.END, f"Height: {data.get('height', 'N/A')}\n")
    widget.insert(tk.END, f"BMI: {data.get('BMI', 'N/A')}\n")
    widget.insert(tk.END, f"MUAC: {data.get('muac', 'N/A')}\n")
    widget.insert(tk.END, "-" * 40 + "\n")


def insert_and_highlight_not_normal(widget, label, key, data):
    value = str(data.get(key, 'N/A')).strip().lower()
    widget.insert(tk.END, f"{label}: {value}\n")

    # If the value is not 'normal' or 'n/a' or similar, highlight it
    non_normal_values = ['normal', 'n/a', 'none']
    if value not in non_normal_values and value.strip():  # Avoid highlighting 'N/A' or empty
        start_index = widget.index("end-2l")
        end_index = widget.index("end-1l lineend")
        widget.tag_add("highlight", start_index, end_index)


def insert_physical_categories(widget, data):
    widget.insert(tk.END, "=== PHYSICAL CATEGORIES ===\n")
    insert_and_highlight_not_normal(widget, "BMI Category", "BMI_category", data)
    insert_and_highlight_not_normal(widget, "MUAC Category", "muac_sam", data)
    insert_and_highlight_not_normal(widget, "Weight for Age", "weight_age", data)
    insert_and_highlight_not_normal(widget, "Length for Age", "length_age", data)
    insert_and_highlight_not_normal(widget, "Weight for Height", "weight_height", data)
    widget.insert(tk.END, "-" * 40 + "\n")
    print("PHYSICAL CATEGORIES DATA:", data)


def insert_eye_section(widget, data):
    widget.insert(tk.END, "=== EYE ===\n")

    widget.insert(tk.END, f"Vision (Left Eye): {data.get('VISON_left', 'N/A')}\n")
    widget.insert(tk.END, f"Vision (Right Eye): {data.get('VISON_right', 'N/A')}\n")
    vision_problem = data.get('VISION_problem', 'N/A')
    widget.insert(tk.END, f"Vision Problem: {vision_problem}\n")
    if vision_problem.lower() == "yes":
        start_index = widget.index("end-2l")
        end_index = widget.index("end-1l lineend")
        widget.tag_add("highlight", start_index, end_index)
    widget.insert(tk.END, "-" * 40 + "\n")

def insert_and_highlight_yes(widget, label, key, data):
    value = data.get(key, 'N/A')
    widget.insert(tk.END, f"{label}: {value}\n")
    if value.lower() == "yes":
        start_index = widget.index("end-2l")
        end_index = widget.index("end-1l lineend")
        widget.tag_add("highlight", start_index, end_index)

def insert_general_health(widget, data):
    widget.insert(tk.END, "=== GENERAL HEALTH ===\n")
    keys = [
        ("Severe Anemia", 'B1_severe_anemia'),
        ("Vitamin A Deficiency", 'B2_Vita_A_deficiency'),
        ("Vitamin D Deficiency", 'B3_Vit_D_deficiency'),
        ("Goitre", 'B4_Goitre'),
        ("Oedema", 'B5_Oedema'),
        ("Convulsive Disorders", 'C1_convulsive_dis'),
        ("Otitis Media", 'C2_otitis_media'),
        ("Dental Condition", 'C3_dental_condition'),
        ("Skin Condition", 'C4_skin_condition'),
    ]
    for label, key in keys:
        insert_and_highlight_yes(widget, label, key, data)


def add_column_if_not_exists():
    connection = sqlite3.connect("gracehealth.db")
    cursor = connection.cursor()

    # Check if the column 'age_screening' exists in the 'student' table
    cursor.execute("PRAGMA table_info(student)")
    columns = cursor.fetchall()

    # Column names are in the second position in each row of the result
    column_names = [column[1] for column in columns]

    if 'age_screening' not in column_names:
        # Add the new column 'age_screening' if it doesn't exist
        cursor.execute("ALTER TABLE student ADD COLUMN age_screening TEXT")
        print("Column 'age_screening' added.")
    else:
        print("Column 'age_screening' already exists.")

    connection.commit()
    connection.close()

# Call the function
add_column_if_not_exists()

import tkinter as tk
from tkinter import ttk

class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None  # Store the ID of the scheduled after() call
        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def schedule_tooltip(self, event=None):
        self.cancel_scheduled_tooltip()  # Cancel any previous scheduling
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def cancel_scheduled_tooltip(self):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def show_tooltip(self, event=None):
        if self.tooltip_window:  # Tooltip already exists
            return
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Removes window borders
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        self.cancel_scheduled_tooltip()  # Ensure no tooltip will be shown
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def new_journal():

    # Create the main application window (if not already created)


    def statistic_search():

        def clear_statistic():
            pass


        def show_record_function():
            connection = sqlite3.connect("gracehealth.db")
            cursor = connection.cursor()
            record = sickness_search.get()
            school = school_options.get()
            clear_statistic()




            from tkinter import ttk
            from tkinter import messagebox

            def height_age_moderate_stunting_all():
                print("moderate stunting function all")
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a date is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with chronic malnutrition and the selected screening date
                    cursor.execute(f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE length_age = 'moderate stunting'
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find the total number of students screened in the selected year
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch the total number of students

                    # Ensure the Treeview is cleared before inserting new data
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Calculate and update statistics
                    if total_student == 0:
                        statistic_text = "No students screened for this year."
                    else:
                        if total_sick == 0:
                            statistic_text = f"0% (0/{total_student}) of students age 2 - 5 years have moderate stunting)"
                        else:
                            percentage = round((total_sick / total_student) * 100, 1)
                            statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students age 2 - 5 years have moderate stunting)"

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(item[0], item[1], item[2]))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")

            def height_age_severe_stunting_all():
                print("severe stunting function all")
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a date is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with chronic malnutrition and the selected screening date
                    cursor.execute(f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE length_age = 'severe stunting'
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find the total number of students screened in the selected year
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch the total number of students

                    # Ensure the Treeview is cleared before inserting new data
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Calculate and update statistics
                    if total_student == 0:
                        statistic_text = "No students screened for this year."
                    else:
                        if total_sick == 0:
                            statistic_text = f"0% (0/{total_student}) of students age 2 - 5 years have severe stunting)"
                        else:
                            percentage = round((total_sick / total_student) * 100, 1)
                            statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students age 2 - 5 years have severe stunting)"

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(item[0], item[1], item[2]))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")



            def muac_all():
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a date is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with severe acute malnutrition for the selected screening date
                    cursor.execute(f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE muac_sam = 'severe acute malnutrition'
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find total students aged 24 - 72 months who were tested for MUAC in the selected year
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 72 
                        AND muac_sam IS NOT NULL  
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch the total student count

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = "No students screened for this year."
                    else:
                        if total_sick == 0:
                            statistic_text = f"0% (0/{total_student}) of students age 6 - 60 months have severe acute malnutrition based on MUAC"
                        else:
                            percentage = round((total_sick / total_student) * 100, 1)
                            statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students age 6 - 60 months have severe acute malnutrition based on MUAC"

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(item[0], item[1], item[2]))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")

            def weight_height_statistic(malnutrition_type):
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a date is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with the specified malnutrition type and the selected screening date
                    cursor.execute(f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE weight_height = ?
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (malnutrition_type, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find total students between 24 and 60 months old screened in the selected year
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch total student count

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = "No students screened for this year."
                    else:
                        if total_sick == 0:
                            statistic_text = f"0% (0/{total_student}) of students age 2 - 5 years have {malnutrition_type} (measuring wasting)"
                        else:
                            percentage = round((total_sick / total_student) * 100, 1)
                            statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students age 2 - 5 years have {malnutrition_type} (measuring wasting)"

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3]))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")

            def B5_Oedema_all():
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a date is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with Oedema/swelling of legs in the selected screening year
                    cursor.execute(f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 72 
                        AND B5_Oedema = 'yes'  
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find total students aged 2 - 6 years in the selected screening year
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 72 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Get the total count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = "No students screened for this year."
                    else:
                        if total_sick == 0:
                            statistic_text = f"0% (0/{total_student}) of students age 2 - 6 years have oedema"
                        else:
                            percentage = round((total_sick / total_student) * 100, 1)
                            statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students age 2 - 6 years have oedema"

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(
                        item[0], item[1], item[2], item[3]))  # Fixed missing tea_garden column

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def vision_problem_all():
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with vision problems in the selected screening year
                    cursor.execute(f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE vision_problem = 'yes' 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to count total students tested (whether "yes" or "no" or any value)
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE vision_problem IS NOT NULL 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Get total count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = "No students screened for vision problems this year."
                    else:
                        if total_sick == 0:
                            statistic_text = f"0% (0/{total_student}) of students tested have vision problems"
                        else:
                            percentage = round((total_sick / total_student) * 100, 1)
                            statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students tested have vision problems"

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(
                        item[0], item[1], item[2], item[3]))  # Fixed missing tea_garden column

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_all(sickness, problem):
                selected_year = screening_year.get()  # Get the selected screening year from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with the specified sickness in the selected year
                    cursor.execute(f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE {sickness} = 'yes' 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to count total students screened in the selected year
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = f"No students screened for {problem} in {selected_year}."
                    else:
                        percentage = round((total_sick / total_student) * 100, 1) if total_sick > 0 else 0
                        statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students had {problem} in {selected_year}."

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(
                        item[0], item[1], item[2], item[3]))  # Ensure all columns are populated

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_all_no(sickness, problem):
                selected_year = screening_year.get()  # Get the selected screening year from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with the specified sickness in the selected year
                    cursor.execute(f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE {sickness} = 'no' 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to count total students screened in the selected year
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = f"No students screened for {problem} in {selected_year}."
                    else:
                        percentage = round((total_sick / total_student) * 100, 1) if total_sick > 0 else 0
                        statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students had not {problem} in {selected_year}."

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(
                        item[0], item[1], item[2], item[3]))  # Ensure all columns are populated

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)




            def statistic_E4_all():
                selected_year = screening_year.get()  # Get the selected screening year from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find female students who have started their menstrual cycle
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden
                        FROM student
                        WHERE E4_Menarke = 'yes' 
                        AND Gender = 'female' 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to count total female students screened in the selected year
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE Gender = 'female' 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = f"No female students were screened in {selected_year}."
                    else:
                        percentage = round((total_sick / total_student) * 100, 1) if total_sick > 0 else 0
                        statistic_text = f"{percentage}% ({total_sick}/{total_student}) of female students have started their menstrual cycle in {selected_year}."

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(
                        item[0], item[1], item[2], item[3]))  # Ensure all columns are populated

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_E5_all():
                """Calculate and display statistics for female students with no period difficulties across all schools."""

                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}")

                    # Query to count female students who have no period difficulties
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                          AND E5_regularity_period_difficulties = 'Yes' 
                          AND Gender = 'female' 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to get the total number of female students who have started menstruation
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                          AND Gender = 'female' 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0] or 0  # Fetch total student count safely

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic text
                    if total_student == 0:
                        statistic_text = f'No screening records found for {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1) if total_student > 0 else 0
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of female students have irregular difficulties.'

                        # Insert data into the Treeview, ensuring all columns are handled properly
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of female students have irregular periods.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    print(f"Database Error: {e}")  # Print error for debugging
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}")

            def statistic_E6_all():
                selected_year = screening_year.get()  # Get the selected screening year from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find female students with UTI/STI symptoms
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student
                        WHERE E6_UTI_STI = 'yes'  
                        AND Gender = 'female' 
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to count total screened students in the given age range
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 120 AND 216  
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = f"No students were screened in {selected_year}."
                    else:
                        percentage = round((total_sick / total_student) * 100, 1) if total_sick > 0 else 0
                        statistic_text = f"{percentage}% ({total_sick}/{total_student}) of students have UTI/STI symptoms (pain/burning sensation while urinating)."

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(
                        item[0], item[1], item[2], item[3]))  # Ensure all columns are displayed

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_E7_all():
                selected_year = screening_year.get()  # Get the selected screening year from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with discharge/foul smell from genito-urinary area
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student
                        WHERE E7 = 'yes'
                        AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to count total screened students
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = f"No students were screened in {selected_year}."
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1) if statistic_sick > 0 else 0
                        statistic_text = f"{percentage}% ({statistic_sick}/{total_student}) of students have discharge/foul smell from genito-urinary area."

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(
                        item[0], item[1], item[2], item[3]))  # Ensure all columns are displayed

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_E8_all():
                selected_year = screening_year.get()  # Get the selected screening year from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find female students with menstrual pain
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student
                        WHERE E8_menstrual_pain = 'yes' 
                        AND Gender = 'female'
                        AND '20' || SUBSTR(screen_date, -2) = ?""",
                                   (selected_year,)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to count total female students who have started their menstrual cycle
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                        AND Gender = 'female' 
                        AND '20' || SUBSTR(screen_date, -2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = f"No female students with menstrual cycle were screened in {selected_year}."
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1) if statistic_sick > 0 else 0
                        statistic_text = (
                            f"{percentage}% ({statistic_sick}/{total_student}) of female students that have started their menstrual cycle experience menstrual pain."
                        )

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end", values=(
                        item[0], item[1], item[2], item[3]))  # Ensure all columns are displayed

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_bmi(category):
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with the selected BMI category on the selected screening date
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE BMI_category = ? 
                        AND '20' || SUBSTR(screen_date, -2) = ?""",
                                   (category, selected_year)
                                   )

                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to count total students aged between 6 to 18 years on the selected date
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 61 AND 216 
                        AND '20' || SUBSTR(screen_date, -2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic message
                    if total_student == 0:
                        statistic_text = f"No students aged 5 to 18 years were screened in {selected_year}."
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1) if statistic_sick > 0 else 0
                        statistic_text = (
                            f"{percentage}% ({statistic_sick}/{total_student}) of students aged between 5 to 18 years have {category} BMI."
                        )

                    # Update the label with the statistic information
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview
                    for item in result:
                        show_record_tree.insert("", "end",
                                                values=(item[0], item[1], item[2], item[3] if item[3] else "N/A"))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            # Usage: Call this function with the specific category, e.g., 'severe under', 'under', or 'over'.

            def handle_school_record(school, sickness, problem):
                """Process and display statistics for students with a specific sickness at a given school and year."""

                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a year is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to count total students in the specified school on the selected date
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE school_name = ? 
                           AND '20' || SUBSTR(screen_date, -2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Query to count students with the specified sickness
                    cursor.execute(
                        f"""SELECT COUNT(*) 
                            FROM student 
                            WHERE {sickness} = ? 
                            AND school_name = ? 
                            AND '20' || SUBSTR(screen_date, -2) = ?""",
                        ("yes", school, selected_year)
                    )
                    statistic_sick = cursor.fetchone()[0]  # Fetch count directly

                    # Query to get the list of students with the sickness
                    cursor.execute(
                        f"""SELECT id, name, school_name, tea_garden 
                            FROM student 
                            WHERE {sickness} = ? 
                            AND school_name = ? 
                            AND '20' || SUBSTR(screen_date, -2) = ?""",
                        ("yes", school, selected_year)
                    )
                    result = cursor.fetchall()

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Ensure total_student is never zero to avoid division by zero
                    if total_student == 0:
                        statistic_text = f'No students recorded at {school} for {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of students have {problem} at {school}.'

                    # Update the existing label (assuming `statistic_label` is defined elsewhere)
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview (if no records, it remains empty)
                    for item in result:
                        show_record_tree.insert("", "end",
                                                values=(item[0], item[1], item[2], item[3] if item[3] else "N/A"))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def handle_school_record_no(school, sickness, problem):
                """Process and display statistics for students with a specific sickness at a given school and year."""

                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a year is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Total students at the school for the selected year
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE school_name = ? 
                           AND '20' || SUBSTR(screen_date, -2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]

                    # Fetch students with the specified sickness = 'no'
                    cursor.execute(
                        f"""SELECT id, name, school_name, tea_garden 
                            FROM student 
                            WHERE {sickness} = ? 
                            AND school_name = ? 
                            AND '20' || SUBSTR(screen_date, -2) = ?""",
                        ("no", school, selected_year)
                    )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No students recorded at {school} for {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of students have not {problem} at {school}.'

                    statistic_label.config(text=statistic_text)

                    for item in result:
                        show_record_tree.insert("", "end",
                                                values=(item[0], item[1], item[2], item[3] if item[3] else "N/A"))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def weight_age_mu_school(school):
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a year is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to count total students between 24 and 60 months old in the selected school on the selected date
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, -2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Query to count students who are moderately underweight
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE weight_age = 'moderately underweight' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, -2) = ?""",
                        (school, selected_year)
                    )
                    total_sick = cursor.fetchone()[0]  # Fetch count directly

                    # Query to fetch details of students who are moderately underweight
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE weight_age = 'moderately underweight' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, -2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Ensure total_student is never zero to avoid division by zero
                    if total_student == 0:
                        statistic_text = f'No students recorded at {school} for {selected_year}.'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years are moderately underweight.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview (if no records, it remains empty)
                    for item in result:
                        show_record_tree.insert("", "end",
                                                values=(item[0], item[1], item[2], item[3] if item[3] else "N/A"))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def weight_age_su_school(school):
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a year is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to count total students between 24 and 60 months old in the selected school on the selected date
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND school_name = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?
                    """, (school, selected_year))
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Query to count students who are severely underweight
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE weight_age = 'severely underweight' 
                          AND school_name = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?
                    """, (school, selected_year))
                    total_sick = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Ensure total_student is never zero to avoid division by zero
                    if total_student == 0:
                        statistic_text = f'No students recorded at {school} for {selected_year}.'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years are severely underweight.'

                        # Fetch student details ONLY if there are severely underweight students
                        cursor.execute("""
                            SELECT id, name, school_name, tea_garden 
                            FROM student 
                            WHERE weight_age = 'severely underweight' 
                              AND school_name = ? 
                              AND '20' || SUBSTR(screen_date, 7, 2) = ?
                        """, (school, selected_year))
                        result = cursor.fetchall()

                        # Insert new data into the Treeview, even if empty
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # **Always update the statistic label**, even if total_sick == 0
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def height_age_moderate_stunting_school(school):

                print("this is moderate stunting school function")
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a date is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with chronic malnutrition (stunting) in the selected school on the selected date
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60 
                             AND length_age = 'moderate stunting' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find total students between 24 and 60 months old in the selected school on the selected date
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        # No students recorded, display message
                        statistic_text = f'No students recorded at {school} for {selected_year}.'
                    else:
                        # Always show the total count, even if total_sick == 0
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years have moderate stunting)'

                        # Insert new data into the Treeview (if no records, it remains empty)
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def height_age_severe_stunting_school(school):
                print("this is severe stunting function")
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a date is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with chronic malnutrition (stunting) in the selected school on the selected date
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60 
                             AND length_age = 'severe stunting' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find total students between 24 and 60 months old in the selected school on the selected date
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        # No students recorded, display message
                        statistic_text = f'No students recorded at {school} for {selected_year}.'
                    else:
                        # Always show the total count, even if total_sick == 0
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years have severe stunting)'

                        # Insert new data into the Treeview (if no records, it remains empty)
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)



            def muac_school(school):
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with severe acute malnutrition (SAM) in the selected school on the selected date
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE muac_sam = 'severe acute malnutrition' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find total students between 6 and 60 months old who were tested for MUAC
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE age_in_month BETWEEN 6 AND 60 
                             AND school_name = ? 
                             AND muac_sam IS NOT NULL  -- Exclude students not tested for MUAC
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        # No students recorded, display message
                        statistic_text = f'No MUAC screening records found for {school} in {selected_year}.'
                    else:
                        # Always show the total count, even if total_sick == 0
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 6 - 60 months have severe acute malnutrition based on MUAC.'

                        # Insert new data into the Treeview (if no records, it remains empty)
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def weight_height_mam_school(school):
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with moderate acute malnutrition (MAM) in the selected school on the selected date
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60 
                             AND weight_height = 'moderate acute malnutrition' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find total students between 24 and 60 months old in the selected school on the selected date
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        # No students recorded, display message
                        statistic_text = f'No weight-for-height screening records found for {school} in {selected_year}.'
                    else:
                        # Always show the total count, even if total_sick == 0
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years have moderate acute malnutrition (measuring wasting).'

                        # Insert new data into the Treeview (if no records, it remains empty)
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def weight_height_sam_school(school):
                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with severe acute malnutrition (SAM) in the selected school on the selected date
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden  
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60 
                             AND weight_height = 'severe acute malnutrition' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find total students between 24 and 60 months old in the selected school on the selected date
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 60 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No weight-for-height screening records found for {school} in {selected_year}.'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years have severe acute malnutrition (measuring wasting).'

                        # Insert new data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def B5_Oedema_school(school):
                selected_year = screening_year.get()  # Get the selected screening year from the combobox

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with Oedema in the selected school and year
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 72 
                             AND B5_Oedema = 'yes' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find the total number of students in the selected school and year
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE age_in_month BETWEEN 24 AND 72 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No screening records found for {school} in {selected_year}.'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 6 years have oedema.'

                        # Insert new data into the Treeview, ensuring all columns are handled properly
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_E4_school(school):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to count female students who have started their menstrual cycle
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE E4_Menarke = 'yes' 
                             AND Gender = 'female' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to get the total number of female students in the selected school and year
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE Gender = 'female' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No screening records found for {school} in {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of female students have started their menstrual cycle.'

                        # Insert new data into the Treeview, ensuring all columns are handled properly
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_E5_school(school):
                """Calculate and display statistics for female students with no period difficulties in a given school."""

                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, School: {school}")

                    # Query to count female students who have no period difficulties
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                          AND E5_regularity_period_difficulties = 'Yes' 
                          AND Gender = 'female' 
                          AND school_name = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (school, selected_year)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to get the total number of female students who have started menstruation
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                          AND Gender = 'female' 
                          AND school_name = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (school, selected_year)
                                   )
                    total_student = cursor.fetchone()[0] or 0  # Fetch total student count safely

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic text
                    if total_student == 0:
                        statistic_text = f'No screening records found for {school} in {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1) if total_student > 0 else 0
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of female students have irregular difficulties.'

                        # Insert data into the Treeview, ensuring all columns are handled properly
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of female students have irregular difficulties.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    print(f"Database Error: {e}")  # Print error for debugging
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, School: {school}")

            def statistic_E6_school(school):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with UTI/STI symptoms (pain/burning sensation)
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE E6_UTI_STI = 'yes' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to get the total number of students in the school on the selected date
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No screening records found for {school} in {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of students have pain/burning sensation while urinating.'

                        # Insert new data into the Treeview, ensuring all columns are handled properly
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # **Ensure 0 is displayed properly even if no students have symptoms**
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students have pain/burning sensation while urinating.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_E7_school(school):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with discharge/foul smell (E7) on the selected date
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE E7 = 'yes' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to get the total number of students in the school on the selected date
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No screening records found for {school} in {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of students have discharge/foul smell from genito-urinary area.'

                        # Insert new data into the Treeview, ensuring all columns are handled properly
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # **Ensure 0 is displayed properly even if no students have symptoms**
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students have discharge/foul smell from genito-urinary area.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_E8_school(school):
                print("statistic school E8")
                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find female students with menstrual pain (E8)
                    cursor.execute(
                        """SELECT id, name, school_name, tea_garden 
                           FROM student 
                           WHERE E8_menstrual_pain = 'yes' 
                             AND Gender = 'female' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    result = cursor.fetchall()
                    statistic_sick = len(result)  # Count the number of students with menstrual pain

                    # Query to get the total number of menstruating female students
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE E4_Menarke = 'yes' 
                             AND Gender = 'female' 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No screening records found for female students in {school} ({selected_year}).'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of female students that have started menstruation have menstrual pain.'

                        # Insert new data into the Treeview, ensuring all columns are handled properly
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # **Ensure 0 is displayed properly even if no students have menstrual pain**
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of female students that have started menstruation have menstrual pain.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def statistic_BMI(sickness, condition, school, problem):
                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with the specified sickness
                    cursor.execute(
                        f"""SELECT id, name, school_name, tea_garden 
                            FROM student 
                            WHERE {sickness} = ? 
                              AND school_name = ? 
                              AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (condition, school, selected_year)
                    )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to get the total number of students in the school
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE age_in_month BETWEEN 61 AND 216 
                             AND school_name = ? 
                             AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                        (school, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch total student count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 5 to 18 years in {school} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students aged 5 to 18 years have {problem}.'

                        # Insert new data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # **Ensure 0 is displayed properly even if no students have the condition**
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students aged 5 to 18 years have {problem}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def weight_age_statistic(weight_category):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query to find students with the specified weight category
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden  
                        FROM student 
                        WHERE weight_age = ?
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (weight_category, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to find the total students aged 2-5 years in the selected year
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (selected_year,)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 2 - 5 years in {selected_year}.'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years are {weight_category}.'

                        # Insert new data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Ensure 0% is displayed correctly when no students match the condition
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students age 2 - 5 years are {weight_category}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            # Consolidated function to handle 'moderately' or 'severely' underweight cases
            def weight_age_area(area, weight_category):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query students by weight category in the selected area
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE weight_age = ? 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (weight_category, area, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students aged 2-5 years in the selected area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Ensure 0% is displayed correctly when no students match the condition
                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 2 - 5 years in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years in {area} are {weight_category}.'

                        # Insert new data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the weight category but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students age 2 - 5 years in {area} are {weight_category}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def height_age_moderate_stunting_area(area):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query students with chronic malnutrition (stunting) in the selected tea garden
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND length_age = 'moderate stunting' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students aged 2-5 years in the selected area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Ensure 0% is displayed correctly when no students match the condition
                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 2 - 5 years in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years in {area} have moderate stunting).'

                        # Insert new data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the weight category but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students age 2 - 5 years in {area} have chronic malnutrition (stunting).'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def height_age_severe_stunting_area(area):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Query students with chronic malnutrition (stunting) in the selected tea garden
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND length_age = 'severe stunting' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students aged 2-5 years in the selected area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Ensure 0% is displayed correctly when no students match the condition
                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 2 - 5 years in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years in {area} have severe stunting).'

                        # Insert new data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the weight category but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students age 2 - 5 years in {area} have chronic malnutrition (stunting).'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)




            def muac_area(area):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                if not area:
                    messagebox.showerror("Error", "Please select an area.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query students with severe acute malnutrition (SAM) in the selected area
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden
                        FROM student 
                        WHERE muac_sam = 'severe acute malnutrition' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students (6-60 months) who were tested for MUAC
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 6 AND 60 
                          AND tea_garden = ? 
                          AND muac_sam IS NOT NULL  -- Ensures only tested students are counted
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Display statistics with proper handling for 0 students
                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 6 - 60 months in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 6 - 60 months in {area} have severe acute malnutrition based on MUAC.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the SAM condition but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students age 6 - 60 months in {area} have severe acute malnutrition based on MUAC.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def weight_height_mam_area(area):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query students with moderate acute malnutrition (MAM) in the selected area
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND weight_height = 'moderate acute malnutrition' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students (24-60 months) in the selected area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Display statistics with proper handling for 0 students
                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 2 - 5 years in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years in {area} have moderate acute malnutrition (measuring wasting).'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the MAM condition but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students age 2 - 5 years in {area} have moderate acute malnutrition (measuring wasting).'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def weight_height_sam_area(area):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query students with Severe Acute Malnutrition (SAM) in the selected area
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden  
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND weight_height = 'severe acute malnutrition' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students (24-60 months) in the selected area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 60 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Handle cases where no data is available
                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 2 - 5 years in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 5 years in {area} have severe acute malnutrition (measuring wasting).'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the SAM condition but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students age 2 - 5 years in {area} have severe acute malnutrition (measuring wasting).'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def B5_Oedema_area(area):
                selected_year = screening_year.get()  # Get the selected screening year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query students with Oedema in the selected area
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden  
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 72 
                          AND B5_Oedema = 'yes' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students (24-72 months) in the selected area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 24 AND 72 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Handle cases where no data is available
                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 2 - 6 years in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students age 2 - 6 years in {area} have Oedema/swelling of legs.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the Oedema condition but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students age 2 - 6 years in {area} have Oedema/swelling of legs.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def vision_problem_school(school):
                print("hello there")  # Debugging statement

                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, School: {school}")

                    # Query students with vision problems
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden  
                        FROM student 
                        WHERE vision_problem = 'yes' 
                          AND school_name = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (school, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students who were tested (either 'yes' or 'no')
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE vision_problem IN ('yes', 'no') 
                          AND school_name = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (school, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Handle cases where no data is available
                    if total_student == 0:
                        statistic_text = f'No screening records found for vision problems in {school} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students tested have vision problems.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students tested have vision problems in {school}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, School: {school}")

            def vision_problem_area(area):
                print("VISION AREA")  # Debugging statement

                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query students with vision problems in the selected area and year
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE vision_problem = 'yes' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query total students who were tested (either 'yes' or 'no')
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE vision_problem IN ('yes', 'no') 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Handle cases where no data is available
                    if total_student == 0:
                        statistic_text = f'No screening records found for vision problems in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students tested have vision problems.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students tested have vision problems in {area}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def statistic_E4_area(area):
                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query female students who have started menstruation in the selected area and year
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                          AND Gender = 'female' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query total female students in the selected area and year
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE Gender = 'female' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Handle cases where no data is available
                    if total_student == 0:
                        statistic_text = f'No screening records found for female students in {area} ({selected_year}).'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of female students have started their menstrual cycle.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of female students have started their menstrual cycle in {area}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def statistic_E5_area(area):
                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query to find female students who have started menstruation and have no period difficulties
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                          AND E5_regularity_period_difficulties = 'Yes' 
                          AND Gender = 'female' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to find total female students who have started menstruation
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                          AND Gender = 'female' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Handle cases where no data is available
                    if total_student == 0:
                        statistic_text = f'No screening records found for female students in {area} ({selected_year}).'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of female students have irregular periods.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of female students have irregular periods in {area}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def statistic_E6_area(area):
                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query to find students with genito-urinary issues (UTI/STI symptoms)
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE E6_UTI_STI = 'yes' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to find the total number of screened students in the selected area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Handle cases where no data is available
                    if total_student == 0:
                        statistic_text = f'No screening records found for students in {area} ({selected_year}).'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of students have pain/burning sensation while urinating.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students have pain/burning sensation while urinating in {area}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def statistic_E7_area(area):
                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query to find students with discharge/foul smell from genito-urinary area
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE E7 = 'yes' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to get the total number of screened students in the selected area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic text
                    if total_student == 0:
                        statistic_text = f'No screening records found for students in {area} ({selected_year}).'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of students have discharge/foul smell from genito-urinary area.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students have discharge/foul smell from genito-urinary area in {area}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def statistic_E8_area(area):
                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}")

                    # Query to find female students with menstrual pain
                    cursor.execute("""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE E8_menstrual_pain = 'yes' 
                          AND Gender = 'female' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    result = cursor.fetchall()
                    statistic_sick = len(result)

                    # Query to get the total number of female students who have started menstruation
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE E4_Menarke = 'yes' 
                          AND Gender = 'female' 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, 7, 2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic text
                    if total_student == 0:
                        statistic_text = f'No screening records found for female students in {area} ({selected_year}).'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of female students that have started menstruation experience menstrual pain.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end", values=(item[0], item[1], item[2], item[3] or "N/A"))

                    # Handle case where no students match the condition but records exist
                    if statistic_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of female students that have started menstruation experience menstrual pain in {area}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}")

            def statistic_BMI_area(sickness, condition, area, problem):
                """Process and display statistics for students with a specific condition in a given area and year."""

                selected_year = screening_year.get()  # Get the selected year

                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Debugging output
                    print(f"Selected Year: {selected_year}, Area: {area}, Problem: {problem}")

                    # Dynamically fetch column names to prevent SQL injection
                    cursor.execute("PRAGMA table_info(student)")
                    valid_columns = {row[1] for row in cursor.fetchall()}  # Fetch all column names

                    if sickness not in valid_columns:
                        messagebox.showerror("Error", f"Invalid column: {sickness}", parent=statistic_window)
                        return

                    # Query to find students with the specified condition
                    query_sick_students = f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE {sickness} = ? 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, -2) = ?"""
                    cursor.execute(query_sick_students, (condition, area, selected_year))
                    result = cursor.fetchall()
                    total_sick = len(result)

                    # Query to get the total number of students in the specified area
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE age_in_month BETWEEN 61 AND 216 
                          AND tea_garden = ? 
                          AND '20' || SUBSTR(screen_date, -2) = ?""",
                                   (area, selected_year)
                                   )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Determine statistic text
                    if total_student == 0:
                        statistic_text = f'No screening records found for students aged 5 to 18 years in {area} ({selected_year}).'
                    else:
                        percentage = round((total_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({total_sick} / {total_student}) of students aged 5 to 18 years have {problem}.'

                        # Insert data into the Treeview
                        for item in result:
                            show_record_tree.insert("", "end",
                                                    values=(item[0], item[1], item[2], item[3] if item[3] else "N/A"))

                    # Handle case where no students match the condition but records exist
                    if total_sick == 0 and total_student > 0:
                        statistic_text = f'0% (0 / {total_student}) of students aged 5 to 18 years have {problem}.'

                    # Update the statistic label
                    statistic_label.config(text=statistic_text)

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

                print(f"Function executed successfully - Year: {selected_year}, Area: {area}, Problem: {problem}")

            def handle_area_record(area, sickness, problem):
                """Process and display statistics for students with a specific sickness in a given tea garden and year."""

                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a year is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Dynamically fetch all column names from the database to validate sickness column
                    cursor.execute("PRAGMA table_info(student)")
                    valid_columns = {row[1] for row in cursor.fetchall()}  # Fetch all column names

                    # Check if the sickness column exists in the database
                    if sickness not in valid_columns:
                        messagebox.showerror("Error", f"Invalid sickness column: {sickness}", parent=statistic_window)
                        return

                    # Query to count total students in the specified tea garden
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE tea_garden = ? 
                           AND '20' || SUBSTR(screen_date, -2) = ?""",
                        (area, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Query to count students with the specified sickness
                    query_sick_count = f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE {sickness} = ? 
                        AND tea_garden = ? 
                        AND '20' || SUBSTR(screen_date, -2) = ?
                    """
                    cursor.execute(query_sick_count, ("yes", area, selected_year))
                    statistic_sick = cursor.fetchone()[0]  # Fetch count directly

                    # Query to get the list of students with the sickness
                    query_sick_students = f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE {sickness} = ? 
                        AND tea_garden = ? 
                        AND '20' || SUBSTR(screen_date, -2) = ?
                    """
                    cursor.execute(query_sick_students, ("yes", area, selected_year))
                    result = cursor.fetchall()

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Ensure total_student is never zero to avoid division by zero
                    if total_student == 0:
                        statistic_text = f'No students recorded in {area} for {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of students have {problem} in {area}.'

                    # Update the existing label (assuming `statistic_label` is defined elsewhere)
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview (if no records, it remains empty)
                    for item in result:
                        show_record_tree.insert("", "end",
                                                values=(item[0], item[1], item[2], item[3] if item[3] else "N/A"))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)

            def handle_area_record(area, sickness, problem):
                """Process and display statistics for students with a specific sickness in a given tea garden and year."""

                selected_year = screening_year.get()  # Get the selected screening date from the combobox

                # Check if a year is selected
                if not selected_year:
                    messagebox.showerror("Error", "Please select a year.", parent=statistic_window)
                    return

                try:
                    # Dynamically fetch all column names from the database to validate sickness column
                    cursor.execute("PRAGMA table_info(student)")
                    valid_columns = {row[1] for row in cursor.fetchall()}  # Fetch all column names

                    # Check if the sickness column exists in the database
                    if sickness not in valid_columns:
                        messagebox.showerror("Error", f"Invalid sickness column: {sickness}", parent=statistic_window)
                        return

                    # Query to count total students in the specified tea garden
                    cursor.execute(
                        """SELECT COUNT(*) 
                           FROM student 
                           WHERE tea_garden = ? 
                           AND '20' || SUBSTR(screen_date, -2) = ?""",
                        (area, selected_year)
                    )
                    total_student = cursor.fetchone()[0]  # Fetch count directly

                    # Query to count students with the specified sickness
                    query_sick_count = f"""
                        SELECT COUNT(*) 
                        FROM student 
                        WHERE {sickness} = ? 
                        AND tea_garden = ? 
                        AND '20' || SUBSTR(screen_date, -2) = ?
                    """
                    cursor.execute(query_sick_count, ("yes", area, selected_year))
                    statistic_sick = cursor.fetchone()[0]  # Fetch count directly

                    # Query to get the list of students with the sickness
                    query_sick_students = f"""
                        SELECT id, name, school_name, tea_garden 
                        FROM student 
                        WHERE {sickness} = ? 
                        AND tea_garden = ? 
                        AND '20' || SUBSTR(screen_date, -2) = ?
                    """
                    cursor.execute(query_sick_students, ("no", area, selected_year))
                    result = cursor.fetchall()

                    # Clear previous entries in the Treeview
                    show_record_tree.delete(*show_record_tree.get_children())

                    # Ensure total_student is never zero to avoid division by zero
                    if total_student == 0:
                        statistic_text = f'No students recorded in {area} for {selected_year}.'
                    else:
                        percentage = round((statistic_sick / total_student) * 100, 1)
                        statistic_text = f'{percentage}% ({statistic_sick} / {total_student}) of students have {problem} in {area}.'

                    # Update the existing label (assuming `statistic_label` is defined elsewhere)
                    statistic_label.config(text=statistic_text)

                    # Insert new data into the Treeview (if no records, it remains empty)
                    for item in result:
                        show_record_tree.insert("", "end",
                                                values=(item[0], item[1], item[2], item[3] if item[3] else "N/A"))

                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}", parent=statistic_window)



            # Dictionary to map records to their corresponding function
            function_mapping_all_schools = {
                "Weight for age: moderately underweight": lambda: weight_age_statistic("moderately underweight"),
                "Weight for age: severely underweight": lambda: weight_age_statistic("severely underweight"),
                "Height for age: moderate stunting": height_age_moderate_stunting_all,
                "Height for age: severe stunting": height_age_severe_stunting_all,
                "Weight for height: moderate acute malnutrition": lambda: weight_height_statistic("moderate acute malnutrition"),
                "Weight for height: severe acute malnutrition": lambda: weight_height_statistic("severe acute malnutrition"),
                "Weight for height: overweight": lambda: weight_height_statistic(
                    "overweight"),
                "Weight for height: obese": lambda: weight_height_statistic(
                    "obese"),

                "Vision problem (objective)": vision_problem_all,
                "BMI severe underweight": lambda: statistic_bmi("severe underweight"),
                "BMI underweight": lambda: statistic_bmi("underweight"),
                "BMI overweight": lambda: statistic_bmi("overweight"),
                "BMI obese": lambda: statistic_bmi("obese"),
                "Has not done deworming": lambda: statistic_all_no(sickness="deworming", problem="been dewormed last 6 months"),
                "Has not done immunization": lambda: statistic_all_no(sickness="vaccination",
                                                                                 problem="been in Government Childhood Vaccination Program"),
                "B1: signs of anemia": lambda: statistic_all(sickness="B1_severe_anemia", problem="signs of anemia"),
                "B2: signs of Vit. A deficiency": lambda: statistic_all(sickness="B2_Vita_A_deficiency",
                                                              problem="signs of Vit A deficiency"),
                "B3: signs of Vit D deficiency": lambda: statistic_all(sickness="B3_Vit_D_deficiency",
                                                             problem="signs of Vit D deficiency"),
                "B4: goitre": lambda: statistic_all(sickness="B4_Goitre", problem="goitre"),
                "B5: oedema": B5_Oedema_all,
                "C1: Convulsive disorder": lambda: statistic_all(sickness="C1_convulsive_dis",
                                                           problem="convulsive disorder"),
                "C2: Otitis media/ear infection": lambda: statistic_all(sickness="C2_otitis_media", problem="otitis media/ear infection"),
                "C3: Dental problem": lambda: statistic_all(sickness="C3_dental_condition",
                                                             problem="dental problem"),
                "C4: Skin problem": lambda: statistic_all(sickness="C4_skin_condition", problem="skin problem"),
                "C5: Heart murmur": lambda: statistic_all(sickness="C5_rheumatic_heart_disease",
                                                                    problem="heart murmur"),
                "C6: Respiratory problem": lambda: statistic_all(sickness="C6_others_TB_asthma", problem="respiratory problem"),
                "D1: Difficulty seeing": lambda: statistic_all(sickness="D1_difficulty_seeing",
                                                              problem="difficulty seeing"),
                "D2: Delay in walking": lambda: statistic_all(sickness="D2_delay_in_walking", problem="delay in  walking"),
                "D3: Stiffness/floppiness/reduced strength": lambda: statistic_all(sickness="D3_stiffness_floppiness",
                                                                 problem="stiffness/floppiness/reduced strength"),

                "D5: Difficulty in reading/writing/calculating": lambda: statistic_all(
                    sickness="D5_reading_writing_calculatory_difficulty",
                    problem="difficulty in reading/writing/calculating"),
                "D6: Difficulty speaking": lambda: statistic_all(sickness="D6_speaking_difficulty",
                                                                problem="difficulty speaking"),
                "D7: Difficulty hearing": lambda: statistic_all(sickness="D7_hearing_problems",
                                                             problem="difficulty hearing"),
                "D8: Difficulty in learning new things": lambda: statistic_all(sickness="D8_learning", problem="difficulty in learning new things"),
                "D9: Difficulty sustaining attention": lambda: statistic_all(sickness="D9_attention", problem="difficulty sustaining attention"),
                "E3: Signs of depression": lambda: statistic_all(sickness="E3_depression_sleep",
                                                             problem="depression or sleep problems"),
                "E4: Started period (menarche)": statistic_E4_all,
                "E5: Has irregular period": statistic_E5_all,
                "E6: Has pain or burning while urinating": statistic_E6_all,
                "E7: Has discharge/ foul smell from genito-urinary area": statistic_E7_all,
                "E8: Has menstrual pain": statistic_E8_all,
                "MUAC: Have SAM based on MUAC": muac_all}
            function_mapping_school_specific = {
                "Weight for age: moderately underweight": lambda school: weight_age_mu_school(school),
                "Weight for age: severely underweight": lambda school: weight_age_su_school(school),

                "Height for age: moderate stunting": lambda school: height_age_moderate_stunting_school(school),
                "Height for age: severe stunting": lambda school: height_age_severe_stunting_school(school),

                "Weight for height: moderate acute malnutrition": lambda school: weight_height_mam_school(school),
                "Weight for height: severe acute malnutrition": lambda school: weight_height_sam_school(school),
                "Vision problem (objective)": lambda school: vision_problem_school(school),
                "BMI severe underweight": lambda school: statistic_BMI('BMI_category', 'severe underweight', school, "severe underweight"),
                "BMI underweight": lambda school: statistic_BMI('BMI_category', 'underweight', school,
                                                                       "underweight"),
                "BMI overweight": lambda school: statistic_BMI('BMI_category', 'overweight', school, 'overweight'),
                "BMI obese": lambda school: statistic_BMI('BMI_category', 'obese', school, 'obese'),
                "Has not done deworming": lambda school: handle_school_record_no(school, "deworming", "been dewormed last 6 months"),
                "Has not  done immunization": lambda school: handle_school_record_no(school, "vaccination",
                                                                                               "been in Government Childhood Vaccination Program"),
                "B1: signs of anemia": lambda school: handle_school_record(school, "B1_severe_anemia", "severe anemia"),
                "B2: signs of Vit. A deficiency": lambda school: handle_school_record(school, "B2_Vita_A_deficiency",
                                                                            "signs of Vit. A deficiency"),
                "B3: signs of Vit D deficiency": lambda school: handle_school_record(school, "B3_Vit_D_deficiency",
                                                                           "signs of Vit. D deficiency"),
                "B4: goitre": lambda school: handle_school_record(school, "B4_Goitre", "goitre"),
                "B5: oedema": lambda school: B5_Oedema_school(school),
                "C1: Convulsive disorder": lambda school: handle_school_record(school, "C1_convulsive_dis",
                                                                         "convulsive disorder"),
                "C2: Otitis media/ear infection": lambda school: handle_school_record(school, "C2_otitis_media", "otitis media/ear infection"),
                "C3: Dental problem": lambda school: handle_school_record(school, "C3_dental_condition",
                                                                           "dental problem"),
                "C4: Skin problem": lambda school: handle_school_record(school, "C4_skin_condition", "skin problem"),
                "C5: Heart murmur": lambda school: handle_school_record(school, "C5_rheumatic_heart_disease",
                                                                                  "heart murmur"),
                "C6: Respiratory problem": lambda school: handle_school_record(school, "C6_others_TB_asthma",
                                                                           "respiratory problem"),
                "D1: Difficulty seeing": lambda school: handle_school_record(school, "D1_difficulty_seeing",
                                                                            "difficulty seeing"),
                "D2: Delay in walking": lambda school: handle_school_record(school, "D2_delay_in_walking",
                                                                           "delay in walking"),
                "D3: Stiffness/floppiness/reduced strength": lambda school: handle_school_record(school, "D3_stiffness_floppiness",
                                                                               "stiffness/floppiness/reduced strength"),

                "D5: Difficulty in reading/writing/calculating": lambda school: handle_school_record(school,
                                                                                                 "D5_reading_writing_calculatory_difficulty",
                                                                                                 "difficulty in reading/writing/calculationg"),
                "D6: Difficulty speaking": lambda school: handle_school_record(school, "D6_speaking_difficulty",
                                                                              "difficulty in speaking"),
                "D7: Difficulty hearing": lambda school: handle_school_record(school, "D7_hearing_problems",
                                                                           "difficulty hearing"),
                "D8: Difficulty in learning new things": lambda school: handle_school_record(school, "D8_learning", "difficulty learning new things"),
                "D9: Difficulty sustaining attention": lambda school: handle_school_record(school, "D9_attention", "difficulty sustaining attention"),
                "E3: Signs of depression": lambda school: handle_school_record(school, "E3_depression_sleep",
                                                                           "depression or sleep problems"),
                "E4: Started period (menarche)": lambda school: statistic_E4_school(school),
                "E5: Has irregular period": lambda school: statistic_E5_school(school),
                "E6: Has pain or burning while urinating": lambda school: statistic_E6_school(school),
                "E7: Has discharge/ foul smell from genito-urinary area": lambda school: statistic_E7_school(school),
                "E8: Has menstrual pain": lambda school: statistic_E8_school(school),
                "MUAC: Have SAM based on MUAC": lambda school: muac_school(school)}

            function_mapping_area_specific = {
                "Weight for age: moderately underweight": lambda area: print(
                    "Moderately Underweight") or weight_age_area(area, "moderately underweight"),
                "Weight for age: severely underweight": lambda area: print("Severely Underweight") or weight_age_area(
                    area, "severely underweight"),
                "Height for age: chronic malnutrition": lambda area: height_age_moderate_stunting_area(area),
                "Height for age: chronic malnutrition": lambda area: height_age_severe_stunting_area(area),
                "Weight for height: moderate acute malnutrition": lambda area: weight_height_mam_area(area),
                "Weight for height: severe acute malnutrition": lambda area: weight_height_sam_area(area),
                "VISION_problem": lambda area: vision_problem_area(area),
                "BMI severe underweight": lambda area: statistic_BMI_area('BMI_category', 'severe underweight', area,
                                                                     "severe underweight"),
                "BMI underweight": lambda area: statistic_BMI_area('BMI_category', 'underweight', area, "underweight"),
                "BMI overweight": lambda area: statistic_BMI_area('BMI_category', 'overweight', area, 'overweight'),
                "BMI obese": lambda area: statistic_BMI_area('BMI_category', 'obese', area, 'obese'),
                "Has not done deworming": lambda area: handle_area_record(area, "deworming", "been dewormed last 6 months"),
                "Has not done immunization": lambda area: handle_area_record(area, "vaccination",
                                                                                           "been in Government Childhood Vaccination Program"),
                "B1: signs of anemia": lambda area: handle_area_record(area, "B1_severe_anemia", "signs of anemia"),
                "B2: signs of Vit. A deficiency": lambda area: handle_area_record(area, "B2_Vita_A_deficiency",
                                                                        "Vitamin A deficiency"),
                "B3: signs of Vit D deficiency": lambda area: handle_area_record(area, "B3_Vit_D_deficiency",
                                                                       "Vitamin D deficiency"),
                "B4: goitre": lambda area: handle_area_record(area, "B4_Goitre", "Goitre"),
                "B5: oedema": lambda area: B5_Oedema_area(area),
                "C1: Convulsive disorder": lambda area: handle_area_record(area, "C1_convulsive_dis",
                                                                     "convulsive disorders/epilepsy"),
                "C2: Otitis media/ear infection": lambda area: handle_area_record(area, "C2_otitis_media", "otitis media"),
                "C3: Dental problem": lambda area: handle_area_record(area, "C3_dental_condition", "dental condition"),
                "C4: Skin problem": lambda area: handle_area_record(area, "C4_skin_condition", "skin condition"),
                "C5: Heart murmur": lambda area: handle_area_record(area, "C5_rheumatic_heart_disease",
                                                                              "heart murmur"),
                "C6: Respiratory problem": lambda area: handle_area_record(area, "C6_others_TB_asthma", "breathing difficulty"),
                "D1: Difficulty seeing": lambda area: handle_area_record(area, "D1_difficulty_seeing",
                                                                        "difficulty seeing"),
                "D2: Delay in walking": lambda area: handle_area_record(area, "D2_delay_in_walking", "delay walking"),
                "D3: Stiffness/floppiness/reduced strength": lambda area: handle_area_record(area, "D3_stiffness_floppiness",
                                                                           "stiffness or floppiness"),
                "D5: Difficulty in reading/writing/calculating": lambda area: handle_area_record(area,
                                                                                             "D5_reading_writing_calculatory_difficulty",
                                                                                             "reading/writing or calculatory difficulty"),
                "D6: Difficulty speaking": lambda area: handle_area_record(area, "D6_speaking_difficulty",
                                                                          "speaking difficulty"),
                "D7: Difficulty hearing": lambda area: handle_area_record(area, "D7_hearing_problems", "hearing problems"),
                "D8: Difficulty in learning new things": lambda area: handle_area_record(area, "D8_learning", "learning problems"),
                "D9: Difficulty sustaining attention": lambda area: handle_area_record(area, "D9_attention", "attention problems"),
                "E3: Signs of depression": lambda area: handle_area_record(area, "E3_depression_sleep",
                                                                       "depression or sleep problems"),
                "E4: Started period (menarche)": lambda area: statistic_E4_area(area),
                "E5: Has irregular period": lambda area: statistic_E5_area(area),
                "E6: Has pain or burning while urinating": lambda area: statistic_E6_area(area),
                "E7: Has discharge/ foul smell from genito-urinary area": lambda area: statistic_E7_area(area),
                "E8: Has menstrual pain": lambda area: statistic_E8_area(area),
                "MUAC: Have SAM based on MUAC": lambda area: muac_area(area)}


            # General function to handle the record based on the school
            def process_record(selected_key, school_selected=None, area_selected=None):
                print(
                    f"Selection: School={school_selected}, Area={area_selected}, Key={selected_key}")  # Debugging line

                if area_selected:
                    # Map selected_key to area-specific functions
                    function_to_call = function_mapping_area_specific.get(selected_key)
                    if function_to_call:
                        function_to_call(area_selected)  # Call with area argument
                    else:
                        print(f"No function mapped for {selected_key} in area {area_selected}")
                elif school_selected == "All schools combined":
                    # Call for all schools without a specific argument
                    function_to_call = function_mapping_all_schools.get(selected_key)
                    if function_to_call:
                        function_to_call()
                    else:
                        print(f"No function mapped for {selected_key} in All schools combined")
                elif school_selected:
                    # Map selected_key to school-specific functions
                    function_to_call = function_mapping_school_specific.get(selected_key)
                    if function_to_call:
                        function_to_call(school_selected)
                    else:
                        print(f"No function mapped for {selected_key} in {school_selected}")
                else:
                    print(
                        "No valid selection for area or school.")  # Handle case where neither area nor school is selected

            # Get user selection from the Comboboxes
            # Get user selection from the Comboboxes
            selected_sickness = sickness_search.get()
            selected_school = school_options.get()  # Get selected school, if any
            selected_area = area_options.get()  # Get selected area, if any

            # Check if selected_school is empty and set to "All schools combined"
            if selected_school == "":
                selected_school = "All schools combined"

            # Call the process_record function with the selected sickness, school, or area
            if selected_area:
                process_record(selected_sickness, area_selected=selected_area)
            elif selected_school:
                process_record(selected_sickness, school_selected=selected_school)
            else:
                print("No area or school selected, cannot process the record.")

            # SET UP WINDOW
        statistic_window = Toplevel(window)
        connection = sqlite3.connect("gracehealth.db")
        cursor = connection.cursor()

        statistic_window.geometry("1450x750+1+1")
        statistic_window.title("Getting information from students")

        #SET UP FRAMES
        topframe = Frame(statistic_window)
        topframe.grid(row=1, rowspan=3)
        secondframe = Frame(statistic_window)
        secondframe.grid(row=4)
        from tkinter import StringVar
        from tkinter import ttk

        # Create a StringVar for storing the selected sickness
        sickness_search = StringVar()

        # List of options for the Combobox
        sickness_options = [
            "Weight for age: moderately underweight",
            "Weight for age: severely underweight",
            "Height for age: moderate stunting",
            "Height for age: severe stunting",
            "Weight for height: moderate acute malnutrition",
            "Weight for height: severe acute malnutrition",
            "Weight for height: overweight",
            "Weight for height: obese",

            "BMI severe underweight",
            "BMI underweight",
            "BMI overweight",
            "BMI obese",
            "MUAC: Have SAM based on MUAC",
            "Vision problem (objective)",
            "B1: signs of anemia",
            "B2: signs of Vit. A deficiency",
            "B3: signs of Vit D deficiency",
            "B4: goitre",
            "B5: oedema",
            "C1: Convulsive disorder",
            "C2: Otitis media/ear infection",
            "C3: Dental problem",
            "C4: Skin problem",
            "C5: Heart murmur",
            "C6: Respiratory problem",
            "D1: Difficulty seeing",
            "D2: Delay in walking",
            "D3: Stiffness/floppiness/reduced strength",
            "D5: Difficulty in reading/writing/calculating",
            "D6: Difficulty speaking",
            "D7: Difficulty hearing",
            "D8: Difficulty in learning new things",
            "D9: Difficulty sustaining attention",
            "E3: Signs of depression",
            "E4: Started period (menarche)",
            "E5: Has irregular period",
            "E6: Has pain or burning while urinating",
            "E7: Has discharge/ foul smell from genito-urinary area",
            "E8: Has menstrual pain",
            "Has not done deworming",
            "Has not done immunization",

        ]

        def reset_other_combobox(selected_combobox):
            # Clear the opposite combobox based on the selected combobox
            if selected_combobox == "school":
                area_options.set("")  # Clear area combobox if school is selected
            elif selected_combobox == "area":
                school_options.set("")  # Clear school combobox if area is selected
        # Create a Combobox
        sickness_combo = ttk.Combobox(topframe, textvariable=sickness_search, values=sickness_options,width=50)
        sickness_combo.grid(row=1, column=2)

        # Optionally set a default value
        sickness_combo.current(0)  # Set the first item as default
        school_label = Label(topframe, text="SCHOOL:   ").grid(row=2, column=1)


        school_options = ttk.Combobox(topframe,values=school_database_list,width=50)
        school_options.grid(row=2, column=2)
        school_options.bind("<<ComboboxSelected>>", lambda e: reset_other_combobox("school"))

        area_label = Label(topframe, text="AREA:   ").grid(row=3, column=1)

        area_options = ttk.Combobox(topframe, values=tea_garden_database_list, width=50)
        area_options.grid(row=3, column=2)
        area_options.bind("<<ComboboxSelected>>", lambda e: reset_other_combobox("area"))


        # Function to populate the Combobox with screening dates from the database
        from datetime import datetime

        def populate_screening_years():
            try:
                # Connect to the database
                connection = sqlite3.connect("gracehealth.db")
                cursor = connection.cursor()

                # Query to extract the year from the mm/dd/yy format using SUBSTR
                cursor.execute("""
                    SELECT DISTINCT '20' || SUBSTR(screen_date, -2) as year
                    FROM student
                    WHERE screen_date LIKE '__/__/__'
                    ORDER BY year DESC
                """)

                years = cursor.fetchall()

                if not years:
                    print("No years found in the database.")
                else:
                    print("Years fetched:", years)  # Debugging

                # Extract the years from the fetched tuples and populate the list
                year_list = [year[0] for year in years]

                # Close the database connection
                connection.close()

                # Populate the combobox with the retrieved years
                screening_year['values'] = year_list
                if year_list:
                    screening_year.current(0)  # Optionally select the most recent year by default
                else:
                    screening_year['values'] = ['No data available']  # Handle the case where no years are found
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Error: {e}")


        # Function to generate the summary statistics

        # Screening year label
        screening_label = Label(topframe, text="Screening Year:")
        screening_label.grid(row=0, column=1)

        # Create a Combobox for screening years
        screening_year = ttk.Combobox(topframe, width=50)
        screening_year.grid(row=0, column=2)





        # Call the process_record function with the selected sickness and school

        # Populate the screening year combobox
        populate_screening_years()

        # Run the main event loop
        search_label = Label(topframe, text="Parameters:   ")
        search_label.grid(row=1, column=1)
        statistic_label = Label(topframe, text="")  # Initially empty
        statistic_label.grid(row=4, column=1,columnspan=3)
        from tkinter import ttk
        # Create a Treeview widget
        show_record_tree = ttk.Treeview(secondframe, columns=("id", "name", "school", "area"), show='headings',
                                        height=10)
        show_record_tree.grid(row=5, column=1, padx=20, pady=10)
        # Define column headings
        show_record_tree.heading("id", text="ID")
        show_record_tree.heading("name", text="Name")
        show_record_tree.heading("school", text="School")
        show_record_tree.heading("area", text="Area")
        # Set column widths
        show_record_tree.column("id", width=100, anchor='center')
        show_record_tree.column("name", width=150, anchor='w')
        show_record_tree.column("school", width=350, anchor='w')
        show_record_tree.column("area", width=300, anchor='center')
        # Example: populate Treeview with data (fetch this data from your database)
        # If you want to delete previous entries and refresh the Treeview before inserting new records:
        show_button = ttk.Button(topframe, text="show record", command=show_record_function)
        show_button.grid(row=3, column=3, columnspan=2)

        connection.commit()
        connection.close()
        statistic_window.mainloop()

    from tkinter import Tk, Toplevel, Frame, Canvas, Scrollbar, Button, Label, BOTH, LEFT, RIGHT, Y, VERTICAL, W
    def create_scrollable_frame(parent):
        # Create a frame for the canvas and scrollbar
        container = Frame(parent)
        container.pack(fill=BOTH, expand=True)

        # Create a canvas
        canvas = Canvas(container)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Create a frame inside the canvas to hold the widgets
        scrollable_frame = Frame(canvas)

        # Add that new frame to a window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        return scrollable_frame

    # Main window setup
    import tkinter as tk
    from tkinter import ttk
    import sqlite3

    # Initialize the main window
    import tkinter as tk
    from tkinter import ttk
    import tkinter as tk
    from tkinter import ttk

    # Initialize the main window
    window = tk.Tk()
    window.title("Create new student journals")

    # Set window size to 90% of the screen dimensions for better scaling on smaller screens
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = int(screen_width)
    window_height = int(screen_height * 0.9)
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{5}+{5}")

    # Configure the window grid
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)

    # Create a Canvas and Scrollbars for a scrollable frame
    canvas = tk.Canvas(window)
    h_scrollbar = ttk.Scrollbar(window, orient="horizontal", command=canvas.xview)
    v_scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Configure canvas scrolling
    canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

    # Place scrollbars and canvas in the main window
    canvas.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    # Add the scrollable frame inside the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Update the scroll region whenever the scrollable frame's size changes
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Updated create_labeled_frame function to accept rowspan
    def create_labeled_frame(parent, text, row, col, colspan=1, rowspan=1, sticky="ew"):
        frame = ttk.LabelFrame(parent, text=text)
        frame.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=sticky, padx=10, pady=5)
        return frame

    # Fixed buttonframe (does not expand vertically)
    buttonframe = create_labeled_frame(scrollable_frame, "Button Frame", 0, 0, colspan=2, sticky="ew")

    # Expanding frames below the buttonframe
    topframe = create_labeled_frame(scrollable_frame, "Top Frame", 1, 0, colspan=2, sticky="nsew")
    secondframe = create_labeled_frame(scrollable_frame, "Second Frame", 2, 0, colspan=2, sticky="nsew")
    sicknessframe = create_labeled_frame(scrollable_frame, "Sickness Frame", 3, 0, colspan=2, sticky="nsew")

    # Journal Summary Frame on the right side, spans 4 rows
    summary_frame = create_labeled_frame(scrollable_frame, "Journal Summary", 0, 2, rowspan=4, sticky="nsew")

    # Configure the row for buttonframe to be fixed
    scrollable_frame.grid_rowconfigure(0, weight=0)

    # Configure rows below buttonframe to expand
    scrollable_frame.grid_rowconfigure(1, weight=1)
    scrollable_frame.grid_rowconfigure(2, weight=1)
    scrollable_frame.grid_rowconfigure(3, weight=1)

    # Configure columns to separate summary_frame from others
    scrollable_frame.grid_columnconfigure(0, weight=1)  # Left side expands
    scrollable_frame.grid_columnconfigure(1, weight=1)
    scrollable_frame.grid_columnconfigure(2, weight=1)  # Summary frame column expands independently

    # Text widget in summary frame
    journal_summary_text = tk.Text(summary_frame, height=10,width=40)
    journal_summary_text.grid(row=0, column=0, sticky="nsew")
    journal_summary_text.insert(tk.END, "Summary text")
    journal_summary_text.config(state=tk.DISABLED)

    # Ensure the summary frame fills remaining space independently
    summary_frame.grid_rowconfigure(0, weight=1)
    summary_frame.grid_columnconfigure(0, weight=1)



    connection = sqlite3.connect("gracehealth.db")
    cursor = connection.cursor()

    import sqlite3
    import tkinter as tk
    from tkinter import ttk, messagebox

    import sqlite3
    import tkinter as tk
    from tkinter import Toplevel, messagebox, ttk, Frame, LabelFrame

    def school_list():
        def edit_last_journal():
            selected_item = tree.selection()
            if not selected_item:
                return
            item_id = tree.item(selected_item[0], 'values')[0]
            clear_text()
            populate_for_edit(item_id)
            display_journal(item_id, summary_frame)
            school_window.destroy()

        def add_journal():
            selected_item = tree.selection()
            if not selected_item:
                return
            item_id = tree.item(selected_item[0], 'values')[0]
            clear_text()

            populate_for_new_journal(item_id)
            display_journal(item_id, summary_frame)
            school_window.destroy()

        def delete_row():
            selected_item = tree.focus()
            if selected_item:
                confirmation = messagebox.askyesno(parent=school_window,
                                                   message="Are you sure you want to delete this student?")
                if confirmation:
                    connection = sqlite3.connect("gracehealth.db")
                    cursor = connection.cursor()
                    row_id = tree.item(selected_item)['values'][0]
                    cursor.execute("DELETE FROM student WHERE id=?", (row_id,))
                    connection.commit()
                    connection.close()
                    refresh_records()  # Refresh the Treeview
                    messagebox.showinfo(parent = main_window_school_list,title="Success",message= "Row deleted successfully")
            else:
                messagebox.showwarning(parent = main_window_school_list,title="Warning",message= "Please select a row to delete")

        def flag_as_graduated():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a student to flag as graduated.")
                return
            item_id = tree.item(selected_item[0], 'values')[0]
            confirmation = messagebox.askyesno(parent=school_window,
                                               message="Are you sure you want to flag this student as 'Graduated'?")
            if confirmation:
                try:
                    connection = sqlite3.connect('gracehealth.db')
                    cursor = connection.cursor()
                    cursor.execute("UPDATE student SET status = 'graduated' WHERE id = ?", (item_id,))
                    connection.commit()
                    connection.close()
                    refresh_records()  # Refresh the Treeview after update
                    messagebox.showinfo(parent=school_window,title="Success", message="Student flagged as 'Graduated'.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating status: {e}")

        def change_to_active():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a student to change status to active.")
                return
            item_id = tree.item(selected_item[0], 'values')[0]
            confirmation = messagebox.askyesno(parent=school_window,
                                               message="Are you sure you want to change this student's status to 'Active'?")
            if confirmation:
                try:
                    connection = sqlite3.connect('gracehealth.db')
                    cursor = connection.cursor()
                    cursor.execute("UPDATE student SET status = 'active' WHERE id = ?", (item_id,))
                    connection.commit()
                    connection.close()
                    refresh_records()  # Refresh the Treeview after update
                    messagebox.showinfo(parent=school_window,title="Success",message= "Student status changed to 'Active'.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating status: {e}")

        def on_filter_change(event):
            refresh_records(
                school_name_filter=school_name_var.get(),
                gender_filter=gender_filter_var.get(),
                student_name_filter=search_name_entry.get(),
                status_filter=status_filter_var.get(),
                area_filter=area_filter_var.get(),
                age_filter=age_filter_var.get(),
                class_filter=class_filter_var.get(),
                year_filter=year_filter_var.get(),
                id_filter=id_filter_var.get().strip()  # Add ID filter
            )

        school_window = Toplevel(window)
        school_window.geometry("1500x600+10+10")

        frame = Frame(school_window)
        frame.place(x=100, y=70)
        frame2 = LabelFrame(school_window)
        frame2.place(x=100, y=20)
        frame3 = LabelFrame(school_window)
        frame3.place(x=100, y=550)

        tree = ttk.Treeview(frame, columns=("ID", "Name", "School Name", "Gender","SL NO"), show="headings", height=20)
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("School Name", text="School Name")
        tree.heading("Gender", text="Gender")
        tree.heading("SL NO", text="SL NO")
        tree.column("ID", width=100, anchor="center")
        tree.column("Name", width=200, anchor="w")
        tree.column("School Name", width=300, anchor="w")
        tree.column("Gender", width=100, anchor="center")
        tree.column("SL NO", width=50, anchor="center")
        tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(frame, command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.config(yscrollcommand=scrollbar.set)

        edit_journal_button = ttk.Button(frame3, text="Edit last screening", command=edit_last_journal)
        edit_journal_button.grid(row=0, column=0, padx=10)
        add_journal_button = ttk.Button(frame3, text="Add new screening", command=add_journal)
        add_journal_button.grid(row=0, column=1)

        flag_graduated_button = ttk.Button(frame3, text="Flag as Graduated", command=flag_as_graduated)
        flag_graduated_button.grid(row=0, column=2, padx=10)

        delete_button = ttk.Button(frame3, text="Delete", command=delete_row)
        delete_button.grid(row=0, column=3, padx=10)

        change_active_button = ttk.Button(frame3, text="Change to Active", command=change_to_active)
        change_active_button.grid(row=0, column=4, padx=10)

        search_label = tk.Label(frame2, text="Search School Name")
        search_label.grid(row=1, column=0, sticky='w')

        connection = sqlite3.connect('gracehealth.db')
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT school_name FROM student")
        school_names = [row[0] for row in cursor.fetchall()]
        school_names.append("All students")

        cursor.execute("SELECT DISTINCT tea_garden FROM student")
        area_list = [row[0] for row in cursor.fetchall()]
        area_list.append("All areas")
        connection.close()

        # Add a new combobox for area filter in frame2
        area_filter_var = tk.StringVar(value="All areas")
        area_filter_label = tk.Label(frame2, text="Filter by Area:")
        area_filter_label.grid(row=1, column=4, sticky='w')

        area_filter_combobox = ttk.Combobox(frame2, textvariable=area_filter_var, values=area_list, width=20)
        area_filter_combobox.grid(row=2, column=4)
        area_filter_combobox.bind("<<ComboboxSelected>>", on_filter_change)
        school_name_var = tk.StringVar()  # Define the variable

        search_school_entry = ttk.Combobox(frame2, textvariable=school_name_var, values=school_names, width=50)
        search_school_entry.grid(row=1, column=1)
        search_school_entry.bind("<<ComboboxSelected>>", on_filter_change)

        name_search_label = tk.Label(frame2, text="Search Student Name")
        name_search_label.grid(row=2, column=0, sticky='w')
        search_name_entry = ttk.Entry(frame2, width=50)
        search_name_entry.grid(row=2, column=1)
        search_name_entry.bind("<KeyRelease>", on_filter_change)

        id_filter_var = tk.StringVar()
        id_filter_label = tk.Label(frame2, text="Search by ID:")
        id_filter_label.grid(row=3, column=0, sticky='w')

        id_filter_entry = ttk.Entry(frame2, width=50, textvariable=id_filter_var)  # Use textvariable
        id_filter_entry.grid(row=3, column=1)
        id_filter_entry.bind("<KeyRelease>", on_filter_change)  # Ensure dynamic searching

        gender_filter_var = tk.StringVar(value="all")
        gender_filter_label = tk.Label(frame2, text="Select Gender:")
        gender_filter_label.grid(row=1, column=2, sticky='w')

        gender_filter_combobox = ttk.Combobox(frame2, textvariable=gender_filter_var, values=["all", "male", "female"],
                                              width=20)
        gender_filter_combobox.grid(row=2, column=2)
        gender_filter_combobox.bind("<<ComboboxSelected>>", on_filter_change)

        age_filter_var = tk.StringVar(value="All ages")
        age_filter_label = tk.Label(frame2, text="Filter by Age (Years):")
        age_filter_label.grid(row=1, column=5, sticky='w')

        age_filter_combobox = ttk.Combobox(frame2, textvariable=age_filter_var,
                                           values=["All ages"] + [str(i) for i in range(2, 19)], width=20)
        age_filter_combobox.grid(row=2, column=5)
        age_filter_combobox.bind("<<ComboboxSelected>>", on_filter_change)

        # Add a class filter Combobox to your GUI
        class_filter_var = tk.StringVar()
        class_filter_label = tk.Label(frame2, text="Filter by Class:")
        class_filter_label.grid(row=1,column=6)
        class_combobox = ttk.Combobox(frame2, textvariable=class_filter_var)
        class_combobox['values'] = ['All Classes'] + [str(i) for i in range(1, 13)]  # Classes 1 to 12
        class_combobox.current(0)  # Default to "All Classes"
        class_combobox.grid(row=2, column=6, padx=10, pady=5)  # Adjust the grid placement as needed

        class_combobox.bind("<<ComboboxSelected>>", on_filter_change)

        def get_unique_years():
            conn = sqlite3.connect("gracehealth.db")
            cursor = conn.cursor()

            # Extract years (last two digits) from MM/DD/YY format in screen_date
            cursor.execute("SELECT DISTINCT SUBSTR(screen_date, -2) FROM student WHERE screen_date IS NOT NULL")
            years = [row[0] for row in cursor.fetchall()]

            conn.close()

            return sorted(years, reverse=True)  # Sort years in descending order

        # Fetch unique years from database
        unique_years = get_unique_years()

        year_filter_var = tk.StringVar()
        year_filter_label = tk.Label(frame2, text="Filter by Year:")
        year_filter_label.grid(row=1, column=7)

        year_combobox = ttk.Combobox(frame2, textvariable=year_filter_var)
        year_combobox['values'] = ["All Years"] + get_unique_years()  # Fetch from DB
        year_combobox.current(0)  # Default to "All Years"
        year_combobox.grid(row=2, column=7, padx=10, pady=5)



        year_combobox.bind("<<ComboboxSelected>>", on_filter_change)

        status_filter_var = tk.StringVar(value="active")
        status_filter_label = tk.Label(frame2, text="Filter by Status:")
        status_filter_label.grid(row=1, column=3, sticky='w')

        status_filter_combobox = ttk.Combobox(frame2, textvariable=status_filter_var, values=["active", "graduated"],
                                              width=20)
        status_filter_combobox.grid(row=2, column=3)
        status_filter_combobox.bind("<<ComboboxSelected>>", on_filter_change)




        # Add a label to show the total number of students
        total_students_var = tk.StringVar(value="Total Students: 0")
        total_students_label = tk.Label(school_window, textvariable=total_students_var, font=("Arial", 12, "bold"))
        total_students_label.place(x=100, y=520)  # Adjust the position as needed

        def refresh_records(school_name_filter="", gender_filter="", student_name_filter="",
                            status_filter="", area_filter="", age_filter="",
                            class_filter="", year_filter="", id_filter=""):

            try:
                # Open a new database connection
                connection = sqlite3.connect('gracehealth.db')
                cursor = connection.cursor()

                # Clear the Treeview
                for item in tree.get_children():
                    tree.delete(item)

                # Base query
                query = """
                           SELECT s.id, s.name, s.school_name, s.gender, s.Class_section
                           FROM student s
                           WHERE s.status = ?
                             AND '20' || SUBSTR(s.screen_date, 7, 2) || '-' || SUBSTR(s.screen_date, 1, 2) || '-' || SUBSTR(s.screen_date, 4, 2) = (
                                 SELECT MAX('20' || SUBSTR(inner_s.screen_date, 7, 2) || '-' || SUBSTR(inner_s.screen_date, 1, 2) || '-' || SUBSTR(inner_s.screen_date, 4, 2))
                                 FROM student inner_s
                                 WHERE inner_s.id = s.id)
                """
                params = [status_filter]

                # Apply filters
                if school_name_filter and school_name_filter != "All students":
                    query += " AND s.school_name LIKE ?"
                    params.append(f"%{school_name_filter.strip()}%")

                if gender_filter and gender_filter != "all":
                    query += " AND s.gender = ?"
                    params.append(gender_filter.strip())

                if student_name_filter:
                    query += " AND s.name LIKE ?"
                    params.append(f"%{student_name_filter.strip()}%")

                if id_filter:
                    query += " AND CAST(s.id AS TEXT) LIKE ?"  # Ensure ID is treated as text
                    params.append(f"%{id_filter.strip()}%")

                if area_filter and area_filter != "All areas":
                    query += " AND s.tea_garden = ?"
                    params.append(area_filter.strip())

                if age_filter and age_filter != "All ages":
                    min_age_in_months = int(age_filter) * 12
                    max_age_in_months = (int(age_filter) + 1) * 12 - 1
                    query += " AND s.age_in_month BETWEEN ? AND ?"
                    params.extend([min_age_in_months, max_age_in_months])

                if class_filter and class_filter != "All Classes":
                    query += " AND s.Class_section = ?"
                    params.append(class_filter.strip())

                if year_filter and year_filter != "All Years":
                    query += " AND SUBSTR(s.screen_date, -2) = ?"
                    params.append(year_filter.strip())

                query += " ORDER BY s.id ASC"

                # Execute query
                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Populate Treeview with serial numbers
                for index, row in enumerate(rows, start=1):  # Serial numbers start from 1
                    tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], index))  # SL NO at the end

                # Update total students count
                total_students_var.set(f"Total Students: {len(rows)}")

            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            finally:
                # Ensure the connection is always closed properly
                if connection:
                    connection.close()

        age_filter_var = tk.StringVar(value="All ages")
        age_filter_label = tk.Label(frame2, text="Filter by Age (Years):")
        age_filter_label.grid(row=1, column=5, sticky='w')

        age_filter_combobox = ttk.Combobox(frame2, textvariable=age_filter_var,
                                           values=["All ages"] + [str(i) for i in range(2, 19)], width=20)
        age_filter_combobox.grid(row=2, column=5)
        age_filter_combobox.bind("<<ComboboxSelected>>", on_filter_change)



        refresh_records()  # Load

    # Create a menu bar
    menu_bar = Menu(window)

    # Create a File menu and add items
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Student list", command=school_list)
    file_menu.add_command(label="Statistics", command=statistic_search)
    #file_menu.add_command(label="clear text", command=clear_entry)
    #file_menu.add_command(label="Statistics", command=statistic_search)

    menu_bar.add_cascade(label="File", menu=file_menu)

    # Create a Help menu and add items

    # Add the menu bar to the main window
    window.config(menu=menu_bar)

    # Run the application

    #SET UP MENU
    # Create a menu bar


    def check_id():
        connection = sqlite3.connect("gracehealth.db")
        cursor = connection.cursor()
        user_id = (id_entry.get())

        cursor.execute("SELECT name from student WHERE id=?", (user_id,))
        used_name = cursor.fetchall()
        numbers = list(range(1, 1000000))
        numbers = str(numbers)

        if used_name != []:
            # check_id_confirmation.config(text=f'{used_name} already has this id!')
            messagebox.showinfo(parent=window, title="error", message=f'{used_name} already has this id!')

        elif user_id == "":
            # check_id_confirmation.config(text="Write an id number")
            messagebox.showinfo(parent=window, title="error", message="id cannot be empty!")
        elif user_id == "0":
            messagebox.showinfo(parent=window, title="error", message="id cannot be 0!")

        elif user_id not in numbers:
            messagebox.showinfo(parent=window, title="error", message="id must be a valid number")
            # check_id_confirmation.config(text='id must be a valid number!')
        else:
            messagebox.showinfo(parent=window, title="success", message="This id number is free")

        connection.commit()
        connection.close()

    def clear_entry():
        screening_date_entry.delete(0,END)
        id_entry.delete(0, END),
        name_entry.delete(0, END),
        date_of_birth_entry.delete(0, END),
        class_entry.delete(0, END),
        roll_entry.delete(0, END),
        aadhaar_entry.delete(0, END),
        father_guardian_entry.delete(0, END),
        mother_entry.delete(0, END),
        contact_no_entry.delete(0, END),
        address_entry.delete(0, END),
        email_entry.delete(0, END),
        teacher_entry.delete(0, END),
        age_entry.config(state=NORMAL),
        age_entry.delete(0, END),
        tea_garden_entry.set("")

        total_month_entry.delete(0,END),
        last_school_entry.delete(0, END),
        place_of_birth_entry.delete(0, END),
        weight_length_entry.delete(0,END),
        length_age_entry.delete(0,END),
        weight_age_entry.delete(0,END),

        known_disease_entry.delete(0, END),
        e9_entry.delete(0, END),

        weight_entry.delete(0, END),
        height_entry.delete(0, END),
        muac_entry.delete(0,END)
        muac_category_entry.delete(0,END)
        BMI_entry.delete(0, END),
        BMI_category_entry.delete(0, END),
        class_entry.delete(0, END),
        roll_entry.delete(0, END),
        aadhaar_entry.delete(0, END),
        vision_problem_entry.delete(0, END),
        left_eyesight_var.set(""),
        right_eyesight_var.set(""),
        school_entry.delete(0, END),
        gender_option.set(""),
        check_id_confirmation.config(text="")

        CheckVar1.set('no')
        CheckVar2.set('no')
        CheckVar3.set('no')
        CheckVar4.set('no')
        CheckVar4.set('no')
        CheckVar5.set('no')
        CheckVar6.set('no')
        CheckVar7.set('no')
        CheckVar8.set('no')
        CheckVar9.set('no')
        CheckVar10.set('no')
        CheckVar11.set('no')
        CheckVar12.set('no')
        CheckVar13.set('no')
        CheckVar14.set('no')

        CheckVar16.set('no')
        CheckVar17.set('no')
        CheckVar18.set('no')
        CheckVar19.set('no')
        CheckVar20.set('no')
        CheckVar23.set('no')
        CheckVar24.set('no')
        CheckVar25.set('N/A')
        CheckVar26.set('no')
        CheckVar27.set('no')
        CheckVar28.set('no')
        CheckVar29.set('unknown')
        CheckVar30.set('unknown')


        # savebtn.config(state=ACTIVE),
        # BMI_entry.config(state=ACTIVE),

    def normal():

        id_entry.config(state=NORMAL),
        name_entry.config(state=NORMAL),

        gender_entry.config(state=ACTIVE),
        class_entry.config(state=NORMAL),
        roll_entry.config(state=NORMAL),
        aadhaar_entry.config(state=NORMAL),

        father_guardian_entry.config(state=NORMAL),
        mother_entry.config(state=NORMAL),
        contact_no_entry.config(state=NORMAL),
        address_entry.config(state=NORMAL),
        email_entry.config(state=NORMAL),
        teacher_entry.config(state=NORMAL),
        school_entry.config(state=ACTIVE),
        last_school_entry.config(state=NORMAL),
        place_of_birth_entry.config(state=NORMAL),
        known_disease_entry.config(state=NORMAL),

        weight_entry.config(state=NORMAL),
        height_entry.config(state=NORMAL),
        muac_entry.config(state=NORMAL),
        muac_category_entry.config(state=NORMAL),
        BMI_entry.config(state=NORMAL),
        vision_left_menu.config(state=ACTIVE),
        vision_right_menu.config(state=ACTIVE),
        vision_problem_entry.config(state=NORMAL),
        b1_entry.config(state=ACTIVE),
        b2_entry.config(state=ACTIVE),
        b3_entry.config(state=ACTIVE),
        b4_entry.config(state=ACTIVE),
        b5_entry.config(state=ACTIVE),
        c1_entry.config(state=ACTIVE),
        c2_entry.config(state=ACTIVE),
        c3_entry.config(state=ACTIVE),
        c4_entry.config(state=ACTIVE),
        c5_entry.config(state=ACTIVE),
        c6_entry.config(state=ACTIVE),
        d1_entry.config(state=ACTIVE),
        d2_entry.config(state=ACTIVE),
        d3_entry.config(state=ACTIVE),
        d5_entry.config(state=ACTIVE),
        d6_entry.config(state=ACTIVE),
        d7_entry.config(state=ACTIVE),
        d8_entry.config(state=ACTIVE),
        d9_entry.config(state=ACTIVE),
        e3_entry.config(state=ACTIVE),
        e4_entry.config(state=ACTIVE),
        e5_entry.config(state=ACTIVE),
        e6_entry.config(state=ACTIVE),
        e7_entry.config(state=ACTIVE),
        e8_entry.config(state=ACTIVE),
        e9_entry.config(state=NORMAL),
        BMI_category_entry.config(state=NORMAL),
        weight_age_entry.config(state=NORMAL),
        length_age_entry.config(state=NORMAL),
        weight_length_entry.config(state=NORMAL),
        deworming_entry.config(state=ACTIVE),
        vaccination_entry.config(state=ACTIVE),


        savebtn.config(state=NORMAL),
    def reset():
        confirmation = messagebox.askyesno(parent=window, title="confirmation",
                                           message="Remember to save before creating new student! Do you want to continue?")
        if confirmation:
            for widget in summary_frame.winfo_children():
                widget.destroy()
            normal()
            clear_entry()
            populate_student_id()


    def clear_text():

        for widget in summary_frame.winfo_children():
            widget.destroy()
        normal()
        clear_entry()
        populate_student_id()


    def custom_messagebox(user_id, cursor, screening_date):
        def update_screening():
            update_last_screening(cursor, user_id, screening_date)
            custom_box.destroy()
            messagebox.showinfo(parent=window, title="success", message="The screening has been updated")


        def save_new_screening():
            save_new_entry(cursor, user_id)
            custom_box.destroy()
            messagebox.showinfo(parent=window, title="success", message="The screening has been saved")


        custom_box = Toplevel(window)
        custom_box.title("Update or New Save")
        custom_box.geometry("300x150+500+300")

        label = tk.Label(custom_box,
                         text=f"Student ID {user_id} exists.\nDo you want to update or create a new screening?")
        label.pack(pady=20)

        update_button = ttk.Button(custom_box, text="Update", command=update_screening)
        update_button.pack(side=tk.LEFT, padx=20)

        new_save_button = ttk.Button(custom_box, text="New Save", command=save_new_screening)
        new_save_button.pack(side=tk.RIGHT, padx=20)

        custom_box.grab_set()
        window.wait_window(custom_box)


    def save_or_update_entry():
        user_id = id_entry.get().strip()  # Strip whitespace from user input

        # Validate user ID
        if not user_id:
            messagebox.showinfo(parent=window, title="Error", message="ID cannot be empty!")
            return
        elif user_id == "0":
            messagebox.showinfo(parent=window, title="Error", message="ID cannot be 0!")
            return
        elif not user_id.isdigit():
            messagebox.showinfo(parent=window, title="Error", message="ID must be a valid number!")
            return

        #confirmation = messagebox.askyesno(parent=window, title="Save", message="Are you sure you want to save?")

        #if not confirmation:
         #   return  # If user cancels, exit the function

        with sqlite3.connect("gracehealth.db") as connection:
            cursor = connection.cursor()

            # Check if the ID exists in the database
            cursor.execute("SELECT COUNT(*) FROM student WHERE id=?", (user_id,))
            exists = cursor.fetchone()[0]

            if exists == 0:
                # ID does not exist, perform a new save
                confirmation = messagebox.askyesno(parent=window, title="New Save",
                                                   message=f"Student ID {user_id} not found. Do you want to save as a new entry?")
                if confirmation:
                    save_new_entry(cursor, user_id)
                    messagebox.showinfo(parent=window, title="Success", message="New student succesfully saved")

            else:
                # ID exists, use custom messagebox for Update/New Save choice
                screening_date = screening_date_entry.get()  # Retrieve the screening date value
                if not screening_date:  # Ensure screening date is provided
                    messagebox.showinfo(parent=window, title="Error", message="Screening date cannot be empty!")
                    return

                custom_messagebox(user_id, cursor, screening_date)  # Pass screening date to custom_messagebox

            # Commit changes after the operation
            connection.commit()
             # Clear input fields after successful operation
            display_journal(user_id, summary_frame)

    def update_last_screening(cursor, user_id, screening_date, *args):
        # First, check if the screening_date exists for this record
        cursor.execute("SELECT screen_date FROM student WHERE id=?", (user_id,))
        existing_date = cursor.fetchone()

        # Collect the parameters to be updated in the database
        parameters = (
            name_entry.get(),
            date_of_birth_entry.get(),
            gender_option.get(),
            class_entry.get(),
            roll_entry.get(),
            aadhaar_entry.get(),
            father_guardian_entry.get(),
            mother_entry.get(),
            contact_no_entry.get(),
            address_entry.get(),
            email_entry.get(),
            teacher_entry.get(),
            school_entry.get(),
            last_school_entry.get(),
            place_of_birth_entry.get(),
            known_disease_entry.get(),
            weight_entry.get(),
            height_entry.get(),
            BMI_entry.get(),
            left_eyesight_var.get(),
            right_eyesight_var.get(),
            vision_problem_entry.get(),
            CheckVar1.get(),
            CheckVar2.get(),
            CheckVar3.get(),
            CheckVar4.get(),
            CheckVar5.get(),
            CheckVar6.get(),
            CheckVar7.get(),
            CheckVar8.get(),
            CheckVar9.get(),
            CheckVar10.get(),
            CheckVar11.get(),
            CheckVar12.get(),
            CheckVar13.get(),
            CheckVar14.get(),
            CheckVar16.get(),
            CheckVar17.get(),
            CheckVar18.get(),
            CheckVar19.get(),
            CheckVar20.get(),
            CheckVar23.get(),
            CheckVar24.get(),
            CheckVar25.get(),
            CheckVar26.get(),
            CheckVar27.get(),
            CheckVar28.get(),
            e9_entry.get(),
            BMI_category_entry.get(),
            weight_age_entry.get(),
            length_age_entry.get(),
            weight_length_entry.get(),
            total_month_entry.get(),
            CheckVar29.get(),
            CheckVar30.get(),
            tea_garden_entry.get(),
            muac_entry.get(),
            muac_category_entry.get(),
            screening_date_entry.get(),  # Keep this if you intend to update screen_date
            age_entry.get(),

            user_id  # Ensure this is the last item, matching the WHERE clause
        )

        # Determine if we need to add or update the screening date
        if existing_date is None or existing_date[0] is None:
            # No existing screening date, so add it in the update
            query = """
                UPDATE student 
                SET name=?,
                    date_of_birth=?,
                    Gender=?,
                    Class_section=?,
                    Roll_no=?,
                    Aadhaar_No=?,
                    Father_or_guardian_name=?,
                    mother_name=?,
                    contact_number=?,
                    Address=?,
                    email=?,
                    Name_teacher=?,
                    school_name=?,
                    last_school_name=?,
                    place_of_birth=?,
                    known_earlier_disease=?,
                    weight=?,
                    height=?,
                    BMI=?,
                
                    VISON_left=?,
                    VISON_right=?,
                    VISION_problem=?,
                    B1_severe_anemia=?,
                    B2_Vita_A_deficiency=?,
                    B3_Vit_D_deficiency=?,
                    B4_Goitre=?,
                    B5_Oedema=?,
                    C1_convulsive_dis=?,
                    C2_otitis_media=?,
                    C3_dental_condition=?,
                    C4_skin_condition=?,
                    C5_rheumatic_heart_disease=?,
                    C6_others_TB_asthma=?,
                    D1_difficulty_seeing=?,
                    D2_delay_in_walking=?,
                    D3_stiffness_floppiness=?,
                    D5_reading_writing_calculatory_difficulty=?,
                    D6_speaking_difficulty=?,
                    D7_hearing_problems=?,
                    D8_learning=?,
                    D9_attention=?,
                    E3_depression_sleep=?,
                    E4_Menarke=?,
                    E5_regularity_period_difficulties=?,
                    E6_UTI_STI=?,
                    E7=?,
                    E8_menstrual_pain=?,
                    E9_remarks=?,
                    BMI_category=?,
                    weight_age=?,
                    length_age=?,
                    weight_height=?,
                    age_in_month=?,
                    deworming=?,
                    vaccination=?,
                    tea_garden=?,
                     muac = ?,
                     muac_sam= ?,  
                    age_screening=?,
                   screen_date=?
                WHERE id=?
            """

        else:
            # Screening date exists, so just update other fields without setting screen_date again
            parameters = parameters[:-3] + (
            age_entry.get(), user_id, screening_date_entry.get()) # Excludes screening_date_entry.get() when not needed

            query = """
                UPDATE student 
                SET name=?,
                    date_of_birth=?,
                    Gender=?,
                    Class_section=?,
                    Roll_no=?,
                    Aadhaar_No=?,
                    Father_or_guardian_name=?,
                    mother_name=?,
                    contact_number=?,
                    Address=?,
                    email=?,
                    Name_teacher=?,
                    school_name=?,
                    last_school_name=?,
                    place_of_birth=?,
                    known_earlier_disease=?,
                    weight=?,
                    height=?,
                    BMI=?,
                
                    VISON_left=?,
                    VISON_right=?,
                    VISION_problem=?,
                    B1_severe_anemia=?,
                    B2_Vita_A_deficiency=?,
                    B3_Vit_D_deficiency=?,
                    B4_Goitre=?,
                    B5_Oedema=?,
                    C1_convulsive_dis=?,
                    C2_otitis_media=?,
                    C3_dental_condition=?,
                    C4_skin_condition=?,
                    C5_rheumatic_heart_disease=?,
                    C6_others_TB_asthma=?,
                    D1_difficulty_seeing=?,
                    D2_delay_in_walking=?,
                    D3_stiffness_floppiness=?,
                    D5_reading_writing_calculatory_difficulty=?,
                    D6_speaking_difficulty=?,
                    D7_hearing_problems=?,
                    D8_learning=?,
                    D9_attention=?,
                    E3_depression_sleep=?,
                    E4_Menarke=?,
                    E5_regularity_period_difficulties=?,
                    E6_UTI_STI=?,
                    E7=?,
                    E8_menstrual_pain=?,
                    E9_remarks=?,
                    BMI_category=?,
                    weight_age=?,
                    length_age=?,
                    weight_height=?,
                    age_in_month=?,
                    deworming = ?,
                    vaccination=?,
                    tea_garden=?,
                    muac = ?,
                    muac_sam = ?,
                    age_screening=?
                    
                WHERE id=? AND screen_date =?
            """

        # Execute the appropriate query
        cursor.execute(query, parameters)

    def save_new_entry(cursor, user_id):
        # Logic to save a new entry for the student
        cursor.execute("""INSERT INTO student(
            id,  -- or remove this column if it is auto-incremented
            name,
            date_of_birth,
            Gender,
            Class_section,
            Roll_no,
            Aadhaar_No,
            Father_or_guardian_name,
            mother_name,
            contact_number,
            Address,
            email,
            Name_teacher,
            school_name,
            last_school_name,
            place_of_birth,
            known_earlier_disease,
            weight,
            height,
            BMI,
            VISON_left,
            VISON_right,
            VISION_problem,
            B1_severe_anemia,
            B2_Vita_A_deficiency,
            B3_Vit_D_deficiency,
            B4_Goitre,
            B5_Oedema,
            C1_convulsive_dis,
            C2_otitis_media,
            C3_dental_condition,
            C4_skin_condition,
            C5_rheumatic_heart_disease,
            C6_others_TB_asthma,
            D1_difficulty_seeing,
            D2_delay_in_walking,
            D3_stiffness_floppiness,
            D5_reading_writing_calculatory_difficulty,
            D6_speaking_difficulty,
            D7_hearing_problems,
            D8_learning,
            D9_attention,
            E3_depression_sleep,
            E4_Menarke,
            E5_regularity_period_difficulties,
            E6_UTI_STI,
            E7,
            E8_menstrual_pain,
            E9_remarks,
            BMI_category, 
            weight_age,
            length_age,
            weight_height,
            age_in_month,
            deworming,
            vaccination,
            tea_garden,
            screen_date,
            age_screening,
            muac,
            muac_sam) 
        VALUES (?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (
                           id_entry.get(),  # Remove if id is auto-incremented
                           name_entry.get(),
                           date_of_birth_entry.get(),
                           gender_option.get(),
                           class_entry.get(),
                           roll_entry.get(),
                           aadhaar_entry.get(),
                           father_guardian_entry.get(),
                           mother_entry.get(),
                           contact_no_entry.get(),
                           address_entry.get(),
                           email_entry.get(),
                           teacher_entry.get(),
                           school_entry.get(),
                           last_school_entry.get(),
                           place_of_birth_entry.get(),
                           known_disease_entry.get(),
                           weight_entry.get(),
                           height_entry.get(),
                           BMI_entry.get(),
                           left_eyesight_var.get(),
                           right_eyesight_var.get(),
                           vision_problem_entry.get(),
                           CheckVar1.get(),
                           CheckVar2.get(),
                           CheckVar3.get(),
                           CheckVar4.get(),
                           CheckVar5.get(),
                           CheckVar6.get(),
                           CheckVar7.get(),
                           CheckVar8.get(),
                           CheckVar9.get(),
                           CheckVar10.get(),
                           CheckVar11.get(),
                           CheckVar12.get(),
                           CheckVar13.get(),
                           CheckVar14.get(),
                           CheckVar16.get(),
                           CheckVar17.get(),
                           CheckVar18.get(),
                           CheckVar19.get(),
                           CheckVar20.get(),
                           CheckVar23.get(),
                           CheckVar24.get(),
                           CheckVar25.get(),
                           CheckVar26.get(),
                           CheckVar27.get(),
                           CheckVar28.get(),
                           e9_entry.get(),
                           BMI_category_entry.get(),
                           weight_age_entry.get(),
                           length_age_entry.get(),
                           weight_length_entry.get(),
                           total_month_entry.get(),
                           CheckVar29.get(),
                           CheckVar30.get(),
                           tea_garden_entry.get(),
                           screening_date_entry.get(),
                           age_entry.get(),
                           muac_entry.get(),
                           muac_category_entry.get()
                       ))

    def populate_student_id():
        last_id = get_next_student_id()
        if last_id:
            id_entry.insert(0, last_id)
        else:
            id_entry.insert(0, "1")

    import sqlite3

    def get_next_student_id():
        # Connect to the SQLite database
        conn = sqlite3.connect("gracehealth.db")
        cursor = conn.cursor()

        try:
            # Execute a query to get all IDs ordered in descending order
            cursor.execute("SELECT id FROM student ORDER BY id DESC")
            results = cursor.fetchall()

            # Loop through the results and find the first valid numeric ID
            for result in results:
                try:
                    # Attempt to convert the id to an integer
                    last_id = int(result[0])
                    return last_id + 1  # Return the next available ID
                except ValueError:
                    # If conversion fails, move to the next row (skip non-numeric IDs)
                    continue

            # If no valid numeric ID is found, start from 1
            return 1

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            # Close the database connection
            conn.close()

    # Example usage: call the function and get the next student ID
    next_id = get_next_student_id()
    print(f"The next available student ID is: {next_id}")

    screening_label=Label(topframe,text="Date of Screening",font="bold")
    screening_label.grid(row=0,column=1)
    screening_date_entry = DateEntry(topframe, date_pattern='MM/DD/YY')
    screening_date_entry.grid(row=0,column=2)

    id_label = Label(topframe, text="Id", width=22)
    id_label.grid(column=1, row=1)
    id_entry = Entry(topframe, width=30)
    id_entry.grid(column=2, row=1)
    populate_student_id()



    name_label = Label(topframe, text="Name", width=22).grid(column=1, row=2)
    name_entry = Entry(topframe, width=30)
    name_entry.grid(column=2, row=2)

    date_of_birth = Label(topframe, text="Date of birth", width=22).grid(column=1, row=3)
    date_of_birth_var = StringVar()
    date_of_birth_entry = DateEntry(topframe, width=30, date_pattern='MM/DD/yy')
    date_of_birth_entry.delete(0, 'end')

    date_of_birth_entry.grid(column=2, row=3)


    # Python3 code to calculate age in years

    from datetime import datetime
    from tkinter import END, NORMAL

    def age_calculator():

        if screening_date_entry.get() == "":
            messagebox.showinfo(parent=window,title="error",message="Please write screening date")
            screening_date_entry.focus_set()
        else:

            age_entry.config(state=NORMAL)
            age_entry.delete(0, END)
            total_month_entry.delete(0, END)

            # Get the two dates from DateEntry widgets
            birthday = date_of_birth_entry.get()
            screening_date = screening_date_entry.get()

            # Convert string dates to datetime objects for easier calculations
            birthday = datetime.strptime(birthday, "%m/%d/%y")
            screening_date = datetime.strptime(screening_date, "%m/%d/%y")

            # Calculate the difference between screening date and birthdate
            age_years = screening_date.year - birthday.year
            age_months = screening_date.month - birthday.month

            # Adjust if the screening month is before the birth month
            if age_months < 0:
                age_years -= 1
                age_months += 12

            # Calculate total months difference
            total_months = age_years * 12 + age_months

            # Display results in the Entry widgets
            age_entry.insert(0, f"{age_years} years and {age_months} months")
            total_month_entry.insert(0, str(total_months))

    age_btn = ttk.Button(topframe, width=22, text="Age at screening", command=age_calculator)
    age_btn.grid(column=1, row=4)


    # button_hover(age_btn)
    age_entry = Entry(topframe, width=30)
    age_entry.grid(column=2, row=4)




    age_in_month_label = Label(topframe, text="Age in total months").grid(column=1, row=5)
    total_month_entry = Entry(topframe)
    total_month_entry.grid(column=2, row=5)

    gender_label = Label(topframe, text="Gender", width=22).grid(column=1, row=6)
    gender_option = StringVar()
    gender_entry = OptionMenu(topframe, gender_option, "female",
                              "male")
    gender_entry.grid(column=2, row=6)

    class_label = Label(topframe, text="Class", width=22).grid(column=3, row=1)
    class_entry = Entry(topframe, width=30)
    class_entry.grid(column=4, row=1)

    roll_no_label = Label(topframe, text="Roll number", width=22).grid(column=3, row=2)
    roll_entry = Entry(topframe, width=30)
    roll_entry.grid(column=4, row=2)

    aadhaar_label = Label(topframe, text="Aadhaar number", width=22).grid(column=3, row=3)
    aadhaar_entry = Entry(topframe, width=30)
    aadhaar_entry.grid(column=4, row=3)

    father_guardian_label = Label(topframe, text="Father or guardian", width=22).grid(column=3, row=4)
    father_guardian_entry = Entry(topframe, width=30)
    father_guardian_entry.grid(column=4, row=4)

    mother_label = Label(topframe, text="Mother", width=22).grid(column=3, row=5)
    mother_entry = Entry(topframe, width=30)
    mother_entry.grid(column=4, row=5)

    contact_no_label = Label(topframe, text="Contact number", width=22).grid(column=3, row=6)
    contact_no_entry = Entry(topframe, width=30)
    contact_no_entry.grid(column=4, row=6)

    address_label = Label(topframe, text="Address", width=22).grid(column=5, row=1)
    address_entry = Entry(topframe, width=30)
    address_entry.grid(column=6, row=1)

    email_label = Label(topframe, text="Email", width=22).grid(column=5, row=2)
    email_entry = Entry(topframe, width=30)
    email_entry.grid(column=6, row=2)
    teacher_label = Label(topframe, text="Teacher", width=22).grid(column=5, row=3)
    teacher_entry = Entry(topframe, width=30)
    teacher_entry.grid(column=6, row=3)

    main_window_school_list = [school for school in school_database_list if school not in ["All schools combined", ""]]
    school_label = Label(topframe, text="School name", width=22).grid(column=5, row=4)
    school_entry = ttk.Combobox(topframe,values=main_window_school_list,width=30)
    school_entry.grid(column=6, row=4)

    last_school_label = Label(topframe, text="Last school name", width=22).grid(column=5, row=5)
    last_school_entry = Entry(topframe, width=30)
    last_school_entry.grid(column=6, row=5)

    place_of_birth = Label(topframe, text="Place of birth", width=22).grid(column=5, row=6)
    place_of_birth_entry = Entry(topframe, width=30)
    place_of_birth_entry.grid(column=6, row=6)

    tea_garden_label=Label(topframe,text="Special area (optional):")
    tea_garden_label.grid(row=7,column=5)
    filtered_tea_garden_list = [tea_garden for tea_garden in tea_garden_database_list if tea_garden not in ["", "None"]]

    # Create the Combobox with the filtered list
    tea_garden_entry = ttk.Combobox(topframe, values=filtered_tea_garden_list)
    tea_garden_entry.grid(row=7,column=6)



    weight_label = Label(secondframe, text="Weight (kg)", width=22).grid(column=1, row=9)
    weight_entry = Entry(secondframe, width=5)
    weight_entry.grid(column=2, row=9)

    height_label = Label(secondframe, text="Height (cm)", width=22)
    height_label.grid(column=1, row=10)
    height_entry = Entry(secondframe, width=5)
    height_entry.grid(column=2, row=10)

    def muac():
        muac_category_entry.delete(0,END)
        try:
            age = int(total_month_entry.get())
            print(age)
            if 6 <= age <= 60:
                muac_category_entry.delete(0, END)
                muach_length = float(muac_entry.get())
                if muach_length >= 11.5:
                    muac_category_entry.insert(0, "normal")
                else:
                    muac_category_entry.insert(0, "severe acute malnutrition")
            else:
                # Trigger the error if age is outside the valid range

                muac_category_entry.insert(0,"N/A")

        except ValueError:
            # Handle non-integer or invalid input gracefully
            messagebox.showerror(title="Error", message="Please enter a valid number for months,and MUAC!")

    muac_label = Label(secondframe, text="MUAC (cm)", width=22)
    muac_label.grid(column=1, row=11)
    muac_entry = Entry(secondframe, width=5)
    muac_entry.grid(column=2, row=11)

    muac_category_btn = ttk.Button(secondframe, text="MUAC category", command=muac)
    muac_category_btn.grid(column=1, row=12)
    muac_category_entry = Entry(secondframe, width=25)
    muac_category_entry.grid(column=2, row=12)

    vision_list = ["3/30", "3/24", "3/19", "3/15", "3/12", "3/9.5", "3/7.5", "3/6", "3/4.8", "3/3.8", "3/3", "3/2.4",
                   "3/1.9", "3/1.5", "3/1.2"]

    # Vision LEFT
    left_eyesight_var = StringVar()
    vision_left_label = Label(secondframe, text="Vision left eye", width=22)
    vision_left_label.grid(column=3, row=9)
    vision_left_menu = OptionMenu(secondframe, left_eyesight_var, *vision_list)
    vision_left_menu.grid(column=4, row=9)

    # Vision RIGHT
    right_eyesight_var = StringVar()
    vision_right_label = Label(secondframe, text="Vision right eye", width=22)
    vision_right_label.grid(column=3, row=10)
    vision_right_menu = OptionMenu(secondframe, right_eyesight_var, *vision_list)
    vision_right_menu.grid(column=4, row=10)

    # Result Logic
    def vision_result():
        vision_problem_entry.delete(0, END)

        # Vision worse than 3/4.8 considered problematic
        critical_vision_set = set(vision_list[:9])  # From 3/30 to 3/4.8

        vision_vars = {
            "left": left_eyesight_var.get(),
            "right": right_eyesight_var.get()
        }

        try:
            left_index = vision_list.index(vision_vars["left"])
            right_index = vision_list.index(vision_vars["right"])
        except ValueError:
            vision_problem_entry.insert(0, "invalid")
            return

        if any(vision in critical_vision_set for vision in vision_vars.values()) \
                or abs(left_index - right_index) > 2:
            vision_problem_entry.insert(0, "yes")
        else:
            vision_problem_entry.insert(0, "no")

    # Button and result entry
    vision_problem_btn = ttk.Button(secondframe, text="Vision problem", command=vision_result, width=22)
    vision_problem_btn.grid(column=3, row=11)

    vision_problem_entry = Entry(secondframe, width=5)
    vision_problem_entry.grid(column=4, row=11)

    def BMI_calculator():
        try:
            # Clear previous BMI result
            BMI_entry.delete(0, tk.END)

            # Get the weight and height inputs and check if they are filled
            weight = weight_entry.get().strip()
            height = height_entry.get().strip()

            if not weight or not height:
                raise ValueError("Please enter both weight and height.")

            # Convert weight and height to floats (to accept decimals)
            weight = float(weight)
            height = float(height)

            # Perform BMI calculation
            result = (weight / height ** 2) * 10000
            BMI_index = round(result, 1)

            # Insert the result into the BMI entry field
            BMI_entry.insert(0, str(BMI_index))

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
            BMI_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            BMI_entry.delete(0, tk.END)

    BMI_btn = ttk.Button(secondframe, text="BMI value", width=22, command=BMI_calculator)
    BMI_btn.grid(column=5,row=12)
    # button_hover(BMI_btn)

    BMI_entry = Entry(secondframe, width=5)
    BMI_entry.grid(column=6, row=12)





    def bmi_category(gender, month, bmi_value):
        """
        Determine the BMI category based on gender, month, and BMI value.
        If the month is out of range, return "N/A". All error messages are displayed in messagebox.

        :param gender: str, "male" or "female"
        :param month: str, the month (as a string) like "73", "74", etc.
        :param bmi_value: float, the BMI value to categorize

        :return: str, the category (severe underweight, underweight, normal, or overweight)
        """
        try:
            # Check if gender is valid
            if gender not in ["male", "female"]:
                raise ValueError("Please select a valid gender (male or female).")

            # Select the correct BMI thresholds based on gender
            thresholds = bmi_thresholds_female if gender == "female" else bmi_thresholds_male

            # Check if the month is within the valid range
            if int(month) < 61 or int(month) > 228:
                return "N/A"

            if month not in thresholds:
                raise ValueError("BMI thresholds for the given month are not available.")

            # Fetch thresholds for the given month
            severe_underweight_threshold, underweight_threshold, overweight_threshold, obese_threshold = thresholds[month]

            # Determine the BMI category
            if bmi_value <= severe_underweight_threshold:
                return "severe underweight"
            elif severe_underweight_threshold < bmi_value < underweight_threshold:
                return "underweight"
            elif underweight_threshold <= bmi_value < overweight_threshold:
                return "normal"
            elif overweight_threshold <= bmi_value < obese_threshold:
                return "overweight"
            else:
                return "obese"

        except ValueError as ve:
            # Display an error message box
            messagebox.showerror("Input Error", str(ve))
            return ""
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return ""

    def show_bmi_category():
        try:
            # Get the BMI, month, and gender inputs
            bmi_value = BMI_entry.get().strip()  # Strip any leading/trailing spaces
            month = total_month_entry.get().strip()  # Already a string
            gender = gender_option.get().strip()  # Already a string

            # Check if the BMI value is numeric
            if not bmi_value.replace('.', '', 1).isdigit():  # Allow a single period for floats
                BMI_category_entry.delete(0, tk.END)  # Clear the previous result
                messagebox.showerror("Input Error", "Please enter a valid numeric value for BMI.")
                return

            # Convert to float
            bmi_value = float(bmi_value)

            # Get the BMI category
            category = bmi_category(gender, month, bmi_value)

            # Display the result in the BMI_category_entry field
            BMI_category_entry.delete(0, tk.END)  # Clear the previous result
            BMI_category_entry.insert(0, category)  # Insert the new category
        except Exception as e:
            # Handle unexpected errors
            BMI_category_entry.delete(0, tk.END)  # Clear previous result
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            gender_entry.focus_set()

    # Button setup in your GUI
    BMI_category_btn = ttk.Button(secondframe, text="BMI category (only for 61 to 228 months)",
                                  command=show_bmi_category)
    BMI_category_btn.grid(column=5, row=13)

    # Entry for displaying the result
    BMI_category_entry = Entry(secondframe, width=19)
    BMI_category_entry.grid(column=6, row=13)

    from tkinter import messagebox

    def weight_length_category():
        weight_length_entry.delete(0, END)

        try:
            height = float(height_entry.get())
            weight = float(weight_entry.get())
            total_months = int(total_month_entry.get())
            gender = gender_option.get()

            if 24 <= total_months <= 60:
                if gender == "female":
                    thresholds = female_weight_height_thresholds
                elif gender == "male":
                    thresholds = male_weight_height_thresholds
                else:
                    messagebox.showerror("Error", "Invalid gender selection.")
                    return

                # Find the closest height in the dictionary
                closest_height = min(thresholds.keys(), key=lambda h: abs(h - height))

                v1, v2, v3, v4 = thresholds[closest_height]

                if weight < v1:
                    weight_length_entry.insert(0, "severe acute malnutrition")
                elif v1 <= weight < v2:
                    weight_length_entry.insert(0, "moderate acute malnutrition")
                elif v2 <= weight <= v3:
                    weight_length_entry.insert(0, "normal")
                elif v3 < weight <= v4:
                    weight_length_entry.insert(0, "overweight")
                elif weight > v4:
                    weight_length_entry.insert(0, "obese")

            else:
                weight_length_entry.insert(0, "N/A")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid values for age, gender, height and weight.")

    def weight_age_category():
        weight_age_entry.delete(0, END)
        #if int(total_month_entry.get()) == 24 and gender_option.get() == "female" and 8.1 <= float(weight_entry.get()) < 9.0:
        #    weight_age_entry.insert(0,"moderately underweight")
        #elif int(total_month_entry.get()) == 24 and gender_option.get() == "female" and float(weight_entry.get()) < 8.1:
        #    weight_age_entry.insert(0, "severely underweight")
        #elif int(total_month_entry.get()) == 24 and gender_option.get() == "female" and float(weight_entry.get()) >= 9.0:
        #    weight_age_entry.insert(0, "normal")
        # Define weight thresholds for each month between 24 and 72
        weight_female_thresholds = {
            24: (8.1, 9.0),
            25: (8.2, 9.2),
            26: (8.4, 9.4),
            27: (8.5, 9.5),
            28: (8.6, 9.7),
            29: (8.7, 9.0),
            30: (8.8, 9.8),
            31: (9.0, 10.1),
            32: (9.1, 10.3),
            33: (9.3, 10.4),
            34: (9.4, 10.5),
            35: (9.5, 10.7),
            36: (9.6, 10.8),
            37: (9.7, 10.9),
            38: (9.8, 11.1),
            39: (9.9, 11.2),
            40: (10.1, 11.3),
            41: (10.2, 11.5),
            42: (10.3, 11.6),
            43: (10.4, 11.7), # Check again for error
            44: (10.5, 11.8) , # Check for error
            45: (10.6, 12.0),
            46: (10.7, 12.1),
            47: (10.8, 12.2),
            48: (10.9, 12.3),
            49: (11.0, 12.4),
            50: (11.1, 12.6),
            51: (11.2, 12.7),
            52: (11.3, 12.8),
            53: (11.4, 12.9),
            54: (11.5, 13.0),
            55: (11.6, 13.2),
            56: (11.7, 13.3),
            57: (11.8, 13.4),
            58: (11.9, 13.5),
            59: (12.0, 13.6),
            60: (12.1, 13.7),
            61: (12.4, 14.0), #check
            62: (12.5, 14.1),
            63: (12.6, 14.2),
            64: (12.7, 14.3),
            65: (12.8, 14.4),
            66: (12.9, 14.6),
            67: (13.0, 14.7),
            68: (13.1, 14.8),
            69: (13.2, 14.9),
            70: (13.3, 15.0),
            71: (13.4, 15.2),
            72: (13.5, 15.3),
            # Add more months as needed up to 72
        }
        weight_male_thresholds = {
            24: (8.6, 9.7),
            25: (8.8, 9.8),
            26: (8.9, 10.0),
            27: (9.0, 10.1),
            28: (9.1, 10.2),
            29: (9.2, 10.4),
            30: (9.4, 10.5),
            31: (9.5, 10.7),
            32: (9.6, 10.8),
            33: (9.7, 10.9),
            34: (9.8, 11.0),
            35: (9.9, 11.2),
            36: (10.0, 11.3),
            37: (10.1, 11.4),
            38: (10.2, 11.5),
            39: (10.3, 11.6),
            40: (10.4, 11.8),
            41: (10.5, 11.9),
            42: (10.6, 12.0),
            43: (10.7, 12.1),  # Check again for error
            44: (10.8, 12.2),  # Check for error
            45: (10.9, 12.4),
            46: (11.0, 12.5),
            47: (11.1, 12.6),
            48: (11.2, 12.7),
            49: (11.3, 12.8),
            50: (11.4, 12.9),
            51: (11.5, 13.1),
            52: (11.6, 13.2),
            53: (11.7, 13.3),
            54: (11.8, 13.4),
            55: (11.9, 13.5),
            56: (12.0, 13.6),
            57: (12.1, 13.7),
            58: (12.2, 13.8),
            59: (12.3, 14.0),
            60: (12.4, 14.1),
            61: (12.7, 14.4),  # check
            62: (12.8, 14.5),
            63: (13.0, 14.6),
            64: (13.1, 14.8),
            65: (13.2, 14.9),
            66: (13.3, 15.0),
            67: (13.4, 15.2),
            68: (13.6, 15.3),
            69: (13.7, 15.4),
            70: (13.8, 15.6),
            71: (13.9, 15.7),
            72: (14.1, 15.9) }


        try:
            # Get the total months, weight, and gender
            total_months = int(total_month_entry.get())
            weight = float(weight_entry.get())
            gender = gender_option.get()

            # Check if the input months are in the valid range
            if 24 <= total_months <= 60:
                if gender == "female" and total_months in weight_female_thresholds:
                    lower_bound, upper_bound = weight_female_thresholds[total_months]
                elif gender == "male" and total_months in weight_male_thresholds:
                    lower_bound, upper_bound = weight_male_thresholds[total_months]
                else:
                    weight_age_entry.insert(0, "N/A")  # If gender is invalid or out of defined months
                    return

                # Classify weight based on thresholds
                if weight < lower_bound:
                    weight_age_entry.insert(0, "severely underweight")
                elif lower_bound <= weight < upper_bound:
                    weight_age_entry.insert(0, "moderately underweight")
                else:
                    weight_age_entry.insert(0, "normal")
            else:
                weight_age_entry.insert(0, "N/A")  # Out of range months show "N/A"

        except ValueError:
            # Show an error message if the input is invalid
            messagebox.showerror("Invalid Input", "Please enter valid values for age, gender, height and weight.")

    def length_age_category():
        length_age_entry.delete(0, tk.END)

        # Female height thresholds
        female_thresholds = {
            24: (76.0, 79.3),
            25: (76.8, 80.0),
            26: (77.5, 80.8),
            27: (78.1, 81.5),
            28: (78.8, 82.2),
            29: (79.5, 82.9),
            30: (80.1, 83.6),
            31: (80.7, 84.3),
            32: (81.3, 84.9),
            33: (81.9, 85.6),
            34: (82.5, 86.2),
            35: (83.1, 86.8),
            36: (83.6, 87.4),
            37: (84.2, 88.0),
            38: (84.7, 88.6),
            39: (85.3, 89.2),
            40: (85.8, 89.8),
            41: (86.3, 90.4),
            42: (86.8, 90.9),
            43: (87.4, 91.5),
            44: (87.9, 92.0),
            45: (88.4, 92.5),
            46: (88.9, 93.1),
            47: (89.3, 93.6),
            48: (89.8, 94.1),
            49: (90.3, 94.6),
            50: (90.7, 95.1),
            51: (91.2, 95.6),
            52: (91.7, 96.1),
            53: (92.1, 96.6),
            54: (92.6, 97.1),
            55: (93.0, 97.6),
            56: (93.4, 98.1),
            57: (93.9, 98.5),
            58: (94.3, 99.0),
            59: (94.7, 99.5),
            60: (95.2, 99.9)
        }

        # Male height thresholds
        male_thresholds = {
            24: (78.0, 81.0),
            25: (78.6, 81.7),
            26: (79.3, 82.5),
            27: (79.9, 83.1),
            28: (80.5, 83.8),
            29: (81.1, 84.5),
            30: (81.7, 85.1),
            31: (82.3, 85.7),
            32: (82.8, 86.4),
            33: (83.4, 86.9),
            34: (83.9, 87.5),
            35: (84.4, 88.1),
            36: (85.0, 88.7),
            37: (85.5, 89.2),
            38: (86.0, 89.8),
            39: (86.5, 90.3),
            40: (87.0, 90.9),
            41: (87.5, 91.4),
            42: (88.0, 91.9),
            43: (88.4, 92.4),
            44: (88.9, 93.0),
            45: (89.4, 93.5),
            46: (89.8, 94.0),
            47: (90.3, 94.4),
            48: (90.7, 94.9),
            49: (91.2, 95.4),
            50: (91.6, 95.9),
            51: (92.1, 96.4),
            52: (92.5, 96.9),
            53: (93.0, 97.4),
            54: (93.4, 97.8),
            55: (93.9, 98.3),
            56: (94.3, 98.8),
            57: (94.7, 99.3),
            58: (95.3, 99.7),
            59: (95.6, 100.2),
            60: (96.1, 100.7)
        }

        # Get user inputs
        try:
            age = int(total_month_entry.get())
            gender = gender_option.get().lower()
            height = float(height_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for months and height.")
            return

        # Determine which thresholds to use
        if gender == "female":
            height_thresholds = female_thresholds
        elif gender == "male":
            height_thresholds = male_thresholds
        else:
            length_age_entry.insert(0, "Invalid gender")
            return

        # Check if age is in thresholds
        if age in height_thresholds:
            lower_threshold, upper_threshold = height_thresholds[age]

            if height < lower_threshold:
                length_age_entry.insert(0, "severe stunting")
            elif lower_threshold <= height < upper_threshold:
                length_age_entry.insert(0, "moderate stunting")
            else:
                length_age_entry.insert(0, "normal")
        else:
            length_age_entry.insert(0, "N/A")

    weight_age = ttk.Button(secondframe, text="Weight for age( only for 24-60 months)", command=weight_age_category)
    weight_age.grid(column=5, row=9)
    # button_hover(weight_age)
    weight_age_entry = Entry(secondframe, width=25)
    weight_age_entry.grid(column=6, row=9)

    length_age = ttk.Button(secondframe, text="Height for age (only for 24-60 months)",command=length_age_category)
    length_age.grid(column=5, row=10)
    # button_hover(length_age)
    length_age_entry = Entry(secondframe, width=25)
    length_age_entry.grid(column=6, row=10)

    weight_length = ttk.Button(secondframe, text="Weight for height (only for 24-60 months and between 45-120cm )", command=weight_length_category)
    weight_length.grid(column=5, row=11)
    # button_hover(weight_length)
    weight_length_entry = Entry(secondframe, width=25)
    weight_length_entry.grid(column=6, row=11)


    CheckVar1 = StringVar(value="no")
    b1_label = Label(sicknessframe, text="B1: Severe anemia", width=22).grid(column=1, row=14)
    b1_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar1, onvalue="yes", offvalue="no")
    b1_entry.grid(column=2, row=14)

    CheckVar2 = StringVar(value="no")
    b2_label = Label(sicknessframe, text="B2: Vitamin A deficiency", width=22).grid(column=1, row=15)
    b2_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar2, onvalue="yes", offvalue="no")
    b2_entry.grid(column=2, row=15)

    CheckVar3 = StringVar(value="no")
    b3_label = Label(sicknessframe, text="B3: Vit D deficiency", width=30).grid(column=1, row=16)
    b3_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar3, onvalue="yes", offvalue="no")
    b3_entry.grid(column=2, row=16)

    CheckVar4 = StringVar(value="no")
    b4_label = Label(sicknessframe, text="B4: Goitre", width=30).grid(column=1, row=17)
    b4_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar4, onvalue="yes", offvalue="no")
    b4_entry.grid(column=2, row=17)

    CheckVar5 = StringVar(value="no")
    b5_label = Label(sicknessframe, text="B5: Oedema / swelling of legs (2-6 years only)").grid(column=1, row=18)
    b5_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar5, onvalue="yes", offvalue="no")
    b5_entry.grid(column=2, row=18)

    CheckVar6 = StringVar(value="no")
    c1_label = Label(sicknessframe, text="C1: Convulsive disorders/epilepsy").grid(column=1, row=19)
    c1_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar6, onvalue="yes", offvalue="no")
    c1_entry.grid(column=2, row=19)

    CheckVar7 = StringVar(value="no")
    c2_label = Label(sicknessframe, text="C2: Otitis media/middle ear infection").grid(column=1, row=20)
    c2_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar7, onvalue="yes", offvalue="no")
    c2_entry.grid(column=2, row=20)

    CheckVar8 = StringVar(value="no")
    c3_label = Label(sicknessframe, text="C3: Dental condition", width=30).grid(column=1, row=21)
    c3_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar8, onvalue="yes", offvalue="no")
    c3_entry.grid(column=2, row=21)

    CheckVar9 = StringVar(value="no")
    c4_label = Label(sicknessframe, text="C4: Skin condition", width=30).grid(column=1, row=22)
    c4_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar9, onvalue="yes", offvalue="no")
    c4_entry.grid(column=2, row=22)

    CheckVar10 = StringVar(value="no")
    c5_label = Label(sicknessframe, text="C5: Rheumatic heart disease", width=30).grid(column=3, row=14)
    c5_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar10, onvalue="yes", offvalue="no")
    c5_entry.grid(column=4, row=14)

    CheckVar11 = StringVar(value="no")
    c6_label = Label(sicknessframe, text="C6: Respiratory problem (suggestive of Asthma/TB)", width=40)
    c6_label.grid(column=3, row=15)
    c6_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar11, onvalue="yes", offvalue="no")
    c6_entry.grid(column=4, row=15)

    CheckVar12 = StringVar(value="no")
    d1_label = Label(sicknessframe, text="D1: Vision problem (night vision or day vision)", width=40).grid(column=3, row=16)
    d1_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar12, onvalue="yes", offvalue="no")
    d1_entry.grid(column=4, row=16)

    CheckVar13 = StringVar(value="no")
    d2_label = Label(sicknessframe, text="D2: Delay in walking", width=30).grid(column=3, row=17)
    d2_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar13, onvalue="yes", offvalue="no")
    d2_entry.grid(column=4, row=17)

    CheckVar14 = StringVar(value="no")
    d3_label = Label(sicknessframe, text="D3: Stiffness/floppiness/reduced strength in arms/legs", width=40).grid(column=3, row=18)
    d3_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar14, onvalue="yes", offvalue="no")
    d3_entry.grid(column=4, row=18)


    CheckVar16 = StringVar(value="no")
    d5_label = Label(sicknessframe, text="D5: Reading/writing/calculatory difficulties", width=40)
    d5_label.grid(column=3, row=19)
    d5_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar16, onvalue="yes", offvalue="no")
    d5_entry.grid(column=4, row=19)

    CheckVar17 = StringVar(value="no")
    d6_label = Label(sicknessframe, text="D6: Difficulty in speaking", width=30).grid(column=3, row=20)
    d6_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar17, onvalue="yes", offvalue="no")
    d6_entry.grid(column=4, row=20)

    CheckVar18 = StringVar(value="no")
    d7_label = Label(sicknessframe, text="D7: Difficulty in hearing", width=30).grid(column=3, row=21)
    d7_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar18, onvalue="yes", offvalue="no")
    d7_entry.grid(column=4, row=21)

    CheckVar19 = StringVar(value="no")
    d8_label = Label(sicknessframe, text="D8: learning difficulties", width=30).grid(column=3, row=22)
    d8_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar19, onvalue="yes", offvalue="no")
    d8_entry.grid(column=4, row=22)

    CheckVar20 = StringVar(value="no")
    d9_label = Label(sicknessframe, text="D9: attention difficulties", width=30).grid(column=5, row=14)
    d9_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar20, onvalue="yes", offvalue="no")
    d9_entry.grid(column=6, row=14)

    #CheckVar21 = StringVar(value="no")

    #CheckVar22 = StringVar(value="no")

    CheckVar23 = StringVar(value="no")
    e3_label = Label(sicknessframe, text="E3: Feeling unduly tired/depressed (all students)").grid(column=5, row=15)
    e3_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar23, onvalue="yes", offvalue="no")
    e3_entry.grid(column=6, row=15)

    CheckVar24 = StringVar(value="no")
    e4_label = Label(sicknessframe, text="E4: Menstrual cycle started(female)?").grid(column=5, row=16)
    e4_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar24, onvalue="yes", offvalue="no")
    e4_entry.grid(column=6, row=16)

    CheckVar25 = StringVar(value="N/A")
    e5_label = Label(sicknessframe, text="E5: If periods started, are they irregular (28 +/- 7d)?").grid(column=5, row=17)
    e5_entry = OptionMenu(sicknessframe,CheckVar25,"N/A","Yes","No")
    e5_entry.grid(column=6, row=17)

    CheckVar26 = StringVar(value="no")
    e6_label = Label(sicknessframe, text="E6:Pain/burning while urinating (all students)?").grid(column=5, row=18)
    e6_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar26, onvalue="yes", offvalue="no")
    e6_entry.grid(column=6, row=18)

    CheckVar27 = StringVar(value="no")
    e7_label = Label(sicknessframe, text="E7: Discharge/foul smell from genito-urinary area (all students)?").grid(column=5, row=19)
    e7_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar27, onvalue="yes", offvalue="no")
    e7_entry.grid(column=6, row=19)

    CheckVar28 = StringVar(value="no")
    e8_label = Label(sicknessframe, text="E8: Menstrual pain (menstruating female)?").grid(column=5, row=20)
    e8_entry = Checkbutton(sicknessframe, text="Yes", width=5, variable=CheckVar28, onvalue="yes", offvalue="no")
    e8_entry.grid(column=6, row=20)

    CheckVar29 = StringVar(value="unknown")
    deworming_label = Label(sicknessframe, text="Dewormed last 6 months").grid(column=5, row=21)
    deworming_entry = OptionMenu(sicknessframe,CheckVar29,"unknown","yes","no")
    deworming_entry.grid(column=6, row=21)

    CheckVar30 = StringVar(value="unknown")
    vaccination_label = Label(sicknessframe, text="Follows govern. Childhood vacc. (immunization)").grid(column=5, row=22)
    vaccination_entry = OptionMenu(sicknessframe,CheckVar30, "unknown","yes","no")
    vaccination_entry.grid(column=6, row=22)

    lastframe = LabelFrame(scrollable_frame)
    lastframe.grid(row=28, rowspan=3, columnspan=2, ipadx=89,sticky=W)

    e9_label = Label(sicknessframe, text="E9: remarks (free text)", width=30)
    e9_label.grid(column=1, row=28)
    e9_entry = Entry(sicknessframe,width=120)
    e9_entry.grid(column=2, row=28,columnspan=4)


    known_disease_label = Label(secondframe, text="Known earlier disease")
    known_disease_label.grid(column=1, row=13)
    known_disease_entry = Entry(secondframe)
    known_disease_entry.grid(column=2, row=13)

    # Load the image (ensure that reset.png is in the correct directory or provide the full path)
    # Load the image
    reset_image = tk.PhotoImage(file="reset.png")

    # Resize the image to fit the button (use subsample to reduce the size)
    reset_image = reset_image.subsample(19, 19)  # Adjust the numbers to scale down (2, 2) means half size

    # Create the button with the image and command
    clearbtn = ttk.Button(buttonframe, image=reset_image, command=reset)
    cleartooltip = ToolTip(clearbtn,"New student")

    # Set the button position in the grid
    clearbtn.grid(row=0, column=2,padx=20)

    save_image = tk.PhotoImage(file="save.png")

    # Resize the image to fit the button (use subsample to reduce the size)
    save_image = save_image.subsample(19,19)  # A
    savebtn = ttk.Button(buttonframe, text="SAVE NEW SCREENING",image=save_image, command=save_or_update_entry)
    savebtn.grid(row=0, column=3,padx=20)
    tooltip = ToolTip(savebtn,"Save screening")

    delete_image = tk.PhotoImage(file="delete.png")

    import sqlite3
    from tkinter import messagebox

    def delete_journal():
        # Retrieve the student_id and screening_date from the relevant widgets
        student_id = id_entry.get()  # Ensure id_entry is correctly initialized
        screening_date = screening_date_entry.get()  # Ensure screening_date_entry is correctly initialized

        # Ensure student_id is provided before attempting to delete
        if not student_id:
            print("Please provide a Student ID.")
            return

        # Confirm with the user before deleting
        confirm_message = f"Are you sure you want to delete the entry for Student ID {student_id}"
        if screening_date:
            confirm_message += f" on {screening_date}?"
        else:
            confirm_message += " with no screening date?"

        confirm = messagebox.askyesno("Confirm Delete", confirm_message)
        if not confirm:
            return

        # Perform the deletion in the database
        try:
            with sqlite3.connect("gracehealth.db") as conn:  # Ensure database file path is correct
                cursor = conn.cursor()

                # Case when screening_date is provided
                if screening_date:
                    cursor.execute("""
                        DELETE FROM student
                        WHERE id = ? AND screen_date = ?
                        
                        
                    """, (student_id, screening_date))
                else:
                    # Case when screening_date is empty or NULL, delete based on student_id only
                    cursor.execute("""
                        DELETE FROM student
                        WHERE id = ? 
                        AND (screen_date IS NULL OR screen_date = '')
                        
                    """, (student_id,))

                conn.commit()

                # Check if the record was deleted
                if cursor.rowcount > 0:
                    print(f"Entry for Student ID {student_id} deleted successfully.")
                    clear_text()  # Call clear_text if it’s meant to clear the entries
                else:
                    print("No matching record found to delete.")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    # Resize the image to fit the button (use subsample to reduce the size)
    delete_image = delete_image.subsample(19, 19)  # A
    delete_btn = ttk.Button(buttonframe, text="SAVE NEW SCREENING", image=delete_image, command=delete_journal)
    delete_btn.grid(row=0, column=9, padx=20)
    delete_tooltip=ToolTip(delete_btn,"Delete this screening")

    def populate_for_edit(user_id=None, screening_date=None):


        with sqlite3.connect("gracehealth.db") as connection:
            cursor = connection.cursor()

            # Use the screening_date and user_id to fetch the student record
            if screening_date is not None:
                cursor.execute("""
                    SELECT * FROM student WHERE id = ? AND screen_date = ?
                """, (user_id, screening_date))
            else:
                cursor.execute("""
                    SELECT * FROM student WHERE id = ? ORDER BY rowid DESC LIMIT 1
                """, (user_id,))

            student_data = cursor.fetchone()

            if student_data is None:

                return

        # Populate each entry widget with the data from the database
        if student_data:
            try:
                # Assuming student_data structure and how you populate your form goes here...
                # Example for populating tea_garden_entry
                value = student_data[60]
                if value is not None and value.strip():
                    if value in tea_garden_entry['values']:
                        tea_garden_entry.set(value)
                    else:
                        print(f"Value '{value}' not found in Combobox values. Setting it as a default.")
                        tea_garden_entry.set('')  # Set a default value or leave it empty
                else:
                    print("Empty or None value from the database. Resetting the combobox.")
                    tea_garden_entry.set('')  # Set to empty string or a default value
            except IndexError:
                print("Index error while accessing student_data.")
            id_entry.delete(0, tk.END)
            id_entry.insert(0, student_data[0])

            name_entry.delete(0, tk.END)
            name_entry.insert(0, student_data[1])

            date_of_birth_entry.delete(0, tk.END)
            date_of_birth_entry.insert(0, student_data[2])

            gender_option.set(student_data[3])

            class_entry.delete(0, tk.END)
            class_entry.insert(0, student_data[4])

            roll_entry.delete(0, tk.END)
            roll_entry.insert(0, student_data[5])

            aadhaar_entry.delete(0, tk.END)
            aadhaar_entry.insert(0, student_data[6])

            father_guardian_entry.delete(0, tk.END)
            father_guardian_entry.insert(0, student_data[7])

            mother_entry.delete(0, tk.END)
            mother_entry.insert(0, student_data[8])

            contact_no_entry.delete(0, tk.END)
            contact_no_entry.insert(0, student_data[9])

            address_entry.delete(0, tk.END)
            address_entry.insert(0, student_data[10])

            email_entry.delete(0, tk.END)
            email_entry.insert(0, student_data[11])

            teacher_entry.delete(0, tk.END)
            teacher_entry.insert(0, student_data[12])

            school_entry.delete(0, tk.END)
            school_entry.insert(0, student_data[13])

            last_school_entry.delete(0, tk.END)
            last_school_entry.insert(0, student_data[14])

            place_of_birth_entry.delete(0, tk.END)
            place_of_birth_entry.insert(0, student_data[15])

            known_disease_entry.delete(0, tk.END)
            known_disease_entry.insert(0, student_data[16])

            weight_entry.delete(0, tk.END)
            weight_entry.insert(0, student_data[19])

            height_entry.delete(0, tk.END)
            height_entry.insert(0, student_data[20])

            BMI_entry.delete(0, tk.END)
            BMI_entry.insert(0, student_data[21])

            left_eyesight_var.set(student_data[23])
            right_eyesight_var.set(student_data[24])

            vision_problem_entry.delete(0, tk.END)
            vision_problem_entry.insert(0, student_data[25])

            CheckVar1.set(student_data[26])
            CheckVar2.set(student_data[27])
            CheckVar3.set(student_data[28])
            CheckVar4.set(student_data[29])
            CheckVar5.set(student_data[30])
            CheckVar6.set(student_data[31])
            CheckVar7.set(student_data[32])
            CheckVar8.set(student_data[33])
            CheckVar9.set(student_data[34])
            CheckVar10.set(student_data[35])
            CheckVar11.set(student_data[36])
            CheckVar12.set(student_data[37])
            CheckVar13.set(student_data[38])
            CheckVar14.set(student_data[39])
            CheckVar16.set(student_data[40])
            CheckVar17.set(student_data[41])
            CheckVar18.set(student_data[42])
            CheckVar19.set(student_data[43])
            CheckVar20.set(student_data[44])
            CheckVar23.set(student_data[45])
            CheckVar24.set(student_data[46])
            CheckVar25.set(student_data[47])
            CheckVar26.set(student_data[48])
            CheckVar27.set(student_data[49])
            CheckVar28.set(student_data[50])

            e9_entry.delete(0, tk.END)
            e9_entry.insert(0, student_data[51])

            BMI_category_entry.delete(0, tk.END)
            BMI_category_entry.insert(0, student_data[52])

            weight_age_entry.delete(0, tk.END)
            weight_age_entry.insert(0, student_data[53])

            length_age_entry.delete(0, tk.END)
            length_age_entry.insert(0, student_data[54])

            weight_length_entry.delete(0, tk.END)
            weight_length_entry.insert(0, student_data[55])

            total_month_entry.delete(0, tk.END)
            total_month_entry.insert(0, student_data[56])

            CheckVar29.set(student_data[57])
            CheckVar30.set(student_data[58])

            screening_date_entry.delete(0,tk.END)
            screening_date = student_data[61]


            if screening_date:  # Only insert if screening_date is not empty or None
                screening_date_entry.delete(0, 'end')  # Clear the DateEntry first
                screening_date_entry.insert(0, screening_date)
            else:
                # Handle the case where the screening_date is empty or None
                screening_date_entry.delete(0, 'end')  # Clear the DateEntry
                print("Empty or None value for screening date. Resetting the DateEntry.")
            #tea_garden_entry.delete(0, tk.END)
            #tea_garden_entry.set(student_data[60])
            age_value = student_data[62] if student_data[62] is not None else ""

            # Convert the value to string if necessary and insert it into the age_entry
            age_entry.delete(0, tk.END)  # Clear the entry before inserting
            age_entry.insert(0, str(age_value))
            #muac_entry.delete(0,END)
            #muac_entry.insert(0,student_data[64])

                # Check and insert data into the 'muac_entry' widget
            if student_data[64] is not None and student_data[64] != "":
                muac_entry.delete(0, 'end')  # Clear any existing text
                muac_entry.insert(0, str(student_data[64]))  # Ensure it's a string
            else:
                print("Empty or None value for 'muac'. Resetting the entry field.")
                muac_entry.delete(0, 'end')  # Clear the field
            if student_data[65] is not None and student_data[65] != "":
                muac_category_entry.delete(0, 'end')  # Clear any existing text
                muac_category_entry.insert(0, str(student_data[65]))  # Ensure it's a string
            else:
                print("Empty or None value for 'muac_category'. Resetting the entry field.")
                muac_category_entry.delete(0, 'end')  # Clear the field

    def populate_for_new_journal(item_id):
        connection = sqlite3.connect("gracehealth.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * from student where id = ? LIMIT 1 ",(item_id,))
        student_data= cursor.fetchone()
        id_entry.delete(0, tk.END)
        id_entry.insert(0, student_data[0])

        name_entry.delete(0, tk.END)
        name_entry.insert(0, student_data[1])

        date_of_birth_entry.delete(0, tk.END)
        date_of_birth_entry.insert(0, student_data[2])

        gender_option.set(student_data[3])
        aadhaar_entry.delete(0, tk.END)
        aadhaar_entry.insert(0, student_data[6])

        father_guardian_entry.delete(0, tk.END)
        father_guardian_entry.insert(0, student_data[7])

        mother_entry.delete(0, tk.END)

        mother_entry.insert(0, student_data[8])
        contact_no_entry.delete(0, tk.END)
        contact_no_entry.insert(0, student_data[9])
        tea_garden_entry.delete(0,tk.END)
        tea_garden_entry.insert(0,student_data[60])

        address_entry.delete(0, tk.END)
        address_entry.insert(0, student_data[10])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, student_data[11])

        teacher_entry.delete(0, tk.END)
        teacher_entry.insert(0, student_data[12])

        school_entry.delete(0, tk.END)
        school_entry.insert(0, student_data[13])

        last_school_entry.delete(0, tk.END)
        last_school_entry.insert(0, student_data[14])

        place_of_birth_entry.delete(0, tk.END)
        place_of_birth_entry.insert(0, student_data[15])

        known_disease_entry.delete(0, tk.END)
        known_disease_entry.insert(0, student_data[16])

        CheckVar29.set("unknown")
        CheckVar30.set(student_data[58])


    def next_record():

        current_id = int(id_entry.get())

        with sqlite3.connect('gracehealth.db') as conn:
            cursor = conn.cursor()

            # Step 1: Find the next available ID greater than current_id
            cursor.execute("SELECT MIN(id) FROM student WHERE id > ?", (current_id,))
            next_id_result = cursor.fetchone()

            if next_id_result and next_id_result[0] is not None:
                next_id = next_id_result[0]

                # Step 2: Get the latest screen_date row for that next_id
                cursor.execute("""
                    SELECT id, screen_date FROM student 
                    WHERE id = ? 
                    ORDER BY strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) DESC
                    
                """, (next_id,))

                latest_record = cursor.fetchall()
                print (f" check {latest_record}")
                cursor.execute("""
                                    SELECT id, screen_date FROM student 
                                    WHERE id = ? 
                                    ORDER BY strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) DESC

                                """, (next_id,))

                latest_record = cursor.fetchone()
                print (f" check latest sinlge {latest_record}")
                if latest_record:
                    print(f"This is the next ID: {next_id} with the latest date: {latest_record}")
                    populate_for_edit(latest_record[0],latest_record[1])
                    display_journal(next_id, summary_frame)
                else:
                    print("No records found for the next ID.")
            else:
                print("No more records available.")

    def previous_record():
        current_id = int(id_entry.get())

        with sqlite3.connect('gracehealth.db') as conn:
            cursor = conn.cursor()

            # Step 1: Find the next available ID greater than current_id
            cursor.execute("SELECT MAX(id) FROM student WHERE id < ?", (current_id,))
            next_id_result = cursor.fetchone()

            if next_id_result and next_id_result[0] is not None:
                next_id = next_id_result[0]

                # Step 2: Get the latest screen_date row for that next_id
                cursor.execute("""
                        SELECT id, screen_date FROM student 
                        WHERE id = ? 
                        ORDER BY strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) DESC

                    """, (next_id,))

                latest_record = cursor.fetchall()
                print(f" check {latest_record}")
                cursor.execute("""
                                        SELECT id, screen_date FROM student 
                                        WHERE id = ? 
                                        ORDER BY strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) DESC

                                    """, (next_id,))

                latest_record = cursor.fetchone()
                print(f" check latest sinlge {latest_record}")
                if latest_record:
                    print(f"This is the next ID: {next_id} with the latest date: {latest_record}")
                    populate_for_edit(latest_record[0], latest_record[1])
                    display_journal(next_id, summary_frame)
                else:
                    print("No records found for the next ID.")
            else:
                print("No more records available.")

    def student_same_previous():
        from datetime import datetime

        student_id = int(id_entry.get())
        display_current_date = screening_date_entry.get()  # Get date in MM/DD/YY format

        # Convert MM/DD/YY to YYYY-MM-DD for comparison
        current_screening_date = datetime.strptime(display_current_date, "%m/%d/%y").strftime("%Y-%m-%d")

        print(f"Current screening date: {current_screening_date}")  # Debugging output

        with sqlite3.connect('gracehealth.db') as conn:
            cursor = conn.cursor()

            # SQL query to find the previous screening date for the same student
            cursor.execute("""
                SELECT screen_date 
                FROM student 
                WHERE id = ? 
                AND strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) < ?
                ORDER BY strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) DESC
                LIMIT 1
            """, (student_id, current_screening_date))

            previous_date = cursor.fetchone()

            if previous_date:
                # Unpack the previous_date tuple
                previous_date_value = previous_date[0]
                print(f"Previous screening date: {previous_date_value}")  # Debugging output

                # Populate the UI with the previous screening date
                populate_for_edit(screening_date=previous_date_value, user_id=student_id)
            else:
                print("No more records available.")

    def student_same_next():
        try:
            from datetime import datetime

            student_id = int(id_entry.get())
            display_current_date = screening_date_entry.get()  # MM/DD/YY format

            # Convert MM/DD/YY to YYYY-MM-DD for comparison
            current_screening_date = datetime.strptime(display_current_date, "%m/%d/%y").strftime("%Y-%m-%d")

            print(f"Current screening date: {current_screening_date}")  # Debugging output

            with sqlite3.connect('gracehealth.db') as conn:
                cursor = conn.cursor()

                # SQL query to find the next screening date
                cursor.execute("""
                    SELECT screen_date 
                    FROM student 
                    WHERE id = ? 
                    AND strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) > ?
                    ORDER BY strftime('%Y-%m-%d', '20' || substr(screen_date, 7, 2) || '-' || substr(screen_date, 1, 2) || '-' || substr(screen_date, 4, 2)) ASC
                    LIMIT 1
                """, (student_id, current_screening_date))

                next_record = cursor.fetchone()

                if next_record:
                    next_screening_date = next_record[0]
                    print(f"Next screening date: {next_screening_date}")  # Debugging output

                    # Populate the UI with the next screening date
                    populate_for_edit(screening_date=next_screening_date, user_id=student_id)

                    # Optionally call display_journal if needed
                    display_journal(next_screening_date, summary_frame)
                else:
                    print("No more records available.")

        except ValueError:
            print("Invalid Student ID or screening date.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    next_image = tk.PhotoImage(file="next.png")

    # Resize the image to fit the button (use subsample to reduce the size)
    next_image = next_image.subsample(19, 19)  # A

    next_btn = ttk.Button(buttonframe, image=next_image, command=next_record)
    next_btn.grid(row=0, column=6, padx=20)
    next_tooltip= ToolTip(next_btn,"Next student")

    before_image = tk.PhotoImage(file="before.png")

    # Resize the image to fit the button (use subsample to reduce the size)
    before_image = before_image.subsample(19, 19)  # A

    before_btn = ttk.Button(buttonframe, image=before_image , command=previous_record)
    before_btn.grid(row=0, column=5, padx=20)
    before_tooltip= ToolTip(before_btn,"Previous student")

    # Hover function for styling buttons (assuming you already have this function)
    up_image = tk.PhotoImage(file="up-arrow.png")

    # Resize the image to fit the button (use subsample to reduce the size)
    up_image = up_image.subsample(19, 19)  # A


    up_btn = ttk.Button(buttonframe, image=up_image, command=student_same_next)
    up_btn.grid(row=0, column=7, padx=20)
    up_tooltip=ToolTip(up_btn,"Newer screening of same student")

    down_image = tk.PhotoImage(file="down-arrow.png")

    # Resize the image to fit the button (use subsample to reduce the size)
    down_image = down_image.subsample(19, 19)  # A


    down_btn = ttk.Button(buttonframe, image=down_image, command=student_same_previous)
    down_btn.grid(row=0, column=8, padx=20)
    down_tooltip =  ToolTip(down_btn,"Earlier screening of same student")

    check_id_confirmation = Label(scrollable_frame)
    check_id_confirmation.grid(row=2, column=4)
    id_value=id_entry.get()
    print(f"id_value is {id_value}")

    # Fix the button command: pass the function reference, not call it
    # Button to show journal, passing the id_entry widget, not the value
    #row_id_label = Label(buttonframe, text="Screening ID: None", font=("Arial", 12), fg="blue")
    #row_id_label.grid(row=0, column=9)



    connection.commit()
    connection.close()
    window.mainloop()





# mainwindow.config(background="light pink")
# mainwindow.title(" School Health records", )


        #Set up imports

connection=sqlite3.connect("gracehealth.db")
cursor=connection.cursor()
cursor.execute("SELECT DISTINCT tea_garden FROM student")
tea_garden_names=cursor.fetchall()
tea_garden_database_list = [tea_garden_chosen[0] for tea_garden_chosen in tea_garden_names]





cursor.execute("SELECT DISTINCT school_name FROM student")
school_names = cursor.fetchall()
school_database= [school[0] for school in school_names]

school_database_list = ["All schools combined"] + school_database
connection.commit()
connection.close()


font="Arial,12"

import sqlite3
import sqlite3



def delete_column_directly(column_name):
    try:
        # Connect to the database
        conn = sqlite3.connect("gracehealth.db")
        cursor = conn.cursor()

        # Drop the column
        cursor.execute(f"ALTER TABLE student DROP COLUMN {column_name};")

        # Commit the changes
        conn.commit()
        conn.close()

        print(f"Column '{column_name}' successfully deleted from the 'student' table.")
    except sqlite3.Error as e:
        print(f"Error while deleting column: {e}")




import sqlite3

def show_table_columns_with_index(database, table_name):
    try:
        # Connect to the database
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Fetch table column info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        # Print column details
        if columns:
            print(f"Columns in table '{table_name}':")
            print(f"{'Index':<10}{'Column Name':<20}{'Type':<10}{'Not Null':<10}{'Default Value'}")
            print("-" * 60)
            for col in columns:
                # col: (index, name, type, notnull, default_value, primary_key)
                index, name, col_type, notnull, default_value, primary_key = col
                print(f"{index:<10}{name:<20}{col_type:<10}{notnull:<10}{default_value}")
        else:
            print(f"No columns found for table '{table_name}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Example usage
show_table_columns_with_index("gracehealth.db", "student")
import sqlite3

def replace_school_name(old_name, new_name):
    try:
        # Connect to the database
        conn = sqlite3.connect("gracehealth.db")
        cursor = conn.cursor()

        # Update the school_name column
        cursor.execute("""
            UPDATE student
            SET school_name = ?
            WHERE school_name = ?;
        """, (new_name, old_name))

        # Commit the changes
        conn.commit()
        updated_rows = cursor.rowcount  # Get the number of updated rows
        conn.close()

        print(f"Successfully updated {updated_rows} rows: '{old_name}' replaced with '{new_name}'.")
    except sqlite3.Error as e:
        print(f"Error while updating school names: {e}")
replace_school_name("Eden Christian English school, Makrapara", "Eden English School")


def fetch_school_names():
    try:
        # Connect to the database
        connection = sqlite3.connect('gracehealth.db')
        cursor = connection.cursor()

        # SQL query to fetch distinct school names
        query = "SELECT DISTINCT school_name FROM student ORDER BY school_name ASC;"
        cursor.execute(query)

        # Fetch all results
        school_names = [row[0] for row in cursor.fetchall()]

        # Close the connection
        connection.close()

        return school_names

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Example usage
school_list = fetch_school_names()
print("School Names:", school_list)
import sqlite3
from tabulate import tabulate


import sqlite3

import sqlite3
import datetime


def show_screendate():
    conn = sqlite3.connect("gracehealth.db")
    cursor = conn.cursor()
    print("this is show_Screendate")

    cursor.execute("SELECT ROWID,id FROM student")
    rows = cursor.fetchall()
    print(rows)
    conn.commit()

    conn.close()


show_screendate()

new_journal()

