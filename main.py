# Program realizujący wymianę kluczy przy użyciu algorytmu Diffie'go Hellmana
# oraz biblioteki do wysyłania wiadomości email.
import csv
import smtplib
import getpass
from random import randrange
from email.mime.text import MIMEText
from email.utils import formataddr



def menuWybierzA(p):
    y = int(input("1 - Podaj liczbę A\n2 - Generuj liczbę A\n3 - Wczytaj z pliku\n"))
    if y == 1:
        liczbaA = int(input("Wpisz liczbę: "))
        menuZapis(liczbaA)
        return liczbaA
    elif y == 2:
        liczbaA = genA(p)
        print("Wygenerowana liczba A to: ", liczbaA)
        menuZapis(liczbaA)
        return liczbaA
    elif y == 3:
        liczbaA = wczytaj()
        liczbaA = int(liczbaA[0])
        return liczbaA


def menuWczytajKlucz():
    y = int(input("1 - Podaj klucz A\n3 - Wczytaj z pliku\n"))
    if y == 1:
        klucz = int(input("Wpisz klucz: "))
        menuZapis(klucz)
        return klucz
    elif y == 2:
        klucz = wczytaj()
        klucz = int(klucz[0])
        return klucz


def menuZapis(x):
    z = int(input("1 - Zapisz do pliku\n2 - Wróć do Menu\n"))
    if z == 1:
        zapiszDoCsv(x)
    else:
        pass


def wczytajPG():
    reader = csv.reader(
        open('liczby.csv', 'r'),
        delimiter=',',
        quoting=csv.QUOTE_NONE
    )
    liczby = list(reader)
    return liczby[0]


def wczytaj():
    filename = input("Podaj nazwę bez rozszerzenia: ")
    filenamecsv = filename + ".csv"
    reader = csv.reader(
        open(filenamecsv, 'r'),
        delimiter=',',
        quoting=csv.QUOTE_NONE
    )
    liczby = list(reader)
    return liczby[0]


def zapiszDoCsv(x):
    filename = input("Podaj nazwę bez rozszerzenia: ")
    filenamecsv = filename + ".csv"
    with open(filenamecsv, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([x])


def genA(p):
    a = randrange(2, p - 2)
    return a


def genKlucz(g, a, p):
    A = (g ** a) % p
    return A


def wyslijEmail(key):
    gmail_user = str(input('Podaj swój adres Gmail: '))
    gmail_password = getpass.getpass('Podaj hasło gmail: ')
    adresat = str(input('Podaj email odbiorcy: '))
    sent_from = gmail_user
    to = adresat

    klucz = "Klucz to: " + str(key)
    email_text = MIMEText(klucz)
    email_text['From'] = formataddr((str(sent_from), str(sent_from)))
    email_text['To'] = formataddr((str(adresat), str(adresat)))
    email_text['Subject'] = 'Klucz publiczny'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text.as_string())
        server.close()

        print('Email wysłany!')
    except:
        print('Coś nie tak...')

def main():
    global UnboundLocalError
    try:
        p, g = wczytajPG()
        p = int(p)
        g = int(g)
        liczbaA = 0

    except (FileNotFoundError, IOError):
        print("Błędny plik lub ścieżka")
    x = 0
    while x != 7:
        print("p = %d, g = %d, liczba A = %d" % (p, g, liczbaA))
        x = int(input("Wybierz: \n1 - Wybierz liczbę A\n2 - Wczytaj wiadomość\n"
                      "3 - Generuj wiadomość\n4 - Generuj klucz\n5 - Pokaż klucz\n6 - Wyślij klucz\n"
                      "7 - Zakończ program\n"))

        if x == 1:
            liczbaA = menuWybierzA(p)

        elif x == 2:
            wiadomoscJawna = wczytaj()
            wiadomoscJawna = int(wiadomoscJawna[0])

        elif x == 3:
            wiadomoscJawna = genKlucz(g, liczbaA, p)
            print("Klucz: ", wiadomoscJawna)
            menuZapis(wiadomoscJawna)

        elif x == 4:
            kluczPrywatny = genKlucz(wiadomoscJawna, liczbaA, p)
            print("Klucz: ", kluczPrywatny)
            menuZapis(kluczPrywatny)

        elif x == 5:
            try:
                print("Wiadomość: ", wiadomoscJawna)
                print("Klucz: ", kluczPrywatny)
            except UnboundLocalError:
                print("Nie wygenerowano klucza!")

            z = int(input("1 - Zapisz klucz prywatny\n2 - Zapisz klucz publiczny\n 3 - Wróć do Menu"))
            if z == 1:
                zapiszDoCsv(wiadomoscJawna)
            elif z == 2:
                zapiszDoCsv(kluczPrywatny)
            else:
                pass
        elif x ==6:
            wyslijEmail(wiadomoscJawna)
    exit()


main()
