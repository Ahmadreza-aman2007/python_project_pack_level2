import models,math
def manager_login(username,password):
    models.Manager.login(username=username,password=password)
def register_student():
    while True:
        firstname = input("please enter the student firstname :").strip()
        if not firstname:
            print("please enter a valid name(not empty or just space)")
            continue
        break
    while True:
        lastname = input("please enter the student lastname :").strip()
        if not lastname:
            print("please enter a valid name(not empty or just space)")
            continue
        break
    while True:
        try:
            major_code=int(input("please enter the major(major code) :").strip())
            major_code=str(major_code)
        except ValueError:
            print("please enter a number")
            continue
        if not models.Major.is_exists(major_code):
            print ("this major code doesnt exist.")
            return
        break
    while True:
        national_code=input("please enter the national code :").strip()
        if not national_code.isdigit():
            print ("please enter a valid national code")
            continue
        if models.Student.is_exists(national_code):
            print("this student alreasdy registered")
            return
        break
    student=models.Student(firstname,lastname,major_code,national_code)
    models.DataManager.registeration(student)
def add_major():
    while True:
        major=input("please enter the name of major :").strip()
        if not major:
            print("name cannot be empty or blank")
            continue
        break
    while True: 
        try:
            code=int(input("please enter the major code :").strip())
        except ValueError:
            print("please enter a valid number")
            continue
        code=str(code)
        break
    models.DataManager.registeration(models.Major(major,code))

register_student()