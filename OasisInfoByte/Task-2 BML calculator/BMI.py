import tkinter as tk
from tkinter import messagebox
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BMI_Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        # Labels and Entry Widgets
        self.label_weight = tk.Label(master, text="Weight (kg):")
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)

        self.entry_weight = tk.Entry(master)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)

        self.label_height = tk.Label(master, text="Height (m):")
        self.label_height.grid(row=1, column=0, padx=10, pady=10)

        self.entry_height = tk.Entry(master)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)

        # Calculate and Clear Buttons
        self.btn_calculate = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.btn_calculate.grid(row=2, column=0, padx=10, pady=10)

        self.btn_clear = tk.Button(master, text="Clear", command=self.clear_inputs)
        self.btn_clear.grid(row=2, column=1, padx=10, pady=10)

        # Result Label
        self.label_result = tk.Label(master, text="", font=("Helvetica", 12, "bold"))
        self.label_result.grid(row=3, column=0, columnspan=2, pady=10)

        # Visualize historical data
        self.load_user_data()

    def calculate_bmi(self):
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers.")

            bmi = weight / (height ** 2)
            category = self.classify_bmi(bmi)

            result_text = f"Your BMI is {bmi:.2f}, which is classified as {category}."
            self.label_result.config(text=result_text, fg=self.get_category_color(category))

            # Save user data
            self.save_user_data(weight, height, bmi, category)

            # Update visualization
            self.load_user_data()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input. {e}")

    def clear_inputs(self):
        self.entry_weight.delete(0, tk.END)
        self.entry_height.delete(0, tk.END)
        self.label_result.config(text="")

    def load_user_data(self):
        if os.path.exists("user_data.csv"):
            with open("user_data.csv", "r", newline="") as file:
                reader = csv.reader(file)
                data = list(reader)
                if data:
                    last_entry = data[-1]
                    self.entry_weight.insert(0, last_entry[0])
                    self.entry_height.insert(0, last_entry[1])

                    # Visualize historical data
                    self.visualize_data(data)

    def save_user_data(self, weight, height, bmi, category):
        with open("user_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([weight, height, bmi, category])

    def visualize_data(self, data):
        bmi_values = []
        categories = []

        for entry in data:
            try:
                bmi = float(entry[2])  # Index 2 contains BMI value
                category = self.classify_bmi(bmi)
                bmi_values.append(bmi)
                categories.append(category)
            except ValueError:
                # Skip non-numeric BMI values
                continue

        # Create a bar chart with different colors for each category
        colors = [self.get_category_color(category) for category in categories]

        fig, ax1 = plt.subplots()

        # Bar chart
        ax1.bar(range(1, len(bmi_values) + 1), bmi_values, color=colors)
        ax1.set(xlabel='Entry Number', ylabel='BMI',
               title='BMI Trends Over Time')
        ax1.grid()

        # Line chart
        ax2 = ax1.twinx()  # Create a secondary y-axis
        ax2.plot(range(1, len(bmi_values) + 1), bmi_values, marker='o', linestyle='-', color='black')
        ax2.set_ylabel('BMI', color='black')

        # Embed the chart in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, pady=10)

    @staticmethod
    def classify_bmi(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    @staticmethod
    def get_category_color(category):
        if category == "Underweight":
            return "blue"
        elif category == "Normal weight":
            return "green"
        elif category == "Overweight":
            return "orange"
        else:
            return "red"


if __name__ == "__main__":
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()
