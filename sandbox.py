import base64

if __name__ == '__main__':
    other_file_path = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image1X1.bmp"

    black_file_path: str = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_black_quarter.bmp"

    blue_file_path: str       = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_blue_quarter.bmp"
    dark_grey_file_path: str  = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_dark_grey_quarter.bmp"
    light_blue_file_path: str = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_light_blue_quarter.bmp"
    light_grey_file_path: str = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_light_grey_quarter.bmp"
    maroon_file_path: str     = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_maroon_quarter.bmp"
    orange_file_path: str     = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_orange_quarter.bmp"
    purple_file_path: str     = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_purple_quarter.bmp"
    red_file_path: str        = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_red_quarter.bmp"
    yellow_file_path: str     = "C:\\CarWars\\CarWarsOnline\\map_designer\\images\\image_yellow_quarter.bmp"

    # Replace 'path/to/your_image.png' with the actual path to your image
    with open(black_file_path, 'rb') as image_file:
        black_encokded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(blue_file_path, 'rb') as image_file:
        blue_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(dark_grey_file_path, 'rb') as image_file:
        dark_grey_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(light_blue_file_path, 'rb') as image_file:
        light_blue_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(light_grey_file_path, 'rb') as image_file:
        light_grey_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(maroon_file_path, 'rb') as image_file:
        maroon_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(orange_file_path, 'rb') as image_file:
        orange_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(purple_file_path, 'rb') as image_file:
        purple_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(red_file_path, 'rb') as image_file:
        red_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open(yellow_file_path, 'rb') as image_file:
        yellow_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    i: int = 0
