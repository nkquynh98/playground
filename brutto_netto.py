import requests
import pickle
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time

"""
Calculate the brutto and netto salary in Germany based on the website SteuerGo
If you want to update the data, please set the USE_CACHED to be False
"""
MAX_SALARY_PER_YEAR = 100000
STEP = 1000
SLEEP_TIME = 0.001
TAX_LEVEL = [1,3,5]
PER_YEAR = False
BRUTTO = []
NETTO_RATE_1 = []
NETTO_RATE_3 = []
NETTO_RATE_5 = []
USE_CACHED = True

#For Couple salary, COUPLE = False will show the graph for an individual person
COUPLE = True
husband_salary = 10000


def get_netto_salary(brutto=10000, tax_level=1):
    URL = 'https://www.steuergo.de/en/rechner/brutto_netto_rechner?jahr=2022&submit=1'
    send_data = {
        "lohn": 1,
        "lohnbetrag": brutto,
        "geburtsjahr_auswahl": 4,
        "steuerklasse": tax_level,
        "faktor": 1.000,
        "kinder": 0,
        "kirchensteuerpflicht": 2,
        "bundesland": "BW",
        "rentenversicherung": 1,
        "krankenversicherung": 0,
        "KVgesetzlichZusatzbeitrag2014": "0,00",
        "KVgesetzlichZusatzbeitrag": "1,00",
        "KVprivatBeitrag":"0,00",
        "pflegeversicherung": 1
    }
    x = requests.post(URL, data = send_data)
    soup = BeautifulSoup(x.text, "lxml")
    # money = []
    # for i in soup.findAll("td",attrs={"class":"spalte_3 text-right"}):
    #     if i.span.text=="Year":
    #         if i.b is not None:
    #             print(float(i.b.text[:-2].replace(".","").replace(",",".")))

    net_salary = soup.findAll("td",text="Net salary:")[0].parent
    net_salary_per_year = net_salary.findAll("span", text="Year")[0].parent
    netto= float(net_salary_per_year.b.text[:-2].replace(".","").replace(",","."))
    # print(tax_level)
    # print(brutto)
    # print(netto)
    return netto
    # for x in i.descendants:
    #     print(x)


if USE_CACHED:
    with open("brutto.pickle","rb") as f:
        BRUTTO = pickle.load(f)
    with open("netto_1.pickle","rb") as f:
        NETTO_RATE_1 = pickle.load(f)
    with open("netto_3.pickle","rb") as f:
        NETTO_RATE_3 = pickle.load(f)
    with open("netto_5.pickle","rb") as f:
        NETTO_RATE_5 = pickle.load(f)        

else:
    salary_per_year = 0
    while salary_per_year<=MAX_SALARY_PER_YEAR:
        BRUTTO.append(salary_per_year)
        print(salary_per_year)
        NETTO_RATE_1.append(get_netto_salary(brutto=salary_per_year,tax_level=1))
        time.sleep(SLEEP_TIME)
        NETTO_RATE_3.append(get_netto_salary(brutto=salary_per_year,tax_level=3))
        time.sleep(SLEEP_TIME)
        NETTO_RATE_5.append(get_netto_salary(brutto=salary_per_year,tax_level=5))
        time.sleep(SLEEP_TIME)
        salary_per_year+=STEP
    with open("brutto.pickle","wb") as f:
        pickle.dump(BRUTTO,f)
    with open("netto_1.pickle","wb") as f:
        pickle.dump(NETTO_RATE_1,f)
    with open("netto_3.pickle","wb") as f:
        pickle.dump(NETTO_RATE_3,f)
    with open("netto_5.pickle","wb") as f:
        pickle.dump(NETTO_RATE_5,f) 
if not COUPLE:
    if PER_YEAR:
        div = 1
    else:
        div = 12
    BRUTTO = np.array(BRUTTO)/div
    NETTO_RATE_1 = np.array(NETTO_RATE_1)/div
    NETTO_RATE_3 = np.array(NETTO_RATE_3)/div
    NETTO_RATE_5 = np.array(NETTO_RATE_5)/div
    plt.plot(BRUTTO, NETTO_RATE_1, "-b", label="Tax class 1")
    plt.plot(BRUTTO, NETTO_RATE_3, "-g", label="Tax class 3")
    plt.plot(BRUTTO, NETTO_RATE_5, "-r", label="Tax class 5")
    plt.legend(loc="upper left")
    plt.title("Netto/Brutto over different tax class")
    plt.xlabel("BRUTTO (euro)")
    plt.ylabel("NETTO (euro)")
    plt.show()
else:
    index = BRUTTO.index(husband_salary)
    husband_net_1 = NETTO_RATE_1[index]
    husband_net_3 = NETTO_RATE_3[index]
    husband_net_5 = NETTO_RATE_5[index]
    WIFE_BRUTTO = np.array(BRUTTO)
    TOTAL_NETTO_44 = np.array(NETTO_RATE_1)+husband_net_1
    TOTAL_NETTO_35 = np.array(NETTO_RATE_5)+husband_net_3
    TOTAL_NETTO_53 = np.array(NETTO_RATE_3)+husband_net_5
    plt.plot(WIFE_BRUTTO, TOTAL_NETTO_44, "-b", label="Tax class husband/wife: 4/4")
    plt.plot(WIFE_BRUTTO, TOTAL_NETTO_35, "-g", label="Tax class husband/wife: 3/5")
    plt.plot(WIFE_BRUTTO, TOTAL_NETTO_53, "-r", label="Tax class husband/wife: 5/3")
    plt.legend(loc="upper left")
    plt.title("Total Netto of a couple (wife and husband) based on wife salary, in case husband salary is {} euro per year".format(husband_salary))
    plt.xlabel("WIFE BRUTTO SALARY (euro)")
    plt.ylabel("TOTAL NETTO PER YEAR OF THE COUPLE(euro)")
    plt.show()    
#print(soup.prettify())
#print(x.text)