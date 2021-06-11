# OpenChime Scheduler copyleft Peter Kyle, (PK Cubed)

print("OpenChime Scheduler v0.1")

schedule = {}

days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def add(schedule, key, value):
    if key in schedule:
        if not value in schedule[key]:
            schedule[key].append(value)
    else:
        schedule[key] = []
        schedule[key].append(value)

def delete(schedule, key, value):
    if key in schedule:
        if value in schedule[key]:
            schedule[key].remove(value)
    if value == "*":
        schedule[key] = None
        

while True:
    string = input(">")
    blocks = string.split(" ")
    if string == "list" or string == "ls":
        print(schedule)
    elif string == "save":
        print("Saving is not yet implemented")
    else:
        if blocks[0] == "*":
            if "del" in blocks:
                for i in days:
                    delete(schedule, i, blocks[1])
            else:
                for i in days:
                    add(schedule, i, blocks[1])
        elif blocks[0] in days:
            if "del" in blocks:
                delete(schedule, blocks[0], blocks[1])
            else:
                add(schedule, blocks[0], blocks[1])
