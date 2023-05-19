from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernombreEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','Espacios sin llenar')
    elif usernombreEntry.get()=='Cesar' and passwordEntry.get()=='1234':
        messagebox.showinfo('Correcto','Bienvenido')
        window.destroy()
        import sms
        
    else:
        messagebox.showerror('Error','Credenciales invalidas')



window=Tk()

window.geometry('1280x700+0+0')
window.title('Sistema de inicio de sesion ')

window.resizable(False,False)

backgroundImage=ImageTk.PhotoImage(file='bg.jpg')

bgLabel=Label(window,image=backgroundImage)
bgLabel.place(x=0,y=0)

loginFrame=Frame(window,bg="greenyellow")
loginFrame.place(x=400,y=150)

logoImage=PhotoImage(file='logo.png')

logoLabel=Label(loginFrame,image=logoImage)
logoLabel.grid(row=0,column=0,columnspan=2,pady=10)
usernombreImage=PhotoImage(file='user.png')
usernombreLabel=Label(loginFrame,image=usernombreImage,text='Usuario: ',compound=LEFT
                    ,font=('times new roman',20,'bold'),bg='greenyellow')
usernombreLabel.grid(row=1,column=0,pady=10,padx=20)

usernombreEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5,fg='royalblue')
usernombreEntry.grid(row=1,column=1,pady=10,padx=20)

passwordImage=PhotoImage(file='password.png')
passwordLabel=Label(loginFrame,image=passwordImage,text='Contraseña: ',compound=LEFT
                    ,font=('times new roman',20,'bold'),bg='greenyellow')
passwordLabel.grid(row=2,column=0,pady=10,padx=20)

passwordEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5,fg='royalblue')
passwordEntry.grid(row=2,column=1,pady=10,padx=20)

loginButton=Button(loginFrame,text='Login',font=('times new roman',14,'bold'),width=15
                   ,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',
                   activeforeground='white',cursor='hand2',command=login)
loginButton.grid(row=3,column=1,pady=10)



window.mainloop()