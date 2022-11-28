from glob import glob
from xml.etree.ElementTree import parse as parse_xml

print("Bitte geben Sie den Nachnamen des Patienten ein")
lastname = input()
print("Bitte geben Sie den Vornamen des Patienten ein")
firstname = input()
print("Ich suche nach " + lastname + ", " + firstname + " ...")

files = glob("./data/Patientenakten/*/" + lastname + "*_" + firstname + "*_*_AW.xml")

print("Ich habe " + str(len(files)) + " Patienten für Sie gefunden:")

pat_count = 0
patients = []

for f in files:
    #f = f.replace("./data/Patientenakten\\", "")
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

    print(pat_count, pat_name[0], pat_name[1])

pat_num = int(input("Bitte geben Sie die Nummer des gewünschten Patienten ein: "))

selected_pat = patients[pat_num - 1]

print("\n\nPATIENTENAKTE")
print("=============")
#print(selected_pat["name"][0] + ", " + selected_pat["name"][1])

tree = parse_xml(selected_pat["file"])
root = tree.getroot()
patient_node = root.findall(".//{http://hl7.org/fhir}Patient")
patient_details = patient_node[0][2][1].text

for line in patient_details.split("|"):
    print(line.strip())
