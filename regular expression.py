import re

import csv

with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

split_list = []
for line in contacts_list:
    string = ','.join(line)

    # исправление номера телефона
    pattern = re.compile("(\+7|8)\s*\(?(\d{3})\)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})\s*\(?(доб\.)?\s?(\d+)?\)?")
    sub_pattern = r"+7(\2)\3-\4-\5\6\7"
    phone_corrected = pattern.sub(sub_pattern, string)

    # поместить каждое значение в своё поле
    pattern1 = re.compile("([А-ЯЁ][а-яё]+)[ ,]([А-ЯЁ][а-яё]+)[ ,]([А-ЯЁа-яё]+)?,{1,3}([А-Я][А-Яа-я]+)?,([^\d+,]+)?,([^a-z,]+)?,(.+)?")
    sub_pattern1 = r"\1,\2,\3,\4,\5,\6,\7"
    correct = pattern1.sub(sub_pattern1, phone_corrected)

    correct_list = correct.split(',')

    split_list.append(correct_list)

# объединить контакты по ключу - фамилия
add_dict = {}
for contact in split_list:
    lastname = contact[0]
    if lastname not in add_dict.keys():
        add_dict[lastname] = contact
    else:
        b = add_dict[lastname] + contact
        add_dict[lastname] = b

# удалить повторяющиеся элементы списка после объединения и переместить должность в своё поле
corrected_contact_list = []
for key, value in add_dict.items():
    new_value = []
    text = 'cоветник отдела Интернет проектов Управления информационных технологий'
    for el in value:

        if text in value:
            result = ','.join(value).replace(text, '')
            value[4] = text

        if el not in new_value:
            new_value.append(el)

    corrected_contact_list.append(new_value)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(corrected_contact_list)
