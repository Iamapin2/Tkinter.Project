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
    space_api_url ="https://api.nasa.gov/planetary/apod"
    params = {"api_key":api_key, "date":date, "hd": True}
    
    try:
        response = requests.get(space_api_url, params = params)
        print(response)
        response.raise_for_status()
        data = response.json()
        if response.status_code == 200 and data["media_type"] == "image" and "hdurl" in data:
            image = requests.get(data["hdurl"])
            img = Image.open(BytesIO(image.content))
        # image_url = response.json()[0]["url", "hdurl"]
        # img_data = requests.get(image_url).content
        # return Image.open(BytesIO(img_data))

    except requests.RequestException:
        print("Status Error")
        return None

    except IndexError:
        print("JSON error")
        return None

def set_background(date):
    image = get_random_star_image(api_key, date)
    if image:
        image = image.resize((400,400))
        photo = ImageTk.PhotoImage(image)
        bg_label.config(image = photo)
        bg_label.image = photo

root = tk.Tk()
root.title("idk at this current moment")
root.geometry("400x400")

placeholder = Image.new("RGB", (400, 400), "white")
placeholder_photo = ImageTk.PhotoImage(placeholder)

bg_label = tk.Label(root, image=placeholder_photo)
bg_label.place(relwidth=1, relheight=1)


set_background(date)

root.mainloop()
