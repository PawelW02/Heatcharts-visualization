import csv
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Entry, filedialog, simpledialog
import subprocess
import pandas as pd

class HeatmapGenerator:
    def __init__(self):
        self.file_paths = []
        self.heatmap_axes = []

    def read_csv_file_with_labels(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            labels = next(reader)  # The first row for x-axis labels
            data = []
            y_labels = []
            for row in reader:
                y_labels.append(row[0])  # First column for y-axis labels
                data.append([float(val) for val in row[1:]])
        return np.array(data), labels[1:], y_labels

    def generate_heatmaps(self, file_paths):
        self.file_paths = file_paths
        self.heatmap_axes = []
        num_files = len(file_paths)
        num_views = (num_files + 7) // 8

        for view in range(num_views):
            heatmap_fig = plt.figure(figsize=(15, 20))
            for i in range(8):
                file_index = view * 8 + i
                if file_index >= num_files:
                    break
                file_path = file_paths[file_index]
                heatmap_data, x_labels, y_labels = self.read_csv_file_with_labels(file_path)

                ax = heatmap_fig.add_subplot(4, 2, i + 1)
                cax = ax.imshow(heatmap_data, cmap='hot', interpolation='nearest')
                ax.set_xticks(np.arange(0, len(x_labels), max(1, len(x_labels)//10)))
                ax.set_xticklabels([x_labels[j] for j in np.arange(0, len(x_labels), max(1, len(x_labels)//10))], rotation=90)
                ax.set_yticks(np.arange(0, len(y_labels), max(1, len(y_labels)//10)))
                ax.set_yticklabels([y_labels[j] for j in np.arange(0, len(y_labels), max(1, len(y_labels)//10))])
                ax.set_xlabel('X Axis')
                ax.set_ylabel('Y Axis')
                ax.set_title(f'{file_path}')
                heatmap_fig.colorbar(cax, ax=ax)

                max_row_index = np.argmax(np.sum(heatmap_data, axis=1))
                y_labels[max_row_index] += ' (Max)'

                self.heatmap_axes.append((file_path, heatmap_data, x_labels, y_labels, ax, max_row_index))

            heatmap_fig.tight_layout()
            heatmap_fig.show()

    def generate_line_plot(self, file_path, heatmap_data, x_labels, y_labels, row_index):
        lineplot_fig = plt.figure(figsize=(8, 6))
        max_row_data = heatmap_data[row_index]

        ax_line = lineplot_fig.add_subplot(1, 1, 1)
        ax_line.plot(x_labels, max_row_data, marker='o')
        ax_line.set_ylim([-70, -35])
        ax_line.set_xlabel('X Axis')
        ax_line.set_ylabel('Values')
        ax_line.set_title(f'Line Plot - {file_path} - {y_labels[row_index]}')
        
        lineplot_fig.tight_layout()
        lineplot_fig.show()

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        entry.delete(0, 'end')
        entry.insert(0, ", ".join(file_paths))

    def browse_txt_file(self):
        txt_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        entry_txt.delete(0, 'end')
        entry_txt.insert(0, txt_file_path)

    def generate_csvs(self):
        txt_file_path = entry_txt.get()
        if txt_file_path:
            command = f"python .\\gui_tests_new.py r'{txt_file_path}'"
            subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            print("Please provide the path to the txt file.")

    def load_and_generate_heatmaps(self):
        file_paths = entry.get().split(", ")
        if file_paths:
            self.generate_heatmaps(file_paths)
        else:
            print("Please provide file paths.")

    def merge_csv_files(self):
        file_paths = entry.get().split(", ")
        if file_paths:
            with open("combined_output.csv", 'w', newline='') as outfile:
                for file_path in file_paths:
                    with open(file_path, 'r') as infile:
                        outfile.write(f"Data from {file_path}\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")
            print("Combined CSV file has been created: combined_output.csv")
        else:
            print("Please provide file paths.")

    def select_and_generate_line_plot(self):
        if not self.heatmap_axes:
            print("No heatmaps generated yet.")
            return
        
        file_path = simpledialog.askstring("Input", "Enter file name for line plot:")
        row_index = simpledialog.askinteger("Input", "Enter row index for line plot:")
        
        for path, heatmap_data, x_labels, y_labels, ax, max_row_index in self.heatmap_axes:
            if path == file_path and 0 <= row_index < len(y_labels):
                self.generate_line_plot(file_path, heatmap_data, x_labels, y_labels, row_index)
                return
        print("Invalid file name or row index.")

# Tkinter GUI
root = Tk()
root.title("Multiple Heatmap Generator")

generator = HeatmapGenerator()

label_txt = Label(root, text="Enter path to TXT file:")
label_txt.pack()

entry_txt = Entry(root, width=50)
entry_txt.pack()

browse_txt_button = Button(root, text="Browse TXT", command=generator.browse_txt_file)
browse_txt_button.pack()

generate_csvs_button = Button(root, text="Generate CSVs", command=generator.generate_csvs)
generate_csvs_button.pack()

label = Label(root, text="Enter paths to CSV files (separated by commas):")
label.pack()

entry = Entry(root, width=50)
entry.pack()

browse_button = Button(root, text="Browse CSVs", command=generator.browse_files)
browse_button.pack()

generate_button = Button(root, text="Generate Heatmaps", command=generator.load_and_generate_heatmaps)
generate_button.pack()

merge_button = Button(root, text="Merge CSV Files", command=generator.merge_csv_files)
merge_button.pack()

line_plot_button = Button(root, text="Generate Line Plot", command=generator.select_and_generate_line_plot)
line_plot_button.pack()

root.mainloop()
