# Import required modules and liberaries
from tkinter import *
import tkinter as tk
from tkinter import font 
from tkinter import filedialog 
from tkinter import colorchooser
import os , sys
from win32printing import Printer
import win32api


root= Tk()
root.geometry("1200x680")
root.title("Text Editor")

global open_status_name 
open_status_name =FALSE 

global selected
selected= False
#New file function
def new_file():
    global open_status_name 
    open_status_name =FALSE 
    Txt_box.delete('1.0', END) #Delete previous text
    root.title("Entitled - Text Editor")
    status_bar.config(text="New file !    ")

#open file function
def open_file():
    Txt_box.delete('1.0', END) #Delete previous text
    #grab fileName
    text_file = filedialog.askopenfilename(title="open File" , filetypes=(("Text Files" , "*.txt"),("HTML Files" , "*.html"),("Python Files" , "*.py"),("ALL Files" , "*.*")))
    if text_file:
        #Make filename global variable
        global open_status_name
        open_status_name =text_file
    
    #Update Status Bar
    name = text_file 
    status_bar.config(text=name)
    root.title(f'{name} - TEXT EDITOR')
    #open the file
    text_file =open(text_file ,'r')
    stuff= text_file.read()
    #Add file to textBox
    Txt_box.insert(END, stuff)
    #close file
    text_file.close()

#Save function
def save_file():
    global open_status_name
    if open_status_name :
        #Save the file
        text_file =open(open_status_name ,'w')
        text_file.write(Txt_box.get(1.0 ,END))
        text_file.close()
        status_bar.config(text=f'Saved : {open_status_name}  ')
    else:
        saveAs_file()


def saveAs_file():
    text_file =filedialog.asksaveasfilename(defaultextension=".*", title="Save file" , filetypes=(("Text Files" , "*.txt"),("HTML Files" , "*.html"),("Python Files" , "*.py"),("ALL Files" , "*.*")))
    if text_file :
        name= text_file
        #Update Status Bar
        status_bar.config(text=name)
        root.title(f'{name} - TEXT EDITOR')

        #Save the file
        text_file =open(text_file ,'w')
        text_file.write(Txt_box.get(1.0 ,END))
        text_file.close()

