#Import Libraries
import customtkinter as ctk
import tkinter as tk
import pyrebase
import json
from PIL import Image, ImageTk
import sys
import os
import tkinter.font as tkfont

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def register_inter_font():
    try:
        path = resource_path('Inter-VariableFont_opsz,wght.ttf')
        if os.path.exists(path):
            return 'Inter'
    except Exception as e:
        print(f'Error loading custom font: {e}')
    return

#Pyrebase setup config thing
config = {
    'apiKey': 'AIzaSyDG_BcyP-8gmey_DDkbPcSULMM8AVfehD8',
    'authDomain': 'py-base-test.firebaseapp.com',
    'databaseURL': 'https://py-base-test-default-rtdb.europe-west1.firebasedatabase.app',
    'storageBucket': 'py-base-test.firebasestorage.app',
}

#More Setup(Real Setup for the Pyrebase stuff)
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
is_verified = False

#More Setup? idk
root = ctk.CTk()
title = 'Dular Land Bank'
root.after(200, lambda: root.title(title))
root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}')
raw_image = Image.open(resource_path('icon.png'))
App_icon = ctk.CTkImage(light_image=raw_image, dark_image=raw_image, size=(root.winfo_screenwidth() // 5, root.winfo_screenwidth() // 5))
window_bar_icon = ImageTk.PhotoImage(raw_image)
root.after(200, lambda: root.iconphoto(False, window_bar_icon))
INTER_FONT = register_inter_font()

#idk what this does but it was in the tutorial so here we are i think it fills stuff to the screen or smt
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#Set Appearance also if you choose light you're wrong
root.configure(fg_color='#121212')

#shifts stuff layering thing
def show_screen(screen):
    screen.tkraise()

#function for no yo army



#self explanatory stuff
def logout():
    global home_screen
    try:
        user = None
        login_email_entry.delete(0, 'end')
        login_password_entry.delete(0, 'end')
        signup_email_entry.delete(0, 'end')
        signup_password_entry.delete(0, 'end')
        confirm_password_entry.delete(0, 'end')
        show_screen(home_screen)
        log_out_label_thing = ctk.CTkLabel(home_screen, text = 'Logged out successfully(Destroyed Current Session)', font = (INTER_FONT, 16), text_color='#44FF44')
        log_out_label_thing.pack(pady = 10)
        root.after(2000, lambda: log_out_label_thing.configure(text=''))
    except Exception as e:
        ctk.CTkLabel(logged_in_screen, text = 'An error occurred during logout.', font = (INTER_FONT, 16), text_color='#FF4444').pack(pady = 10)
    show_screen(home_screen)
def login(email, password):
    global user, logged_in_screen, login_email_entry, login_password_entry, login_error_label, is_verified, user_info
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        user_info = auth.get_account_info(user['idToken'])
        user = auth.refresh(user['refreshToken'])
        login_error_label.configure(text='')
        is_verified = user_info['users'][0]['emailVerified']
        if is_verified:
            show_screen(logged_in_screen)
            login_error_label.configure(text='')
            login_success_label = ctk.CTkLabel(logged_in_screen, text = 'Logged in successfully!', font = (INTER_FONT, 16), text_color='#44FF44')
            login_success_label.pack(pady = 10)
            root.after(2000, lambda: login_success_label.configure(text=''))
        else:
            login_error_label.configure(text='Email not verified or credentials not entered, if you cant find the email to verify your account, please check in your spam folder as well or please wait 3-7 days and try again. or contact support.', text_color='#FF4444')
    except Exception as e:
        try:
            error_json = json.loads(e.args[1])
            error_data = error_json['error']
            error_code = error_data['code']
            error_message = error_data['message']
            
            clean_text = f'Firebase Error Code: {error_code}: {error_message}'
            login_error_label.configure(text=clean_text, text_color='#FF4444')
        except Exception as e:
            login_error_label.configure(text='An unknown error occurred during login.', text_color='#FF4444')
def signup():
    global user, user_info, signup_email_entry, signup_password_entry, confirm_password_entry, signup_screen, signup_error_label, Check_Verification_Button
    try:
        if signup_password_entry.get() == confirm_password_entry.get():
            user = auth.create_user_with_email_and_password(signup_email_entry.get(), signup_password_entry.get())
            user_info = auth.get_account_info(user['idToken'])
            login(signup_email_entry.get(), signup_password_entry.get())
            auth.send_email_verification(user['idToken'])
            signup_error_label.configure(signup_screen, text='Verification email sent. Please verify your email before logging in and make sure to check your spam folder as well.', font = (INTER_FONT, 16), text_color='#44FF44')
        else:
            signup_error_label.configure(signup_screen, text='Passwords do not match.', font = (INTER_FONT, 16), text_color='#FF4444')
    except Exception as e:
        try:
            error_json = json.loads(e.args[1])
            error_data = error_json['error']
            error_code = error_data['code']
            error_message = error_data['message']
            
            clean_text = f'Firebase Error Code: {error_code}: {error_message}'
            signup_error_label.configure(text=clean_text, font = (INTER_FONT, 16), text_color='#FF4444')
        except Exception as e:
            signup_error_label.configure(signup_screen, text='An unknown error occurred during signup.', font = (INTER_FONT, 16), text_color='#FF4444')

def check_ver():
    global user_info, is_verified, signup_error_label, logged_in_screen, Check_Verification_Button, user
    try:
        user = auth.refresh(user['refreshToken'])
        user_info = auth.get_account_info(user['idToken'])
        is_verified = user_info['users'][0]['emailVerified']
        if is_verified:
            show_screen(logged_in_screen)
            signup_error_label.configure(text='')
            show_screen(logged_in_screen)
            Email_ver_success = ctk.CTkLabel(logged_in_screen, text = 'Email verified successfully! You are now logged in.', font = (INTER_FONT, 16), text_color='#44FF44')
            Email_ver_success.pack(pady = 10)
            root.after(2000, lambda: Email_ver_success.configure(text=''))
        else:
            signup_error_label.configure(text='Email not verified yet.', font = (INTER_FONT, 16), text_color='#FF4444')
    except Exception as e:
        try:
            error_json = json.loads(e.args[1])
            error_data = error_json['error']
            error_code = error_data['code']
            error_message = error_data['message']
            
            clean_text = f'Firebase Error Code: {error_code}: {error_message}'
            signup_error_label.configure(text=clean_text, font = (INTER_FONT, 16), text_color='#FF4444')
        except Exception as e:
            signup_error_label.configure(text='An unknown error occurred while checking verification status.', font = (INTER_FONT, 16), text_color='#FF4444')

#Screens
home_screen = ctk.CTkFrame(root, fg_color='#121212')
check_request_id_status_screen = ctk.CTkFrame(root, fg_color='#121212')
login_screen = ctk.CTkFrame(root, fg_color='#121212')
signup_screen = ctk.CTkFrame(root, fg_color='#121212')
logged_in_screen = ctk.CTkFrame(root, fg_color='#121212')

#i again dk what this does but it was in the tutorial so here we are i think it does setup stuff for the screens or smt
for screen in home_screen, check_request_id_status_screen, login_screen, signup_screen, logged_in_screen:
    screen.grid(row=0, column=0, sticky='nsew')

#Home_Screen
ctk.CTkLabel(home_screen, image = App_icon,text = '', font = (INTER_FONT, 30)).pack(pady = 20)
ctk.CTkButton(home_screen, text = 'Login', font = (INTER_FONT, 20), width = 400, height = 50, corner_radius = 12, command = lambda: show_screen(login_screen)).pack(pady = (15, 15))
ctk.CTkButton(home_screen, text = 'Sign Up', font = (INTER_FONT, 20), width = 400, height = 50, corner_radius = 12, command = lambda: show_screen(signup_screen)).pack(pady = (15, 15))
ctk.CTkLabel(home_screen, text = "Don't have an account? Press Sign Up! Press Login to access an existing account!", font = (INTER_FONT, 16)).pack(pady = (15, 0))


#logged_in_screen

ctk.CTkLabel(logged_in_screen, text = 'Welcome to Dular Land Bank!', font = (INTER_FONT, 60, 'bold'), text_color='#FFFFFF').pack(pady = 20)
ctk.CTkButton(logged_in_screen, text = 'Logout', font = (INTER_FONT, 20), width = 400, height = 50, corner_radius = 12, command = lambda: logout()).pack(pady = 20, expand = True)


#MAGIC
id_entry = ctk.CTkEntry(check_request_id_status_screen, placeholder_text = 'Request ID', font = (INTER_FONT, 20), width = 400, height = 50)
id_entry.pack(pady = 20, expand = True) 

#check_request_id_status_screen
ctk.CTkButton(check_request_id_status_screen, text = 'Check Status', font = (INTER_FONT, 20), fg_color = '#FF0000', hover_color='#CC0000', width = 200, height = 50,corner_radius = 12 ,command = lambda: check_ver()).pack(pady = 20, expand = True)

#login screen
login_email_entry = ctk.CTkEntry(login_screen, placeholder_text = 'Email', font = (INTER_FONT, 20), width = 400, height = 50)
login_password_entry = ctk.CTkEntry(login_screen, placeholder_text = 'Password', font = (INTER_FONT, 20), width = 400, height = 50, show = '*')
login_email_entry.pack(pady = (20, 15))
login_password_entry.pack(pady = (15, 20))
login_error_label = ctk.CTkLabel(login_screen, text = '', font = (INTER_FONT, 16))
login_error_label.pack(pady = 10)
ctk.CTkButton(login_screen, text = 'Login', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: login(login_email_entry.get(), login_password_entry.get())).pack(pady = 30)

#label for the status message stuff
status_msg_label = ctk.CTkLabel(check_request_id_status_screen, text = '', font = (INTER_FONT, 20))
status_msg_label.pack(pady = 20, expand = True)

#signup screen
signup_email_entry = ctk.CTkEntry(signup_screen, placeholder_text = 'Email', font = (INTER_FONT, 20), width = 400, height = 50)
signup_password_entry = ctk.CTkEntry(signup_screen, placeholder_text = 'Password', font = (INTER_FONT, 20), width = 400, height = 50, show = '*')
confirm_password_entry = ctk.CTkEntry(signup_screen, placeholder_text = 'Confirm Password', font = (INTER_FONT, 20), width = 400, height = 50, show = '*')
signup_error_label = ctk.CTkLabel(signup_screen, text = '', font = (INTER_FONT, 16))
Check_Verification_Button = ctk.CTkButton(signup_screen, text = 'Check Verification Status', font = (INTER_FONT, 20), width = 300, height = 50, command = lambda: check_ver())

signup_email_entry.pack(pady = (20, 15))
signup_password_entry.pack(pady = (15, 15))
confirm_password_entry.pack(pady = (15, 15))
signup_error_label.pack(pady = (15, 15))
ctk.CTkButton(signup_screen, text = 'Sign Up', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: signup()).pack(pady = 30)
Check_Verification_Button.pack(pady = (15, 20))



#i forgot to add back buttons so here we are
ctk.CTkButton(check_request_id_status_screen, text = 'Back', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: show_screen(logged_in_screen)).pack(pady = 20, expand = True)
ctk.CTkButton(login_screen, text = 'Back', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: show_screen(home_screen)).pack(pady = 20, expand = True)
ctk.CTkButton(signup_screen, text = 'Back', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: show_screen(home_screen)).pack(pady = 20, expand = True)

#f5/fn+f5
show_screen(home_screen)

#wait... contact support stuff ugh... i most probably wont respond but i think i should add it for showcase
for custom in home_screen, login_screen, signup_screen, logged_in_screen:
    support_label = ctk.CTkLabel(custom, text='Support: (enter support contact here uh)', font=(INTER_FONT, 13, 'bold'), text_color='#757575', fg_color='#121212')
    support_label.place(relx=0.98, rely=0.98, anchor='se')


#STARTTTTTTTTTTTTTTTTTTTTTTTTTTTT
root.mainloop()
