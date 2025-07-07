from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    with open(path) as level_map:
        return [list(row) for row in reader(level_map, delimiter=',')]

def import_folder(path):
    for _, _, image_files in walk(path):
        images = []
        for image_file in image_files:
            full_path = path + '/' + image_file
            image = pygame.image.load(full_path).convert_alpha()
            images.append(image)
        return images