from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import traceback

ZOOPLA_BASE_URL = 'https://www.zoopla.co.uk'

class Property:
    def __init__(self, title, address, price, listed_date):
        self.title = title
        self.address = address
        self.price = price
        self.listed_date = listed_date

    def format_details(self):
        return f'{self.title}\n{self.address}\n{self.price}\n{self.listed_date}\n'


def main():
    try:
        while True:
            url = input('Enter a zoopla.co.uk search URL: ')
            get_and_list_properties(url)
            if input('Press enter to search again (or type "q" to quit): ') == 'q':
                break
    except Exception as err:
        print(format_error(err))


def get_and_list_properties(url):
    """
    Gets elements from URL, parses into properties and prints results.
    Receives a URL as a string.
    """

    url_to_get = url
    start_property_num = 1
    # Iteratively get results until no result pages left
    while True:
        html = get_html_from_url(url_to_get)
        soup_html = BeautifulSoup(html, 'html.parser')
        properties = get_properties_from_soup_html(soup_html)
        print_properties(properties, start_property_num)

        next_page_url = get_next_page_url(soup_html)
        if next_page_url is None:
            break
        url_to_get = ZOOPLA_BASE_URL + next_page_url
        start_property_num += len(properties)


def get_html_from_url(url):
    """
    Opens a URL, gets the response and returns the body.
    Receives a URL as string; returns HTML as bytes.
    """

    print('Getting properties...\n')
    try:        
        web_client = urlopen(url)
        html = web_client.read()
        web_client.close()
        return html
    except Exception as err:
        print(format_error(err, 'An error occurred while getting the web results!'))
        sys.exit()


def get_properties_from_soup_html(soup_html):
    """
    Parses HTML from Zoopla search results page into property results.
    Receives HTML as BeautifulSoup object; returns a list of Property objects.
    """

    # Find all divs with id starting with "property-"
    soup_properties = soup_html.findAll('div', {'data-testid' : 'search-result'})
    if len(soup_properties) == 0:
        print('No properties found for the provided URL!')
        sys.exit()

    properties = []
    for soup_property in soup_properties:
        address = get_address(soup_property)
        title = get_property_type(soup_property)
        price = get_price(soup_property)
        listed_date = get_listed_date(soup_property)
        properties.append(Property(title, address, price, listed_date))
    return properties


def get_address(property):
    """
    Gets the address from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns address as string, or None if not found.
    """

    address = property.find('p', {"data-testid" : "listing-description"})
    if not address or not address.text:
        return None
    return address.text


def get_property_type(property):
    """
    Gets the property type from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns property type as string, or None if not found.
    """

    property_type = property.find('h2', {"data-testid" : "listing-title"})
    if not property_type or not property_type.text:
        return None
    return property_type.text


def get_price(property):
    """
    Gets the price from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns price as string, or None if not found.
    """

    price = property.find('div', {'data-testid' : 'listing-price'})
    if not price or not price.p or not price.p.text:
        return None
    return price.p.text


def get_listed_date(property):
    """
    Gets the added-by-agent details from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns added-by-agent details as string, or None if not found.
    """

    listed_on = property.find('span', {'data-testid':'date-published'})
    if not listed_on or not listed_on.text:
        return None
    return listed_on.text


def print_properties(properties, start_property_num=1):
    """
    Loops through properties and prints details.
    Receives properties as a list of Property objects.
    """

    for property_num, property in enumerate(properties, start=start_property_num):
        print(f'----------------------------- #{property_num} -----------------------------')
        print(property.format_details())


def get_next_page_url(soup_html):
    """
    Gets the next page URL from a Zoopla results page.
    Receives a webpage as a BeautifulSoup object; returns relative URL as a string (or None if no more results).
    """
    
    return soup_html.find('div', {'data-testid' : 'pagination'}).findAll('a')[-1].get('href')


def format_error(err, msg_prefix='An error occurred!'):
    """
    Formats an error including traceback details.
    Receives an Exception object and an optional error message prefix string; returns formatted error string.
    """

    return f'{msg_prefix} Details: "{err}", Traceback: {traceback.format_tb(err.__traceback__)}.'


def get_search_parameters():
    pass # TODO
    # e.g. https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E12263&insId=1
    # &radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=3&sortByPriceDescending=
    # &_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=
    # &letType=&letFurnishType=&houseFlatShare=
    # location identifier (how to get?)
    # radius (miles) (0, 0.25, 0.5, 1, 3, 5, 10, 15, 20, 30, 40)
    # min price
    # max price
    # min beds
    # max beds
    # days since added


if __name__ == '__main__':
    main()