#cut text
def cut_text(e):
    global selected
    if e:
        selected =root.clipboard_get()
    else:
        if Txt_box.selection_get():
            #grab selected text 
            selected= Txt_box.selection_get()
            #delete selected box
            Txt_box.delete("sel.first","sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)


#copy text
def copy_text(e):
    global selected
    if e:
        selected =root.clipboard_get()
    else:
        if Txt_box.selection_get():
            #grab selected text 
            selected= Txt_box.selection_get()
            root.clipboard_clear()
            root.clipboard_append(selected)

#paste text
def paste_text(e):
    global selected
    if e:
        selected =root.clipboard_get()
    else:
        if selected :
            position =Txt_box.index(INSERT)
            Txt_box.insert(position, selected)

#Select all function
def select_all(e):
    #add sel tag to select all text
    Txt_box.tag_add('sel','1.0', 'end')


#clear text box function 
def clear():
    Txt_box.delete(1.0 ,END)

# bold function 
def bold_it():
    bold_font =font.Font(Txt_box ,Txt_box.cget("font"))
    bold_font.configure(weight="bold")

    Txt_box.tag_configure("bold" , font=bold_font)
    current_tags= Txt_box.tag_names("sel.first")
    if "bold" in current_tags :
        Txt_box.tag_remove("bold" , "sel.first" ,"sel.last")
    else:
        Txt_box.tag_add("bold" , "sel.first" ,"sel.last")

#Italics function
def italics_it():
    italics_font =font.Font(Txt_box ,Txt_box.cget("font"))
    italics_font.configure(slant="italic")

    Txt_box.tag_configure("italic" , font=italics_font)

    current_tags= Txt_box.tag_names("sel.first")

    if "italic" in current_tags :
        Txt_box.tag_remove("italic" , "sel.first" ,"sel.last")
    else:
        Txt_box.tag_add("italic" , "sel.first" ,"sel.last")

#color text function

def text_color():
    #pick color
    my_color=colorchooser.askcolor()[1]
    if my_color:
        color_font =font.Font(Txt_box ,Txt_box.cget("font"))
        Txt_box.tag_configure("colored" , font=color_font , foreground=my_color)

        current_tags= Txt_box.tag_names("sel.first")

        if "colored" in current_tags :
            Txt_box.tag_remove("colored" , "sel.first" ,"sel.last")
        else:
            Txt_box.tag_add("colored" , "sel.first" ,"sel.last")

#Bg color function
def bg_color():
    my_color=colorchooser.askcolor()[1]
    if my_color:
        Txt_box.config(bg=my_color)

#All text
def all_text_color():
    my_color=colorchooser.askcolor()[1]
    if my_color:
        Txt_box.config(fg=my_color)

#print files picture
def print_file():
    printer_name= Printer.get_default_doc_name
    status_bar.config(text=printer_name)

    file_to_print=filedialog.askopenfilename(defaultextension=".*", title="Save file" , filetypes=(("Text Files" , "*.txt"),("HTML Files" , "*.html"),("Python Files" , "*.py"),("ALL Files" , "*.*")))
    if file_to_print :
        win32api.ShellExecute(0, "print" , file_to_print ,None , "." , 0)

#create toolBar frame
toolbar_frame=Frame(root)
toolbar_frame.pack(fill=X)
        

#Main Frame

main_frame = Frame(root)
main_frame.pack(pady=5)

 # Vertical Scrollbar for the text box
txt_scroll = Scrollbar(main_frame)
txt_scroll.pack(side=RIGHT , fill=Y)

# #Horizantal Scrollbar for the text box
txt_scrollX = Scrollbar(main_frame ,orient='horizontal')
txt_scrollX.pack(side=BOTTOM , fill=X)

#text Box
Txt_box= Text(main_frame , width=97 , height= 25 , font= ('Helvetica', 16) , selectbackground="yellow" , undo=True ,selectforeground="black" ,yscrollcommand=txt_scroll.set ,xscrollcommand=txt_scrollX.set ,wrap="none")
Txt_box.pack()
#Config ScrollBars
txt_scroll.config(command=Txt_box.yview)
txt_scrollX.config(command=Txt_box.xview)


#Create Menu
My_menu= Menu(root)
root.config(menu=My_menu)

#Add file menu
file_menu=Menu(My_menu ,tearoff=False)
My_menu.add_cascade(label="File" ,menu=file_menu)
file_menu.add_command(label="New" ,command=new_file)
file_menu.add_command(label="Open" ,command=open_file)
file_menu.add_command(label="Save" ,command=save_file)
file_menu.add_command(label="Save As..." ,command=saveAs_file)
file_menu.add_separator()
file_menu.add_command(label="Print" ,command=print_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
#Add edit Menu
edit_menu=Menu(My_menu,tearoff=False)
My_menu.add_cascade(label="Edit" ,menu=edit_menu)
edit_menu.add_command(label="Cut" ,command=lambda: cut_text(False) , accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy",command=lambda: copy_text(False) ,accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste",command=lambda: paste_text(False) ,accelerator="(Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo" ,command=Txt_box.edit_undo , accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo" , command=Txt_box.edit_redo ,accelerator="(Ctrl+y)")
edit_menu.add_separator()
edit_menu.add_command(label="Select All" ,command=lambda: select_all(False) , accelerator="(Ctrl+a)")
edit_menu.add_command(label="Clear" , command=clear )

#Add color Menu
color_menu=Menu(My_menu,tearoff=False)
My_menu.add_cascade(label="Colors" ,menu=color_menu)
color_menu.add_command(label="Selected text color" ,command=text_color)
color_menu.add_command(label="All text",command=all_text_color)
color_menu.add_command(label="Baground Color",command=bg_color)

#Add Status Bar to bottom
status_bar= Label (root , text='Ready           ', anchor='e')
status_bar.pack(fill=X, side=BOTTOM , ipady=15)

#edit bindings
root.bind('<Control-Key-x>' ,cut_text)
root.bind('<Control-Key-c>' ,copy_text)
root.bind('<Control-Key-v>' ,paste_text)
root.bind('<Control-a>' ,select_all)
root.bind('<Control-A>' ,select_all)

# bold button
bold_button = Button(toolbar_frame, text="BOLD" , command=bold_it)
bold_button.grid(row=0 , column= 0 , sticky='w' ,padx=5)
# italics button
italics_button = Button(toolbar_frame, text="Italics" , command=italics_it)
italics_button.grid(row=0 , column= 1 , sticky='w' ,padx=5)

#text color button
color_text_button=Button(toolbar_frame , text="Text Color" , command=text_color )
color_text_button.grid(row=0 , column=2 ,sticky='w' ,padx=5)


#Run 
root.mainloop()