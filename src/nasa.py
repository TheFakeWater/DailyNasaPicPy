import os
from tkinter import *
from tkinter import messagebox

import PIL
import requests
import wget
from PIL import ImageTk, Image

path = os.getcwd()
path = path.replace(r'\src', r'\downloads')
your_api_key = "<ENTER HERE API KEY>"


def download_daily_photo(api_key, isHd):
    try:
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key={}&hd={}".format(api_key, isHd))
        remaining_time = response.headers['X-RateLimit-Remaining']
        result = response.json()
        url = result['url']
        daily_image = wget.download(url, path)
        os.chdir(path)
        show_requests_left(remaining_time)
    except:
        messagebox.showerror("Error occurred", "Something went wrong with the api\nIs your api key correct ?")


def show_requests_left(xtimesleft):
    remaining_time_label = Label(font=("Arial", 24), text="You have {} requests left".format(xtimesleft)).place(x=800,
                                                                                                                y=500)
    rename_daily_photo()


def rename_daily_photo():
    try:
        os.chdir(path)
        images_list = os.listdir(path)
        for x in images_list:
            os.rename(x, 'daily.jpg')
        resize_and_show_daily_photo()
    except:
        messagebox.showerror("Oops!", "Something went wrong.\nPlease press reset button and try again.")


def resize_and_show_daily_photo():
    try:
        os.chdir(path)
        basewidth = 300
        img = Image.open("daily.jpg")
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save("daily_re.jpg", 'JPEG')
        re_img = Image.open("daily_re.jpg")
        render = ImageTk.PhotoImage(re_img)
        img = Label(image=render)
        img.image = render
        img.place(x=800, y=200)
    except:
        messagebox.showerror("Oops!", "Something went wrong.\nPlease press reset button and try again.")


def reset():
    os.chdir(path)
    images_list = os.listdir(path)
    for x in images_list:
        os.remove(x)
    info = messagebox.showinfo("Reset successful", "The program was reset successfully")


window = Tk()
window.title("NasaPy")
welcome_label = Label(text="Welcome to NasaPy", font=("Arial Black", 50)).pack()
daily_photo_button = Button(text="Daily photo", height=5, width=20,
                            command=lambda: download_daily_photo(your_api_key,
                                                                 True)).place(x=200, y=200)
exit_button = Button(text="Reset", height=5, width=20, command=reset).place(x=200, y=310)
window.geometry("1280x720")
window.mainloop()
