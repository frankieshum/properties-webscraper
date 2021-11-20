from types import TracebackType
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

def main():
    try:
        while True:
            url = input('Enter a Rightmove.co.uk search URL: ')
            html = get_html_from_url(url)
            soup_results = get_properties_from_html(html)
            list_properties(soup_results)

            if input('Press enter to search again (or type "q" to quit)') == 'q':
                break
    except Exception as err:
        print(f'An error occurred! Details: "{err}", Traceback: {TracebackType.format_tb(err.__traceback__)}.')


def get_search_parameters():
    pass
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


def get_properties_from_html(html):
    """
    Parses HTML from Rightmove into property results.
    Receives HTML as bytes; returns properties as a BeautifulSoup resultSet.
    """

    soup_html = BeautifulSoup(html, 'html.parser')
    # Find all divs with id starting with "property-"
    soup_results = soup_html.findAll('div', {'id' : lambda L: L and L.startswith('property-')})
    if len(soup_results) == 0:
        print('No properties found for the provided URL!')
        sys.exit()
    return soup_results


def list_properties(property_results):
    """
    Loops through property results and prints details.
    Receives properties as a BeautifulSoup resultSet.
    """

    # Loop through results and print details
    for index, property in enumerate(property_results, start=1):
        address = get_address(property)
        title = get_property_type(property)
        price = get_price(property)
        added_by_agent = get_added_by_agent(property)
        if address is not None and title is not None and price is not None:
            print(f'----------------------------- #{index} -----------------------------')
            print(f'{title}\n{address}\n{price}\n{added_by_agent}\n')


def get_address(property):
    """
    Gets the address from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns address as string, or None if not found.
    """

    address = property.find('address')
    if not address or not address.span or not address.span.text:
        return None
    return address.span.text


def get_property_type(property):
    """
    Gets the property type from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns property type as string, or None if not found.
    """

    property_type = property.find('h2')
    if not property_type or not property_type.text:
        return None
    return property_type.text.replace('\n', '').strip()


def get_price(property):
    """
    Gets the price from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns price as string, or None if not found.
    """

    price = property.find('span', {'class':'propertyCard-priceValue'})
    if not price or not price.text:
        return None
    return price.text


def get_added_by_agent(property):
    """
    Gets the added-by-agent details from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns added-by-agent details as string, or None if not found.
    """

    added_by_agent = property.find('div', {'class':'propertyCard-branchSummary'})
    if not added_by_agent or not added_by_agent.text:
        return None
    return added_by_agent.text.replace('\n', '')


def format_error(err, msg_prefix='An error occurred!'):
    """
    Formats an error including traceback details.
    Receives an Exception object and an optional error message prefix string; returns formatted error string.
    """

    return f'{msg_prefix} Details: "{err}", Traceback: {TracebackType.format_tb(err.__traceback__)}.'


if __name__ == '__main__':
    main()
