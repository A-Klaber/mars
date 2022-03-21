#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
from urllib.request import urlopen

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser) 
    hemispheres = mars_hemispheres(browser)
# Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=3)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # news_title

    # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
        # news_p

    except AttributeError:
        return None, None

    return news_title, news_paragraph


# ### Featured Images

def featured_image(browser):

# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

# Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel

    except AttributeError:
        return None

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
    # Use the base URL to create an absolute URL

        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return  df.to_html()

def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    page = urlopen("https://marshemispheres.com/")
    soups = soup(page, "html.parser")


    # In[ ]:


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    city_list = len(soups.find_all( "img", class_="thumb" ))
    for i in range(city_list):
        try:
            #create empty dictionary
            hemispheres = {}
            browser.find_by_css('a.product-item h3')[i].click()
            element = browser.find_link_by_text('Sample').first
            img_url = element['href']
            title = browser.find_by_css("h2.title").text
            hemispheres["img_url"] = img_url
            hemispheres["title"] = title
            hemisphere_image_urls.append(hemispheres)
            browser.back()
        except:
            break
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())   




