import tkinter as tk
from tkinter import ttk
import numpy as np
import csv

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

animals = ['giraffe', 'horse', 'cat']
param_names = ['neck_length', 'leg_length', 'tail_length']

def generate_proposal(current_state):
    proposal = np.random.normal(current_state, 0.07 * current_state)
    for i, param in enumerate(['neck_length', 'leg_length', 'tail_length']):
        min_val, max_val = param_range[param]
        proposal[i] = max(min(proposal[i], max_val), min_val)
    return proposal

def create_figure(state, canvas):
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
    def __init__(self, master):
        self.master = master
        master.title("Animal Category Experiment")

        self.canvas1 = tk.Canvas(master, width=300, height=200)
        self.canvas1.pack(side=tk.LEFT, padx=20, pady=20)
        self.canvas2 = tk.Canvas(master, width=300, height=200)
        self.canvas2.pack(side=tk.RIGHT, padx=20, pady=20)

        self.remaining_choices = 300
        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate", maximum=300)
        self.progress.pack(pady=20)
        self.progress['value'] = 300
        self.choices_label = tk.Label(master, text=f"Remaining Choices: {self.remaining_choices}")
        self.choices_label.pack()

       
        self.reset_button = tk.Button(master, text="Restart", command=self.reset_experiment)
        self.reset_button.pack()
        self.reset_button.pack_forget()

        # Bind keys
        self.master.bind('j', lambda event: self.update_state(1))
        self.master.bind('k', lambda event: self.update_state(2))

        self.animal_index = 0  
        self.init_experiment()

    def init_experiment(self):
        self.animal = animals[self.animal_index % len(animals)]
        self.current_state = np.array(params[self.animal])
        self.proposal = generate_proposal(self.current_state)
        self.file = open(f'{self.animal}_experiment.csv', 'w', newline='') 
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Pic 1', 'Pic 2', 'Pick'])  
        self.update_label()
        create_figure(self.current_state, self.canvas1)
        create_figure(self.proposal, self.canvas2)

    def update_label(self):
        if hasattr(self, 'label'):
            self.label.config(text=f"Which figure represents a {self.animal} better?")
        else:
            self.label = tk.Label(self.master, text=f"Which figure represents a {self.animal} better?")
            self.label.pack()

    def update_state(self, selected_figure):
        if self.remaining_choices > 0:
            self.remaining_choices -= 1
            self.choices_label.config(text=f"Remaining Choices: {self.remaining_choices}")
            self.progress['value'] = self.remaining_choices
            formatted_current = [f'{x:.3f}' for x in self.current_state]
            formatted_proposal = [f'{x:.3f}' for x in self.proposal]
            self.writer.writerow([formatted_current, formatted_proposal, selected_figure])
            self.proposal = generate_proposal(self.current_state if selected_figure == 1 else self.proposal)
            create_figure(self.proposal, self.canvas1 if selected_figure == 2 else self.canvas2)
            if self.remaining_choices == 0:
                self.file.close()
                self.reset_button.pack()

    def reset_experiment(self):
        self.file.close()  
        self.animal_index = (self.animal_index + 1) % len(animals)
        self.animal = animals[self.animal_index]
        self.current_state = np.array(params[self.animal])
        self.remaining_choices = 300
        self.progress['value'] = 300
        self.init_experiment()  
        self.reset_button.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = MCMCExperiment(root)
    root.mainloop()


   