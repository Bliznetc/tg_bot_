import json
import random


def myFuncSort(word):
    return word['degree']


with open("dictionary.json", "r", encoding="utf-8") as file:
    dictionary = json.load(file)


dictionary.sort(key=myFuncSort)
for i in range(10):
    print(dictionary[i])

