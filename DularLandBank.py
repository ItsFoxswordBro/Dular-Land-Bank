#Import Libraries
import customtkinter as ctk
import tkinter as tk
import pyrebase
import json
from PIL import Image, ImageTk
import sys
import os
import tkinter.font as tkfont

#helper function for binary files
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

#Make inter font exist as it is not a default font and i want it to be used in the app
def register_inter_font():
    try:
        path = resource_path('Inter-VariableFont_opsz,wght.ttf')
        if os.path.exists(path):
            return 'Inter'
    except Exception as e:
        print(f'Error loading custom font: {e}')
    return

#Pyrebase4 setup config
config = {
    'apiKey': 'AIzaSyDG_BcyP-8gmey_DDkbPcSULMM8AVfehD8',
    'authDomain': 'py-base-test.firebaseapp.com',
    'databaseURL': 'https://py-base-test-default-rtdb.europe-west1.firebasedatabase.app',
    'storageBucket': 'py-base-test.firebasestorage.app',
}

#Intialize Pyrebase4 Essential Variables
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
is_verified = False

#Setup for CustomTkinter
root = ctk.CTk()
title = 'Dular Land Bank'
root.after(200, lambda: root.title(title))
root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}')
raw_image = Image.open(resource_path('icon.png'))
App_icon = ctk.CTkImage(light_image=raw_image, dark_image=raw_image, size=(root.winfo_screenwidth() // 5, root.winfo_screenwidth() // 5))
window_bar_icon = ImageTk.PhotoImage(raw_image)
root.after(200, lambda: root.iconphoto(False, window_bar_icon))
INTER_FONT = register_inter_font()
dulars = '?'
#i have unfortunately forgotten what this does
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#Set Appearance also if you choose light you're wrong, i will have to add light mode support later in settings -> accessibility tho
root.configure(fg_color='#121212')

#Screen Layering, but really showing
def show_screen(screen):
    screen.tkraise()

#FUNCTIONS(juicy part)
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
def login(email2, password):
    global user, logged_in_screen, login_email_entry, login_password_entry, login_error_label, is_verified, user_info, email, dulars
    try:
        user = auth.sign_in_with_email_and_password(email2, password)
        user_info = auth.get_account_info(user['idToken'])
        login_error_label.configure(text='')
        is_verified = user_info['users'][0]['emailVerified']
        if is_verified:
            show_screen(logged_in_screen)
            login_error_label.configure(text='')
            login_success_label = ctk.CTkLabel(logged_in_screen, text = 'Logged in successfully!', font = (INTER_FONT, 16), text_color='#44FF44')
            login_success_label.pack(pady = 10)
            root.after(2000, lambda: login_success_label.configure(text=''))
            email = email2
            login_error_label.configure(text='Email not verified or credentials not entered, if you cant find the email to verify your account, please check in your spam folder as well or please wait 3-7 days and try again. or contact support.', text_color='#FF4444')
        try:
            dulars = float(db.child('users').child(email.replace('.', ',')).child("dulars").get(token=user['idToken']).val())
        except:
            dulars = "?"

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

    global user, user_info, signup_email_entry, signup_password_entry, confirm_password_entry, signup_screen, signup_error_label, Check_Verification_Button, dulars, email
    try:
        if signup_password_entry.get() == confirm_password_entry.get():
            user = auth.create_user_with_email_and_password(signup_email_entry.get(), signup_password_entry.get())
            user_info = auth.get_account_info(user['idToken'])
            login(signup_email_entry.get(), signup_password_entry.get())
            auth.send_email_verification(user['idToken'])
            signup_error_label.configure(signup_screen, text='Verification email sent. Please verify your email before logging in and make sure to check your spam folder as well.', font = (INTER_FONT, 16), text_color='#44FF44')
            email = signup_email_entry.get()
            # --- ISOLATED DB PUSH ---
            try:    
                request = {
                    'uid': user['localId'],
                    'type': 'signup',
                    'email': email
                }
                db.child('requests').push(request, user['idToken'])
            except Exception as db_e:
                print('--- DATABASE ERROR DETAILS START ---')
                print(f'Error type: {type(db_e)}')
                print(f'Error message: {db_e}')
                print('--- DATABASE ERROR DETAILS END ---')
            try:
                dulars = float(db.child('users').child(email.replace('.', ',')).child("dulars").get(token=user['idToken']).val())
            except:
                dulars = "?"


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

def send_dulars():
    global send_dulars_screen, email, logged_in_screen, not_true_verified_label, dulars
    safe_email = email.replace('.', ',')
    if db.child('users').child(safe_email).get(token = user['idToken']).val():
        if 0 < float(dulars) >=float(Amount_entry.get()):
            request = {
                'uid': user['localId'],
                'type': 'send_dulars',
                'recipient_email': Recipient_email_entry.get(),
                'amount': float(Amount_entry.get()),
                'email': email.replace('.', ',')
            }
            db.child('requests').push(request, token = user['idToken'])
            somewhat_success_label = ctk.CTkLabel(send_dulars_screen, text = 'Dulars are in the process of being sent! If this request was invalid the dulars will not be sent. Sending Dulars Can Take Some time', font = (INTER_FONT, 16), text_color='#44FF44')
            somewhat_success_label.place(relx = 0.5, rely = 0.9, anchor = 's')
    else:
        not_true_verified_label = ctk.CTkLabel(send_dulars_screen, text = 'You do not have a true verified account in the database. Please contact support or wait.', font = (INTER_FONT, 16), text_color='#FF4444')
        not_true_verified_label.place(relx = 0.5, rely = 0.9, anchor = 's')
        root.after(2000, lambda: not_true_verified_label.configure(text=''))

def check_dulars():
    global dulars, email
    try:
        dulars = float(db.child('users').child(email.replace('.', ',')).child("dulars").get(token=user['idToken']).val())
        dulars_label.configure(text = dulars)
        dulars_label2.configure(text = dulars)
    except:
        dulars = "?"
        dulars_label.configure(text = dulars)
        dulars_label2.configure(text = dulars)

#Screens
home_screen = ctk.CTkFrame(root, fg_color='#121212')
login_screen = ctk.CTkFrame(root, fg_color='#121212')
signup_screen = ctk.CTkFrame(root, fg_color='#121212')
logged_in_screen = ctk.CTkFrame(root, fg_color='#121212')
send_dulars_screen = ctk.CTkFrame(root, fg_color='#121212')

#i have unfortunately forgotten what this does
for screen in home_screen, login_screen, signup_screen, logged_in_screen, send_dulars_screen:
    screen.grid(row=0, column=0, sticky='nsew')

#Home_Screen
ctk.CTkLabel(home_screen, image = App_icon,text = '', font = (INTER_FONT, 30)).pack(pady = 20)
ctk.CTkButton(home_screen, text = 'Login', font = (INTER_FONT, 20), width = 400, height = 50, corner_radius = 12, command = lambda: show_screen(login_screen)).pack(pady = (15, 15))
ctk.CTkButton(home_screen, text = 'Sign Up', font = (INTER_FONT, 20), width = 400, height = 50, corner_radius = 12, command = lambda: show_screen(signup_screen)).pack(pady = (15, 15))
ctk.CTkLabel(home_screen, text = "Don't have an account? Press Sign Up! Press Login to access an existing account!", font = (INTER_FONT, 16)).pack(pady = (15, 0))

#logged_in_screen
chhota_app_icon = ctk.CTkImage(light_image = raw_image, size = (20, 20), dark_image = raw_image)
icon_label = ctk.CTkLabel(logged_in_screen, image = chhota_app_icon, text = '')
icon_label.place(relx = 0.01, rely = 0.01, anchor = 'nw')
dulars_label = ctk.CTkLabel(logged_in_screen, text = dulars, font = (INTER_FONT, 20), text_color='#44FF44')
dulars_label.place(relx = 0.03, rely = 0.01, anchor = 'nw')
icon_label2 = ctk.CTkLabel(send_dulars_screen, image = chhota_app_icon, text = '')
icon_label2.place(relx = 0.01, rely = 0.01, anchor = 'nw')
dulars_label2 = ctk.CTkLabel(send_dulars_screen, text = dulars, font = (INTER_FONT, 20), text_color='#44FF44')
dulars_label2.place(relx = 0.03, rely = 0.01, anchor = 'nw')
ctk.CTkLabel(logged_in_screen, text = 'Welcome to Dular Land Bank!', font = (INTER_FONT, 60, 'bold'), text_color='#FFFFFF').pack(pady = 20)
ctk.CTkButton(logged_in_screen, text = 'Logout', font = (INTER_FONT, 20), width = 400, height = 50, corner_radius = 12, command = lambda: logout()).pack(pady = 20, expand = True)
ctk.CTkButton(logged_in_screen, text = 'Send Dulars', font = (INTER_FONT, 20), width = 400, height = 50, corner_radius = 12, command = lambda: show_screen(send_dulars_screen)).pack(pady = 20, expand = True)
reload_dulars_button = ctk.CTkButton(logged_in_screen, text = '🔄️', font = (INTER_FONT, 20), width = 120, height = 25, corner_radius = 12, command = lambda: check_dulars())
reload_dulars_button2 = ctk.CTkButton(send_dulars_screen, text = '🔄️', font = (INTER_FONT, 20), width = 120, height = 25, corner_radius = 12, command = lambda: check_dulars())
reload_dulars_button.place(relx = 0.1, rely = 0, anchor = 'n')
reload_dulars_button2.place(relx = 0.1, rely = 0, anchor = 'n')
#send dulars screen
Recipient_email_entry = ctk.CTkEntry(send_dulars_screen, placeholder_text = 'Recipient Email', font = (INTER_FONT, 20), width = 400, height = 50)
Amount_entry = ctk.CTkEntry(send_dulars_screen, placeholder_text = 'Amount', font = (INTER_FONT, 20), width = 400, height = 50)
ctk.CTkButton(send_dulars_screen, text = 'Send', font = (INTER_FONT, 20), fg_color = '#FF0000', hover_color='#CC0000', width = 200, height = 50,corner_radius = 12 ,command = lambda: send_dulars()).pack(pady = 20, expand = True)
Recipient_email_entry.pack(pady = (20, 15))
Amount_entry.pack(pady = (15, 20))

#login screen
login_email_entry = ctk.CTkEntry(login_screen, placeholder_text = 'Email', font = (INTER_FONT, 20), width = 400, height = 50)
login_password_entry = ctk.CTkEntry(login_screen, placeholder_text = 'Password', font = (INTER_FONT, 20), width = 400, height = 50, show = '*')
login_email_entry.pack(pady = (20, 15))
login_password_entry.pack(pady = (15, 20))
login_error_label = ctk.CTkLabel(login_screen, text = '', font = (INTER_FONT, 16))
login_error_label.pack(pady = 10)
ctk.CTkButton(login_screen, text = 'Login', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: login(login_email_entry.get(), login_password_entry.get())).pack(pady = 30)

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



#Back Buttons(idk why bundled together)
ctk.CTkButton(login_screen, text = 'Back', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: show_screen(home_screen)).pack(pady = 20, expand = True)
ctk.CTkButton(signup_screen, text = 'Back', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: show_screen(home_screen)).pack(pady = 20, expand = True)
ctk.CTkButton(send_dulars_screen, text = 'Back', font = (INTER_FONT, 20), width = 200, height = 50, command = lambda: show_screen(logged_in_screen)).pack(pady = 20, expand = True)

#Show Home Screen on Startup
show_screen(home_screen)

#Contact Support Stuff(useless but i want it to be there)
for custom in home_screen, login_screen, signup_screen, logged_in_screen, send_dulars_screen:
    support_label = ctk.CTkLabel(custom, text='Support: dularsupport@gmail.com', font=(INTER_FONT, 13, 'bold'), text_color='#757575', fg_color='#121212')
    support_label.place(relx=0.98, rely=0.98, anchor='se')


#STARTTTTTTTTTTTTTTTTTTTTTTTTTTTT
root.mainloop()
