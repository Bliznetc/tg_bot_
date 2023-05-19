import json
import constants as const
import json_functions as jsonFunc
import random

"""
def registration(user_id):
    if user_id in const.chat_ids:
        pass
    else:
        with open(f"user_dictionaries/{user_id}.json", "w") as file:
            json.dump([], file, indent=4)
        
if __name__ == "__main__":
    
    with open("user_ids.json", "r") as file:
        user_ids = json.load(file)

    for user_id in user_ids:
        registration(user_id)
"""

s = "abab"
l = list(s);
l[0] = s[0].upper()
s = "".join(l)
print(s)

#в этом файле я создал наши словари, которые соответсвуют нашим id
#этот файл не готов к использованию, и будет полностью переделан

