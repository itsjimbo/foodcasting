# -*- coding: utf-8 -*-
import sys
import scrapy
import re
import os
import json
from captchaMiddleware.middleware import RETRY_KEY
from urllib.parse import urlparse,parse_qs
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from itertools import product
from string import ascii_lowercase
from scrapy.http import TextResponse
from bs4 import BeautifulSoup
from ..items import ScrapyYelpItem
from ..items import ImageItem
from ..items import ScrapyYelpMenuItems
import pandas as pd
from pandas.io.json import json_normalize
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import json
import os
import requests
from time import time
from multiprocessing.pool import ThreadPool
import tempfile
import subprocess
from os.path import relpath
import numpy as np
import base64
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy.exceptions import IgnoreRequest,CloseSpider
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class YelpSpider(scrapy.Spider):
    name = 'yelp'
    allowed_domains = ['m.yelp.com']
    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')
    # template
    SEARCH_URL = "https://m.yelp.com/search?find_desc={description}&find_loc={location}"
    url_matcher = re.compile('^https:\/\/m\.yelp\.com\/')
    # use same session for all requests
    session = requests.Session()
    #create a webdriver object and set options for headless browsing
    options = webdriver.ChromeOptions()
    options.headless = False
    prefs = {"profile.managed_default_content_settings.images": 1}
    options.add_experimental_option("prefs", prefs)
    print("Found chromedriver {}",chromedriver_binary.chromedriver_filename)
    browser = webdriver.Chrome(chromedriver_binary.chromedriver_filename,options=options)


    def __init__(self, find=None, near=None, max_results=3, **kwargs) -> None:
        """
        This method will take any spider arguments and copy them to the spider as attributes.
        Spider arguments are passed through the crawl command using the -a option. For Example:
        `scrapy crawl yelp -a find=Restaurants -a near=...`
        Args:
            :param find: what to search in the Yelp website (required)
            :param near: an location for the search (required)
            :param max_results: the max of results (default is 3)
        """
        super(YelpSpider, self).__init__(**kwargs)
        self.find = find
        self.near = near
        self.max_results = int(max_results)

    def start_requests(self) -> [scrapy.Request, None]:
        """
        This method must return an iterable with the first Requests to crawl for this spider.
        It is called by Scrapy when the spider is opened for scraping.
        """

        chicago_zip_codes = ['60601', '60602', '60603', '60604', '60605', '60606', '60607', '60608', '60609', '60610', '60611', '60612', '60613', '60614', '60615', '60616', '60617', '60618', '60619', '60620', '60621', '60622', '60623', '60624', '60625', '60626', '60628', '60629', '60630', '60631', '60632', '60633', '60634', '60636', '60637', '60638', '60639', '60640', '60641', '60643', '60644', '60645', '60646', '60647', '60649', '60651', '60652', '60653', '60654', '60655', '60656', '60657', '60659', '60660', '60661', '60663', '60664', '60666', '60668', '60669', '60670', '60673', '60674', '60675', '60677', '60678', '60679', '60680', '60681', '60682', '60684', '60685', '60686', '60687', '60688', '60689', '60690', '60691', '60693', '60694', '60695', '60696', '60697', '60699', '60701']
        if self._arguments_valid():
            # special argument not good way, but it works ok for now
            if self.near=="ALL":
                """
                Read in all zip codes from population_by_zip_2010.csv.gz
                """
                df = pd.read_csv('../data/usa_2010_population_by_zip_tmp.csv.gz', compression='gzip', header=0, sep=',', quotechar='"', error_bad_lines=False)
                # take the top 1000 zip codes
                a = df.sort_values(by='population', ascending=False)['zipcode'].to_numpy()
                a = a[0:1000]
                # remove chicago zip codes (already done from prior run )
                b = np.array(chicago_zip_codes)
                zipcodes = np.setdiff1d(np.union1d(a, b), np.intersect1d(a, b))
                for i,zipcode in enumerate(zipcodes):
                    x = str(zipcode).zfill(5)
                    url = self.SEARCH_URL.format(description=self.find, location=x)
                    yield scrapy.Request(url, meta={'cookiejar': i,'RETRY_KEY':0}, callback=self.parse)

            elif self.near=="ALL_CHICAGO":
                """
                use only chicago zip within chicago_zip_codes
                """
                for i, x in enumerate(chicago_zip_codes):
                    url = self.SEARCH_URL.format(description=self.find, location=x)
                    yield scrapy.Request(url, meta={'cookiejar': i,'RETRY_KEY':0}, callback=self.parse)
            else:
                """
                use the user parameters
                """
                # Returns a Request object when the arguments are valid, so that the response
                # can be parsed by the YelpSpider#parse method.
                url = self.SEARCH_URL.format(description=self.find, location=self.near)
                yield scrapy.Request(url,meta={'cookiejar': 0,'RETRY_KEY':0})

        else:
            # TODO: display how to use, required parameters, etc...
            print("scrapy crawl yelp -a find='pizza' -a near='chicago'")
            print("scrapy crawl yelp  -s JOBDIR=crawls/spider-1 -a find='Restaurants' -a near='ALL_CHICAGO'")



    def parse(self, response: TextResponse) -> [scrapy.Request, ScrapyYelpItem]:
        if response.url.startswith("https://m.yelp.com/visit_captcha"):
            print("----------------------------")
            print("---- CAPTCHA            ",response.url)
            print("----------------------------")
            # rar row rorge

            self.browser.get(response.url)
            self.crawler.engine.pause()
            wait = WebDriverWait(webdriver, 10000)

            wait.until(lambda driver: self.browser.current_url == "http://www.google.com")
            #wait(driver, 10000).until(EC.url_changes(response.url))
            self.crawler.engine.unpause()
            #raise CloseSpider('captcha_request aborting')



            #wait(self.browser, 20).until(EC.frame_to_be_available_and_switch_to_it(self.browser.find_element_by_xpath('//iframe[contains(@src, "google.com/recaptcha")]')))
            #wait(self.browser, 30).until(EC.element_to_be_clickable((By.ID, 'recaptcha-anchor'))).click()
            #raise CloseSpider('captcha_request aborting')




        elif response.url.startswith("https://m.yelp.com/menu"):
            items = self._handle_menu(response)
            if items!=None:
                https, slug = os.path.split(response.url)
                yield {
                    'slug': slug,
                    'menuitems': items
                }
        # make sure we are still in some list of yelp
        elif response.url.startswith("https://m.yelp.com/search?"):
            # build dataframe from the yConfig object (30 results)
            df =  self._handle_search_results(response)
            # yield these 30 results as detail items
            for url in df["biz.url"]:
                # replace biz with menu
                idx = url.index("biz")
                new_url = url.replace(url[idx:idx+3],"menu")
                yield scrapy.Request(new_url)
            # yield the results ===> which ends in pipeline and written out as csv
            yield ScrapyYelpItem(df=df)

            # yield the next 30
            next_30 = response.css(".next::attr(href)")
            if next_30 is not None:
                print("===== next 30 page ====")
                for url in next_30[:self.max_results]:
                    # Joins the url found with the domain url
                    next_page = response.urljoin(url.extract())
                    # yield the next 30 (turn off if you are debugging one page)
                    yield scrapy.Request(next_page)

    def _handle_menu(self, response: TextResponse) -> ScrapyYelpItem:
        soup = BeautifulSoup(response.text, "html.parser")
        https, slug = os.path.split(response.url)
        menu_found = soup.find("section", { "class" : "std-section webview-hidden" }).find("h1", recursive=False).findAll(text=re.compile('.*Menu.*'))
        if menu_found!=None:
            items=[]
            for section in soup.findAll('section','section-full'):
                for li in section.findAll('li',{'class':'action-item'}):
                    hastitle=li.find("h3", { "class" : "alternate" })
                    if hastitle!=None:
                        title = li.find("h3", { "class" : "alternate" }).find("a", recursive=False)
                        desc = li.find("p", { "class" : "menu-item-description" })
                        price= li.find("p", { "class" : "price" })
                        if (title!=None):
                            title=title.get_text().strip()
                        if (desc!=None):
                            desc=desc.get_text().strip()
                        if (price!=None):
                            price=price.get_text().strip()
                        items.append((slug,title,desc,price))
            return items
            """
            items now contain title,desc,price tuple
            ('Soda', '', '1.25')
            ('Bottled Water', '', '1.50')
            ('San Pellegrino Aranciata', '', '1.75')
            ('Goose Island Root Beer', '', '2.00')
            ('Lacroix Sparkling Water', '', '2.00')
            ('Chicken Wings', 'Buffalo or BBQ. Served with blue cheese or ranch.', '7.00')
            ('Garlic Bread', '', '4.00')
            ('Pesto Bread', '', '5.00')
            """
            #print(items)
        else:
            print("no menu for ",response.url)
            return None

    def _handle_search_results(self, response: TextResponse) -> ScrapyYelpItem:
        """
        Maps a `TextResponse` to a `ScrapyYelpItem` instance.
        Args:
            :param response: the response received from a `Request` object
            :return: an instance of `ScrapyYelpItem` populated with the data scraped from the response
        """

        # get yConfig
        pattern = re.compile(r"""\n\s+yConfig\s+=\s+""", re.MULTILINE | re.DOTALL)
        soup = BeautifulSoup(response.text, "html.parser")
        script = soup.find("script", text=pattern)
        myjson = script.get_text()
        # remove start pattern (js assignment)
        s = re.sub(pattern, '', myjson)
        # remove html (parser problems)
        s = re.sub('<[^<]+?>', '', s)
        # remove last semi colon (end-of-data)
        s = s[0:s.rfind(';')]
        json_object = json.loads(s,strict=False)

        keys = [x for x in json_object["js_display"]["hovercard_data"] if x.isnumeric()]
        # first part is the hovercard data - which contains most of the aggregate biz informative
        # such as total_reviews and summary_score
        df_hovercard_data = pd.DataFrame()
        for x in keys:
            tmpdf = json_normalize(json_object["js_display"]["hovercard_data"][x])
            df_hovercard_data = df_hovercard_data.append(tmpdf,ignore_index=True)

        df_hovercard_data = df_hovercard_data.set_index("result_number")
        df_hovercard_data.index = df_hovercard_data.index.astype(int)
        # second part is the resourceid which might be useful later on, not sure if this is used at all, but
        # it serves as a good example of how to join to other "parts" of the nested json structure and flatten it
        df_markers = json_normalize(json_object["js_display"]["map_state"]["markers"])
        df_markers = df_markers[df_markers['resourceType'] == 'business'].loc[:, ["url","resourceId","hovercardId","label","location.latitude","location.longitude",]]
        df_markers = df_markers.set_index('label')
        df_markers.index = df_markers.index.astype(int)

        # combine data into a single dataframe which will eventually be written out by our pipeline
        df = df_hovercard_data.join(df_markers)

        # at this point we want to also scrape the indvidual biz listing for the menu, syntax is verbose here


        ## deubg write to file
        #json_formatted = json.dumps(json_object, indent=2)
        # print(json_formatted)
        # with open("files/"+'blah.json', 'wb') as file:
        #     file.write(str.encode(json_formatted))

        """

        Here is a smample of what the yConfig object looks like:

        json_object.keys() ====>
            ['cookies', 'gaConfig', 'adjustAndroidPaidTrafficUrl', 'webviewFlow', 'enabledSitRepChannels',
                isWebviewRequest', 'js_display', 'isLoggedIn', 'uaInfo', 'isSitRepEnabled', 'comscore', 'isBugsnagEnabled',
                'support', 'deprecatedEncryptedYUV', 'vendorExternalURLs', 'smartBannerFallbackActive', 'version',
                'recaptchaV3PublicKey', 'googlePlacesUrl', 'redesignActive', 'currentBaseLang', 'isClientErrorsEnabled',
                'uniqueRequestId', 'yelpcodeTemplateVersion', 'appInstallDialogEnabled', 'smartBannerPersistent',
                'imageUrls', 'siteUrl', 'referrer', 'webviewInfo', 'cookieDomain', 'recaptchaPublicKey',
                'send_user_agent_to_ga', 'pGifUrl']


        json_object["js_display"].keys() ===>
                ['polyglot_translations', 'raq_links', 'locale', 'hovercard_data', 'is_first_ad_hovercard_opened',
                'zoom', 'centerLng', 'map_state', 'advertising_business_id_list', 'centerLat', 'pager']

        json_object["js_display"]["hovercard_data"] ==>
        '1': {'resource_id': None,
          'result_number': 1,
          'biz': {'alias': 'lou-malnatis-pizzeria-chicago',
           'review_count': 5998,
           'name': "Lou Malnati's Pizzeria",
           'rating': 4.07785928642881,
           'url': 'https://m.yelp.com/biz/lou-malnatis-pizzeria-chicago',
           'price': '$$',
           'categories': 'Pizza, Italian, Sandwiches',
           'distance': '2.5 mi'},
          'lat': 41.890357,
          'lng': -87.633704,
          'type': 'natural'},
         '2': {'resource_id': None,
         ....


         json_object["js_display"]["map_state"]["markers"] ===>
         [{'resourceType': 'business',
          'url': '/biz/lou-malnatis-pizzeria-chicago',
          'resourceId': '8vFJH_paXsMocmEO_KAa3w',
          'label': '1',
          'shouldOpenInNewTab': False,
          'location': {'latitude': 41.890357, 'longitude': -87.633704},
          'key': 1,
          'hovercardId': 'Q6nXAEw3UuAVFSztE4lPnA',
          'icon': {'name': 'business',
           'anchorOffset': [12, 32],
           'activeOrigin': [24, 0],
           'scaledSize': [48, 320],
           'regularUri': 'https://media0.fl.yelpcdn.com/mapmarkers/yelp_map_range/20160801/1/10.png',
           'size': [24, 32],
           'activeUri': 'https://media0.fl.yelpcdn.com/mapmarkers/yelp_map_range/20160801/1/10.png',
           'regularOrigin': [0, 0]}},
         {'resourceType': 'business',
          'url': '/biz/pequods-pizzeria-chicago',
          'resourceId': 'DXwSYgiXqIVNdO9dazel6w',
          'label': '2',
          'shouldOpenInNew
          ...

        """
        #print(json_object["js_display"]["hovercard_data"])



        return df



    def _arguments_valid(self) -> bool:
        """
        Checks if the required arguments have been properly set via command-line.
        :return: an boolean indicating if all arguments are valid
        """
        return self.find and self.near and self.max_results >= 1
