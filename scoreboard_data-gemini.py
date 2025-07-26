import xml.etree.ElementTree as ET
import time
import tkinter as tk

def scoreboard_data(file):
    """
    Parses the XML file to extract 'RunsRequiredToWin' and 'CurrentRunRate',
    then calculates and returns the rounded 'OversToWin'.
    """
    try:
        tree = ET.parse(file)
        root = tree.getroot()

        scoreboard = root.find('scoreboard')
        if scoreboard is None:
            return "Error: Scoreboard element not found"

        req = scoreboard.find("field[@key='RunsRequiredToWin']")
        rr = scoreboard.find("field[@key='CurrentRunRate']")

        if req is None or rr is None:
            return "Error: RunsRequiredToWin or CurrentRunRate not found"

        toWin = req.text.strip()
        runRate = rr.text.strip()

        toWin = float(toWin)
        runRate = float(runRate)

        if runRate == 0:
            return "Indefinite" # Avoid division by zero
        
        OvToWin = toWin / runRate
        OvToWin_rounded = int(round(OvToWin, 0))
        return OvToWin_rounded
    except Exception as e:
        return f"Error: {e}"

def update_scoreboard():
    """
    Calls scoreboard_data to get the latest value and updates the label.
    Schedules itself to run again after a delay.
    """
    new_data = scoreboard_data('nvplay-scoreboard1.xml')
    # Update the text of the existing label
    overs_label.config(text=new_data) 
    # Schedule the function to run again after 1000 milliseconds (1 second)
    root.after(1000, update_scoreboard) 

# Initialize the main window
root = tk.Tk()
root.title("Overs to Win")
root.geometry("300x200")
root.attributes('-topmost', True) # Keep window on top

# Create a label to display the overs to win. 
# We'll update its text later using .config()
overs_label = tk.Label(root, text="Loading...", font="Ariel, 100")
overs_label.pack()

# Create a close button
b = tk.Button(root, text="Close", command=root.destroy)
b.pack()

# Start the continuous update
update_scoreboard()

# Run the Tkinter event loop
root.mainloop()