import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from glob import glob
from xml.etree.ElementTree import parse as parse_xml
import customtkinter as ctk

#Hauptfenster erzeugen
root = ctk.CTk()

#Fenstertitel
root.title("RED-Medical-Dataviewer")

image = Image.open("image_01.jpg")
photo = ImageTk.PhotoImage(image)

#Fenstergröße
root.geometry("800x500")
root.minsize(width=400, height=250)

#Label, Labeltext
label1 = ctk.CTkLabel(root, text="Bitte geben Sie den Nachnamen des Patienten ein:")
label1.grid(row=0, column=0)
label1.configure(font=ctk.CTkFont(family='Arial', size=12))
label2 = ctk.CTkLabel(root, text="Bitte geben Sie den Vornamen des Patienten ein:")
label2.grid(row=1, column=0)
label2.configure(font=ctk.CTkFont(family='Arial', size=12))
#label3 = ttk.Label(root, image=photo)
#label3.grid()

#Entryfields erstellen
input_field1 = ctk.CTkEntry(root, width=100)
input_field1.grid(row=0, column=1)

input_field2 = ctk.CTkEntry(root, width=100)
input_field2.grid(row=1, column=1)

def read_input_fields():
    input_field1.get()
    input_field2.get()

    files = glob("./data/Patientenakten/*/" + input_field1.get() + "*_" + input_field2.get() + "*_*_AW.xml")

    label4 = ctk.CTkLabel(root, text="Ich habe " + str(len(files)) + " Patienten für Sie gefunden:")  
    label4.grid(row=4, column=1)
    label4.configure(font=ctk.CTkFont(family='Arial', size=12))

    pat_count = 0
    patients = []

    # Tree erstellen
    tree = ttk.Treeview(root)
    tree['columns'] = ("Nummer", "Nachname", "Vorname")
    tree.column("#0", width=0, stretch=NO)
    tree.column("Nummer", width=60, anchor=CENTER)
    tree.column("Nachname", width=200, anchor=W)
    tree.column("Vorname", width=200, anchor=W)

    # Überschriften erstellen
    tree.heading("#0", text="", anchor=CENTER)
    tree.heading("Nummer", text="Nummer", anchor=CENTER)
    tree.heading("Nachname", text="Nachname", anchor=W)
    tree.heading("Vorname", text="Vorname", anchor=W)
       
    tree.grid(row=6, column=1)

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

        # Daten einfügen
        tree.insert(parent= '', index='end', iid=pat_count, values=(pat_count, pat_name[0], pat_name[1]))

    label6 = ctk.CTkLabel(root, text="Bitte geben Sie die Nummer des gewünschten Patienten ein: ")  
    label6.grid(row=7, column=0)
    label6.configure(font=ctk.CTkFont(family='Arial', size=12))
    enter_patientnumber = ctk.CTkEntry(root, width=50)
    enter_patientnumber.grid(row=7, column=1)

    def read_input_field():
        enter_patientnumber.get()
        pat_num = int(enter_patientnumber.get())
        selected_pat = patients[pat_num - 1]

        label7 = ctk.CTkLabel(root, text="PATIENTENAKTE")  
        label7.grid(row=9, column=1)
        label7.configure(font=ctk.CTkFont(family='Arial', size=12))

        xml_tree = parse_xml(selected_pat["file"])
        xml_root = xml_tree.getroot()
        patient_node = xml_root.findall(".//{http://hl7.org/fhir}Patient")
        patient_details = patient_node[0][2][1].text

        textbox = ctk.CTkTextbox(root, width=400, height=150)
        textbox.grid(row=10, column=1)

        for line in patient_details.split("|"):
            textbox.insert('10.0', line.strip() + '\n') # 10.0 sonst steht zuletzt bearbeitet als erstes da

        textbox.configure(state="disabled")

    # OK Button erstellen
    ok_button = ctk.CTkButton(root, text="OK", command=read_input_field)
    ok_button.grid(row=8, column=1)

# Suche Button erstellen
search_button = ctk.CTkButton(root, text="Suche starten", command=read_input_fields)
search_button.grid(row=2, column=1)

root.mainloop()