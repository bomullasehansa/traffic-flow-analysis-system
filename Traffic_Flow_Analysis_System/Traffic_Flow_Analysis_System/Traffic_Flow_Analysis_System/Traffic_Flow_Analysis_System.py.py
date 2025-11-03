# Author : Sehansa Rithmini Bomulla
# Date : 24/12/2024
# Student ID : 20232922 (w2120517)

import tkinter as tk
import csv

# Task A: Input Validation
def get_valid_number(prompt, minimum_value, maximum_value):
    while True:
        user_input = input(prompt)
        if not user_input.isdigit():
            print("Integer required.")
        else:
            value = int(user_input)
            if value < minimum_value or value > maximum_value:
                print(f"Out of range - values must be in the range {minimum_value} and {maximum_value}.")
            else:
                return value

def validate_date_input(day, month, year):
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if month in [4, 6, 9, 11] and day == 31:
        return False
    if month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return day <= 29
        else:
            return day <= 28
    return True

def validate_continue_input():
    while True:
        print()
        choice = input("Do you want to select a data file for a different date? (Y/N): ").strip().lower()
        if choice == "y":
            return True  # Continue
        elif choice == "n":
            print("End of run.")
            return False  # Exit the program
        else:
            print("Please enter 'Y' or 'N'.")

def load_dataset():
    while True:
        day = get_valid_number("Please enter the day of the survey in the format dd: ", 1, 31)
        month = get_valid_number("Please enter the month of the survey in the format MM: ", 1, 12)
        year = get_valid_number("Please enter the year of the survey in the format YYYY: ", 2000, 2024)

        if not validate_date_input(day, month, year):
            print(f"Invalid date: {day:02d}/{month:02d}/{year}")
            continue
        else:
            break

    filename = f"traffic_data{day:02d}{month:02d}{year}.csv"
    try:
        with open(filename) as f: 
            print(f"\n*****************************")
            print(f"Data file selected is {filename}")
            print(f"******************************")
            return filename
    except FileNotFoundError:
        print(f"Dataset not found for the date: {day:02d}/{month:02d}/{year}")
        return None

