import json

print("Удалил всё ненужное")

#удаление словаря
with open("dictionary.json", "w") as file:
    json.dump([], file)
