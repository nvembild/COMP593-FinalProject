""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import date
import requests
import os
import image_lib
import inspect
from ast import Return
from multiprocessing import connection
import sqlite3
from sre_constants import SUCCESS
from sys import argv, exit
from hashlib import sha256
from typing import Text
from os import path
from urllib import response



# Global variables
image_cache_dir = None  # Full path of image cache directory
image_cache_db = None   # Full path of image cache database

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # Initialize the image cache
    init_apod_cache(script_dir)

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # TODO: Complete function body
    apod_date =date.today().strftime('%Y-%m-%d')
    if len(argv) > 1:
        try:
            apod_date= datetime.strptime(argv[1], '%Y-%m-%d').date().isoformate()

        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        apod_date = date.today().strftime('%Y-%m-%d')
    
    apod_date = date.fromisoformat('2022-12-25')
    print("APOD date:", apod_date)
    return apod_date

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """
    global image_cache_dir
    global image_cache_db
    # TODO: Determine the path of the image cache directory
    image_cache_dir =os.path(parent_dir, 'image_cache')

    # TODO: Create the image cache directory if it does not already exist
    if not os.path.exists(image_cache_dir):
        os.makedirs(image_cache_dir)

    # TODO: Determine the path of image cache DB
    image_cache_db = os.path(image_cache_dir, 'image_cache.db')

    # TODO: Create the DB if it does not already exist
con = sqlite3.connect(image_cache_db)
cur = con.cursor


def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    # TODO: Download the APOD information from the NASA API
    API_KEY = 'XHqg9khmPMgrbkVdCXz7YK8AfN2uXGyfM9jxBkdt'
    APOD_API_URL = 'https://api.nasa.gov/planetary/apod'
    res = requests.get(APOD_API_URL)

    # TODO: Download the APOD image
    res = requests.get(APOD_API_URL, stream=True)

    # TODO: Check whether the APOD already exists in the image cache
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    cur.execute("SELECT * FROM image WHERE date", {apod_date.isoformat()})
    existing_apod = cur.fetchone()

    # TODO: Save the APOD file to the image cache directory
    f_name = os.path.basename(APOD_API_URL)
    f_path = os.path(image_cache_dir, f_name)

    # TODO: Add the APOD information to the DB
    cur.execute("insert into image {apod_date, APOD_API_URL, f_path}", {apod_date.isoformation()})
    con.commit()
    return 0

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """
    # TODO: Complete function body
    get_apod_info(title, explanation, file_path,sha256,)
    if not get_apod_id_from_db(image_cache_db, sha256):
        determine_apod_file_path(title, file_path)
        get_apod_info(image_cache_db, file_path, explanation, sha256)
    return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    con = sqlite3.connect('image_cache.db')
    con = con.cursor()
    con.execute("select if from apod where sha256 is", {image_sha256})
    result = con.fetchone
    con.close()
    
    if result:
        return result [0]
    else:
        return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    response = requests.get(image_url)

    image_title = path.join(argv[1], image_url.split('/')[-1])

    if response.status_code == 200:
        with open (image_title, 'wb') as n:
            n.write(response.content)

    return image_title

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """

    # TODO: Query DB for image info
    query = f"select title, explanation, f_path from APOD, {image_id}"
    cur.execute(query)
    result = cur.fetchone()

    # TODO: Put information into a dictionary
    apod_info = {
        'title': 'T', 
        'explanation': 'E',
        'file_path': 'TBD',
    }

    con.close()
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    title = []
    for apod in image_cache_db:
        title.append(apod['title'])

    # NOTE: This function is only needed to support the APOD viewer GUI
    return title

if __name__ == '__main__':
    main()