# Приводит файл к нужному формату и добавляет в бд
import processing
import db_interface

# with open("Anton1.txt", 'r', encoding='utf-8') as file:
#     file_content = file.read()
# with open("A1.txt", 'r', encoding='utf-8') as file:
#     file_content = file.read()
# #
# arr = file_content.split(";")
# arr2 = file_content2.split("\n")
# arr3 = []
#
# for i in range(2960):
#     s = arr[i] + "-" + arr2[i]
#     cur = s.replace("\n", "")
#     cur = cur.replace(chr(8211), "-")
#     cur = cur.replace(chr(8212), "-")
#     cur = cur.replace(" - ", "-")
#     cur = cur.replace("- ", "-")
#     cur = cur.replace(" -", "-")
#     arr3.append(cur)
#
# print(arr3)
# arr2 = []
# arr3 = []
# used = {}
# cnt = 0
#
# for i in arr:
#     i = i.lower()
#     if i.find("≡") != -1 or i.find("=") != -1:
#         continue
#     cur = i.replace("\n", "")
#     cur = cur.replace(chr(8211), "-")
#     cur = cur.replace(chr(8212), "-")
#     cur = cur.replace(" - ", "-")
#     cur = cur.replace("- ", "-")
#     cur = cur.replace(" -", "-")
#     cur_key1 = cur.split("-")
#     cur_key = cur_key1[0]
#     if cur_key in used:
#         cnt += 1
#         continue
#     arr2.append(cur)
#     arr3.append(cur_key)
#     used[cur_key] = 1
#
#
# # print(arr2)
# # print(len(arr2))
# text = ";\n".join(arr)
# text2 = "\n".join(arr3)
# with open("Anton_keys.txt", "w", encoding="utf-8") as file:
#     file.write(text2)
# with open("Anton2.txt", "w", encoding="utf-8") as file:
#     file.write(text)
#
# # print(text)
new_dictionary = processing.prepare_text("")
text_0 = db_interface.add_new_dictionary(new_dictionary, 'TEST_TRASH')
print(text_0)