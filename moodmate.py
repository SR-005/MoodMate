import customtkinter as ctk
from tkinter import font
from datetime import datetime
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

main=ctk.CTk()
main.geometry("800x800")

#FONT FAMILIES
font1=ctk.CTkFont(family="Coolvetica",size=12)
        #font1=font.Font(family="Coolvetica Rg",size=12)
font2=ctk.CTkFont(family="EastmanRomanTrial-Medium",size=12)


heading=ctk.CTkLabel(main,text="MoodMate",font=("Coolvetica",65),width=125,height=25,text_color="#096fb3")
heading.place(x=255,y=20)

currentdate=datetime.today().strftime('%d-%m-%Y')
datelabel=ctk.CTkLabel(main,text="Date: "+currentdate,font=("Coolvetica",20))
datelabel.place(x=320,y=87)

welcomelabel=ctk.CTkLabel(main,text="Hello User!! Hope your having a GREAT DAY",font=("EastmanRomanTrial-Medium",20))
welcomelabel.place(x=200,y=200)

main.mainloop()