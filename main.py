import tkinter as tk
import re
import json
from os.path import exists

import vanity

CONFIG_FILENAME = 'config.json'

MAX_PLATE_LEN = 7

default_font = ("Arial", 16)

smaller_font = ("Arial", 12)

class WindowFrame:
    def __init__(self, parent):
        self.parent = parent

        self.parent.bind('<Return>', self.check_plate)

        self.main_panel = tk.Frame(parent)
        self.main_panel.pack()

        self.info_label = tk.Label(self.main_panel, text="Current Info:", font=default_font)
        self.info_label.pack(pady=10)

        self.plate_label = tk.Label(self.main_panel, text="Current license plate number:", font=smaller_font)
        self.plate_label.pack(pady=5)

        self.input_plate = tk.Entry(self.main_panel, font=smaller_font)
        self.input_plate.pack(pady=5)
        self.input_plate.focus()

        self.vin_label = tk.Label(self.main_panel, text="Last three digits of VIN:", font=smaller_font)
        self.vin_label.pack(pady=5)

        self.input_vin = tk.Entry(self.main_panel, font=smaller_font)
        self.input_vin.pack(pady=5)
       
        self.label = tk.Label(self.main_panel, text="Custom Plate Name:", font=default_font)
        self.label.pack(pady=10)

        self.input_var = tk.StringVar()
        self.input_var.trace("w", self.autocapitalize)

        self.input_box = tk.Entry(self.main_panel, font=("Consolas", 16), textvariable=self.input_var)
        self.input_box.pack(pady=10)

        self.check_button = tk.Button(self.main_panel, text="Check availability", command=self.check_plate, font=default_font)
        self.check_button.pack(pady=10)

        self.result_var = tk.StringVar()

        self.result_label = tk.Label(self.main_panel, textvariable=self.result_var, font=default_font)

        self.load_config()

    def check_plate(self, *args):
        plate_name = self.input_var.get()

        if len(plate_name) < 2:
            self.result_var.set("Plate name must have at least two characters!")
            self.result_label.configure(fg='#bd0300')
            self.result_label.pack(pady=20)
            return
        elif '//' in plate_name:
            self.result_var.set("Plate name cannot have two half spaces in a row!")
            self.result_label.configure(fg='#bd0300')
            self.result_label.pack(pady=20)
            return

        self.result_var.set("Checking availability...")
        self.result_label.configure(fg='#36c6ff')
        self.result_label.pack(pady=20)

        self.parent.update()       

        plate_status = vanity.check_plate(self.input_plate.get(), self.input_vin.get(), plate_name)

        if plate_status == vanity.PlateResult.invalid_info:
            self.result_label.configure(fg='#bd0300')
            self.result_var.set("Invalid plate or VIN!")
        else:
            self.save_config()
            if plate_status == vanity.PlateResult.taken:
                self.result_label.configure(fg='#bd0300')
                self.result_var.set(f"{plate_name} is taken!")
            elif plate_status == vanity.PlateResult.available:
                self.result_label.configure(fg='#00b52a')
                self.result_var.set(f"{plate_name} is available!")

    def autocapitalize(self, *arg):
        self.input_var.set(self.input_var.get().upper())
        if len(self.input_var.get()) > MAX_PLATE_LEN:
            self.input_var.set(self.input_var.get()[:MAX_PLATE_LEN])
        pattern = re.compile('[^1-9A-Za-z\/ ]+')
        self.input_var.set(pattern.sub('', self.input_var.get()))

    def load_config(self):
        if exists(CONFIG_FILENAME):
            with open(CONFIG_FILENAME) as json_file:
                config_data = json.load(json_file)
                self.input_plate.delete(0,"end")
                self.input_plate.insert(0, config_data['plate'])
                self.input_vin.delete(0,"end")
                self.input_vin.insert(0, config_data['vin'])
            self.input_box.focus()

    def save_config(self):
        config_data = {
            'plate': self.input_plate.get(),
            'vin': self.input_vin.get()
        }

        with open(CONFIG_FILENAME, 'w') as outfile:
            json.dump(config_data, outfile)

root = tk.Tk()
root.title("CA Custom Plate Checker")
root.geometry("720x480")

window_frame = WindowFrame(root)

root.mainloop()