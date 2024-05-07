import tkinter as tk
from tkinter import messagebox
import numpy as np

# Parameters for the animals [neck length, leg length, tail length, body height]
params = {
    'giraffe': [1.8, 1.0, 0.5, 2.5],
    'horse': [0.8, 1.2, 0.3, 1.5],
    'cat': [0.4, 0.5, 0.8, 0.8]
}

# Standard deviations for the proposals
std_devs = [0.1, 0.1, 0.1, 0.1]

def generate_proposal(current_state):
    """ Generate a new proposal state based on current state """
    proposal = np.random.normal(current_state, std_devs)
    return proposal

def create_figure(state):
    """ Simulate creating a figure (string representation for simplicity) """
    return f"Neck: {state[0]:.2f}, Leg: {state[1]:.2f}, Tail: {state[2]:.2f}, Body: {state[3]:.2f}"

class MCMCExperiment:
    def __init__(self, master):
        self.master = master
        master.title("Animal Category Experiment")

        self.animal = 'giraffe'  # Change to 'horse' or 'cat' to test different animals
        self.current_state = np.array(params[self.animal])  # Start with the base parameters
        self.proposal = generate_proposal(self.current_state)

        # Setup the GUI
        self.label = tk.Label(master, text="Which figure represents the animal better?")
        self.label.pack()

        self.fig1_text = create_figure(self.current_state)
        self.fig2_text = create_figure(self.proposal)

        self.fig1_button = tk.Button(master, text=self.fig1_text, command=lambda: self.update_state(self.current_state))
        self.fig2_button = tk.Button(master, text=self.fig2_text, command=lambda: self.update_state(self.proposal))
        
        self.fig1_button.pack()
        self.fig2_button.pack()

    def update_state(self, chosen_state):
        """ Update the current state and regenerate proposals """
        if np.array_equal(chosen_state, self.proposal):
            self.current_state = chosen_state
        self.proposal = generate_proposal(self.current_state)
        
        # Update buttons
        self.fig1_text = create_figure(self.current_state)
        self.fig2_text = create_figure(self.proposal)
        self.fig1_button.config(text=self.fig1_text)
        self.fig2_button.config(text=self.fig2_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MCMCExperiment(root)
    root.mainloop()
