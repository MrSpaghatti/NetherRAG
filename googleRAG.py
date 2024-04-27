import requests
from obsidian import Obsidian

# Replace with your own values
GOOGLE_CSE_API_KEY = 'your-google-custom-search-api-key'
OBSIDIAN_VAULT_PATH = 'path/to/your/obsidian/vault'
QUERY = 'the information you want to search'

# Get access token for Obsidian
try:
    obs = Obsidian()
    access_token = obs.login(email='your-email', password='your-password')
except Exception as e:
    print(f"Error while getting the access token: {e}")
    exit()

# Base URL for Google Custom Search API
base_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_CSE_API_KEY}&cx=YOUR_SEARCH_ENGINE_ID&q={QUERY}"

# Make a request to the Google Custom Search API
try:
    response = requests.get(base_url)
except Exception as e:
    print(f"Error while making the API request: {e}")
    exit()

data = response.json()

if 'items' in data:
    for item in data['items']:
        title = item['title']
        url = item['link']
        
        # Create a note with the title as the file name and content from the URL
        note_data = {
            "file": f"{title}.md",
            "parent": OBSIDIAN_VAULT_PATH,
            "content": requests.get(url).text,
            "tags": ["google-search"]
        }
        
        # Create a new note using the access token
        try:
            obs.create_note(access_token, **note_data)
        except Exception as e:
            print(f"Error while creating the note: {e}")
else:
    print("No results found.")