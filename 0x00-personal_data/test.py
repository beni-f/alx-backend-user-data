import re

messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]
fields = ["password", "date_of_birth"]

new_messages = []
for message in messages:
    message = message.split(';')
    print(message)
    new_messages.append(message)

print(new_messages)

for message in new_messages:
    for field in fields:
        pattern = r'{}=\w;$'.format(field)
        re.sub(pattern, '{}=xxx'.format(field), message)

print(new_messages)