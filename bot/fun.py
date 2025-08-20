import random

JOKES = [
    "Atoms make up everything!",
    "You have a byte of class!",
    "Didn’t get arrays.",
    "Computer went to sleep.",
]
FACTS = [
    "Honey never spoils.",
    "Bananas are berries.",
    "Octopuses have 3 hearts.",
    "Sharks existed before trees.",
]
RIDDLES = [
    "Hands but can’t clap? — A clock.",
    "Gets wetter as it dries? — Towel.",
    "Speaks without mouth? — Echo.",
]
COMPLIMENTS = [
    "You're coding like a wizard 🧙",
    "Brain worth benchmarking 🧠",
    "Focus could power a data center ⚡",
]


def joke():
    return random.choice(JOKES)


def fact():
    return random.choice(FACTS)


def riddle():
    return random.choice(RIDDLES)


def compliment():
    return random.choice(COMPLIMENTS)