# Task B: Processed Outcomes
def process_csv_data(filename):
    try:
        with open(filename, newline='') as file:
            reader = csv.DictReader(file) # Create a CSV dictionary reader

            total_vehicles = 0
            total_trucks = 0
            total_electric_vehicles = 0
            two_wheeled_vehicles = 0
            total_busses_north = 0
            vehicles_no_turn = 0
            vehicles_over_speed = 0
            elm_vehicles = 0
            hanley_vehicles = 0
            scooter_elm = 0
            bicycles_total = 0
            rain_hours = set()
            peak_hour_counts = {} # Dictionary to store hourly counts
            hourly_data = {"Elm Avenue/Rabbit Road": [0] * 24, "Hanley Highway/Westway": [0] * 24}

            for row in reader:
                total_vehicles += 1
                hour = int(row['timeOfDay'].split(':')[0])
                junction = row['JunctionName']

                # Aggregate hourly data
                if junction in hourly_data:
                    hourly_data[junction][hour] += 1

                vehicle_type = row['VehicleType'].lower()
                if vehicle_type == 'truck': #  trucks passing through all junctions for the selected date
                    total_trucks += 1
                elif vehicle_type in ['bicycle', 'motorcycle', 'scooter']: # “two wheeled” vehicles through all junctions
                    two_wheeled_vehicles += 1  
                    
                    if vehicle_type == 'bicycle':
                        bicycles_total += 1
 
                    if vehicle_type == 'scooter' and row['JunctionName'] == 'Elm Avenue/Rabbit Road':
                        scooter_elm += 1

                # Electric vehicles passing through all junctions
                if row['elctricHybrid'].lower() == 'true':
                    total_electric_vehicles += 1
                    
                # busses leaving Elm Avenue/Rabbit Road junction heading north 
                if row['JunctionName'] == "Elm Avenue/Rabbit Road" and row['travel_Direction_out'] == "N" and vehicle_type == "buss":
                    total_busses_north += 1

                #T vehicles passing through both junctions without turning left or right 
                if row['travel_Direction_in'] == row['travel_Direction_out']:
                    vehicles_no_turn += 1

                    
                # vehicles recorded as over the speed limit  
                if int(row['VehicleSpeed']) > int(row['JunctionSpeedLimit']):
                    vehicles_over_speed += 1

                junction = row['JunctionName']
                if 'Elm' in junction: # vehicles recorded through only Elm Avenue/Rabbit Road junction 
                    elm_vehicles += 1
                elif 'Hanley' in junction: # vehicles recorded through only Hanley Highway/Westway junction 
                    hanley_vehicles += 1
                    peak_hour_counts[hour] = peak_hour_counts.get(hour, 0) + 1

                # Total no of hours of rain 
                if 'rain' in row['Weather_Conditions'].lower():
                    rain_hours.add(hour)

            # Peak hour calculations
            peak_hour_vehicles = max(peak_hour_counts.values()) if peak_hour_counts else 0
            peak_hour_times = [f"Between {hour}:00 and {int(hour)+1}:00" for hour, count in peak_hour_counts.items() if count == peak_hour_vehicles]

            # percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters
            scooter_elm_percentage = round((scooter_elm / elm_vehicles) * 100) if elm_vehicles > 0 else 0

            outcomes = {
                "Total Vehicles": total_vehicles,
                "Total Trucks": total_trucks,
                "Total Electric Vehicles": total_electric_vehicles,
                "Two-Wheeled Vehicles": two_wheeled_vehicles,
                "Total busses Heading North": total_busses_north,
                "Vehicles No Turn": vehicles_no_turn,
                "Truck Percentage": round((total_trucks / total_vehicles) * 100) if total_vehicles > 0 else 0, # percentage of all vehicles recorded that are Trucks for the selected date 
                "Average Bicycles Per Hour": round(bicycles_total / 24) if total_vehicles > 0 else 0, # Average number Bicycles per hour for the selected date 
                "Vehicles Over Speed": vehicles_over_speed,
                "Elm Avenue/Rabbit Road Vehicles": elm_vehicles,
                "Hanley Highway/Westway Vehicles": hanley_vehicles,
                "Scooter Percentage Elm": scooter_elm_percentage,
                "Peak Hour Vehicles": peak_hour_vehicles,
                "Peak Hour Times": peak_hour_times,
                "Rain Hours": len(rain_hours),
                "Hourly Data": hourly_data,
            }
            return outcomes

    except Exception as e:
        print(f"Error processing the file: {e}")
        return None

