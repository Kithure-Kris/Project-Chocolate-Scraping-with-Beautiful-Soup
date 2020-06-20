import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import re

webpage_request = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html')
webpage = webpage_request.content
soup = BeautifulSoup(webpage, 'html.parser')

#How many terrible chocolate bars are out there? And how many earned a perfect 5?

all_ratings = soup.find_all(attrs = {'class':'Rating'})
ratings = []
for rating in all_ratings[1:]:
  ratings.append(float(rating.get_text()))

#Plotting a Histogram of the ratings values:
plt.hist(ratings)
plt.xlabel('Rating')
plt.ylabel('No. of ratings')
plt.title('Histogram of ratings')
plt.show()

#Which chocolatier makes the best chocolate?
companies = soup.find_all(attrs ={'class':'Company'})
company_names = []
for company in companies[1:]:
  company_names.append(company.get_text())

#print(company_names)

#Creating a dataframe with 'company_names' and 'ratings' columns
cols = {'Company':company_names, 'Ratings':ratings}
cacao_ratings = pd.DataFrame.from_dict(cols)
print(cacao_ratings.head())

#Grouping the data by company and taking the average of the grouped ratings
mean_ratings = cacao_ratings.groupby('Company').Ratings.mean()
ten_best = mean_ratings.nlargest(10)
#print(ten_best)

#Is more cacao better?
cocoa_percent = soup.find_all(attrs = {'class':'CocoaPercent'})
cocoa_amount = []
for cocoa in cocoa_percent[1:]:
  cocoa_amount.append(cocoa.get_text())
#OR
#cocoa_percents = []
#cocoa_percent_tags = soup.select(".CocoaPercent")

#Clean, then convert to int/float
cocoa_amount = [float(amount[:-1]) for amount in cocoa_amount]
print(cocoa_amount)
#OR
#for td in cocoa_percent_tags[1:]:
 # percent = int(td.get_text().strip('%'))
  #cocoa_percents.append(percent)

#Add the cocoa percentages as a column in the cacao_ratings dataframe
cols = {'Company':company_names, 'Ratings':ratings, 'CocoaPercentage':cocoa_amount}
cacao_ratings = pd.DataFrame.from_dict(cols)
print(cacao_ratings.head())

#Plotting a scatterplot
plt.clf()
plt.scatter(cacao_ratings.CocoaPercentage, cacao_ratings.Ratings)
plt.xlabel('Cocoa Percentage')
plt.ylabel('Rating')
plt.title('Rating vs Percentage of Cocoa')
#Is there any correlation? 
#Plotting a line of best-fit over the scatterplot
z = np.polyfit(cacao_ratings.CocoaPercentage, cacao_ratings.Ratings, 1)
line_function = np.poly1d(z)
plt.plot(cacao_ratings.CocoaPercentage, line_function(cacao_ratings.CocoaPercentage), "r--")
plt.show()

#Where are the best cocoa beans grown? Which countries produce the highest-rated bars?