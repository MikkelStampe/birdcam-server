
import random

BIRD_SPECIES = [
    "Eurasian Blue Tit",
    "Great Spotted Woodpecker",
    "European Robin",
    "Blackbird",
    "House Sparrow",
    "Goldfinch",
    "Chaffinch",
    "Greenfinch",
    "Magpie",
    "Wood Pigeon"
]

def classify_bird(image_path):
    # Dummy classifier: returns a random species from the list
    return random.choice(BIRD_SPECIES)
