import random
import string

def generate_pnr():
    return ''.join(random.choices(string.digits, k=10))

def generate_seat():
    coach = random.choice(['A', 'B', 'C', 'D'])
    number = random.randint(1, 72)
    return f"{coach}{number}"