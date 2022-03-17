import numpy as np
import matplotlib.pyplot as plt

NUMBER_OF_YEAR = 20
SAVING_MONEY_PER_YEAR = 100000000
INTEREST_RATE = 1.2
DIV = 1000000
years = np.arange(NUMBER_OF_YEAR)
total_money_per_year = np.zeros(NUMBER_OF_YEAR)
total_money_per_year_without_interest = np.zeros(NUMBER_OF_YEAR)
current_year = SAVING_MONEY_PER_YEAR
for year in years:
    total_money_per_year[year] = current_year
    total_money_per_year_without_interest[year] = SAVING_MONEY_PER_YEAR*(year+1) 
    current_year = INTEREST_RATE*current_year+SAVING_MONEY_PER_YEAR

plt.plot(years, total_money_per_year/DIV, "-b", label="With interest")
plt.plot(years, total_money_per_year_without_interest/DIV, "-g", label="Without interest")
plt.plot(years, (total_money_per_year-total_money_per_year_without_interest)/DIV, "-r", label="Difference")
plt.legend(loc="upper left")
plt.title("Save {} VND each year with interest rate {:.2f} % per year in {} years".format(format(SAVING_MONEY_PER_YEAR,","), (INTEREST_RATE-1)*100, NUMBER_OF_YEAR))
plt.xlabel("Year")
plt.ylabel("Total Money (Million VND)")
plt.show()
