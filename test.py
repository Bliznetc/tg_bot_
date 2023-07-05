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
# new_dictionary = processing.prepare_text("")
# text_0 = db_interface.add_new_dictionary(new_dictionary, 'TEST_TRASH')
# print(text_0)

# def try_except(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(e)
#     return wrapper
#
# import db_interface
# import re
# import codecs
#
#
# def formating(dict_id):
#     content = db_interface.get_words_by_dict_id(dict_id)
#
#     for key, value in content.items():
#         for elem in value:
#             for key2, value2 in elem.items():
#                 if isinstance(value2, str):
#                     elem[key2] = transform(value2)
#
#     db_interface.update_content(dict_id, content)
#
#     print("probitie")
#
#
# def check_substring(s):
#     match = re.search(r'u0\w{3}', s)
#     if match:
#         return (match.start(), match.group())
#     return -1
#
#
# def transform(string: str):
#     while check_substring(string) != -1:
#         index, letter = check_substring(string)
#         print(index, letter)
#         string = string[:index] + codecs.decode(f"\\{letter}", "unicode_escape") + string[index + 5:]
#         print(string)
#     print('----------------------------------------------')
#     return string
#
#
# formating('TEST_B1')


