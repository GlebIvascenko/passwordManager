from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters

    shuffle(password_list)

    generated_password = "".join(password_list)

    password_input.insert(END, string=generated_password)
    pyperclip.copy(generated_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    website_text = website_input.get()
    user_text = user_input.get()
    password_text = password_input.get()
    new_data = {website_text: {
        "email": user_text,
        "password" : password_text
        }
    }

    if len(website_text) == 0 or len(password_text) == 0 or len(user_text) == 0:
        messagebox.showerror(title="Oops", message="Please fill all empty fields")
    else:
        try:
            with open("password_manager.json", "r") as file:
                add_to_list = json.load(file)

        except FileNotFoundError:
            with open("password_manager.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            if website_text in add_to_list:
                warning = messagebox.askokcancel(title="Oops", message=f"Data for {website_text} already exist.\n"
                                                                       f"Would you like to update it?")
            if warning:
                add_to_list.update(new_data)
                with open("password_manager.json", "w") as file:
                    json.dump(add_to_list, file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)
            website_input.focus()


# ---------------------------- SEARCH DATA ---------------------------- #
def search_data():
    website_text = website_input.get()

    if len(website_text) == 0:
        messagebox.showerror(title="Oops", message="Please enter a website you are looking for")
    else:
        try:
            with open("password_manager.json", "r") as file:
                search_in_file = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="No file found")
        else:
            if website_text in search_in_file:
                messagebox.showinfo(title="Oops", message=f"These ae the details you are looking for:\n"
                                                            f"Email: {search_in_file[website_text]['email']}\n"
                                                            f"Password: {search_in_file[website_text]['password']}")
            else:
                messagebox.showinfo(title="Oops", message=f"Data for {website_text} not exist")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website = Label(text="Website:", padx=10, pady=5)
website.grid(column=0, row=1)
user = Label(text="Email/Username:", padx=10, pady=5)
user.grid(column=0, row=2)
password = Label(text="Password:", padx=10, pady=5)
password.grid(column=0, row=3)

website_input = Entry(width=36)
website_input.grid(column=1, row=1)
website_input.focus()
user_input = Entry(width=55)
user_input.insert(END, string="ivascenko.gleb@gmail.com")
user_input.grid(column=1, row=2, columnspan=2)

password_input = Entry(width=36)
password_input.grid(column=1, row=3)

gen_password = Button(text="Generate Password", command=generate_password)
gen_password.grid(column=2, row=3)

add = Button(text='Add', highlightthickness=0, width=47, command=save_data)
add.grid(column=1, row=4, columnspan=2)


search_button = Button(text='Search', highlightthickness=0, width=15, command=search_data)
search_button.grid(column=2, row=1)

window.mainloop()
