import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from glob import glob
from xml.etree.ElementTree import parse as parse_xml

#Hauptfenster erzeugen
root = tk.Tk()

#Fenstertitel
root.title("RED-Medical-Dataviewer")

image = Image.open("image_01.jpg")
photo = ImageTk.PhotoImage(image)

#Fenstergröße
root.geometry("800x500")
root.minsize(width=400, height=250)

#Label, Labeltext
label1 = ttk.Label(root, text="Bitte geben Sie den Nachnamen des Patienten ein:")
label1.grid(row=0, column=0)
label1.configure(font=("Arial"))
label2 = ttk.Label(root, text="Bitte geben Sie den Vornamen des Patienten ein:")
label2.grid(row=1, column=0)
label2.configure(font=("Arial"))
#label3 = ttk.Label(root, image=photo)
#label3.grid()

#Entryfields erstellen
input_field1 = ttk.Entry(root, width=30)
input_field1.grid(row=0, column=1)

input_field2 = ttk.Entry(root, width=30)
input_field2.grid(row=1, column=1)

def read_input_fields():
    current_input1 = input_field1.get()
    current_input2 = input_field2.get()

    files = glob("./data/Patientenakten/*/" + input_field1.get() + "*_" + input_field2.get() + "*_*_AW.xml")

    label4 = ttk.Label(root, text="Ich habe " + str(len(files)) + " Patienten für Sie gefunden:")  
    label4.grid(row=4, column=1)
    label4.configure(font=("Arial"))

    pat_count = 0
    patients = []

    for f in files:
        pat_name = f.split("\\")
        pat_name = pat_name[2]
        pat_name = pat_name.split("_")
        pat_name = pat_name[0:2]
        pat_count = pat_count + 1

        patient = {
            "name": pat_name,
            "file": f
        }
        patients.append(patient)

        #print(pat_count, pat_name[0], pat_name[1])
        
        #listbox = tk.Listbox(root)
        #listbox.insert(pat_count, pat_name[0], pat_name[1])
        #listbox.grid(row=6, column=1)
        #listbox.configure(font=("Arial"), width=50)

        tree = ttk.Treeview(root)
        tree['columns'] = ("Nummer", "Nachname", "Vorname")
        tree.column("#0", width=120)
        tree.column("Nummer", anchor=W)
        tree.column("Nachname", anchor=CENTER)
        tree.column("Vorname", anchor=E)

        # Überschriften erstellen
 #       tree.heading("#0", text=)
        tree.heading("Nummer", text="Nummer", anchor=CENTER)
        tree.heading("Nachname", text="Nachname", anchor=CENTER)
        tree.heading("Vorname", text="Vorname", anchor=CENTER)
       
        tree.insert(parent= '', index='end', iid=0, text=str(pat_count))
        tree.grid(row=6, column=1)

    label6 = ttk.Label(root, text="Bitte geben Sie die Nummer des gewünschten Patienten ein: ")  
    label6.grid(row=7, column=0)
    label6.configure(font=("Arial"))
    input_field3 = ttk.Entry(root, width=8)
    input_field3.grid(row=7, column=1)

    ok_button2 = Button(root, text="OK")
    ok_button2.grid(row=8, column=1)

#pat_num = int(input_field3)

#Button erstellen
ok_button = Button(root, text="Suche starten", command=read_input_fields)
ok_button.grid(row=2, column=1)

root.mainloop()