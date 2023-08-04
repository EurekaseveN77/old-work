#James Carton
# 2/19/2023
# hw#2

with open("ingest_this.txt") as open:
    input = open.read()

vowels = "aeiouAEIOU"
for letter in vowels:
    input = input.replace(letter, "9")

print(input)