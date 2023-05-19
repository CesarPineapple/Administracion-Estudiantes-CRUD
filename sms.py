from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas
#functionality Part

def iexit():
    result=messagebox.askyesno('Conrfirmar','¿Quieres salir?')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfilenombre(defaultextension='.csv')
    indexing=estudianteTable.get_children()
    newlist=[]
    for index in indexing:
        content=estudianteTable.item(index)
        datalist=content['values']
        newlist.append(datalist)


    table=pandas.DataFrame(newlist,columns=['Id','nombre','telefono','correo','domicilio','genero','ddn','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Perfecto','Datos guardados correctamente')

def toplevel_data(title,button_text,command):
    global idEntry,phoneEntry,nombreEntry,correoEntry,domicilioEntry,generoEntry,ddnEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nombreLabel = Label(screen, text='Nombre', font=('times new roman', 20, 'bold'))
    nombreLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nombreEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nombreEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Telefono', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    correoLabel = Label(screen, text='Correo', font=('times new roman', 20, 'bold'))
    correoLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    correoEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    correoEntry.grid(row=3, column=1, pady=15, padx=10)

    domicilioLabel = Label(screen, text='Domicilio', font=('times new roman', 20, 'bold'))
    domicilioLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    domicilioEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    domicilioEntry.grid(row=4, column=1, pady=15, padx=10)

    generoLabel = Label(screen, text='Genero', font=('times new roman', 20, 'bold'))
    generoLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    generoEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    generoEntry.grid(row=5, column=1, pady=15, padx=10)

    ddnLabel = Label(screen, text='D.D.N', font=('times new roman', 20, 'bold'))
    ddnLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    ddnEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    ddnEntry.grid(row=6, column=1, pady=15, padx=10)

    estudiante_button = ttk.Button(screen, text=button_text, command=command)
    estudiante_button.grid(row=7, columnspan=2, pady=15)
    if title=='Update estudiante':
        indexing = estudianteTable.focus()

        content = estudianteTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nombreEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        correoEntry.insert(0, listdata[3])
        domicilioEntry.insert(0, listdata[4])
        generoEntry.insert(0, listdata[5])
        ddnEntry.insert(0, listdata[6])

def update_data():
    query='update estudiante set nombre=%s,telefono=%s,correo=%s,domicilio=%s,genero=%s,ddn=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(nombreEntry.get(),phoneEntry.get(),correoEntry.get(),domicilioEntry.get(),
                            generoEntry.get(),ddnEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Perfecto',f'Id {idEntry.get()} fue modificado exitosamente',parent=screen)
    screen.destroy()
    show_estudiante()

def show_estudiante():
    query = 'select * from estudiante'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    estudianteTable.delete(*estudianteTable.get_children())
    for data in fetched_data:
        estudianteTable.insert('', END, values=data)

def delete_estudiante():
    indexing=estudianteTable.focus()
    print(indexing)
    content=estudianteTable.item(indexing)
    content_id=content['values'][0]
    query='delete from estudiante where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} is deleted succesfully')
    query='select * from estudiante'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    estudianteTable.delete(*estudianteTable.get_children())
    for data in fetched_data:
        estudianteTable.insert('',END,values=data)

