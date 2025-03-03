import shlex


person = input()
place = input()

res = shlex.join(['register', person, place])
print(res)
print(shlex.split(res))
