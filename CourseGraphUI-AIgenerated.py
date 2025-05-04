#####
# This code is 100% AI generated
# I'm using this as reference as I have 0 experience with tkinter
#####


import CourseGraph
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox

class CourseGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Graph Visualizer")
        self.root.geometry("800x600")
        
        # Initialize course graph
        self.current_graph = CourseGraph.CourseGraph("New Course Graph")
        
        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title label
        title_label = ttk.Label(self.main_frame, text="Course Graph Visualizer", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Create current graph name label
        self.graph_name_var = tk.StringVar(value=f"Current Graph: {self.current_graph.name}")
        graph_name_label = ttk.Label(self.main_frame, textvariable=self.graph_name_var, font=("Arial", 12))
        graph_name_label.pack(pady=5)
        
        # Create buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(pady=20, fill=tk.X)
        
        # Create buttons
        btn_width = 20
        
        import_btn = ttk.Button(buttons_frame, text="Import JSON File", width=btn_width, command=self.import_json)
        import_btn.grid(row=0, column=0, padx=10, pady=5)
        
        save_btn = ttk.Button(buttons_frame, text="Save to JSON File", width=btn_width, command=self.save_json)
        save_btn.grid(row=0, column=1, padx=10, pady=5)
        
        rename_btn = ttk.Button(buttons_frame, text="Rename Course Graph", width=btn_width, command=self.rename_graph)
        rename_btn.grid(row=1, column=0, padx=10, pady=5)
        
        add_course_btn = ttk.Button(buttons_frame, text="Add Course", width=btn_width, command=self.add_course)
        add_course_btn.grid(row=1, column=1, padx=10, pady=5)
        
        edit_course_btn = ttk.Button(buttons_frame, text="Edit Course", width=btn_width, command=self.edit_course)
        edit_course_btn.grid(row=2, column=0, padx=10, pady=5)
        
        delete_course_btn = ttk.Button(buttons_frame, text="Delete Course", width=btn_width, command=self.delete_course)
        delete_course_btn.grid(row=2, column=1, padx=10, pady=5)
        
        visualize_btn = ttk.Button(buttons_frame, text="Visualize Course Graph", width=btn_width, command=self.visualize_graph)
        visualize_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        # Create courses display area
        courses_frame = ttk.LabelFrame(self.main_frame, text="Courses", padding="10")
        courses_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for courses
        self.courses_tree = ttk.Treeview(courses_frame, columns=("name", "semester", "prereqs"), show="headings")
        self.courses_tree.heading("name", text="Course Name")
        self.courses_tree.heading("semester", text="Semester")
        self.courses_tree.heading("prereqs", text="Prerequisites")
        
        self.courses_tree.column("name", width=250)
        self.courses_tree.column("semester", width=150)
        self.courses_tree.column("prereqs", width=200)
        
        self.courses_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(courses_frame, orient=tk.VERTICAL, command=self.courses_tree.yview)
        self.courses_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Update courses display
        self.update_courses_display()
    
    def update_courses_display(self):
        # Clear existing items
        for item in self.courses_tree.get_children():
            self.courses_tree.delete(item)
        
        # Update graph name
        self.graph_name_var.set(f"Current Graph: {self.current_graph.name}")
        
        # Add course items
        if self.current_graph.size > 0:
            for course in self.current_graph.course_list:
                prereqs = ", ".join([p.get_course_code() for p in course.get_prerequisites()]) if course.get_prerequisites() else "None"
                
                semester_text = "Unassigned"
                if course.get_semester() != -1:
                    season = ["Winter", "Summer", "Fall"][course.get_semester() % 3]
                    year = (course.get_semester() // 3) + 2000
                    semester_text = f"{season} {year}"
                
                self.courses_tree.insert("", tk.END, values=(
                    f"{course.get_course_name()} ({course.get_course_code()})",
                    semester_text,
                    prereqs
                ))
    
    def import_json(self):
        filepath = filedialog.askopenfilename(
            title="Select JSON file to import",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            success = self.current_graph.import_from_json(filepath)
            if success:
                self.status_var.set(f"Successfully imported from {filepath}")
                self.update_courses_display()
            else:
                self.status_var.set(f"Failed to import from {filepath}")
    
    def save_json(self):
        filepath = filedialog.asksaveasfilename(
            title="Save course graph as JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            self.current_graph.export_to_json(filepath)
            self.status_var.set(f"Saved to {filepath}")
    
    def rename_graph(self):
        new_name = simpledialog.askstring("Rename Graph", "Enter new name for the course graph:", 
                                         initialvalue=self.current_graph.name)
        if new_name:
            self.current_graph.name = new_name
            self.graph_name_var.set(f"Current Graph: {self.current_graph.name}")
            self.status_var.set(f"Renamed graph to {new_name}")
    
    def add_course(self):
        # Create a new dialog window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Course")
        add_window.geometry("400x300")
        add_window.transient(self.root)
        add_window.grab_set()
        
        ttk.Label(add_window, text="Add New Course", font=("Arial", 14, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Course code
        ttk.Label(form_frame, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=5)
        code_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=code_var, width=30).grid(row=0, column=1, pady=5)
        
        # Course name
        ttk.Label(form_frame, text="Course Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var, width=30).grid(row=1, column=1, pady=5)
        
        # Semester
        ttk.Label(form_frame, text="Semester:").grid(row=2, column=0, sticky=tk.W, pady=5)
        semester_frame = ttk.Frame(form_frame)
        semester_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        season_var = tk.StringVar(value="Fall")
        season_combo = ttk.Combobox(semester_frame, textvariable=season_var, values=["Fall", "Winter", "Summer"], width=10)
        season_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        year_var = tk.StringVar(value="2025")
        ttk.Entry(semester_frame, textvariable=year_var, width=5).pack(side=tk.LEFT)
        
        # Prerequisites (would be implemented in a more sophisticated way in a real app)
        ttk.Label(form_frame, text="Prerequisites:").grid(row=3, column=0, sticky=tk.W, pady=5)
        prereq_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=prereq_var, width=30).grid(row=3, column=1, pady=5)
        ttk.Label(form_frame, text="(Comma-separated course codes)").grid(row=4, column=1, sticky=tk.W)
        
        # Buttons
        buttons_frame = ttk.Frame(add_window)
        buttons_frame.pack(pady=10)
        
        def save_course():
            code = code_var.get().strip()
            name = name_var.get().strip()
            
            if not code or not name:
                messagebox.showerror("Error", "Course code and name are required")
                return
            
            try:
                # Create a new course node
                new_course = CourseGraph.CourseGraph.CourseNode(
                    course_code=code,
                    course_name=name,
                    prerequisites=[],  # We'll add these later
                    corequisites=[],
                    semester=-1  # Set to unassigned initially
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
                self.update_courses_display()
                self.status_var.set(f"Added course: {code}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course: {str(e)}")
        
        ttk.Button(buttons_frame, text="Save", command=save_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=add_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_course(self):
        # This would be implemented similar to add_course but pre-filled with the selected course
        selection = self.courses_tree.selection()
        if not selection:
            messagebox.showinfo("Edit Course", "Please select a course to edit")
            return
        
        self.status_var.set("Edit course feature not fully implemented in this example")
    
    def delete_course(self):
        selection = self.courses_tree.selection()
        if not selection:
            messagebox.showinfo("Delete Course", "Please select a course to delete")
            return
        
        selected_item = self.courses_tree.item(selection[0])
        course_name = selected_item['values'][0]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {course_name}?")
        if confirm:
            # In a real implementation, you would find the actual course object and remove it
            self.status_var.set(f"Delete course feature not fully implemented in this example")
    
    def visualize_graph(self):
        if self.current_graph.size == 0:
            messagebox.showinfo("Visualize", "No courses to visualize")
            return
        
        try:
            self.current_graph.visualize()
            self.status_var.set("Graph visualization displayed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize graph: {str(e)}")

def main():
    root = tk.Tk()
    app = CourseGraphApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()