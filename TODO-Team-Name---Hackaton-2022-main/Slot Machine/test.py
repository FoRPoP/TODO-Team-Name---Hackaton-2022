import string
from tokenize import String
from typing import List


def horisontalCheck(row):
    length = len(row)
    max_length, element = 0, None
    for i in range(length):
        current_length = 0
        for j in range(i, length):
            if row[i] == row[j] :
                current_length += 1
                if current_length >= max_length:
                    max_length, element =  current_length, row[i]
    return element, max_length

# TODO zameniti sa calculate_best_from_beggining
# def calculate_best(row):
    # length = len(row)
    # max_winnings, winnings = 0.0 , 0.0
    # for i in range(length):
        # current_length = 0
        # for j in range(i, length):
            # if row[i] == row[j]:
                # current_length += 1
            # #winnings = Payout.evaluate(row[i] , current_length)
            # if winnings > max_winnings:
                # max_winnings = winnings            
    # return max_winnings


lista = [x for x in range(15)]
element , duzina = horisontalCheck(lista)


def proba(zadato, treba):
    if zadato == treba:
        return True
    else:
        return False

pom_list = [x for i, x in enumerate(lista) if i == 10 or i == 0]

print(lista)
print(pom_list)

def intersection(list1, list2):
    return set(list1).intersection(pom_list)

#print(intersection(lista, pom_list))