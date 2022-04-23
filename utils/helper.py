import random, string

def generate_random_string():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + "-" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return random_string