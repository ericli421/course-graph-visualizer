try:
    import matplotlib as mp
    import matplotlib.pyplot as plt
    import networkx as nx
    import json
    import os
except:
    print("Please install matplotlib and networkx libraries to proceed")
    print("To install with pip, use 'pip install matplotlib networkx'")
    exit()


class CourseGraph:

    '''Class that represents a graph of courses in a particular program'''

    def __init__(self):
        '''Filler constructor'''
        self.name = ""
        self.size = 0
        self.course_list = []

    def __init__(self, name):
        '''
        Constructor that creates a new blank course graph

        Arguments:
            name (string): name of the program
        Returns:
            None (creates a new CourseGraph object)
        >>> comp_sci = CourseGraph('Computer Science')
        >>> print(comp_sci)
        Course Graph for Computer Science:
        Number of courses: 0
        Courses: None
        '''
        self.name = name
        self.size = 0
        self.course_list = []


    def __str__(self):
        '''
        Returns a string representation of the course graph
        Arguments:
            None
        Returns:
            string: string representation of the course graph
        '''
        line1 = "Course Graph for " + self.name + ":\n"
        line2 = "Number of courses: " + str(self.size) + "\n"
        line3 = "Courses: "
        if self.size == 0: 
            line3 += "None"
        else:
            for course in self.course_list:
                line3 += str(course.get_course_code()) + " "
        return line1 + line2 + line3
    
    def add_course(self, course):
        '''
        Adds a course to the course graph
        Arguments:
            course (CourseNode): course to be added
        Returns:
            None
        >>> comp_sci = CourseGraph('Computer Science')
        >>> comp202 = CourseNode('COMP 202', 'Foundations of Programming', [], [], 74)
        >>> comp_sci.add_course(comp202)
        >>> print(comp_sci)
        Course Graph for Computer Science:
        Number of courses: 1
        Courses: COMP 202 
        '''
        if self.size == 0:
            self.course_list = [course]
            self.size += 1
        else:
            self.course_list.append(course)
            self.size += 1

    def remove_course(self, course):
        '''
        Removes a course from the course graph
        Arguments:
            course (CourseNode): course to be removed
        Returns:
            None
        >>> comp_sci = CourseGraph('Computer Science')
        >>> comp202 = CourseNode('COMP 202', 'Foundations of Programming', [], [], 74)
        >>> comp_sci.add_course(comp202)
        >>> print(comp_sci)
        Course Graph for Computer Science:
        Number of courses: 1
        Courses: COMP 202 
        >>> comp_sci.remove_course(comp202)
        >>> print(comp_sci)
        Course Graph for Computer Science:
        Number of courses: 0
        Courses: None
        '''
        if self.size == 0 or course not in self.course_list:
            print("Error: Course does not exist")
            return
        else:
            self.course_list.remove(course)
            self.size -= 1

    # The following methods are fully AI generated
    def get_all_courses(self):
        """
        Get all courses in the graph.
        
        Returns:
            list: A list of all CourseNode objects in the graph
        """
        return list(self.courses.values())
    
    def get_course(self,code):
        '''
        Returns course node that matches course

        Arguments:
            code (string): Course code
        Returns:
            course (CourseNode): course
        '''
        if (len(self.course_list) <= 0):
            return None
        else:
            for course in self.course_list:
                if course.course_code == code:
                    return course
            return None
    
    def get_courses_by_semester(self, semester):
        """
        Get all courses in a specific semester.
        
        Arguments:
            semester (int): The semester to get courses for
            
        Returns:
            list: A list of CourseNode objects in the specified semester
        """
        return [course for course in self.courses.values() if course.semester == semester]
    
    def get_courses_without_semester(self):
        """
        Get all courses that haven't been assigned a semester yet.
        
        Returns:
            list: A list of CourseNode objects with semester = -1
        """
        return [course for course in self.courses.values() if course.semester == -1]
    
    def get_prerequisites_for(self, course_code):
        """
        Get all prerequisites for a specific course.
        
        Arguments:
            course_code (string): The code of the course to get prerequisites for
            
        Returns:
            list: A list of CourseNode objects that are prerequisites for the specified course
        """
        course = self.get_course(course_code)
        if course:
            return course.prerequisites
        return []
    
    def get_courses_requiring(self, course_code):
        """
        Get all courses that require a specific course as a prerequisite.
        
        Arguments:
            course_code (string): The code of the prerequisite course
            
        Returns:
            list: A list of CourseNode objects that have the specified course as a prerequisite
        """
        requiring_courses = []
        for course in self.courses.values():
            if any(prereq.course_code == course_code for prereq in course.prerequisites):
                requiring_courses.append(course)
        return requiring_courses
    
    def check_prerequisites_satisfied(self, course_code):
        """
        Check if all prerequisites for a course have been assigned a semester
        that comes before the course's semester.
        
        Arguments:
            course_code (string): The code of the course to check
            
        Returns:
            bool: True if all prerequisites are satisfied, False otherwise
        """
        course = self.get_course(course_code)
        if not course or course.semester == -1:
            return False
            
        for prereq in course.prerequisites:
            if prereq.semester == -1 or prereq.semester >= course.semester:
                return False
        return True
    
    def get_all_semesters(self):
        """
        Get a list of all semesters that have courses assigned to them.
        
        Returns:
            list: A sorted list of unique semester values (excluding -1)
        """
        semesters = set()
        for course in self.courses.values():
            if course.semester != -1:
                semesters.add(course.semester)
        return sorted(list(semesters))
    
    def export_to_json(self, filename):
        """
        Export the course graph to a JSON file.
        
        Arguments:
            filename (string): The name of the file to export to
        """

        # Convert the graph to a serializable format
        data = {}
        data["program_name"] = self.name
        for item in self.course_list:
            
            data[item.course_code] = {
                'name': item.course_name,
                'semester': item.semester,
                'prerequisites': [prereq.course_code for prereq in item.prerequisites],
                'corequisites': [coreq.course_code for coreq in item.corequisites]
            }
        
        # Write to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Course data exported to {filename}")
    
    def import_from_json(self, filename):
        """
        Import a course graph from a JSON file.
        
        Arguments:
            filename (string): The name of the file to import from
            
        Returns:
            bool: True if import was successful, False otherwise
        """
        
        
        if not os.path.exists(filename):
            print(f"Error: File {filename} does not exist")
            return False
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # First pass: Create all course nodes (without prerequisites/corequisites)
            for course_code, course_data in data.items():
                if (course_code == "program_name"):
                    self.name = course_data
                else:
                    self.add_course(CourseGraph.CourseNode(
                        course_code,
                        course_data['name'],
                        [],
                        [],
                        course_data['semester']
                    ))
                
            # Second pass: Add prerequisites/corequisites
            for course_code, course_data in data.items():
                if course_code != "program_name":
                    course = self.get_course(course_code)
                    for prereq_code in course_data['prerequisites']:
                        prereq = self.get_course(prereq_code)
                        if prereq:
                            course.add_prerequisite(prereq)
                    for coreq_code in course_data['corequisites']:
                        coreq = self.get_course(coreq_code)
                        if coreq:
                            course.add_corequisite(coreq)
                
            print(f"Successfully imported course data from {filename}")
            return True
        
        except Exception as e:
            print(f"Error importing course data: {str(e)}")
            return False
    
    def validate_graph(self):
        """
        Validate the graph to ensure there are no cycles or other issues.
        
        Returns:
            tuple: (is_valid, list of issues)
        """
        issues = []
        
        # Check for prerequisite cycles using DFS
        def has_cycle(node, visited, rec_stack):
            visited.add(node.course_code)
            rec_stack.add(node.course_code)
            
            for prereq in node.prerequisites:
                if prereq.course_code not in visited:
                    if has_cycle(prereq, visited, rec_stack):
                        return True
                elif prereq.course_code in rec_stack:
                    return True
                    
            rec_stack.remove(node.course_code)
            return False
        
        # Check each course for cycles
        for course in self.courses.values():
            visited = set()
            rec_stack = set()
            if has_cycle(course, visited, rec_stack):
                issues.append(f"Cycle detected involving {course.course_code}")
        
        # Check for prerequisite courses that come after the courses that require them
        for course in self.courses.values():
            if course.semester != -1:
                for prereq in course.prerequisites:
                    if prereq.semester == -1:
                        issues.append(f"{course.course_code} requires {prereq.course_code}, which has no semester assigned")
                    elif prereq.semester >= course.semester:
                        issues.append(f"{course.course_code} (semester {course.semester}) requires {prereq.course_code} (semester {prereq.semester}), which comes after or in the same semester")
        
        return (len(issues) == 0, issues)
    
    def get_semester_name(self, semester):
        """
        Convert a semester index to a human-readable name.
        
        Arguments:
            semester (int): The semester index
            
        Returns:
            string: The human-readable semester name (e.g., "Fall 2024")
        """
        if semester == -1:
            return "Unassigned"
            
        season = ["Fall", "Winter", "Summer"][semester % 3]
        year = (semester + 2) // 3 + 2024
        return f"{season} {year}"
    
    def visualize(self):
        '''
        Visualizes the course graph using a spring layout
        
        Arguments:
            None
        Returns:
            None
        '''
        import matplotlib.pyplot as plt
        
        # Create a directed graph
        G = nx.DiGraph()
        
        # Calculate how many courses have each course as a prerequisite or corequisite
        prereq_count = {}
        coreq_count = {}
        
        for course in self.course_list:
            course_code = course.get_course_code()
            if course_code not in prereq_count:
                prereq_count[course_code] = 0
            if course_code not in coreq_count:
                coreq_count[course_code] = 0
                
            # Count how many courses have this course as a prerequisite or corequisite
            for other_course in self.course_list:
                if course in other_course.get_prerequisites():
                    prereq_count[course_code] += 1
                if course in other_course.get_corequisites():
                    coreq_count[course_code] += 1
        
        # Add nodes and edges
        for course in self.course_list:
            course_code = course.get_course_code()
            semester = course.get_semester()
            
            # Add node with semester and dependency counts
            G.add_node(course_code, 
                      semester=semester,
                      prereq_count=prereq_count.get(course_code, 0),
                      coreq_count=coreq_count.get(course_code, 0))
            
            # Add edges for prerequisites and corequisites
            for prereq in course.get_prerequisites():
                G.add_edge(prereq.get_course_code(), course_code, type='prereq')
            
            for coreq in course.get_corequisites():
                G.add_edge(coreq.get_course_code(), course_code, type='coreq')
        
        # Calculate the total number of nodes to set appropriate figure size
        node_count = len(G.nodes())
        width = max(14, node_count * 0.8)
        height = max(10, node_count * 0.6)
        
        # Use a spring layout with optimized parameters for reduced overlap
        # Higher k value means more space between nodes (stronger repulsion)
        # More iterations mean better layout convergence
        pos = nx.spring_layout(G, k=1.8, iterations=100, seed=42)
        
        plt.figure(figsize=(width, height))
        plt.title(f"Course Graph for {self.name}", fontsize=16)
        
        # Color nodes by semester for visual grouping
        node_colors = []
        node_sizes = []
        color_map = plt.cm.get_cmap('viridis', 30)  # Color map with enough colors
        
        # Get unique semesters for color mapping
        all_semesters = set()
        for course in self.course_list:
            all_semesters.add(course.get_semester())
            
        semester_to_color = {sem: color_map(i/max(1, len(all_semesters)-1)) 
                            for i, sem in enumerate(sorted(all_semesters))}
        
        # Prepare node colors and sizes based on attributes
        for node in G.nodes():
            # Get node attributes
            node_data = G.nodes[node]
            semester = node_data.get('semester')
            prereq_count = node_data.get('prereq_count', 0)
            
            # Set node color based on semester
            if semester in semester_to_color:
                node_colors.append(semester_to_color[semester])
            else:
                node_colors.append('lightgrey')  # Default for unassigned
                
            # Set node size based on how many courses depend on it 
            # Base size of 2000, plus 500 for each course that depends on it
            node_sizes.append(2000 + (prereq_count * 500))
        
        # Draw the nodes with semester-based colors and size based on dependency count
        nx.draw_networkx_nodes(G, pos, 
                              node_size=node_sizes, 
                              node_color=node_colors,
                              edgecolors='black',
                              linewidths=1.0)
        
        # Draw prerequisite edges (solid lines)
        prereq_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'prereq']
        nx.draw_networkx_edges(G, pos, 
                              edgelist=prereq_edges,
                              width=1.5,
                              arrows=True,
                              arrowsize=15,
                              arrowstyle='->')
        
        # Draw corequisite edges (dashed lines)
        coreq_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'coreq']
        nx.draw_networkx_edges(G, pos, 
                              edgelist=coreq_edges,
                              width=1.5,
                              arrows=True,
                              arrowsize=15,
                              style='dashed',
                              arrowstyle='->',
                              edge_color='blue')
        
        # Create labels with dependency information
        custom_labels = {}
        for node in G.nodes():
            prereq_count = G.nodes[node].get('prereq_count', 0)
            coreq_count = G.nodes[node].get('coreq_count', 0)
            
            if prereq_count > 0 or coreq_count > 0:
                label = f"{node}\n(P:{prereq_count}, C:{coreq_count})"
            else:
                label = f"{node}"
            
            custom_labels[node] = label
            
        # Draw labels with dependency count information
        nx.draw_networkx_labels(G, pos, labels=custom_labels, font_size=9, font_weight='bold')
        
        # Add a legend for semesters
        legend_elements = []
        legend_labels = []
        
        for sem in sorted(all_semesters):
            if sem != -1:  # Skip unassigned semester
                season = ["Winter", "Summer", "Fall"][sem % 3]
                year = (sem // 3) + 2000
                semester_text = f"{season} {year}"
                legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                                 markerfacecolor=semester_to_color[sem], 
                                                 markersize=10))
                legend_labels.append(semester_text)
        
        # Add legend items for node size meaning
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                         markerfacecolor='lightgrey', 
                                         markersize=8))
        legend_labels.append('Node size = prerequisite importance')
        
        # Add legend items for prereq and coreq edges
        legend_elements.append(plt.Line2D([0], [0], color='black', lw=2))
        legend_labels.append('Prerequisite')
        
        legend_elements.append(plt.Line2D([0], [0], color='blue', lw=2, linestyle='--'))
        legend_labels.append('Corequisite')
        
        # Add legend explanation for labels
        legend_elements.append(plt.Line2D([0], [0], marker='', color='w'))
        legend_labels.append('P:X = X courses have this as prerequisite')
        
        legend_elements.append(plt.Line2D([0], [0], marker='', color='w'))
        legend_labels.append('C:Y = Y courses have this as corequisite')
        
        plt.legend(legend_elements, legend_labels, loc='upper right')
        
        plt.tight_layout()
        plt.axis('off')  # Hide axes
        plt.show()
        

    #End of AI generated methods
    
    class CourseNode:

        def __init__(self,
                    course_code,
                    course_name,
                    prerequisites,
                    corequisites,
                    semester
                    ):
            '''
            Constructor that creates a new node that represents a course

            Arguments:
                course_code (string)
                course_name (string)
                prerequisites (list of nodes)
                corequisites (list of nodes)
                semester (int): represents the semester where 0 = W2000, 1 = S2000, 2 = F2000, 3 = W2001 etc.
                                If this value is -1, it means it hasn't been assigned a semester yet
            Returns:
                None (creates a new CourseNode object)
            >>> comp202 = CourseNode('COMP 202', 'Foundations of Programming', [], [], 74)
            >>> print(comp202)
            Foundations of Programming (COMP 202):
                Prerequisites: None
                Corequisites: None
                This course has been taken (or expected to be taken) during Fall 2024
            >>> comp250 = CourseNode('COMP 250', 'Introduction to Computer Science', [comp202], [], 75)
            >>> print(comp250)
            Introduction to Computer Science (COMP 250):
                Prerequisites: COMP 202
                Corequisites: None
                This course has been taken (or expected to be taken) during Winter 2025
            '''
            self.course_code = course_code
            self.course_name = course_name
            self.prerequisites = prerequisites
            self.corequisites = corequisites
            self.semester = semester

        def __str__(self):
            line1 = self.course_name + " (" + self.course_code + "):\n" 

            if len(self.prerequisites) == 0:
                line2 = "   Prerequisites: None\n"
            else:
                line2 = "   Prerequisites: "
                for node in self.prerequisites:
                    line2 = line2 + node.course_code + " "
                line2 = line2 + '\n'

            if len(self.corequisites ) == 0:
                line3 = "   Corequisites: None\n"
            else:
                line3 = "   Corequisites: "
                for node in self.corequisites:
                    line3 = line3 + node.course_code + " "
                line3 = line3 + '\n'
            
            if self.semester == -1:
                line4 = "   This course has not been assigned a semester yet."
            else:
                line4 = "   This course has been taken (or expected to be taken) during " 
                if (self.semester % 3 == 0):
                    line4 = line4 + "Winter "
                elif (self.semester % 3 == 1):
                    line4 = line4 + "Summer "
                else:
                    line4 = line4 + "Fall "
                
                year = (self.semester) // 3 + 2000 
                line4 = line4 + str(year)
            
            return line1 + line2 + line3 + line4
        
        def get_course_code(self):
            return self.course_code
        
        def get_course_name(self): 
            return self.course_name
        
        def get_prerequisites(self):
            return self.prerequisites
        
        def get_corequisites(self):
            return self.corequisites
        
        def get_semester(self):
            return self.semester
        
        def add_prerequisite(self, course):
            '''Appends prereq node to prerequisites list'''
            if course not in self.prerequisites:
                self.prerequisites.append(course)

        def remove_prerequisite(self,course):
            if course in  self.prerequisites:
                self.prerequisites.remove(course)
            else:
                print("Course is not a prerequisite")
        
        def add_corequisite(self, course):
            '''Appends prereq node to prerequisites list'''
            if course not in self.corequisites:
                self.corequisites.append(course)

        def remove_corequisite(self,course):
            if (course in self.corequisites):
                self.prerequisites.remove(course)
            else:
                print("Course is not a corequisite")

        def set_semester(self, season, year):
            '''
            Sets semester value for object
            Arguments:
                season (string): either "fall", "winter" or "summer"
                year (int):
            Returns:
                None
            '''
            lower_season = season.lower()
            semester_value = 0

            if (lower_season == 'w' or lower_season == 'winter'):
                semester_value += 0
            elif (lower_season == 's' or lower_season == 'summer'):
                semester_value += 1
            elif (lower_season == 'f' or lower_season == 'fall'):
                semester_value += 2
            else:
                print(f"Error, {lower_season} is not a valid season")
                return
            
            if (int(year) < 2000):
                print("Error: Years before 2000 are not supported")
                return
            
            semester_value += (year - 2000) * 3

            for course in self.prerequisites:
                if semester_value >= course.semester:
                    print("WARNING: The prerequisiste " + course.course_code + " will not have been completed by this semester")
                
            for course in self.corequisites:
                if semester_value > course.semester:
                    print("WARNING: The corequisite " + course.course_code + " will not have been completed by this semester")

            self.semester = semester_value

        def remove_semester(self):
            '''
            Sets semester value for object to -1 (removes semester)
            Arguments:
                None
            Returns:
                None
            '''
            self.semester = -1
        
        def modify_code(self, new_code):
            '''
            Modifies course code
            Arguments:
                new_code (string): new course code
            Returns:
                None
            '''
            self.course_code = new_code
        
        def modify_name(self, new_name):
            '''
            Modifies course name
            Arguments:
                new_name (string): new course name
            Returns:
                None
            '''
            self.course_name = new_name

        def modify_prereqs(self,new_prereqs):
            '''
            Modifies prerequisites
            Arguments:
                new_prereqs (list of CourseNodes): new prereqs
            Returns:
                None
            '''
            self.prerequisites = new_prereqs
        
        def modify_coreqs(self,new_coreqs):
            '''
            Modifies corequisites
            Arguments:
                new_coreqs (list of CourseNodes): new coreqs
            Returns:
                None
            '''
            self.corequisites = new_coreqs



if __name__ == '__main__':
    graph = CourseGraph("test")
    c202 = CourseGraph.CourseNode('COMP 202', 'Foundations of Programming', [], [], 74)
    graph.add_course(c202)
    c250 = CourseGraph.CourseNode('COMP 250', 'Introduction to Computer Science', [c202], [], 75)
    graph.add_course(c250)
    c206 = CourseGraph.CourseNode('COMP 206', 'Introduction to Software Systems', [c202], [], 75)
    graph.add_course(c206)
    c273 = CourseGraph.CourseNode('COMP 273', 'Introduction to Computer Systems', [], [c206], 75)
    graph.add_course(c273)
    m240 =CourseGraph.CourseNode('MATH 240', 'Discrete Structures', [], [], 74)
    graph.add_course(m240)
    c251 = CourseGraph.CourseNode('COMP 251', 'Algorithms and Data Structures', [c250,m240],[],77)
    graph.add_course(c251)

    for course in graph.course_list:
        print(course)

    graph.export_to_json('test.json')
    graph2 = CourseGraph("test32")
    graph2.import_from_json('test.json')
    print(graph2)