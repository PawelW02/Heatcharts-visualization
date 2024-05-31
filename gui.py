import csv
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Entry, filedialog
import subprocess

class HeatmapGenerator:
    def __init__(self):
        self.file_paths = []

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
        num_files = len(file_paths)
        num_views = (num_files + 7) // 8

        for view in range(num_views):
            heatmap_fig = plt.figure(figsize=(15, 20))
            lineplot_fig = plt.figure(figsize=(15, 20))
            for i in range(8):
                file_index = view * 8 + i
                if file_index >= num_files:
                    break
                file_path = file_paths[file_index]
                heatmap_data, x_labels, y_labels = self.read_csv_file_with_labels(file_path)
                title = file_path[-11:-4]

                ax = heatmap_fig.add_subplot(4, 2, i + 1)
                cax = ax.imshow(heatmap_data, cmap='hot', interpolation='nearest')
                ax.set_xticks(np.arange(0, len(x_labels), max(1, len(x_labels)//10)))
                ax.set_xticklabels([x_labels[j] for j in np.arange(0, len(x_labels), max(1, len(x_labels)//10))], rotation=90)
                ax.set_yticks(np.arange(0, len(y_labels), max(1, len(y_labels)//10)))
                ax.set_yticklabels([y_labels[j] for j in np.arange(0, len(y_labels), max(1, len(y_labels)//10))])
                ax.set_xlabel('X Axis')
                ax.set_ylabel('Y Axis')
                ax.set_title(title)
                heatmap_fig.colorbar(cax, ax=ax)

                max_row_index = np.argmax(np.sum(heatmap_data, axis=1))
                max_row_data = heatmap_data[max_row_index]
                
                ax_line = lineplot_fig.add_subplot(4, 2, i + 1)
                ax_line.plot(x_labels, max_row_data, marker='x')
                ax_line.set_xlabel('X Axis')
                ax_line.set_ylabel('Values')
                ax_line.set_title(f'Line Plot - {title} - Row {max_row_index + 1}')
            
            heatmap_fig.tight_layout()
            lineplot_fig.tight_layout()
            heatmap_fig.show()
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

root.mainloop()
