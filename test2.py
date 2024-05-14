import tkinter as tk
from tkinter import ttk
import numpy as np
import csv

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
    'neck_length': (0.2,1),
    'leg_length': (0.3 ,0.7),
    'tail_length': (0.2, 0.7),
}

animals = ['giraffe', 'horse', 'cat']
param_names = ['neck_length', 'leg_length', 'tail_length']
def generate_discrimination_proposal():
    re = np.array([0.0, 0.0, 0.0])
    for i in range(len(re)):
        param_r = discrimination_range[param_names[i]]
        re[i] = np.random.uniform(param_r[0], param_r[1])
    return re

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
    
class DiscriminationExperiment:
    def __init__(self, master):
        self.master = master
        master.title("Animal Discrimination Experiment")
        
        self.file = open('discrimination_experiment.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Figure', 'Choice'])

        self.label = tk.Label(master, text="Select the animal that the figure most closely represents (j = Giraffe, k = Dog, l = Cat)")
        self.label.pack()

        self.canvas = tk.Canvas(master, width=300, height=200)
        self.canvas.pack(pady=20)

        self.remaining_trials = 300
        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate", maximum=300)
        self.progress.pack()
        self.progress['value'] = 300

        master.bind('j', lambda event: self.record_choice('giraffe'))
        master.bind('k', lambda event: self.record_choice('dog'))
        master.bind('l', lambda event: self.record_choice('cat'))

        self.display_new_figure()

    def display_new_figure(self):
        self.current_state = generate_discrimination_proposal()
        create_figure(self.current_state, self.canvas)

    def record_choice(self, animal):
        if self.remaining_trials > 0:
            self.remaining_trials -= 1
            self.progress['value'] = 300 - self.remaining_trials
            formatted_current = [f'{x:.3f}' for x in self.current_state]
            self.writer.writerow([formatted_current, animal])
            if self.remaining_trials == 0:
                self.file.close()  
                self.label.config(text="Experiment completed. Thank you!")
            else:
                self.display_new_figure()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscriminationExperiment(root)
    root.mainloop()
    