def display_outcomes(outcomes):
    if outcomes:
        print(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}")
        print(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}")
        print(f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}")
        print(f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}")
        print(f"The total number of busses leaving Elm Avenue/Rabbit Road heading north is {outcomes['Total busses Heading North']}")
        print(f"The total number of vehicles through both junctions not turning left or right is {outcomes['Vehicles No Turn']}")
        print(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Truck Percentage']}%")
        print(f"the average number of Bikes per hour for this date is {outcomes['Average Bicycles Per Hour']}")
        print()
        print(f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['Vehicles Over Speed']}")
        print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Avenue/Rabbit Road Vehicles']}")
        print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Highway/Westway Vehicles']}")
        print(f"{outcomes['Scooter Percentage Elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
        print()
        print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Peak Hour Vehicles']}")
        print(f"The most vehicles through Hanley Highway/Westway were recorded {', '.join(outcomes['Peak Hour Times'])}")
        print(f"The number of hours of rain for this date is {outcomes['Rain Hours']}")

# Task C: Save Results to Text File
def save_results_to_file(outcomes, filename):
    with open("results.txt", "a") as file:
        file.write(f"Data file selected is {filename}\n")
        file.write(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}\n")
        file.write(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}\n")
        file.write(f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}\n")
        file.write(f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}\n")
        file.write(f"The total number of busses leaving Elm Avenue/Rabbit Road heading north is {outcomes['Total busses Heading North']}\n")
        file.write(f"The total number of vehicles through both junctions not turning left or right is {outcomes['Vehicles No Turn']}\n")
        file.write(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Truck Percentage']}%\n")
        file.write(f"the average number of Bikes per hour for this date is {outcomes['Average Bicycles Per Hour']}\n")
        file.write(f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['Vehicles Over Speed']}\n")
        file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Avenue/Rabbit Road Vehicles']}\n")
        file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Highway/Westway Vehicles']}\n")
        file.write(f"{outcomes['Scooter Percentage Elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n")
        file.write(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Peak Hour Vehicles']}\n")
        file.write(f"The most vehicles through Hanley Highway/Westway were recorded {', '.join(outcomes['Peak Hour Times'])}\n")
        file.write(f"The number of hours of rain for this date is {outcomes['Rain Hours']}\n")
        file.write(f"\n*************************\n")

# Task D: Histogram Display

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title("Histogram")
        self.canvas = tk.Canvas(self.root, width=900, height=650, bg="white")
        self.canvas.pack()

    def draw_histogram(self):

        self.canvas.create_text(400, 20, text=f"Histogram of vehicle frequency per Hour {self.date}", font=("Arial", 16, "bold"))
        self.canvas.create_line(50, 550, 750, 550)  #X (axis)
        self.canvas.create_text(425, 580, text="Hours 00:00 to 24:00", font=("Arial", 10))

        junctions = list(self.traffic_data.keys())
        color = ["light green", "orange"]
        for i, junction in enumerate(junctions):
            self.canvas.create_rectangle(600, 60 + i * 20, 620, 80 + i * 20,fill=color[i % len(color)])
            #Add text to the legend (next to the colored box)
            self.canvas.create_text(650, 70 + i * 20, text=junction, anchor="w")

        max_count = max(max(self.traffic_data[j]) for j in junctions)
        column_width = 12
        for hour in range(24):
            start_x = 60 + hour * 30
            for i, junction in enumerate(junctions):
                height_of_bar = int((self.traffic_data[junction][hour] / max_count) * 350)
                column_gap = i * column_width # to avoid overlap
                self.canvas.create_rectangle(
                    start_x + column_gap,
                    550 - height_of_bar,
                    start_x + column_gap + column_width,
                    550,
                    fill=color[i % len(color)]
                )

                
                self.canvas.create_text(
                    start_x + column_gap + column_width // 2,
                    550 - height_of_bar - 10,
                    text=str(self.traffic_data[junction][hour]),
                    font=("Arial", 8),
                    fill=color[i % len(color)]
                )

        # Hour labels
        for hour in range(24):
            x = 60 + hour * 30 + column_width // 2
            self.canvas.create_text(x, 560, text=str(hour), font=("Arial", 8))

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        pass  # Logic for adding a legend (if not already implemented in draw_histogram)

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.root.mainloop()


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        outcomes = process_csv_data(file_path)
        if outcomes:
            display_outcomes(outcomes)
            hourly_data = outcomes["Hourly Data"]
            save_results_to_file(outcomes, file_path)

            # Pass data to HistogramApp
            histogram = HistogramApp(hourly_data, self.current_data["date"])
            histogram.run()

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            dataset = load_dataset()
            if dataset:
                day = int(dataset[12:14])
                month = int(dataset[14:16])
                year = int(dataset[16:20])
                date = f"{day:02d}/{month:02d}/{year}"
                self.current_data = {"dataset": dataset, "date": date}
                self.load_csv_file(dataset)

            if not validate_continue_input():
                break

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.handle_user_interaction()

# Main Program 

processor = MultiCSVProcessor()
processor.process_files()
