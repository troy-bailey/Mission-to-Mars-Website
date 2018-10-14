##########################
## Imports
##########################

# Import BeautifulSoup
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import pymongo
import re

# Import Splinter and set the chromedriver path
from splinter import Browser
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

##############################################################
### Function to Scrape Mars Mission Data from various websites
##############################################################

def scrape():

    ############################
    ### Get NASA Mars News
    ############################

    # URL of page to be scraped into soup
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the title for the first article
    results = soup.find('div', class_="content_title")
    news_title = results.text.strip()
    # print(news_title)

    # Retrieve the lede for the first article
    results = soup.find('div', class_="article_teaser_body")
    news_p = results.text.strip()
    # print(news_p)

    ################################
    ## Get JPL's Featured Mars Image
    ################################

    # URL of page to be scraped into soup
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_base = 'https://www.jpl.nasa.gov'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    style = soup.find('article')['style']
    urls = re.findall('url\((.*?)\)', style)
    url_f = urls[0]
    url_f = url_f[1:-1]
    featured_image_url = url_base + url_f
    # print(featured_image_url)

    #################################
    ## Get Latest Mars Weather Report
    #################################

    # URL of page to be scraped into soup
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Get all the tweets then loop through to find the latest tweet that includes a weather report
    results = soup.find_all('div', class_="js-tweet-text-container")
    for result in results:
        mars_weather = result.text.strip()
        if mars_weather[0:4]== "Sol ":
            break
    # print(mars_weather)

    #################################
    ## Get Table of Mars Facts
    #################################

    # url of page with table of Mars facts
    url = 'https://space-facts.com/mars/'

    # use pandas to pull table(s) into dataframe
    tables = pd.read_html(url)

    # we want the first table
    mars_table = tables[0]

    # reset index, convert to html, and remove spaces
    # mars_table.set_index(0, inplace=True)
    mars_html_table = mars_table.to_html(header=False, index=False)
    mars_html_table = mars_html_table.replace('\n', '')
    # print(mars_html_table)

    #################################
    ## Get Photos of Mars Hemispheres
    #################################

    # url with high res images of Mar's 4 hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # beginning of url to be appended to local reference hrefs
    url_base = "https://astrogeology.usgs.gov"

    # dictionary to hold image data
    hemisphere_images_urls =[]

    # visit url and scrape into soup
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the "item" divisions that hold the image links
    results = soup.find_all('div', class_="item")

    # loop through the items and extract title and url and append to dictionary
    for result in results:
        # the only h3 in the division holds the title
        desc = result.find('h3').text
        # remove the last 9 charaters to cut the word "Extended"
        desc =desc[:-9]

        # get the href to the page with hi res image and build the full url
        anchor = result.find('a')
        anchor_link = anchor.get('href')
        url = url_base+anchor_link

        # visit the url and scrape into soup
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # find the downloads div and pull the href from the hires imnage anchor
        htm = soup.find('div', class_='downloads')
        htm_li = htm.find('li')
        htm_li_a = htm_li.find('a')
        image_link = htm_li_a.get('href')

        # add the title and image url to the dictionary
        hemisphere_images_urls.append({"title": desc, "img_url": image_link})
        
    # print(hemisphere_images_urls)

    ################################################
    ## create a python dictionary with all mars data
    ################################################

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_html_table': mars_html_table,
        'hemisphere_images_urls': hemisphere_images_urls
    }

    return (mars_data)

# print(scrape())

