from CourseGraph import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import tkinter.font as font
from math import *
import re
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

        add_btn = ttk.Button(buttons_frame, text="Add Course", width = btn_width, command = self.add_course)
        add_btn.grid(row = 1, column = 1, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        edit_btn = ttk.Button(buttons_frame, text="Edit Course", width = btn_width, command = self.edit_course)
        edit_btn.grid(row = 2, column = 0, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        remove_btn = ttk.Button(buttons_frame, text="Remove Course", width = btn_width, command = self.remove_course)
        remove_btn.grid(row = 2, column = 1, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        visualize_btn = ttk.Button(buttons_frame, text="Generate Graph", width = btn_width, command = self.visualize_graph)
        visualize_btn.grid(row = 3, column = 0, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        reset_btn = visualize_btn = ttk.Button(buttons_frame, text="Clear Data", width = btn_width, command = self.reset_graph)
        reset_btn.grid(row = 3, column = 1, padx = floor(10 * ZOOM_MULTIPLIER), pady = floor(5 * ZOOM_MULTIPLIER))

        #Course display area
        courses_frame = ttk.LabelFrame(self.main_frame, text="Courses", padding=str(floor(10 * ZOOM_MULTIPLIER)))
        courses_frame.pack(fill=tk.BOTH, expand=True, padx=floor(10 * ZOOM_MULTIPLIER), pady=floor(10 * ZOOM_MULTIPLIER))

        # Create treeview for courses
        self.courses_tree = ttk.Treeview(courses_frame, columns=("name", "semester", "prereqs", "coreqs"), show="headings")
        self.courses_tree.heading("name", text="Course Name")
        self.courses_tree.heading("semester", text="Semester")
        self.courses_tree.heading("prereqs", text="Prerequisites")
        self.courses_tree.heading("coreqs", text="Corequisites")
        
        self.courses_tree.column("name", width=floor(250 * ZOOM_MULTIPLIER))
        self.courses_tree.column("semester", width=floor(100 * ZOOM_MULTIPLIER))
        self.courses_tree.column("prereqs", width=floor(150 * ZOOM_MULTIPLIER))
        self.courses_tree.column("coreqs", width=floor(100 * ZOOM_MULTIPLIER))
        
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

                #Coreqs
                if (len(course.get_corequisites()) > 0):
                    coreqs_text = ", ".join([p.get_course_code() for p in course.get_corequisites()])
                else:
                    coreqs_text = "None"

                #Semester
                semester_text = "Unassigned"
                if course.get_semester() != -1:
                    season = ["Winter", "Summer", "Fall"][course.get_semester() % 3]
                    year = (course.get_semester() // 3) + 2000
                    semester_text = f"{season} {year}"

                self.courses_tree.insert("", tk.END, values=(
                    f"{course.get_course_name()} ({course.get_course_code()})",
                    semester_text,
                    prereqs_text,
                    coreqs_text
                ))

    def import_data(self):
        filePath = filedialog.askopenfilename(
            title = "Select JSON file to import",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filePath:
            #Filler for now
            self.current_graph = CourseGraph("New Course Graph")
            #end of filler
            success = self.current_graph.import_from_json(filePath)
            if success:
                self.status_var.set(f"Successfully imported from {filePath}")
                self.update_course_display()
            else:
                self.status_var.set(f"Failed to import from {filePath}")

            #Save filepath to automatically reopen json file next session
            file = open('savedata','w')
            file.write(filePath)
            file.close()
    
        
        
    def rename_graph(self):
        new_name = simpledialog.askstring("Rename Graph", "Enter new name for the course graph:", 
                                         initialvalue=self.current_graph.name)
        if new_name:
            self.current_graph.name = new_name
            self.graph_name_var.set(f"Current Graph: {self.current_graph.name}")
            self.status_var.set(f"Renamed graph to {new_name}")

    def save_data(self):
        filepath = filedialog.asksaveasfilename(
            title="Save course graph as JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            self.current_graph.export_to_json(filepath)
            self.status_var.set(f"Saved to {filepath}")

            #Save filepath to automatically reopen json file next session
            file = open('savedata','w')
            file.write(filepath)
            file.close()

    def add_course(self):
        #Dialog window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Course")
        add_window.geometry(str(floor(400 * ZOOM_MULTIPLIER)) + "x" + str(floor(300 * ZOOM_MULTIPLIER)))
        add_window.transient(self.root)
        add_window.grab_set()

        ttk.Label(add_window,
                  text="Add New Course",
                  font=(FONT, 
                         floor(14 * ZOOM_MULTIPLIER),
                         "bold")).pack(pady=floor(10 * ZOOM_MULTIPLIER))
        
        form_frame = ttk.Frame(add_window, padding = str(floor(10 * ZOOM_MULTIPLIER)))
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Course code
        ttk.Label(form_frame, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=floor(5 * ZOOM_MULTIPLIER))
        code_var = tk.StringVar()
        ttk.Entry(form_frame,
                  textvariable=code_var,
                  width=floor(30 * ZOOM_MULTIPLIER)).grid(row=0, 
                                                          column=1, 
                                                          pady=floor(5 * ZOOM_MULTIPLIER))
        
        #Course name
        ttk.Label(form_frame, text="Course Name:").grid(row=1, column=0, sticky=tk.W, pady=floor(5 * ZOOM_MULTIPLIER))
        name_var = tk.StringVar()
        ttk.Entry(form_frame,
                  textvariable=name_var,
                  width=floor(30 * ZOOM_MULTIPLIER)).grid(row=1, 
                                                          column=1, 
                                                          pady=floor(5 * ZOOM_MULTIPLIER))
        
        # Semester
        ttk.Label(form_frame, text="Semester:").grid(row=2, column=0, sticky=tk.W, pady=floor(5 * ZOOM_MULTIPLIER))
        semester_frame = ttk.Frame(form_frame)
        semester_frame.grid(row=2, column=1, sticky=tk.W, pady=floor(5 * ZOOM_MULTIPLIER))
        
        season_var = tk.StringVar(value="")
        season_combo = ttk.Combobox(semester_frame, textvariable=season_var, values=["","Fall", "Winter", "Summer"], width=floor(8 * ZOOM_MULTIPLIER))
        season_combo.pack(side=tk.LEFT, padx=(0, floor(5 * ZOOM_MULTIPLIER)))
        
        # Add label for year
        ttk.Label(semester_frame, text="Year:").pack(side=tk.LEFT, padx=(0, floor(2 * ZOOM_MULTIPLIER)))
        
        year_var = tk.StringVar()
        year_entry = ttk.Entry(semester_frame, textvariable=year_var, width=floor(5 * ZOOM_MULTIPLIER))
        year_entry.pack(side=tk.LEFT)


        # Prerequisites
        ttk.Label(form_frame, text="Prerequisites:").grid(row=3, 
                                                          column=0, 
                                                          sticky=tk.W, 
                                                          pady=floor(5 * ZOOM_MULTIPLIER)
                                                          )
        prereq_var = tk.StringVar()
        ttk.Entry(form_frame, 
                  textvariable=prereq_var, 
                  width=floor(30 * ZOOM_MULTIPLIER)
                  ).grid(row=3, column=1, pady=floor(5 * ZOOM_MULTIPLIER))

        # Corequisites
        ttk.Label(form_frame, text="Corequisites:").grid(row=4, 
                                                          column=0, 
                                                          sticky=tk.W, 
                                                          pady=floor(5 * ZOOM_MULTIPLIER)
                                                          )
        coreq_var = tk.StringVar()
        ttk.Entry(form_frame, 
                  textvariable=coreq_var, 
                  width=floor(30 * ZOOM_MULTIPLIER)
                  ).grid(row=4, column=1, pady=floor(4 * ZOOM_MULTIPLIER))
        ttk.Label(form_frame, text="(Enter comma-separated course codes for multiple courses)").grid(row=5, column=1, sticky=tk.W)
        ttk.Label(form_frame, text="Note: Prerequisite/Corequisite courses will only").grid(row=7, column=1,columnspan=2, sticky=tk.W)
        ttk.Label(form_frame, text="appear if they already exist in the dataset").grid(row=8, column=1,columnspan=2, sticky=tk.W)

        # Buttons
        buttons_frame = ttk.Frame(add_window)
        buttons_frame.pack(pady=floor(10 * ZOOM_MULTIPLIER))

        def save_button():
            #Get name and code
            code = code_var.get().strip()
            name = name_var.get().strip()

            if not code or not name:
                messagebox.showerror("Error", "Course code and name are required")
                return
            
            #Get prereqs and coreqs
            prereq_strings = prereq_var.get().split(',')
            prereq_courses = []
            if len(prereq_strings) > 1 or prereq_strings[0] != '':
                for string in prereq_strings:
                    string = string.strip()
                    course = self.current_graph.get_course(string)
                    if course != None:
                        prereq_courses.append(course)
                

            coreq_strings = coreq_var.get().split(',')
            coreq_courses = []
            if len(coreq_strings) > 1 or coreq_strings[0] != '':
                for string in coreq_strings:
                    string = string.strip()
                    course = self.current_graph.get_course(string)
                    if course != None:
                        coreq_courses.append(course)

            try:
                # Create a new course node
                new_course = CourseGraph.CourseNode(
                    course_code=code,
                    course_name=name,
                    prerequisites=prereq_courses,
                    corequisites=coreq_courses,
                    semester=-1
                )
                
                # Set the semester if provided
                if year_var.get().strip():
                    try:
                        new_course.set_semester(season_var.get(), int(year_var.get()))
                    except:
                        pass
                
                # Add to graph
                self.current_graph.add_course(new_course)
                
                # Close dialog
                add_window.destroy()
                
                # Update display
                self.update_course_display()
                self.status_var.set(f"Added course: {code}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course: {str(e)}")

        ttk.Button(buttons_frame, text="Save", command=save_button).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=add_window.destroy).pack(side=tk.LEFT, padx=5)

        

    def edit_course(self):

        selection = self.courses_tree.selection()
        ## Test lines
        # print(self.courses_tree.item(selection))
        # return
        if not selection:
            messagebox.showinfo("Edit Course", "Please select a course to edit")
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Course")
        edit_window.geometry(str(floor(400 * ZOOM_MULTIPLIER)) + "x" + str(floor(300 * ZOOM_MULTIPLIER)))
        edit_window.transient(self.root)
        edit_window.grab_set()

        ttk.Label(edit_window,
                  text="Edit Course",
                  font=(FONT, 
                         floor(14 * ZOOM_MULTIPLIER),
                         "bold")).pack(pady=floor(10 * ZOOM_MULTIPLIER))
        
        form_frame = ttk.Frame(edit_window, padding = str(floor(10 * ZOOM_MULTIPLIER)))
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Regex bs
        selected_course_text = self.courses_tree.item(selection)['values'][0]
        
        match = re.search(r'(.*) \(([^)]+)\)$', selected_course_text)
        
        if match:
            course_name = match.group(1).strip()
            course_code = match.group(2).strip()
        else:
            # Fallback if regex fails
            course_name = selected_course_text
            course_code = ""
            
        code_var = tk.StringVar(value=course_code)
        name_var = tk.StringVar(value=course_name)

        #Semester Values
        selected_semester_text = self.courses_tree.item(selection)['values'][1]

        if selected_semester_text == 'Unassigned':
            course_season = ""
            course_year = ""
        else:
            course_season, course_year = selected_semester_text.split()

        season_var = tk.StringVar(value=course_season)
        year_var = tk.StringVar(value=course_year)


        #Prereq/Coreq values
        selected_prereqs_text = self.courses_tree.item(selection)['values'][2]
        if selected_prereqs_text == 'None':
            prereq_var = tk.StringVar()
        else:
            prereq_var = tk.StringVar(value = selected_prereqs_text)

        selected_coreqs_text = self.courses_tree.item(selection)['values'][3]
        if selected_coreqs_text == 'None':
            coreq_var = tk.StringVar()
        else:
            coreq_var = tk.StringVar(value = selected_coreqs_text)

        
        # Course code
        ttk.Label(form_frame, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=floor(5 * ZOOM_MULTIPLIER))
        ttk.Entry(form_frame,
                  textvariable=code_var,
                  width=floor(30 * ZOOM_MULTIPLIER)).grid(row=0, 
                                                          column=1, 
                                                          pady=floor(5 * ZOOM_MULTIPLIER))
        
        #Course name
        ttk.Label(form_frame, text="Course Name:").grid(row=1, column=0, sticky=tk.W, pady=floor(5 * ZOOM_MULTIPLIER))
        ttk.Entry(form_frame,
                  textvariable=name_var,
                  width=floor(30 * ZOOM_MULTIPLIER)).grid(row=1, 
                                                          column=1, 
                                                          pady=floor(5 * ZOOM_MULTIPLIER))
        
        # Semester
        ttk.Label(form_frame, text="Semester:").grid(row=2, column=0, sticky=tk.W, pady=floor(5 * ZOOM_MULTIPLIER))
        semester_frame = ttk.Frame(form_frame)
        semester_frame.grid(row=2, column=1, sticky=tk.W, pady=floor(5 * ZOOM_MULTIPLIER))
        
        
        season_combo = ttk.Combobox(semester_frame, textvariable=season_var, values=["Fall", "Winter", "Summer"], width=floor(8 * ZOOM_MULTIPLIER))
        season_combo.pack(side=tk.LEFT, padx=(0, floor(5 * ZOOM_MULTIPLIER)))
        
        # Add label for year
        ttk.Label(semester_frame, text="Year:").pack(side=tk.LEFT, padx=(0, floor(2 * ZOOM_MULTIPLIER)))
        
        year_entry = ttk.Entry(semester_frame, textvariable=year_var, width=floor(5 * ZOOM_MULTIPLIER))
        year_entry.pack(side=tk.LEFT)


        # Prerequisites
        ttk.Label(form_frame, text="Prerequisites:").grid(row=3, 
                                                          column=0, 
                                                          sticky=tk.W, 
                                                          pady=floor(5 * ZOOM_MULTIPLIER)
                                                          )
        ttk.Entry(form_frame, 
                  textvariable=prereq_var, 
                  width=floor(30 * ZOOM_MULTIPLIER)
                  ).grid(row=3, column=1, pady=floor(5 * ZOOM_MULTIPLIER))
        ttk.Label(form_frame, text="(Comma-separated course codes)").grid(row=4, column=1, sticky=tk.W)

        ttk.Entry(form_frame, 
                  textvariable=coreq_var, 
                  width=floor(30 * ZOOM_MULTIPLIER)
                  ).grid(row=4, column=1, pady=floor(4 * ZOOM_MULTIPLIER))
        ttk.Label(form_frame, text="(Enter comma-separated course codes for multiple courses)").grid(row=5, column=1, sticky=tk.W)
        ttk.Label(form_frame, text="Note: Prerequisite/Corequisite courses will only").grid(row=7, column=1,columnspan=2, sticky=tk.W)
        ttk.Label(form_frame, text="appear if they already exist in the dataset").grid(row=8, column=1,columnspan=2, sticky=tk.W)


        # Buttons
        buttons_frame = ttk.Frame(edit_window)
        buttons_frame.pack(pady=floor(10 * ZOOM_MULTIPLIER))

        def save_button():
            #Get name and code
            code = code_var.get().strip()
            name = name_var.get().strip()

            if not code or not name:
                messagebox.showerror("Error", "Course code and name are required")
                return
            
            #Get prereqs and coreqs
            prereq_strings = prereq_var.get().split(',')
            prereq_courses = []
            if len(prereq_strings) > 1 or prereq_strings[0] != '':
                for string in prereq_strings:
                    string = string.strip()
                    course = self.current_graph.get_course(string)
                    if course != None:
                        prereq_courses.append(course)
                

            coreq_strings = coreq_var.get().split(',')
            coreq_courses = []
            if len(coreq_strings) > 1 or coreq_strings[0] != '':
                for string in coreq_strings:
                    string.strip()
                    course = self.current_graph.get_course(string)
                    if course != None:
                        coreq_courses.append(course)

            try:
                # Obtain referenced coursenode
                cur_course = self.current_graph.get_course(course_code)
                
                # Set new values
                cur_course.modify_code(code)
                cur_course.modify_name(name)
                cur_course.modify_prereqs(prereq_courses)
                cur_course.modify_coreqs(coreq_courses)
                
                # Set the semester if provided
                if year_var.get().strip():
                    try:
                        cur_course.set_semester(season_var.get(), int(year_var.get()))
                    except:
                        pass
                
                
                # Close dialog
                edit_window.destroy()
                
                # Update display
                self.update_course_display()
                self.status_var.set(f"Edited course: {code}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit course: {str(e)}")

        ttk.Button(buttons_frame, text="Save", command=save_button).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)

    def remove_course(self):
        selection = self.courses_tree.selection()
        if not selection:
            messagebox.showinfo("Delete Course", "Please select a course to delete")
            return
        
        selected_item = self.courses_tree.item(selection[0])
        course_name = selected_item['values'][0]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {course_name}?")
        if confirm:
            try:
                # Regex bs
                selected_course_text = self.courses_tree.item(selection)['values'][0]
                
                match = re.search(r'(.*) \(([^)]+)\)$', selected_course_text)
                
                if match:
                    course_name = match.group(1).strip()
                    course_code = match.group(2).strip()
                else:
                    # Fallback if regex fails
                    course_name = selected_course_text
                    course_code = ""
                
                deleted_course = self.current_graph.get_course(course_code)
                self.current_graph.remove_course(deleted_course)

                self.update_course_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete course: {str(e)}")

    def visualize_graph(self):
        """
        Calls the visualize method of the current graph to display a visual
        representation of the course structure.
        """
        if self.current_graph.size == 0:
            messagebox.showinfo("Visualize Graph", "The graph is empty. Please add courses first.")
            return
            
        try:
            self.current_graph.visualize()
            self.status_var.set("Graph visualization displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize graph: {str(e)}")
            self.status_var.set("Graph visualization failed")

    def reset_graph(self):
        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear your current data?")

        if confirm:
            self.current_graph = CourseGraph('New Course Graph')
            self.update_course_display()
            file = open('savedata','w')
            file.close()


def main():
    root = tk.Tk()
    app = CourseGraphApp(root)
    try:
        file = open('savedata','r')
        json_file = file.readline()
        app.current_graph.import_from_json(json_file)
        app.update_course_display()
        file.close()
    except:
        pass
    root.mainloop()

if __name__ == "__main__":
    main()
    # test = tk.Tk()
    # test.mainloop()
