####################  IMPORTS  ####################

import os
import numpy as np
import pandas as pd

import httplib2
import yaml
import ssl
import urllib
import requests
import re
from bs4 import BeautifulSoup
import csv
from bs4.element import Comment
import json
import pickle


####################  FUNCTIONS  #################### 


def get_protocol(urls):
    """Get website protocol.

    Parameters
    ----------
    urls : list
        List of urls.

    Returns
    -------
    tuple : shape = (2, )
        Returns two list, the first one with the urls using http protocols and
        the other one for the ones using https.

    """
    http_urls = list()
    https_urls = list()
    fail_urls = list()
    for i, url in enumerate(urls):
        try:
            r = requests.get('http://' + url) # first we try http
            resp = r.url # check the actual URL for the site
            if 'https' in resp :
                https_urls.append(url)
            else :
                http_urls.append(url)
        except:
            pass
        print('{}/{}'.format(i+1, len(urls)), end='\r')

    if len(http_urls)+len(https_urls)==len(url_list):
        print('No error occured.')

    return http_urls, https_urls


def verify_urls(urls, https=True):
    """Verify urls.

    Parameters
    ----------
    urls : list
        List of urls.
    https : bool
        Use https if set to True, http otherwise. Default=True.

    Returns
    -------
    list
        List of urls raising errors.

    """
    broken_urls = list()
    for i, url in enumerate(urls):
        if https:
            try:
                r = requests.get('https://' + url) # first we try http
                if r.status_code == 404:
                    broken_urls.append(url)
            except:
                broken_urls.append(url)
        else:
            try:
                r = requests.get('http://' + url) # first we try http
                if r.status_code == 404:
                    broken_urls.append(url)
            except:
                broken_urls.append(url)
        print('{}/{}'.format(i+1, len(urls)), end='\r')
    return broken_urls


def get_redirected_url(urls):
    """Get final redirected url.

    Parameters
    ----------
    urls : list
        List of urls.

    Returns
    -------
    dict
        Dictionary with old urls as keys and new urls as values.

    """
    output = dict()
    for i, url in enumerate(urls):
        try:
            r = requests.get(url)
            if r.url != url :
                output[url] = r.url
        except:
            pass
        print('{}/{}'.format(i+1, len(urls)), end='\r')
    return output


def get_outgoing_links(urls):
    """Get all outgoing links from webpage.

    Parameters
    ----------
    urls : list
        List of urls.

    Returns
    -------
    dict
        Dictionary with urls as keys and a list of outgoing links as values.

    """
    output = dict()
    j = 0
    for i, url in enumerate(urls):
        try:
            html_page = urllib.request.urlopen('http://'+url)
            soup = BeautifulSoup(html_page)
            links = []

            for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                links.append(link.get('href'))
            output[url]=links

        except :
            j+=1
            output[url]=None

        print('{}/{}'.format(i+1, len(urls)), end='\r')

    print('{} failures'.format(j))

    return output


def get_html(url):
    """Get webpage content.

    Parameters
    ----------
    url : str
        Url with protocal as string.

    Returns
    -------
    str
        HTML content.

    """
    if 'http' not in url:
        raise ValueError('Please add protocol to url.')
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, features='html.parser')
    strHtml = soup.decode('latin-1')
    return strHtml


def get_languages(url):
    """Returns if whether the website uses multiple languages or only one.

    Parameters
    ----------
    url : str
        Url as string.

    Returns
    -------
    bool
        Return True if the website is as multiple languages, False otherwise.

    """
    html = get_html(url)
    # MULTIPLE LANGUAGES
    multilang_words = ['languageMenu', 'cmbLanguage', 'wpml-ls-flag',
                       'multilingual', 'class="flag', 'id="lang',
                       'id="flag"' 'class="lang', 'langSwitch', 'lang-',
                       'set-lang', 'switchLanguage', 'language-chooser',
                       'lang-chooser', 'language-flags', 'lang-holder',
                       'setlang']
    if re.compile('|'.join(multilang_words),re.IGNORECASE).search(html):
        return True
    else:
        return False

def get_prices(url, **kwargs):
    """Get prices available on website from url.

    Parameters
    ----------
    url : type
        Description of parameter `url`.

    Returns
    -------
    type
        Description of returned object.

    """
    html = get_html(url)
    prices_keywords = ["Vraag een prijs aan", "vraag een prijs aan",
                       "VRAAG EEN PRIJS AAN", "Prijsaanvraag", "PRIJSAANVRAAG",
                       "Offerte", "offerte", "OFFERTE", "PRICES", "Prices",
                       "prices", "Vraag een offerte aan",
                       "vraag een offerte aan", "VRAAG EEN OFFERTE AAN",
                       "Offerte aanvragen", "OFFERTE AANVRAGEN", "Calculator",
                       "CALCULATOR", "calculator", "TARIEVEN", "Tarieven",
                       "offerte aanvragen", "rates", "Rates", "RATES",
                       "Request a quote", "REQUEST A QUOTE", "request a quote",
                       "Request a Quote"]
    other_keywords = [v for v in kwargs.values()]
    prices_keywords += other_keywords
    for p in prices:
        if p in html:
            print('{} in text'.format(p))
