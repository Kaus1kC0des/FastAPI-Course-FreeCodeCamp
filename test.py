def generate():
    i = 0
    while True:
        yield i
        i += 1


g = generate()

# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))

print(g)
