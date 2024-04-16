import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

class HeatmapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Heatmap GUI")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.plot_button = ttk.Button(self.main_frame, text="Generate Heatmaps", command=self.generate_heatmaps)
        self.plot_button.pack(pady=5)

        self.fig, self.axes = plt.subplots(nrows=2, ncols=4, figsize=(12, 6))

    def generate_heatmaps(self):
        for ax in self.axes.ravel():
            ax.clear()

        for i in range(8):
            row = i // 4
            col = i % 4
            ax = self.axes[row, col]

            data = np.random.rand(10, 10)
            ax.imshow(data, cmap='hot', interpolation='nearest')
            ax.set_title(f'Heatmap {i+1}')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = HeatmapGUI(root)
    root.mainloop()
