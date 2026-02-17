import numbers
import random
def get_numbers_ticket(min, max, quantity):
    i = 0
    numbers = []
    while(len(numbers)) < quantity:
            num = random.randint(min, max)
            if num in numbers:
                continue
            numbers.append(num)
    print(numbers)
get_numbers_ticket(1, 60, 10)