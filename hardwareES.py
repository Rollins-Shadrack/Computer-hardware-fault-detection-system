import csv
from rapidfuzz import fuzz, process
import tkinter as tk

# Load the dataset from the CSV file
with open('data.csv') as file:
    reader = csv.DictReader(file)
    dataset = [row for row in reader]

# Create a list of faults based on the dataset
faults = [row['fault'].lower() for row in dataset]

# Create a list of rules based on the dataset
rules = []
for row in dataset:
    rule = {
        'symptoms': [row['cpu_ram'].lower(), row['hard_disk_drive'].lower(), row['display'].lower()],
        'diagnosis': row['diagnosis'].lower(),
        'recommendation': row['recommendations'].lower()
    }
    rules.append(rule)



# Define a function to find the best match for a given fault
def find_best_match(fault):
    best_ratio = 0
    best_match = None
    for f in faults:
        # Calculate similarity ratio using fuzz.ratio
        ratio = fuzz.ratio(f, fault)
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = f
    if best_match:
        return best_match
    else:
        # If no best match is found, use rapidfuzz's process.extractOne method to find the closest match
        best_match = process.extractOne(fault, faults)
        return best_match[0] if best_match else None


# Define a function to diagnose the problem based on the symptoms
def diagnose_problem(symptoms):
    # Initialize the diagnoses and recommendations lists to empty
    diagnoses = []
    # recommendations = []
    # Loop through the rules and check if any of them match the symptoms
    for rule in rules:
        if all(symptom.lower() in rule['symptoms'] for symptom in symptoms):
            diagnoses.append(rule['diagnosis'])

    # If diagnoses were found, return the list of recommended solutions
    if diagnoses:
        return diagnoses
    else:
        return None
def diagnose():
    # Ask the user if they know which hardware has an issue
    knows_issue = issue_entry.get()

    if knows_issue.lower() == 'yes':
        # If the user knows which hardware has an issue, ask for details about each component
        cpu_ram = cpu_ram_entry.get()
        hard_disk_drive = hard_disk_drive_entry.get()
        display = display_entry.get()

        # Diagnose the problem based on the symptoms entered by the user
        symptoms = [cpu_ram.lower(), hard_disk_drive.lower(), display.lower()]
        diagnoses = diagnose_problem(symptoms)
        # If no diagnoses were found, try to find a matching fault and diagnose based on that
        if not diagnoses:
            fault = ' '.join(symptoms)
            matches = find_best_match(fault)
            if matches:
                diagnoses = [row['diagnosis'] for row in dataset if row['fault'] in matches]

        # Display the diagnosis in the GUI
        if diagnoses:
            diagnosis_text.set('Diagnosis: ' + ', '.join(diagnoses))
        else:
            diagnosis_text.set('Sorry, we could not diagnose the problem.')
            recommendation_text.set('')

    elif knows_issue.lower() == 'no':
        # If the user doesn't know which hardware has an issue, ask for a description of the problem
        fault = fault_entry.get()
        # Find the diagnoses based on the fault entered by the user
        best_match = find_best_match(fault)
        if best_match:
            fault = best_match
        diagnoses = []
        recommendations = []
        for row in dataset:
            if row['fault'].lower() == fault.lower():
                diagnoses.append(row['diagnosis'])
                recommendations.append(row['recommendations'])

        # Display the diagnosis in the GUI
        if diagnoses:
            diagnosis_text.set('Diagnosis: ' + ', '.join(diagnoses))
            recommendation_text.set('Recommendation: ' + ', '.join(recommendations))
        else:
            diagnosis_text.set('Sorry, we could not diagnose the problem.')
            recommendation_text.set('')


# Create the GUI window
root = tk.Tk()
root.title('Fault Diagnosis Tool')

# Create the welcome label
welcome_label = tk.Label(root, text='Welcome to hardware faults detection expert system')
welcome_label.pack(padx=5, pady=10)


# Create the input box for knowing which hardware has an issue
issue_label = tk.Label(root, text='Do you know which computer hardware has a problem ? (Yes/No):')
issue_entry = tk.Entry(root, width=50)
issue_label.pack()
issue_entry.pack()

def validate_input():
    # Get the input from the issue_entry box
    knows_issue = issue_entry.get()

    # Check if the input is either "yes" or "no"
    if knows_issue.lower() == 'yes':
        show_symptoms()
    elif knows_issue.lower() == 'no':
        show_fault()
    else:
        # If input is not "yes" or "no", display an error message
        diagnosis_text.set('Invalid input. Please enter "yes" or "no".')

# Create the 'Continue' button to proceed with diagnosis
continue_button = tk.Button(root, text='Continue', command=validate_input)
continue_button.pack(padx=5, pady=6)

# Create the input boxes for symptoms
cpu_ram_label = tk.Label(root, text='CPU/RAM [problem/OK]:')
cpu_ram_entry = tk.Entry(root, width=50)

hard_disk_drive_label = tk.Label(root, text='Hard Disk Drive [problem/OK]:')
hard_disk_drive_entry = tk.Entry(root, width=50)

display_label = tk.Label(root, text='Display [problem/OK]:')
display_entry = tk.Entry(root, width=50)

# Create the input box for fault description
fault_label = tk.Label(root, text='Please describe the problem :')
fault_entry = tk.Entry(root, width=50)

# Create the 'Diagnose' button
diagnose_button = tk.Button(root, text='Diagnose', command=diagnose)

# Create the label for diagnosis
diagnosis_text = tk.StringVar()
diagnosis_label = tk.Label(root, textvariable=diagnosis_text)
diagnosis_label.pack()

# Create a StringVar to store the recommendation text
recommendation_text = tk.StringVar()

# Create a label to display the recommendation text
recommendation_label = tk.Label(root, textvariable=recommendation_text)
recommendation_label.pack(padx=5, pady=10)

def show_symptoms():
    # Get the input from the user
    cpu_ram = cpu_ram_entry.get()
    hard_disk_drive = hard_disk_drive_entry.get()
    display = display_entry.get()
    # Remove the 'Do you know what the problem is?' input box and 'Continue' button
    issue_label.pack_forget()
    issue_entry.pack_forget()
    continue_button.pack_forget()

    # Display the input boxes for symptoms and 'Diagnose' button
    cpu_ram_label.pack()
    cpu_ram_entry.pack()
    hard_disk_drive_label.pack()
    hard_disk_drive_entry.pack()
    display_label.pack()
    display_entry.pack()
    diagnose_button.pack()

def show_fault():
    # Remove the 'Do you know what the problem is?' input box and 'Continue' button
    issue_label.pack_forget()
    issue_entry.pack_forget()
    continue_button.pack_forget()

    # Display the input box for fault description and 'Diagnose' button
    fault_label.pack()
    fault_entry.pack()
    diagnose_button.pack()


# Start the GUI
root.mainloop()

