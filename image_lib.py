'''
Library of useful functions for working with images.
'''

import requests
import ctypes



def main():
    # TODO: Add code to test the functions in this module
    image_data = download_image('https://apod.nasa.gov/apod/ap230418.html')
    result = save_image_file(image_data, r'"C:\Users\rosea\OneDrive\Documents\image\EclipseMap_nasa_5400.jpg"')
    return

def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        bytes: Binary image data, if succcessful. None, if unsuccessful.
    """
    # TODO: Complete function body
    print(f'Downloading picture from {image_url}...', end='')
    resp_msg = requests.get(image_url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        return resp_msg.content
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

    return

def save_image_file(image_data, image_path):
    """Saves image data as a file on disk.
    
    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bytes: True, if succcessful. False, if unsuccessful
    """
    # TODO: Complete function body

    try:
        print(f"Saving image file as {image_path}...", end='')
        with open(image_path, 'wb') as file:
            file.write(image_data)
        print("success")
        return True
    except:
        print("failure")
        return False
    
   

def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bytes: True, if succcessful. False, if unsuccessful        
    """
    # TODO: Complete function body
    print(f"Setting desktop to {image_path}...", end='')
    WINDOWS_WALLPAPPER = 20
    try:
        if ctypes.windll.user32.SystemParametersInfoW(WINDOWS_WALLPAPPER, 0, image_path, 3):
            print("success")
            return True
        else:
            print("failure")
    except:
        print("failure")
    return False

    

def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    # NOTE: This function is only needed to support the APOD viewer GUI
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()