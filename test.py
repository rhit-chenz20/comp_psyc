import tkinter as tk
import numpy as np

params = {
    'giraffe': [1.8, 1.0, 0.5, 2.5],
    'horse': [0.8, 1.2, 0.3, 1.5],
    'cat': [0.4, 0.5, 0.8, 0.8]
}

std_devs = [0.1, 0.1, 0.1, 0.1]

def generate_proposal(current_state):
    """ Generate a new proposal state based on current state """
    proposal = np.random.normal(current_state, std_devs)
    return proposal

def create_figure(state, canvas):
    """ Draw the figure on a given canvas """
    canvas.delete("all")  
    neck, leg, tail, body = state

    scale = 50
    neck_length = neck * scale
    leg_length = leg * scale
    tail_length = tail * scale
    body_height = body * scale

   
    x_start = 100
    y_start = 100
    canvas.create_line(x_start, y_start, x_start + body_height, y_start, fill="black", width=2)
    canvas.create_line(x_start + body_height, y_start, x_start + body_height + neck_length, y_start - neck_length / 2, fill="black", width=2)
    canvas.create_line(x_start, y_start, x_start - tail_length, y_start + tail_length / 2, fill="black", width=2)
    canvas.create_line(x_start + body_height * 0.25, y_start, x_start + body_height * 0.25, y_start + leg_length, fill="black", width=2)
    canvas.create_line(x_start + body_height * 0.75, y_start, x_start + body_height * 0.75, y_start + leg_length, fill="black", width=2)

class MCMCExperiment:
    def __init__(self, master):
        self.master = master
        master.title("Animal Category Experiment")

        self.animal = 'cat' 
        self.current_state = np.array(params[self.animal])  
        self.proposal = generate_proposal(self.current_state)

        # Setup the GUI
        self.label = tk.Label(master, text="Which figure represents the animal better?")
        self.label.pack()

        self.canvas1 = tk.Canvas(master, width=300, height=200)
        self.canvas1.pack(side=tk.LEFT, padx=20, pady=20)

        self.canvas2 = tk.Canvas(master, width=300, height=200)
        self.canvas2.pack(side=tk.RIGHT, padx=20, pady=20)

        create_figure(self.current_state, self.canvas1)  
        create_figure(self.proposal, self.canvas2)

        self.fig1_button = tk.Button(master, text="Figure 1", command=lambda: self.update_state(1))
        self.fig2_button = tk.Button(master, text="Figure 2", command=lambda: self.update_state(2))
        
        self.fig1_button.pack(side=tk.LEFT, expand=True)
        self.fig2_button.pack(side=tk.RIGHT, expand=True)

    def update_state(self, selected_figure):
        """ Update the current state and regenerate proposals """
        if selected_figure == 1:
          
            self.proposal = generate_proposal(self.current_state)
            create_figure(self.proposal, self.canvas2)
        else:
           
            #temp = self.proposal
            self.current_state = self.proposal 
            self.proposal = generate_proposal(self.current_state)  
            #create_figure(self.current_state, self.canvas2)  # Update the canvas for figure 2
            create_figure(self.proposal, self.canvas1)  # Generate and display a new proposal on canvas 1

if __name__ == "__main__":
    root = tk.Tk()
    app = MCMCExperiment(root)
    root.mainloop()
