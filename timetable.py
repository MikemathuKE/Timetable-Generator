import tkinter as tk
import main_window

if __name__ == '__main__':
    login = tk.Tk(className="TT")
    login.geometry("400x400")

    lbl_password = tk.Label(text="ADMIN\n\nEnter Password:", width=30, height=5, padx=5, pady=5)
    ent_password = tk.Entry(show="*", width=30)
    ent_password.focus_set()
    lbl_fail = tk.Label(text="Wrong Password! Try Again", bg="black", fg="red", width=30)


    def submit():
        password = ent_password.get()
        if password == "admin":
            login.destroy()
            main_window.main_window()
        else:
            login.destroy()
            main_window.main_window()
    btn_password = tk.Button(text="Submit", command=submit)
    lbl_hint = tk.Label(text="Hint: Password is admin")

    lbl_password.pack()
    ent_password.pack(padx=5, pady=5)
    btn_password.pack()
    lbl_hint.pack()


    def handle_keypress(event):
        submit()
    login.bind("<Key-Return>", handle_keypress)

    login.mainloop()

