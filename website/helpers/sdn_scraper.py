import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin

# Main URL for the forum
base_url = "https://forums.studentdoctor.net/forums/2023-2024-md-medical-school-specific-discussions.1198/page-{page_num}"

def find_secondary_prompt_text(element):
    return (re.match(r'(\d+)\.(.+)', element.strip()) is not None
            or element.name == 'b'
            or element == '&quot;')


def get_full_text(element):
    full_text = ''
    for content in element.contents:
        if isinstance(content, str):
            full_text += content
        else:
            full_text += content.get_text(strip=True)
        full_text += ' '  # Add a space between sibling elements
    return full_text

def scrape_prompts(thread_url):
    full_thread_url = f"https://forums.studentdoctor.net{thread_url}"
    response = requests.get(full_thread_url)

    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        thread_title = soup.find('title').text
        
        prompts = []

        # Find the first post's content
        first_post = soup.find('div', class_='js-messageContent')
        if first_post:
            # Find the div containing essay prompts
            essay_div = soup.find('div', class_='bbWrapper')

            # Extract and print each essay prompt
            essay_prompts = []
            current_prompt = None

            for item in essay_div.find_all(['b', 'span']):
                if item.name == 'b':
                    current_prompt = item.text.strip()
                elif item.name == 'span' and current_prompt is not None and "." in item.text:
                    essay_prompts.append(f"{current_prompt} {item.text.strip()}")


            pattern = r'(\d+)\s*[\.-]\s*(.+)'

            for text in essay_prompts:
                matches = re.findall(pattern, text)
                for match in matches:
                    number, content = match
                    prompts.append((number, content))
        unique_prompts = []
        if prompts:
            for item in prompts:
                if item not in unique_prompts:
                    unique_prompts.append(item)
        return thread_title, unique_prompts
    else:
        print(f"Failed to retrieve {full_thread_url}")
        return None, None


# Scrape thread URLs from the main page
response = requests.get(base_url.format(page_num=1))  # Start with the first page
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    thread_links = soup.select('a[data-tp-primary="on"]')

    # Calculate the total number of pages in the forum
    last_page_num = int(4)

    # Create a list to store DataFrames for each thread's prompts
    prompts_dfs = []

    for page_num in range(1, last_page_num + 1):
        page_url = base_url.format(page_num=page_num)


        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            thread_links = soup.select('a[data-tp-primary="on"]')

            for thread_link in thread_links:
                thread_url = thread_link['href']

                # Call the scraping function for the current page
                school_name, prompts = scrape_prompts(thread_url)

                school_name = school_name.replace(" | Student Doctor Network","")
                school_name = school_name.replace("2023-2024 ","")

                if prompts:
                    prompts_list = []
                    for prompt in prompts:
                        prompt_number, prompt_text= prompt
                        prompts_list.append({
                            'School Name': school_name,
                            'Prompt Number': prompt_number,
                            'Prompt': prompt_text,
                        })
                    
                    prompts_df = pd.DataFrame(prompts_list)
                    prompts_dfs.append(prompts_df)

    # Concatenate all DataFrames and save to a CSV file
    prompts_combined_df = pd.concat(prompts_dfs, ignore_index=True)
    prompts_combined_df.to_csv('prompts.csv', index=False)
else:
    print("Failed to retrieve the main page.")
