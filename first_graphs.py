# -*- coding: utf-8 -*-
"""This code makes 2 plots of Amount of males and females and Mean alchohol
 consumation in weekends"""
import pandas
import matplotlib.pyplot as plt

c = ['red', 'blue']

dataframe = pandas.read_csv('data/Maths.csv')
a = dataframe["sex"].value_counts()

plt.bar(a.keys(), a, color = c)
plt.title("Amount of males and females")
plt.show()
plt.bar(dataframe['sex'].unique() ,
        list(dataframe.loc[dataframe['sex']==x].mean()["Walc"]
                                        for x in dataframe['sex'].unique()),
        color = c)
plt.title("Mean consumption of alchohol in weekend")
plt.show()
