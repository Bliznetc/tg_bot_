# def try_except(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(e)
#     return wrapper

import db_interface
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

dict_ids = db_interface.get_dict_ids()

num_to_part = ["noun", "verb", "adj", "adv", "other"]
for dict in dict_ids:
    cur_dict = db_interface.get_words_by_dict_id(dict)
    print(dict + ":")
    # print(cur_dict)
    sum = 0
    for x in num_to_part:
        print (x + " - ", len(cur_dict[x]))
        sum += len(cur_dict[x])
    print(sum)



