from glob import glob
from xml.etree.ElementTree import parse as parse_xml
from tkinter.ttk import Treeview, Frame, Scrollbar
from tkinter import NO, W, CENTER, END, NORMAL, DISABLED

import customtkinter as ctk
import os


def search_patients(last_name, first_name):
    global patients
    files = glob("./data/Patientenakten/*/" + last_name + "*_" + first_name + "*_*_AW.xml")
    patients = []

    for f in files:
        pat_name = f.split(os.sep)
        pat_name = pat_name[-1]
        pat_name = pat_name.split("_")
        pat_name = pat_name[0:2]

        patient = {
            "name": pat_name,
            "file": f
        }
        patients.append(patient)


def show_search_results(event):
    global patients, root, results_view, input_name, details_box
    name = input_name.get()
    
    if ',' in name:
        last_name, first_name = name.split(',')
        last_name = last_name.strip()
        first_name = first_name.strip()
    else:
        last_name = name
        first_name = ''
    
    search_patients(last_name, first_name)

    # delete old data
    for i in results_view.get_children():
        results_view.delete(i)

    # insert data
    for pat_count, patient in enumerate(patients, start=1):
        results_view.insert(parent='', index='end', iid=pat_count, 
                            values=(pat_count, patient['name'][0], patient['name'][1]))

    # clear detail box
    details_box.configure(state=NORMAL)
    details_box.delete('1.0', END)

    # insert new content
    details_box.insert('1.0', str(len(patients)) + ' Patienten gefunden')
    details_box.configure(state=DISABLED)


def show_patient_details(event):
    global patients, root, results_view, input_name, details_box
    pat_num = int(results_view.selection()[0])
    selected_pat = patients[pat_num - 1]

    xml_tree = parse_xml(selected_pat["file"])
    xml_root = xml_tree.getroot()
    patient_node = xml_root.findall(".//{http://hl7.org/fhir}Patient")
    patient_details = patient_node[0][2][1].text

    # clear detail box
    details_box.configure(state=NORMAL)
    details_box.delete('1.0', END)

    # insert new content
    for line_number, line in enumerate(patient_details.split("|"), start=1):
        details_box.insert(str(line_number) + '.0' , line.strip() + '\n')

    details_box.configure(state=DISABLED)


def main():
    global patients, root, results_view, input_name, details_box, search_button

    # main window
    root = ctk.CTk()
    root.title("RED-Medical-Dataviewer")
    frame = Frame(root)
    frame.pack(padx=10, pady=10)

    # search
    input_name = ctk.CTkEntry(frame, width=460)
    input_name.grid(row=1, column=0, padx=3, pady=10)
    input_name.bind("<Return>", show_search_results)

    def tab_input_name(event):
        results_view.selection_set(1)
        results_view.focus(1)
    
    input_name.bind("<Tab>", tab_input_name)            
    input_name.focus()
    
    search_button = ctk.CTkButton(frame, text="Patient suchen", width=200, command=show_search_results)
    search_button.grid(row=1, column=1, padx=3, pady=10)
    

    # results
    results_view = Treeview(frame)
    results_view['columns'] = ("Nummer", "Nachname", "Vorname")
    results_view.column("#0", width=0, stretch=NO)
    results_view.column("Nummer", width=60, anchor=CENTER)
    results_view.column("Nachname", width=300, anchor=W)
    results_view.column("Vorname", width=300, anchor=W)
    results_view.heading("#0", text="", anchor=CENTER)
    results_view.heading("Nummer", text="Nummer", anchor=CENTER)
    results_view.heading("Nachname", text="Nachname", anchor=W)
    results_view.heading("Vorname", text="Vorname", anchor=W)       
    results_view.grid(row=2, column=0, columnspan=3, sticky="nws")
    results_view.bind("<Double-1>", show_patient_details)
    results_view.bind("<Return>", show_patient_details)
    results_view.bind("<Tab>", lambda e: input_name.focus())

    result_scrollbar = Scrollbar(frame, orient='vertical', command=results_view.yview)
    result_scrollbar.grid(row=2, column=1, sticky='nes')
    results_view.configure(yscrollcommand=result_scrollbar.set)
    result_scrollbar.configure(command=results_view.yview)

    details_box = ctk.CTkTextbox(frame, height=100)
    details_box.grid(row=3, column=0, sticky='nsew', padx=3, pady=10, columnspan=3)

    root.mainloop()

# run app
main()