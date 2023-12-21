# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:17:19 2023

@author: Administrator
"""
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Reading excel or xlsx files
data = pd.read_excel("articles.xlsx")

# Summary of the data
data.describe()

# Summary of columns
data.info()

# Counting the  number of articles per source
# Format:  dataframe.groupby(['column_to_group'])['column_to_count'].count()
data.groupby(['source_id'])['article_id'].count()
 
# source_id
# 1                             0
# abc-news                   1139
# al-jazeera-english          499
# bbc-news                   1242
# business-insider           1048
# cbs-news                    952
# cnn                        1132
# espn                         82
# newsweek                    539
# reuters                    1252
# the-irish-times            1232
# the-new-york-times          986
# the-wall-street-journal     333

# number of reactions by publisher
data.groupby(['source_id'])['engagement_reaction_count'].sum()

# source_id
# 1                                0.0
# abc-news                    343779.0
# al-jazeera-english          140410.0
# bbc-news                    545396.0
# business-insider            216545.0
# cbs-news                    459741.0
# cnn                        1218206.0
# espn                             0.0
# newsweek                     93167.0
# reuters                      16963.0
# the-irish-times              26838.0
# the-new-york-times          790449.0
# the-wall-street-journal      84124.0

# Dropping a column
data = data.drop(['engagement_comment_plugin_count'], axis = 1)

# # Creating a keyword flag
keyword = 'crash' 

# Lets create a for loop to isolate the title row
# length = len(data['title'])

# keyword_flag = []
# for x in range (0, length):
#     heading = data['title'][x]
#     if keyword in heading:
#         flag = 1
#     else:
#         flag = 0
#     keyword_flag.append(flag)

#Creating a function
def keywordflag(keyword):
    length = len(data['title'])
    keyword_flag = []
    for x in range (0, length):
        heading = data['title'][x]
        try:
            if keyword in heading:
                flag = 1
            else:
                flag = 0
        except:
            flag = 0
        keyword_flag.append(flag)
    return keyword_flag

keywordflag = keywordflag('murder')

# Craeting a newcolumn in data dataframe

data['keyword_flag'] = pd.Series(keywordflag)

# SentimentIntensityAnalyzer
sent_int = SentimentIntensityAnalyzer()

text = data['title'][16]
sent = sent_int.polarity_scores(text)

neg = sent['neg']
pos = sent['pos']
neu = sent['neu']

# Adding a for loop to extract sentiment per title

title_neg_sentiment = []
title_pos_sentiment = []
title_neu_sentiment = []

length = len(data)

for x in range (0, length):
    try:
        text = data['title'][x]
        sent_int = SentimentIntensityAnalyzer()
        sent = sent_int.polarity_scores(text)
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except:
        neg = 0
        pos = 0
        neu = 0
    title_neg_sentiment.append(neg)
    title_pos_sentiment.append(pos)
    title_neu_sentiment.append(neu)

title_neg_sentiment = pd.Series(title_neg_sentiment)
title_pos_sentiment = pd.Series(title_pos_sentiment)
title_neu_sentiment = pd.Series(title_neu_sentiment)

data['title_neg_sentiment'] = title_neg_sentiment
data['title_pos_sentiment'] = title_pos_sentiment
data['title_neu_sentiment'] = title_neu_sentiment

# Writing the data
data.to_excel('blogme_clean.xlsx', sheet_name = 'blogmedata', index = False)
