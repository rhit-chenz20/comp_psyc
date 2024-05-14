import tkinter as tk
from tkinter import ttk
import numpy as np


# Parameters for the animals [neck length, leg length, tail length, body height]
params = {
    'giraffe': [2.0, 1.12, 0.97],
    'horse': [2.0, 0.38, 0.97],
    'cat': [0.5, 0.38, 0.28]
}

param_range = {
    'neck_length': (0, 2.5),
    'leg_length': (0.1,1.5),
    'tail_length': (0.05, 1.2),
}

discrimination_range = {
    'neck_length': (0,1),
    'leg_length': (0.3 ,0.7),
    'tail_length': (0.2, 0.7),
}

lows = [0, 0.3, 0.2]
highs = [1, 0.7, 0.7]

animals = ['giraffe', 'horse', 'cat']
param_names = ['neck_length', 'leg_length', 'tail_length']

def generate_proposal(current_state):
    """ Generate a new proposal state based on current state """
    proposal = np.random.normal(current_state, 0.07*current_state)
    
    for i in range(len(proposal)):
        p = proposal[i]
        if(p < param_range[param_names[i]][0]):
            proposal[i] = param_range[param_names[i]][0]
        elif (p > param_range[param_names[i]][1]):
            proposal[i] = param_range[param_names[i]][1]
    return proposal

def generate_discrimination_proposal():
    re = np.array([0.0,0.0,0.0])
    for i in range(len(re)):
        param_r = discrimination_range[param_names[i]]
        re[i] = np.random.uniform(param_r[0], param_r[1])
    return re

def create_figure(state, canvas):
    """ Simulate creating a figure (string representation for simplicity) """
    canvas.delete("all")
    neck, leg, tail = state

    scale = 50
    neck_length = neck * scale
    leg_length = leg * scale
    tail_length = tail * scale
    body_height = 1 * scale

    x_start = 100
    y_start = 100
    canvas.create_line(x_start, y_start, x_start + body_height, y_start, fill="black", width=2)
    canvas.create_line(x_start + body_height, y_start, x_start + body_height + neck_length, y_start - neck_length / 2, fill="black", width=2)
    canvas.create_line(x_start, y_start, x_start - tail_length, y_start + tail_length / 2, fill="black", width=2)
    canvas.create_line(x_start + body_height * 0.25, y_start, x_start + body_height * 0.25, y_start + leg_length, fill="black", width=2)
    canvas.create_line(x_start + body_height * 0.75, y_start, x_start + body_height * 0.75, y_start + leg_length, fill="black", width=2)


class MCMCExperiment:
    def __init__(self, master, animal):
        self.master = master
        master.title("Animal Category Experiment")

        self.animal = animal  # Change to 'horse' or 'cat' to test different animals
        self.current_state = np.array(params[self.animal])  # Start with the base parameters
        self.proposal = generate_proposal(self.current_state)

        # Setup the GUI
        self.label = tk.Label(master, text=f"Which figure represents a {animal} better?")
        self.label.pack()
        
        #add keyboard control
        self.master.bind('j', lambda event: self.update_state(1))
        self.master.bind('k', lambda event: self.update_state(2))
        
        # Progress bar
        self.remaining_choices = 300
        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate", maximum=300)
        self.progress.pack(pady=20)
        self.progress['value'] = 300  # Start value for progress

        # Remaining choices label
        self.choices_label = tk.Label(master, text=f"Remaining Choices: {self.remaining_choices}")
        self.choices_label.pack()

        self.canvas1 = tk.Canvas(master, width=300, height=200)
        self.canvas1.pack(side=tk.LEFT, padx=20, pady=20)

        self.canvas2 = tk.Canvas(master, width=300, height=200)
        self.canvas2.pack(side=tk.RIGHT, padx=20, pady=20)

        create_figure(self.current_state, self.canvas1)
        create_figure(self.proposal, self.canvas2)
        
        # self.fig1_button = tk.Button(master, text=self.fig1_text, command=lambda: self.update_state(self.current_state))
        # self.fig2_button = tk.Button(master, text=self.fig2_text, command=lambda: self.update_state(self.proposal))
        
        # self.fig1_button.pack()
        # self.fig2_button.pack()

    def update_state(self, selected_figure):
        if self.remaining_choices > 0:
            self.remaining_choices -= 1
            self.choices_label.config(text=f"Remaining Choices: {self.remaining_choices}")
            self.progress['value'] = self.remaining_choices

        if selected_figure == 1:
            self.proposal = generate_proposal(self.current_state)
            create_figure(self.proposal, self.canvas2)
        else:
            self.current_state = self.proposal
            self.proposal = generate_proposal(self.current_state)
            create_figure(self.proposal, self.canvas1)

if __name__ == "__main__":
    root = tk.Tk()
    for n in animals:
        app = MCMCExperiment(root, n)
        root.mainloop()
