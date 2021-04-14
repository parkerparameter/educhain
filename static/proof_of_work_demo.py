### disutile script - do not use in any deployment

from hashlib import sha256

hidden = 5

guess = 0

while sha256(f'{hidden*guess}'.encode()).hexdigest()[-1] != "0":

    guess += 1

print(f'Solution is {guess}')