import cowsay
import sys

f = open("deadpool-face.cow")
print(cowsay.cowsay(sys.argv[1], cowfile=cowsay.read_dot_cow(f)))
