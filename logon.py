from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow
from tkinter import messagebox
import mysql.connector
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from hotel import HotelManagementSystem

class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("LOGIN")
        self.root.geometry("1600x700+0+0")

        self.bg = ImageTk.PhotoImage(file="login_background.jpg")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame = Frame(self.root, bg="black")
        frame.place(x=500, y=150, width=340, height=450)

        img1 = Image.open("login_icon.ico")
        img1 = img1.resize((90, 90))
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lblimg1 = Label(image=self.photoimage1, bg="black", borderwidth=0)
        lblimg1.place(x=630, y=170, width=90, height=90)

        get_start = Label(frame, text="GET STARTED", font=("arial", 14, "bold"), fg="white", bg="black")
        get_start.place(x=108, y=120)

        ###### LABEL #########
        username_lbl = Label(frame, text="USERNAME :", font=("arial", 11, "bold"), fg="white", bg="black")
        username_lbl.place(x=40, y=155)

        self.txtuser = ttk.Entry(frame, font=("arial", 11, "bold"))
        self.txtuser.place(x=40, y=190, width=210)

        password_lbl = Label(frame, text="PASSWORD :", font=("arial", 11, "bold"), fg="white", bg="black")
        password_lbl.place(x=40, y=235)

        self.txtpass = ttk.Entry(frame, font=("arial", 11, "bold"), show="*")
        self.txtpass.place(x=40, y=270, width=210)

        ########## ICON IMAGES ###############
        img2 = Image.open("login_icon.ico")
        img2 = img2.resize((25, 25))
        self.photoimage2 = ImageTk.PhotoImage(img2)
        lblimg2 = Label(image=self.photoimage2, bg="black", borderwidth=0)
        lblimg2.place(x=510, y=306, width=25, height=25)

        img3 = Image.open("password_icon.ico")
        img3 = img3.resize((25, 25))
        self.photoimage3 = ImageTk.PhotoImage(img3)
        lblimg3 = Label(image=self.photoimage3, bg="black", borderwidth=0)
        lblimg3.place(x=510, y=386, width=25, height=25)

        login_btn = Button(frame, text="LOGIN", command=self.login, font=("arial", 11, "bold"), bd=3, relief=RIDGE, fg="black", bg="blue", activeforeground="white", activebackground="blue")
        login_btn.place(x=110, y=320, width=120, height=35)

        register_btn = Button(frame, text="REGISTER", command=self.register_window, font=("arial", 11, "bold"), borderwidth=0, relief=RIDGE, fg="black", bg="black", activeforeground="white", activebackground="black")
        register_btn.place(x=2, y=370, width=120, height=20)

        forgot_password_btn = Button(frame, text="FORGOT PASSWORD", command=self.forgot_password_window, font=("arial", 11, "bold"), borderwidth=0, relief=RIDGE, fg="black", bg="black", activeforeground="white", activebackground="black")
        forgot_password_btn.place(x=20, y=415, width=160, height=20)

    def register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = register(self.new_window)

    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("ERROR", "ALL FIELD REQUIRED!!")
        elif self.txtuser.get() == "admin" and self.txtpass.get() == "root":
            messagebox.showinfo("WELCOME", "WELCOME USER")
        else:
            conn = mysql.connector.connect(host="localhost", username="root", password="12345678", database="hotel_management")
            my_cursor = conn.cursor()
            my_cursor.execute("select * from register2 where email=%s and pass=%s", (self.txtuser.get(), self.txtpass.get()))
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("ERROR", "INVALID USERNAME AND PASSWORD!!!")
            else:
                open_main = messagebox.askyesno("ADMIN", "ACCESS GRANTED , READY TO START THE DAY?")
                if open_main > 0:
                    self.new_window = Toplevel(self.root)
                    self.app = HotelManagementSystem(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()

    ################## RESET PASSWORD ################
    def reset_password_data(self):
        if self.combo_security_q.get() == "SELECT":
            messagebox.showerror("ERROR", "SELECT THE SECURITY QUESTION!!", parent=self.root2)
        elif self.txt_security_a.get() == "":
            messagebox.showerror("ERROR", "PLEASE ENTER THE ANSWER!!", parent=self.root2)
        elif self.txt_new_password.get() == "":
            messagebox.showerror("ERROR", "PLEASE ENTER THE PASSWORD!!", parent=self.root2)
        else:
            conn = mysql.connector.connect(host="localhost", username="root", password="12345678", database="hotel_management")
            my_cursor = conn.cursor()
            query = ("select * from register2 where email=%s and security_q=%s and security_a=%s")
            value = (self.txtuser.get(), self.combo_security_q.get(), self.txt_security_a.get())
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("ERROR", "PLEASE ENTER THE CORRECT ANSWER", parent=self.root2)
            else:
                query = ("update register2 set pass=%s where email=%s")
                value = (self.txt_new_password.get(), self.txtuser.get())
                my_cursor.execute(query, value)

                conn.commit()
                conn.close()
                messagebox.showinfo("INFO", "YOUR PASSWORD HAS BEEN RESET, PLEASE LOGIN WITH NEW PASSWORD", parent=self.root2)
                self.root2.destroy()

    ############## FORGOT PASSWORD ############
    def forgot_password_window(self):
        if self.txtuser.get() == "":
            messagebox.showerror("ERROR", "PLEASE ENTER THE EMAIL ADDRESS TO RESET PASSWORD!!")
        else:
            conn = mysql.connector.connect(host="localhost", username="root", password="12345678", database="hotel_management")
            my_cursor = conn.cursor()
            query = ("select * from register2 where email=%s")
            value = (self.txtuser.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            # print(row)

            if row is None:
                messagebox.showerror("ERROR", "PLEASE ENTER VALID USERNAME")
            else:
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("FORGOT PASSWORD")
                self.root2.geometry("340x450+610+170")

                l = Label(self.root2, text="FORGOT PASSWORD", font=("arial", 12, "bold"), fg="red", bg="white")
                l.place(x=0, y=10, relwidth=1)

                security_q = Label(self.root2, text="SELECT SECURITY QUESTION:", font=("arial", 15, "bold"), bg="white", fg="black")
                security_q.place(x=30, y=80)

                self.combo_security_q = ttk.Combobox(self.root2, font=("arial", 15, "bold"), state="readonly")
                self.combo_security_q["values"] = ("SELECT", "YOUR BIRTH PLACE", "YOUR CLG NAME", "YOUR PET NAME")
                self.combo_security_q.place(x=50, y=110, width=250)
                self.combo_security_q.current(0)

                security_a = Label(self.root2, text="SECURITY ANSWER", font=("arial", 15, "bold"), bg="white", fg="black")
                security_a.place(x=50, y=150)

                self.txt_security_a = ttk.Entry(self.root2, font=("arial", 15, "bold"))
                self.txt_security_a.place(x=50, y=180, width=250)

                new_password = Label(self.root2, text="NEW PASSWORD", font=("arial", 15, "bold"), bg="white", fg="black")
                new_password.place(x=50, y=220)

                self.txt_new_password =ttk.Entry(self.root2, font=("arial", 15, "bold"))
                self.txt_new_password.place(x=50, y=250, width=250)
                btn = Button(self.root2, text="RESET", command=self.reset_password_data, font=("arial", 15, "bold"), fg="white", bg="green")
                btn.place(x=100, y=290)


class register:
    def __init__(self, root):
        self.root = root
        self.root.title("REGISTER")
        self.root.geometry("1600x900+0+0")

        self.bg = ImageTk.PhotoImage(file="register_background.jpg")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.left = ImageTk.PhotoImage(file="left.png")
        left_lbl = Label(self.root, image=self.left)
        left_lbl.place(x=50, y=100, width=470, height=550)

        frame = Frame(self.root, bg="white")
        frame.place(x=520, y=100, width=800, height=550)

        register_lbl = Label(frame, text="REGISTER HERE", font=("arial", 20, "bold"), fg="green", bg="white")
        register_lbl.place(x=20, y=20)

        ########## LABEL AND ENTRY FIELD #########
        fname = Label(frame, text="FIRST NAME :", font=("arial", 15, "bold"), bg="white")
        fname.place(x=50, y=100)

        self.fname_entry = ttk.Entry(frame, font=("arial", 15, "bold"))
        self.fname_entry.place(x=50, y=130, width=250)

        lname = Label(frame, text="LAST NAME :", font=("arial", 15, "bold"), bg="white")
        lname.place(x=370, y=100)

        self.txt_lname = ttk.Entry(frame, font=("arial", 15, "bold"))
        self.txt_lname.place(x=370, y=130, width=250)

        contact = Label(frame, text="CONTACT NO. :", font=("arial", 15, "bold"), bg="white")
        contact.place(x=50, y=170)

        self.txt_contact = ttk.Entry(frame, font=("arial", 15, "bold"))
        self.txt_contact.place(x=50, y=200, width=250)

        email = Label(frame, text="EMAIL :", font=("arial", 15, "bold"), bg="white")
        email.place(x=370, y=170)

        self.txt_email = ttk.Entry(frame, font=("arial", 15, "bold"))
        self.txt_email.place(x=370, y=200, width=250)

        security_q = Label(frame, text="SELECT SECURITY QUESTION :", font=("arial", 15, "bold"), bg="white")
        security_q.place(x=50, y=240)

        self.combo_security_q = ttk.Combobox(frame, font=("arial", 15, "bold"), state="readonly")
        self.combo_security_q["values"] = ("SELECT", "YOUR BIRTH PLACE", "YOUR CLG NAME", "YOUR PET NAME")
        self.combo_security_q.place(x=50, y=270, width=250)
        self.combo_security_q.current(0)

        security_a = Label(frame, text="SECURITY ANSWER :", font=("arial", 15, "bold"), bg="white")
        security_a.place(x=370, y=240)

        self.txt_security = ttk.Entry(frame, font=("arial", 15, "bold"))
        self.txt_security.place(x=370, y=270, width=250)

        pswd = Label(frame, text="PASSWORD :", font=("arial", 15, "bold"), bg="white")
        pswd.place(x=50, y=310)

        self.txt_pswd = ttk.Entry(frame, font=("arial", 15, "bold"))
        self.txt_pswd.place(x=50, y=340, width=250)

        confirm_pswd = Label(frame, text="CONFIRM PASSWORD :", font=("arial", 15, "bold"), bg="white")
        confirm_pswd.place(x=370, y=310)

        self.txt_confirm_pswd = ttk.Entry(frame, font=("arial", 15, "bold"))
        self.txt_confirm_pswd.place(x=370, y=340, width=250)

        self.var_chk = IntVar()
        self.checkbtn = Checkbutton(frame, variable=self.var_chk, text="I AGREE THE TERMS & CONDITIONS", font=("arial", 12, "bold"), onvalue=1, offvalue=0, bg="white")
        self.checkbtn.place(x=50, y=380)

        self.verify_code = None
        self.verified = False

        img = Image.open("register_button.jpg")
        img = img.resize((200, 50))
        self.photoimage = ImageTk.PhotoImage(img)
        b1 = Button(frame, image=self.photoimage, command=self.register_data, borderwidth=0, cursor="hand2", font=("arial", 15, "bold"))
        b1.place(x=50, y=420, width=300)

        img1 = Image.open("login_button.jpg")
        img1 = img1.resize((200, 45))
        self.photoimage1 = ImageTk.PhotoImage(img1)
        b1 = Button(frame, image=self.photoimage1, command=self.return_login, borderwidth=0, cursor="hand2", font=("arial", 15, "bold"))
        b1.place(x=400, y=420, width=300)

    def return_login(self):
        self.root.destroy()

    def send_verification_email(self, email):
        try:
            # Generate a random verification code
            self.verify_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            subject = "Email Verification Code"
            body = f"Your verification code is: {self.verify_code}"

            # Set up the email
            msg = MIMEMultipart()
            msg['From'] = "youremail@example.com"
            msg['To'] = email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # Send the email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("youremail@example.com", "yourpassword")
            text = msg.as_string()
            server.sendmail("youremail@example.com", email, text)
            server.quit()

            messagebox.showinfo("Success", "Verification code sent to your email!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send verification email. Error: {str(e)}")

    def verify_email(self):
        code = self.txt_verify_code.get()
        if code == self.verify_code:
            self.verified = True
            messagebox.showinfo("Success", "Email verified successfully!")
        else:
            messagebox.showerror("Error", "Invalid verification code!")

    def register_data(self):
        if self.fname_entry.get() == "" or self.txt_email.get() == "" or self.combo_security_q.get() == "SELECT":
            messagebox.showerror("ERROR", "ALL FIELDS ARE REQUIRED!!")
        elif self.txt_pswd.get() != self.txt_confirm_pswd.get():
            messagebox.showerror("ERROR", "PASSWORD & CONFIRM PASSWORD MUST BE SAME!!")
        elif self.var_chk.get() == 0:
            messagebox.showerror("ERROR", "PLEASE AGREE OUR TERMS & CONDITIONS!!")
        else:
            if not self.verified:
                self.send_verification_email(self.txt_email.get())
                self.verification_window()
            else:
                conn = mysql.connector.connect(host="localhost", username="root", password="12345678", database="hotel_management")
                my_cursor = conn.cursor()
                query = ("select * from register2 where email=%s")
                value = (self.txt_email.get(),)
                my_cursor.execute(query, value)
                row = my_cursor.fetchone()
                if row is not None:
                    messagebox.showerror("ERROR", "USER ALREADY EXIST, PLEASE TRY ANOTHER EMAIL")
                else:
                    my_cursor.execute("insert into register2 values(%s,%s,%s,%s,%s,%s,%s)", (
                        self.fname_entry.get(),
                        self.txt_lname.get(),
                        self.txt_contact.get(),
                        self.txt_email.get(),
                        self.combo_security_q.get(),
                        self.txt_security.get(),
                        self.txt_pswd.get()
                    ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo("SUCCESS", "REGISTER SUCCESSFULLY")

    def verification_window(self):
        self.root2 = Toplevel()
        self.root2.title("Email Verification")
        self.root2.geometry("340x200+610+170")

        l = Label(self.root2, text="VERIFY YOUR EMAIL", font=("arial", 12, "bold"), fg="red", bg="white")
        l.place(x=0, y=10, relwidth=1)

        verify_code = Label(self.root2, text="ENTER VERIFICATION CODE:", font=("arial", 15, "bold"), bg="white", fg="black")
        verify_code.place(x=30, y=80)

        self.txt_verify_code = ttk.Entry(self.root2, font=("arial", 15, "bold"))
        self.txt_verify_code.place(x=50, y=110, width=250)

        btn = Button(self.root2, text="VERIFY", command=self.verify_email, font=("arial", 15, "bold"), fg="white", bg

="green")
        btn.place(x=100, y=150)


if __name__ == "__main__":
    root = Tk()
    app = Login_window(root)
    root.mainloop()