def search_data():
    query='select * from estudiante where id=%s or nombre=%s or correo=%s or telefono=%s or domicilio=%s or genero=%s or ddn=%s'
    mycursor.execute(query,(idEntry.get(),nombreEntry.get(),correoEntry.get(),phoneEntry.get(),domicilioEntry.get(),generoEntry.get(),ddnEntry.get()))
    estudianteTable.delete(*estudianteTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        estudianteTable.insert('',END,values=data)

def add_data():
    if idEntry.get()=='' or nombreEntry.get()=='' or phoneEntry.get()=='' or correoEntry.get()=='' or domicilioEntry.get()=='' or generoEntry.get()=='' or ddnEntry.get()=='':
        messagebox.showerror('Error','Todos los campos son obligatorios',parent=screen)

    else:
        try:
            query='insert into estudiante values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),nombreEntry.get(),phoneEntry.get(),correoEntry.get(),domicilioEntry.get(),
                                    generoEntry.get(),ddnEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Datos agregados correctamente. ¿Quieres quitar el formulario?',parent=screen)
            if result:
                idEntry.delete(0,END)
                nombreEntry.delete(0,END)
                phoneEntry.delete(0,END)
                correoEntry.delete(0,END)
                domicilioEntry.delete(0,END)
                generoEntry.delete(0,END)
                ddnEntry.delete(0,END)
            else:
                pass
        except:
            messagebox.showerror('Error','La Id no se puede repetir',parent=screen)
            return


        query='select *from estudiante'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        estudianteTable.delete(*estudianteTable.get_children())
        for data in fetched_data:
            estudianteTable.insert('',END,values=data)

def connect_database():
    def connect():
        global mycursor,con
        try:
            con=pymysql.connect(host='localhost',user='root',password='tu_contrasena')
            mycursor=con.cursor()
            
        except:
            messagebox.showerror('Error','Datos incorrectos',parent=connectWindow)
            return

        try:
            query='create database gestionestudiantes'
            mycursor.execute(query)
            query='use gestionestudiantes'
            mycursor.execute(query)
            query='create table estudiante(id int not null primary key, nombre varchar(30),telefono varchar(10),correo varchar(30),' \
                  'domicilio varchar(100),genero varchar(20),ddn varchar(20),date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query='use gestionestudiantes'
            mycursor.execute(query)
        messagebox.showinfo('Perfecto', 'Base de datos conectada exitosamente', parent=connectWindow)
        connectWindow.destroy()
        addestudianteButton.config(state=NORMAL)
        searchestudianteButton.config(state=NORMAL)
        updateestudianteButton.config(state=NORMAL)
        showestudianteButton.config(state=NORMAL)
        exportestudianteButton.config(state=NORMAL)
        deleteestudianteButton.config(state=NORMAL)


    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Conexión de base de datos')
    connectWindow.resizable(0,0)

    hostnombreLabel=Label(connectWindow,text='Nombre del host',font=('arial',17,'bold'))
    hostnombreLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernombreLabel = Label(connectWindow, text='Usuario', font=('arial', 17, 'bold'))
    usernombreLabel.grid(row=1, column=0, padx=20)

    usernombreEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernombreEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Contraseña', font=('arial', 17, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='Conectar',command=connect)
    connectButton.grid(row=3,columnspan=2)

count=0
text=''
def slider():
    global text,count
    # if count==len(s):
    #     count=0
    #     text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)

def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Fecha: {date}\nHora: {currenttime}')
    datetimeLabel.after(1000,clock)

#GUI Part
root=ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('itft1')

root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('Sistema de gestión de Estudiantes')

datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()
s='Sistema de gestión de Estudiantes' #s[count]=t when count is 1
sliderLabel=Label(root,font=('arial',28,'italic bold'),width=30)
sliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Conectar Base de datos',command=connect_database)
connectButton.place(x=970,y=0)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='student.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

addestudianteButton=ttk.Button(leftFrame,text='Agregar Estudiante',width=25,state=DISABLED,command=lambda :toplevel_data('Add estudiante','Agregar',add_data))
addestudianteButton.grid(row=1,column=0,pady=20)

searchestudianteButton=ttk.Button(leftFrame,text='Buscar Estudiante',width=25,state=DISABLED,command=lambda :toplevel_data('Search estudiante','Buscar',search_data))
searchestudianteButton.grid(row=2,column=0,pady=20)

deleteestudianteButton=ttk.Button(leftFrame,text='Eliminar Estudiante',width=25,state=DISABLED,command=delete_estudiante)
deleteestudianteButton.grid(row=3,column=0,pady=20)

updateestudianteButton=ttk.Button(leftFrame,text='Actualizar Estudiante',width=25,state=DISABLED,command=lambda :toplevel_data('Update estudiante','Actualizar',update_data))
updateestudianteButton.grid(row=4,column=0,pady=20)

showestudianteButton=ttk.Button(leftFrame,text='Mostrar Estudiante',width=25,state=DISABLED,command=show_estudiante)
showestudianteButton.grid(row=5,column=0,pady=20)

exportestudianteButton=ttk.Button(leftFrame,text='Exportar Datos',width=25,state=DISABLED,command=export_data)
exportestudianteButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Salir',width=10,command=iexit)
exitButton.grid(row=6,column=1,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

estudianteTable=ttk.Treeview(rightFrame,columns=('Id','nombre','telefono','correo','domicilio','genero',
                                 'D.O.B','Added Date','Added Time'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=estudianteTable.xview)
scrollBarY.config(command=estudianteTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

estudianteTable.pack(expand=1,fill=BOTH)

estudianteTable.heading('Id',text='Id')
estudianteTable.heading('nombre',text='Nombre')
estudianteTable.heading('telefono',text='Telefono')
estudianteTable.heading('correo',text='Correo Electronico')
estudianteTable.heading('domicilio',text='Domicilio')
estudianteTable.heading('genero',text='Genero')
estudianteTable.heading('D.O.B',text='D.D.N')
estudianteTable.heading('Added Date',text='Fecha añadida')
estudianteTable.heading('Added Time',text='Tiempo añadido')

estudianteTable.column('Id',width=50,anchor=CENTER)
estudianteTable.column('nombre',width=200,anchor=CENTER)
estudianteTable.column('correo',width=300,anchor=CENTER)
estudianteTable.column('telefono',width=200,anchor=CENTER)
estudianteTable.column('domicilio',width=300,anchor=CENTER)
estudianteTable.column('genero',width=100,anchor=CENTER)
estudianteTable.column('D.O.B',width=200,anchor=CENTER)
estudianteTable.column('Added Date',width=200,anchor=CENTER)
estudianteTable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview', rowheight=40,font=('arial', 12, 'bold'), fieldbackground='white', background='white',)
style.configure('Treeview.Heading',font=('arial', 14, 'bold'),foreground='blue')

estudianteTable.config(show='headings')

root.mainloop()
