from CourseGraph import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import tkinter.font as font
from math import *
###########################
# Basic Overview:
# Options: Import JSON, Export JSON (save), Rename Graph, Add Course, Remove Course, Edit Course, Visualize Graph, Exit
###########################

#Constants (change at will)
FONT = "Arial"
ZOOM_MULTIPLIER = 1.5

class CourseGraphApp:
    '''A GUI application that manages course graphs'''

    #Begin Constructor
    def __init__(self, root):
        '''Constructor'''
        self.root = root
        self.root.title("Course Graph Visualizer")
        width = 800 * ZOOM_MULTIPLIER
        height = 600 * ZOOM_MULTIPLIER
        self.root.geometry(str(floor(width)) + 'x' + str(floor(height)))

        #Load a blank graph
        self.current_graph = CourseGraph("New Course Graph")

        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding=str(floor(10 * ZOOM_MULTIPLIER)))
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        #Create Main label
        title_label = ttk.Label(self.main_frame, text="Course Graph Visualizer", font=(FONT, int(floor(18 * ZOOM_MULTIPLIER)), "bold"))
        title_label.pack(pady=floor(10 * ZOOM_MULTIPLIER))

        #Create current graph label
        self.graph_name_var = tk.StringVar(value=f"Current Data: {self.current_graph.name}")
        graph_name_label = ttk.Label(self.main_frame, textvariable=self.graph_name_var, font=(FONT, int(floor(12 * ZOOM_MULTIPLIER))))
        graph_name_label.pack(pady=floor(5 * ZOOM_MULTIPLIER))

        #Create buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(pady= int(floor(20 * ZOOM_MULTIPLIER)), fill=tk.X)

        #Buttons
        btn_width = floor(20 * ZOOM_MULTIPLIER)

        import_btn = ttk.Button(buttons_frame, text="Import JSON data", width = btn_width, command = self.import_data)
        import_btn.grid(row = 0, column = 0, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        rename_btn = ttk.Button(buttons_frame, text="Rename Graph", width = btn_width, command = self.rename_graph)
        rename_btn.grid(row = 0, column = 1, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        save_btn = ttk.Button(buttons_frame, text="Save to JSON", width = btn_width, command = self.save_data)
        save_btn.grid(row = 1, column = 0, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        add_btn = ttk.Button(buttons_frame, text="Add Course", width = btn_width, command = self.edit_course)
        add_btn.grid(row = 1, column = 1, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        edit_btn = ttk.Button(buttons_frame, text="Edit Course", width = btn_width, command = self.edit_course)
        edit_btn.grid(row = 2, column = 0, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        remove_btn = ttk.Button(buttons_frame, text="Remove Course", width = btn_width, command = self.remove_course)
        remove_btn.grid(row = 2, column = 1, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        visualize_btn = ttk.Button(buttons_frame, text="Generate Graph", width = btn_width * 2 + floor(5 * ZOOM_MULTIPLIER), command = self.visualize_graph)
        visualize_btn.grid(row = 3, column = 0, columnspan=2, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        #Course display area
        courses_frame = ttk.LabelFrame(self.main_frame, text="Courses", padding=str(floor(10 * ZOOM_MULTIPLIER)))
        courses_frame.pack(fill=tk.BOTH, expand=True, padx=floor(10 * ZOOM_MULTIPLIER), pady=floor(10 * ZOOM_MULTIPLIER))

        # Create treeview for courses
        self.courses_tree = ttk.Treeview(courses_frame, columns=("name", "semester", "prereqs"), show="headings")
        self.courses_tree.heading("name", text="Course Name")
        self.courses_tree.heading("semester", text="Semester")
        self.courses_tree.heading("prereqs", text="Prerequisites")
        
        self.courses_tree.column("name", width=floor(250 * ZOOM_MULTIPLIER))
        self.courses_tree.column("semester", width=floor(150 * ZOOM_MULTIPLIER))
        self.courses_tree.column("prereqs", width=floor(200 * ZOOM_MULTIPLIER))
        
        self.courses_tree.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(courses_frame, orient=tk.VERTICAL, command=self.courses_tree.yview)
        self.courses_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_course_display()

    #End constructor

    def update_course_display(self):
        #Clear data
        for course in self.courses_tree.get_children():
            self.courses_tree.delete(course)

        #Update name and data
        self.graph_name_var.set(f"Current Data: {self.current_graph.name}")

        if self.current_graph.size > 0:
            for course in self.current_graph.course_list:
                
                #Prereqs
                if (len(course.get_prerequisites()) > 0):
                    prereqs_text = ", ".join([p.get_course_code() for p in course.get_prerequisites()])
                else:
                    prereqs_text = "None"

                #Semester
                semester_text = "Unassigned"
                if course.get_semester() != -1:
                    season = ["Winter", "Summer", "Fall"][course.get_semester() % 3]
                    year = (course.get_semester() // 3) + 2000
                    semester_text = f"{season} {year}"

                self.courses_tree.insert("", tk.END, values=(
                    f"{course.get_course_name()} ({course.get_course_code()})",
                    semester_text,
                    prereqs_text
                ))

    def import_data(self):
        filePath = filedialog.askopenfilename(
            title = "Select JSON file to import",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filePath:
            success = self.current_graph.import_from_json(filePath)
            if success:
                self.status_var.set(f"Successfully imported from {filePath}")
                self.update_course_display()
            else:
                self.status_var.set(f"Failed to import from {filePath}")
    
        
        
    def rename_graph(self):
        pass

    def save_data(self):
        pass

    def add_course(self):
        pass
        
    def edit_course(self):
        pass

    def remove_course(self):
        pass

    def visualize_graph(self):
        pass


def main():
    root = tk.Tk()
    app = CourseGraphApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    # test = tk.Tk()
    # test.mainloop()
    