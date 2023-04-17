import os
import smtplib
from email.mime.text import MIMEText

dict_list = []

filepath = "./file.txt"
()


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


def zapiszDoPliku():
    wynik = ""
    for element in dict_list:
        wynik += element["imie"] + " " + element["nazwisko"] + " " + element["email"] + " " + str(
            element["punkty"]) + " " + str(element["ocena"]) + " " + element["status"] + "\n"
    with open(filepath, "w") as file_object:
        file_object.write(wynik)


def wystawOcene(punkty):
    ocena = 0
    if punkty <= 50:
        ocena = 2
    if punkty > 50 and punkty <= 60:
        ocena = 3
    if punkty > 60 and punkty <= 70:
        ocena = 3.5
    if punkty > 70 and punkty <= 80:
        ocena = 4
    if punkty > 80 and punkty <= 90:
        ocena = 4.5
    if punkty > 90 and punkty <= 100:
        ocena = 5
    return ocena


with open(filepath) as file_object:
    for line in file_object:
        linia = line.rstrip().split(" ")
        students = {}
        students["imie"] = linia[0]
        students["nazwisko"] = linia[1]
        students["email"] = linia[2]
        students["punkty"] = linia[3]
        if (len(linia) == 4):
            students["ocena"] = wystawOcene(int(linia[3]))
            students["status"] = ""
        if (len(linia) == 5):
            if (linia[4] == "GRADED" or linia[4] == "MAILED"):
                students["ocena"] = wystawOcene(int(linia[3]))
                students["status"] = linia[4]
            if linia[4] == "2" or linia[4] == "3" or linia[4] == "3.5" or linia[4] == "4" or linia[4] == "4.5" or linia[
                4] == "5":
                students["ocena"] = linia[4]
                students["status"] = ""
        if (len(linia) == 6):
            students["ocena"] = linia[4]
            students["status"] = linia[5]
        dict_list.append(students)

wybor = ""
while True:
    os.system("cls")
    index = 0
    for x in dict_list:
        print(str(index) + ". " + str(x))
        index += 1
    print("==============================")
    print("1. Dodaj studenta")
    print("2. Usuń studenta")
    print("3. Wyślij maile")
    print("4. Wyjdź")
    wybor = input("Wybierz funkcję: ")
    match wybor:
        case "1":
            isUnique = True

            students = {}
            students["imie"] = input("Podaj imie: ")
            students["nazwisko"] = input("Podaj nazwisko: ")
            email = input("Podaj email: ")
            for x in dict_list:
                if x["email"] == email:
                    isUnique = False
            while isUnique == False:
                isUnique = True
                print("Podany email już istnieje")
                email = input("Podaj email: ")
                for x in dict_list:
                    if x["email"] == email:
                        isUnique = False
            students["email"] = email
            students["punkty"] = input("Podaj punkty: ")
            students["ocena"] = wystawOcene(int(students["punkty"]))
            students["status"] = ""
            dict_list.append(students)
            zapiszDoPliku()
        case "2":
            index = input("Podaj index rekordu do usunięcia: ")
            if int(index) <= len(dict_list) - 1 and int(index) >= 0:
                dict_list.pop(int(index))
            zapiszDoPliku()
        case "3":
            for element in dict_list:
                if element["status"] != "MAILED":
                    subject = "Ocena z PPY"
                    body = "Ocena z PPY wynosi: " + element["ocena"]
                    sender = "tfd28598@zslsz.com"
                    recipients = element["email"]
                    password = "pswd123"
                    send_email(subject, body, sender, recipients, password)
            zapiszDoPliku()
        case "4":
            zapiszDoPliku()
            break