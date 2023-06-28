# Приводит файл к нужному формату
import processing
import db_interface

with open("B1.txt", 'r', encoding='utf-8') as file:
    file_content = file.read()

arr = file_content.split(";")
arr2 = []
used = {}

for i in arr:
    cur = i.replace("\n", "")
    cur = cur.replace("- ", "-")
    cur = cur.replace(" -", "-")
    cur_key1 = cur.split("-")
    cur_key = cur_key1[0]
    if cur_key in used:
        continue
    arr2.append(cur)
    used[cur_key] = 1

text = ";".join(arr2)
new_dictionary = processing.prepare_text(text)
text_0 = db_interface.add_new_dictionary(new_dictionary, 'TEST_B1')
print(text_0)