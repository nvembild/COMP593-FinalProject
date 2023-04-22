'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''

import requests

APOD_API_URL:'https://api.nasa.gov/planetary/apod'

API_KEY :'XHqg9khmPMgrbkVdCXz7YK8AfN2uXGyfM9jxBkdt'


def main():
    # TODO: Add code to test the functions in this module
    resp_msg = requests.get(APOD_API_URL)
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """

    apod_date  = "2023-04-19"

    if apod_date == '':
        print('Error: apod date specified.')
        return 
    else:
        return None

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    apod_info_dict = get_apod_info(apod_date=)
    print(f'Getting information for {apod_info_dict}...', end='')
    url = APOD_API_URL + API_KEY
    resp_msg = requests.get(url)
    return

if __name__ == '__main__':
    main()