#a temperature conversion

import customtkinter as ctk

# Conversion functions
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def celsius_to_kelvin(c):
    return c + 273.15

def kelvin_to_celsius(k):
    return k - 273.15

def fahrenheit_to_kelvin(f):
    return (f - 32) * 5/9 + 273.15

def kelvin_to_fahrenheit(k):
    return (k - 273.15) * 9/5 + 32

# Conversion handler
def convert():
    try:
        value = float(entry.get())
        from_unit = from_option.get()
        to_unit = to_option.get()

        if from_unit == to_unit:
            result_label.configure(text=f"{value:.2f} {to_unit}")
            return

        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                result = celsius_to_fahrenheit(value)
            else:
                result = celsius_to_kelvin(value)

        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                result = fahrenheit_to_celsius(value)
            else:
                result = fahrenheit_to_kelvin(value)

        else:  # Kelvin
            if to_unit == "Celsius":
                result = kelvin_to_celsius(value)
            else:
                result = kelvin_to_fahrenheit(value)

        result_label.configure(text=f"{result:.2f} {to_unit}")
    except ValueError:
        result_label.configure(text="Enter a valid number!")

# Clear input/output
def clear():
    entry.delete(0, "end")
    result_label.configure(text="")
    from_option.set("Celsius")
    to_option.set("Fahrenheit")

# Toggle theme
def toggle_theme():
    current = ctk.get_appearance_mode()
    if current == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")

# Setup window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Temperature Converter")
app.geometry("420x320")

# Input field
entry = ctk.CTkEntry(app, placeholder_text="Enter value")
entry.pack(pady=10)

# Dropdowns for units
unit_frame = ctk.CTkFrame(app)
unit_frame.pack(pady=5)

from_label = ctk.CTkLabel(unit_frame, text="From:")
from_label.grid(row=0, column=0, padx=5)

from_option = ctk.CTkOptionMenu(unit_frame, values=["Celsius", "Fahrenheit", "Kelvin"])
from_option.set("Celsius")
from_option.grid(row=0, column=1, padx=5)

to_label = ctk.CTkLabel(unit_frame, text="To:")
to_label.grid(row=0, column=2, padx=5)

to_option = ctk.CTkOptionMenu(unit_frame, values=["Celsius", "Fahrenheit", "Kelvin"])
to_option.set("Fahrenheit")
to_option.grid(row=0, column=3, padx=5)

# Buttons frame
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

convert_button = ctk.CTkButton(button_frame, text="Convert", command=convert)
convert_button.grid(row=0, column=0, padx=5)

clear_button = ctk.CTkButton(button_frame, text="Clear", command=clear)
clear_button.grid(row=0, column=1, padx=5)

theme_button = ctk.CTkButton(button_frame, text="Dark/Light", command=toggle_theme)
theme_button.grid(row=0, column=2, padx=5)

# Result label
result_label = ctk.CTkLabel(app, text="", font=("Arial", 16))
result_label.pack(pady=15)

# Run app
app.mainloop()