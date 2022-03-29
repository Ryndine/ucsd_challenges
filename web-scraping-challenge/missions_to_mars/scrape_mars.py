# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict={}

    # Mars news site
    url_mars_news = 'https://redplanetscience.com/'
    browser.visit(url_mars_news)
    html = browser.html
    soup_news = bs(html, 'html.parser')

    # Latest news title and paragraph
    news_title = soup_news.find_all('div', class_='content_title')[0].text
    news_paragraph = soup_news.find_all('div', class_='article_teaser_body')[0].text

    # Jpl image site
    jpl_image_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_image_url)
    html = browser.html
    soup_images = bs(html, 'html.parser')

    # Find the featured image
    relative_image_path = soup_images.find_all('img')[1]["src"]
    featured_image_url = jpl_image_url + relative_image_path

    # Mars facts site
    mars_facts_url ='https://galaxyfacts-mars.com/'
    facts_table = pd.read_html(mars_facts_url)
    facts_df = facts_table[0]
    facts_df = facts_df.rename(columns={0:'Description', 1:'Mars', 2:'Earth'})
    facts_df.set_index("Description", inplace=True)
    
    facts_df_table = facts_df.to_html()
    facts_df_table.replace('\n', '')

    # Scrape mars hemisphere title and image
    hemisphere_site = 'https://marshemispheres.com/'
    browser.visit(hemisphere_site)
    html = browser.html
    soup_hems = bs(html,'html.parser')
   
    # Hhemispheres item
    mars_hemispheres = soup_hems.find('div',class_='collapsible results')
    mars_class_item = mars_hemispheres.find_all('div',class_='item')
    hemisphere_image_urls = []
   
    # Loop each hemisphere
    for item in mars_class_item:
        try:
            # Title
            hemisphere = item.find('div',class_='description')
            title = hemisphere.h3.text
            # Image
            hems_url = hemisphere.a['href']
            browser.visit(hemisphere_site + hems_url)
            html = browser.html
            soup = bs(html,'html.parser')
            relative_image = soup.find('li').a['href']
            image_url = hemisphere_site + relative_image
            if (title and relative_image):
                print(title)
                print(image_url)
            # Title & url dict
            hemisphere_dict={
                'title':title,
                'image_url':image_url
            }
            hemisphere_image_urls.append(hemisphere_dict)

        except Exception as e:
            print(e)

    # Create dictionary for all info scraped from sources above
    mars_dict = {
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image_url":featured_image_url,
        "facts_df_table":facts_df_table,
        "hemisphere_image_urls":hemisphere_image_urls
        }

    browser.quit()
    return mars_dict