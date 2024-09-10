from bs4 import BeautifulSoup
import pandas as pd

def scrap_donor_data(html_content) -> pd.DataFrame:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize lists to store the data
    parties = []
    donations = []
    donor_names = []
    donor_adresses = []
    donor_zip_and_cities = []
    donation_dates = []
    notification_dates = []

    # Find the table body
    table_body = soup.find('tbody')

    # Iterate through the rows of the table
    for row in table_body.find_all('tr'):
        # Check if the row contains data (not a header or notes row)
        cols = row.find_all('td')
        if len(cols) == 5:
            # Extract data for each column and append it to the corresponding list
            parties.append(cols[0].text.strip())
            donations.append(cols[1].text.strip())
            
            donor_description = list(cols[2].p.stripped_strings)
            if len(donor_description) == 2:
                donor_names.append(donor_description[0])
                donor_adresses.append('')
                donor_zip_and_cities.append(donor_description[1])
            elif len(donor_description) == 3:
                donor_names.append(donor_description[0])
                donor_adresses.append(donor_description[1])
                donor_zip_and_cities.append(donor_description[2])
            elif len(donor_description) == 4:
                donor_names.append(' '.join(donor_description[0:2]))
                donor_adresses.append(donor_description[2])
                donor_zip_and_cities.append(donor_description[3])
            else:
                print("Wrong donor information format:", donor_description)
                donor_names.append('')
                donor_adresses.append('')
                donor_zip_and_cities.append('')

            donation_dates.append(cols[3].text.strip())
            notification_dates.append(cols[4].text.strip())

    # Create a DataFrame with the extracted data
    return pd.DataFrame({
        'Party': parties,
        'Donation Amount': donations,
        'Donor Name': donor_names,
        'Donor Address': donor_adresses,
        'Donor ZIP and City': donor_zip_and_cities,
        'Donation Date': donation_dates,
        'Notification Date': notification_dates
    })