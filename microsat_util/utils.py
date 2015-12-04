import os
import cv2


__all__ = ['save_image']


def save_image(filename, output_image):
    absolute_path = os.path.abspath(filename)
    directory_path = os.path.dirname(absolute_path)

    # Create directory if it does not exist
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)

    cv2.imwrite(filename=absolute_path, img=output_image)
