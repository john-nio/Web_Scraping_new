# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7

import os
import requests
import re
# Code here - Import BeautifulSoup library
from bs4 import BeautifulSoup
# Code ends here

# function to get the html source text of the medium article
def get_page():
    global url
    url = input("Enter URL of the article you want to scrap: ")
    print(f"You entered: {url}")
    
    #Handling Errors
    #r' is used to escape backslash. Or double backslash can be used
    #s? - To make sure to it accept the url either with s or without it
    if not re.match(r'https?://medium.com/',url):
        print('Please enter a valid website, or make sure it is a medium article')
        sys.exit(1)
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        print("Request successful.")
       
        
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>": "\n"}
    
    # Escape the dictionary keys for use in regex
    rep = dict((re.escape(k), v) for k, v in rep.items())
    
    # Create a regex pattern to match any of the keys
    pattern = re.compile("|".join(rep.keys()))
    
    # Substitute tags with their corresponding replacements
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    
    # Remove any remaining HTML tags
    text = re.sub(r'<[^>]*>', '', text)  # Changed pattern to handle all tags
    return text


def collect_text(soup):
	text = f'url: {url}\n\n'
	para_text = soup.find_all('p')
	print(f" Number of paragraphs found:  {len(para_text)}")
	for para in para_text:
		text += f"{para.text}\n\n"
	return text

# function to save file in the current directory
def save_file(text):
    # Ensure the global variable 'url' is defined
    global url
    
    # Define the directory path
    directory = './scraped_articles'
    
    # Create directory if it does not exist
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    # Generate a file name based on the URL
    name = url.split("/")[-1]
    fname = f'{directory}/{name}.txt'
    
    # Debug information
    print(f"Saving file to: {fname}")
    
    # Write the text to the file
    with open(fname, 'w') as file:
        file.write(text)
    
    print(f'File saved in directory {fname}')


if __name__ == '__main__':
    try:
        soup = get_page()  # Get the BeautifulSoup object
        text = collect_text(soup)  # Collect the text
        save_file(text)  # Save the text to a file
    except Exception as e:
        print(f"An error occurred: {e}")
	# Instructions to Run this python code
	# Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7