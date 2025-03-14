
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import random


dates = ['2025-03-01', '2025-03-02', '2025-03-01', '2025-03-04', '2025-03-05', '2025-02-27', '2025-02-26', '2025-02-11']

date = random.choice(dates)

api_key = os.environ['nasa_api_key']

def get_random_star_image(api_key, date):
    space_api_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "date": date}

    try:
        response = requests.get(space_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200 and data["media_type"] == "image":
            image_url = data.get("hdurl", data.get("url"))
            if image_url:
                img_response = requests.get(image_url)
                img_response.raise_for_status()
                return Image.open(BytesIO(img_response.content))

        print(f"No suitable image found for date {date}")
        return None

    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def set_background(date):
    image = get_random_star_image(api_key, date)
    if image:
        image = image.resize((400, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        bg_label.config(image=photo)
        bg_label.image = photo
    else:
        print("Failed to set background image")

def try_new_date():
    new_date = random.choice(dates)
    print(f"Trying new date: {new_date}")
    set_background(new_date)

root = tk.Tk()
root.title("NASA Astronomy Picture of the Day")
root.geometry("400x400")

placeholder = Image.new("RGB", (400, 400), "black")
placeholder_photo = ImageTk.PhotoImage(placeholder)

bg_label = tk.Label(root, image=placeholder_photo)
bg_label.place(relwidth=1, relheight=1)

refresh_button = tk.Button(root, text="New Image", command=try_new_date)
refresh_button.pack(side=tk.BOTTOM, pady=10)


set_background(date)

root.mainloop()
