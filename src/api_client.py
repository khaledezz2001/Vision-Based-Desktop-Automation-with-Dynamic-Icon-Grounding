# api_client.py

import requests

def fetch_posts(api_url):
    """
    Fetches posts from the specified API URL.

    Args:
        api_url (str): The URL of the API endpoint.

    Returns:
        list: A list of post dictionaries, or None if an error occurs.
    """
    print("Fetching posts from API...")
    try:
        response = requests.get(api_url, timeout=10) # Added timeout
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None