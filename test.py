# Приводит файл к нужному формату и добавляет в бд
import processing
import db_interface

# with open("A.txt", 'r', encoding='utf-8') as file:
#     file_content = file.read()
#
# arr = file_content.split("\n")

# text2 = "\n".join(arr3)
# with open("Anton_keys.txt", "w", encoding="utf-8") as file:
#     file.write(text2)
# print(text)

# new_dictionary = processing.prepare_text("")
# print(text_0)









# a = db_interface.get_words_by_dict_id("TEST_B1")
#
# words = []
# trans = []
#
# for x in a:
#     for z in a[x]:
#         words.append(z['word'])
#         trans.append(z['trsl'])
#
#
# # print(len(arr))
# print(len(words))
# print(len(trans))
#
# #
# # text2 = "\n".join(words)
# # with open("A.txt", "w", encoding="utf-8") as file:
# #     file.write(text2)
#
#
# arr2 = []
#
# for i in range(len(words)):
#     cur = words[i] + "-" + trans[i] + "-" + arr[i]
#     arr2.append(cur)
#
#
# used = {}
# cnt = 0
# arr3 = []
# for i in arr2:
#     i = i.lower()
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
#     arr3.append(i)
#     used[cur_key] = 1
#
#
# print(len(arr), len(arr3))
# print(arr3)
#
# text = ";\n".join(arr3)
# new_dictionary = processing.prepare_text(text)
# text_0 = db_interface.add_new_dictionary(new_dictionary, 'TEST_B1_0')
# #
# # print(text_0)






# a = db_interface.get_words_by_dict_id("TEST_B1")
# b = db_interface.get_words_by_dict_id("TEST_ALL")
#
# words = []
# for x in a:
#     for z in a[x]:
#         words.append(z['word'])
#
# # print(words)
# # print(b)
#
# vec = []
# for x in b:
#     for z in b[x]:
#         if z['word'] in words:
#             set_word = [z['word'], "TEST"]
#             print(z['word'])
#         else:
#             cur_dict = z['word'] + '-' + z['trsl'] + '-' + z['trsc']
#             vec.append(cur_dict)
#
# text = ";\n".join(vec)
# new_dictionary = processing.prepare_text(text)
# text_0 = db_interface.add_new_dictionary(new_dictionary, 'TEST_ALL1')
# 955008318


# dict_ids = db_interface.get_dict_ids()
# num = 0
# for x in dict_ids:
#     dict = db_interface.get_words_by_dict_id(x)
#     for key in dict:
#         num += len(dict[key])
#     print(x, num)
#
# print(num)


