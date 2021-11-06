from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

def main():
    # Get URL from user
    url = input('Enter a Rightmove.co.uk search URL: ')

    # Get data from webpage
    print('Getting properties...\n')
    web_client = urlopen(url)
    html = web_client.read()
    web_client.close()

    # Parse to HTML and get search results
    html_soup = BeautifulSoup(html, 'html.parser')
    results = html_soup.findAll("div", {"id" : lambda L: L and L.startswith('property-')})
    if len(results) == 0:
        print('No properties found for the provided URL!')
        sys.exit()

    # Loop through results and print details
    for index, property in enumerate(results, start=1):
        address = property.find('address').span.text
        if address != '':
            # Proceed only if address found (there are some empty elements on the page)
            title = property.find('h2').text.replace('\n', '').strip()
            price = property.find('span', {'class':'propertyCard-priceValue'}).text
            added_by_agent = property.find('div', {'class':'propertyCard-branchSummary'}).text.replace('\n', '')
            print(f'----------------------------- #{index} -----------------------------')
            print(f'{title}\n{address}\n{price}\n{added_by_agent}\n')

if __name__ == "__main__":
    main()
