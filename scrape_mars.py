import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape():
    url = "https://mars.nasa.gov/news/"
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    response = requests.get(url)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find(class_='content_title').find('a').text

    news_p = soup.find(class_='article_teaser_body').text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    response = requests.get(url)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image = soup.find(class_='button fancybox')['data-fancybox-href']
    image_link = 'https://www.jpl.nasa.gov' + featured_image

    url ='https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find(class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    url='https://space-facts.com/mars/'
    tables = pd.read_html(url)

    df=tables[0]
    df.columns = ['Title', 'Fact']

    data_table = df.to_html()

    data_table.replace('\n', '')

    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    hemis = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']

    images_urls = []

    for item in hemis:
        hemisphere_image_urls = {}
        browser.click_link_by_partial_text(item)
        html = browser.html
        soup = bs(html, 'html.parser')
        hemisphere_image_urls['img_url'] = soup.find(class_='downloads').find('a')['href']
        hemisphere_image_urls['title'] = item
        url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        images_urls.append(hemisphere_image_urls)
    
    results = {'mars_news_title':news_title,
              'mars_news_text':news_p,
              'mars_featured_image':featured_image,
              'featured_image_link':image_link,
              'weather':mars_weather,
              'table':data_table,
              'hemisphere data':images_urls
              }
    return results