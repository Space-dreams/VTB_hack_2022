import feedparser
import csv
import pandas as pd
import re

from rss_channels_for_accountants import *
from rss_chanels_for_lawyers import *
from rss_chanels_for_personal import *


def check_url(rss_channel_url): 
    return feedparser.parse(rss_channel_url)


def getHeadlines(rss_channel_url): 
    return [item_of_news['title'] for item_of_news in (check_url(rss_channel_url))['items']]


def getDescriptions(rss_channel_url): 
    return [item_of_news['description'] for item_of_news in (check_url(rss_channel_url))['items']]


def getLinks(rss_channel_url):
    return [item_of_news['link'] for item_of_news in (check_url(rss_channel_url))['items']]


def getDates(rss_channel_url):
    return [item_of_news['published'] for item_of_news in (check_url(rss_channel_url))['items']]


all_head_lines = []
all_descriptions = []
all_links = []
all_dates = []

def extends_url(rss_channels):
    for key, url in rss_channels.items():
        all_head_lines.extend(getHeadlines(url))
        all_descriptions.extend(getDescriptions(url))
        all_links.extend(getLinks(url))
        all_dates.extend(getDates(url))


def write_all_news(all_news_filepath):
    header = ['Title', 'Description', 'Links', 'Publication Date']

    with open(all_news_filepath, 'w', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(i for i in header)
        for a, b, c, d in zip(all_head_lines, all_descriptions, all_links, all_dates):
            writer.writerow((a, b, c, d))

        df = pd.read_csv(all_news_filepath)
    return df


def looking_for_certain_news(all_news_filepath, certain_news_filepath, target1, target2):
    df = pd.read_csv(all_news_filepath)
    result = df.apply(lambda x: x.str.contains(target1, na=False, flags=re.IGNORECASE, regex=True)).any(axis=1)
    result2 = df.apply(lambda x: x.str.contains(target2, na=False, flags=re.IGNORECASE, regex=True)).any(axis=1)
    new_df = df[result & result2]
    new_df.to_csv(certain_news_filepath, sep='\t', encoding='utf-8-sig')

    return new_df

# парсер всех новостей для юристов
# extends_url(rss_chanels_for_lawyers)
# write_all_news(all_news_law)


# # парсер всех новостей для кадровиков
# extends_url(rss_chanels_for_personal)
# write_all_news(all_news_pers)


# # парсер всех новостей для бухгалтеров
# extends_url(rss_channels_for_accountants)
# write_all_news(all_news_acc)


# парсер новостей по таргетам для юристов
extends_url(rss_chanels_for_lawyers)
vector1, vector2 = targets_law
looking_for_certain_news(all_news_law, certain_news_law, vector1, vector2)


# # парсер новостей по таргетам для кадровиков
extends_url(rss_chanels_for_personal)
vector1, vector2 = targets_pers
looking_for_certain_news(all_news_pers, certain_news_pers, vector1, vector2)


# парсер новостей по таргетам для бухгалтеров
extends_url(rss_channels_for_accountants)
vector1, vector2 = targets_acc
looking_for_certain_news(all_news_acc, certain_news_acc, vector1, vector2)
