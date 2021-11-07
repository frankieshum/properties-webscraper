from types import NoneType
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

def main():
    url = input('Enter a Rightmove.co.uk search URL: ')
    html = get_html_from_url(url)
    soup_results = get_properties_from_html(html)
    list_properties(soup_results)


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
    except Exception as ex:
        print(f'An error occurred while getting the web results! Details: {ex}')
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
    if address is None or address.span is None or address.span.text is None or address.span.text == '':
        return None
    return address.span.text


def get_property_type(property):
    """
    Gets the property type from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns property type as string, or None if not found.
    """
    property_type = property.find('h2')
    if property_type is None or property_type.text is None:
        return None
    return property_type.text.replace('\n', '').strip()


def get_price(property):
    """
    Gets the price from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns price as string, or None if not found.
    """
    price = property.find('span', {'class':'propertyCard-priceValue'})
    if price is None or price.text is None:
        return None
    return price.text


def get_added_by_agent(property):
    """
    Gets the added-by-agent details from a property if exists.
    Receives a property as a BeautifulSoup resultSet; returns added-by-agent details as string, or None if not found.
    """
    added_by_agent = property.find('div', {'class':'propertyCard-branchSummary'})
    if added_by_agent is None or added_by_agent.text is None:
        return None
    return added_by_agent.text.replace('\n', '')


if __name__ == '__main__':
    main()
