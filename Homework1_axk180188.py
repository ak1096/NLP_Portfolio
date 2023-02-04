# Homework 1
# Anushka Karthikeyan
# AXK180188

import sys
import pathlib
import re
import pickle


# Define Person Class
class Person:
    """
    A class representing a person.
    Attributes:
        last :
            last name of the person
        first : str
            first name of the person
        mi : str
            middle name of the person
        id: str
            employee id of the person
        phone: str
            phone number of the person
    """

    def __init__(self, last, first, mi, id, phone):
        """ Constructs attributes for person. """
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        """ displays person object attributes  """
        print(f'Employee id: {self.id}\n\t{self.first} {self.mi} {self.last}\n\t{self.phone}')


# function to process input file
def process_lines(text):
    """
      Processes strings to break down employee information
      Args:
        text: A list of strings containing employee information
      Returns:
        Dictionary of Person Objects
      """

    # dictionary to hold person objects for each employee
    emp_dict = {}

    # iterate through each employee to ensure info is correct
    for t in text:
        # split on comma to get fields as text variables
        emp = t.split(',')

        # ensure last and first name are capitalized
        emp[0] = emp[0].capitalize()
        emp[1] = emp[1].capitalize()

        # modify middle initial to be single upper case
        if emp[2] == '':
            emp[2] == 'X'
        emp[2] = emp[2].capitalize()

        # modify and check id with regex
        id_check = bool(re.search('[a-zA-z]{2}[0-9]{4}', emp[3]))
        while not id_check:
            print('ID invalid: ' + emp[3])
            print('ID is two letters followed by 4 digits')
            emp[3] = input('Please enter a valid id: ')
            id_check = bool(re.search('[a-zA-z]{2}[0-9]{4}', emp[3]))

        # modify and check phone number with regex
        phone_check = bool(re.search('(\d{1,3})?[-. ]*(\d{1,3})?[-. ]*(\d{1,3})', emp[4]))
        while not phone_check:
            print('Phone ' + emp[4] + ' is invalid')
            print('Enter phone number in form 123-456-7890')
            emp[4] = input("Enter phone number: ")
            phone_check = bool(re.search('(\d{1,3})?[-. ]*(\d{1,3})?[-. ]*(\d{1,3})', emp[4]))

        # create Person object
        person = Person(emp[0], emp[1], emp[2], emp[3], emp[4])

        # check for duplicate ID
        if emp[3] in emp_dict:
            print('An ID is repeated in the input file')
        emp_dict[emp[3]] = person

    return emp_dict


# main function to read file, send to process_lines and save dictionary as pickle file
if __name__ == '__main__':
    # sysarg for 'data/data.csv'
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    # read in file
    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read().splitlines()

    # process the text to be standarized
    employees = process_lines(text_in[1:])  # will ignore header

    # pickle employees:
    pickle.dump(employees, open('employees.pickle', 'wb'))

    # read the pickle back in
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    # output employees
    print('\n\nEmployee List:')

    for emp_id in employees_in.keys():
        employees_in[emp_id].display()
