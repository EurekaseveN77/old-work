#James Carton
#2/12/2023
#hw 1
import random

n = [random.randint(0, 100) for _ in range(20)]

print("Random numbers:", n)

def find_max(n):
    max = n[0]
    
    for x in n:
        if x > max:
            max = x
    return max
    
max = find_max(n)

print("Largest number:", max)