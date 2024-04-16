import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

class HeatmapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Heatmap GUI")

        # Tworzenie głównego ramienia
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Tworzenie przycisku do generowania wykresów
        self.plot_button = ttk.Button(self.main_frame, text="Generate Heatmaps", command=self.generate_heatmaps)
        self.plot_button.pack(pady=5)

    def generate_heatmaps(self):
        # Tworzenie subplotów (wykresów) 2x4
        fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(12, 6))

        # Czyszczenie wszystkich subplotów (wykresów)
        for ax in axes.ravel():
            ax.clear()

        # Iteracja po każdym subplotcie (wykresie)
        for i in range(8):
            row = i // 4
            col = i % 4
            ax = axes[row, col]

            # Generowanie losowych danych dla wykresu cieplnego
            data = np.random.rand(10, 10)
            im = ax.imshow(data, cmap='hot', interpolation='nearest')

            # Ustawianie tytułu dla wykresu
            ax.set_title(f'Heatmap {i+1}')

            # Dodawanie legendy do wykresu
            fig.colorbar(im, ax=ax)

        # Dopasowanie layoutu wykresów
        plt.tight_layout()

        # Wyświetlenie wykresów
        plt.show()

if __name__ == "__main__":
    # Inicjalizacja głównego okna Tkinter
    root = tk.Tk()
    
    # Tworzenie instancji klasy HeatmapGUI
    app = HeatmapGUI(root)
    
    # Rozpoczęcie pętli głównej Tkinter
    root.mainloop()
