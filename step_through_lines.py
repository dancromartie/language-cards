import sys

lines = sys.stdin.readlines()
sys.stdin = open("/dev/tty")
for line in lines:
    print(line)
    response = input("Hit enter to advance:")
