# Course graph visualizer

A simple app that allows you to visualize university course loads in graph form. Useful for seeing prerequisite/corequisite networks

If this gets enough attention, I'll work on either an app version or a web version

A json file representing the [Major in Computer Science program](https://www.mcgill.ca/study/2024-2025/faculties/science/undergraduate/programs/bachelor-science-bsc-major-computer-science) at McGill University is included in this repo for demonstration purposes.

# Installation Instructions

This script currently requires you to install **Python**. To install it, head to [Python's official website](https://www.python.org/) and install the latest version by following the on screen instructions.

Firstly, download the repository's zip file. To do so, head to the code button here![the code button](https://docs.github.com/assets/cb-13128/mw-1440/images/help/repository/code-button.webp)

Click on "Download ZIP", and unzip the files.

From there, there are many ways you can start the program

- You can start the **_CourseGraphUI.py_** file by opening it through Python. You can do this with "Open With" and selecting Python or opening an [IDE](https://www.geeksforgeeks.org/top-python-ide/). If you select this option, make sure to install the MatPlotLib and NetworkX modules, which this program relies on. To do so, first install pip.

  > [Install pip on Windows](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)
  >
  > [Install pip on MacOS](https://www.geeksforgeeks.org/how-to-install-pip-in-macos/)
  >
  > To install pip on most linux distros run the command `$ sudo apt install python3-pip`. If this command doesn't work, this probably means you're on a more advanced version of Linux. If that's the case I'm trusting you to know how to install pip on your own.

  Once you installed pip, run the following two command on your terminal. Then run the **_CourseGraphUI.py_** file

  ```
  pip install matplotlib networkx
  ```

- If all of that sounded too complicated, don't worry, I packaged an easier way to open the file.

  - For Linux and MacOS users, run the _start.sh_ file included in the repository. If that doesn't work, open terminal, drag the file into the terminal window and run that.

  - For Windows users, run the _start.bat_ file.

  In either situation, if the script doesn't work, make sure pip is installed. Otherwise, please contact someone knowledgeable about the matter.
