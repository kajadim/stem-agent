# Benchmark case 1 — security issues
def get_user(username):
    query = "SELECT * FROM users WHERE name = " + username
    return query

# Benchmark case 2 — resource leak  
def read_file(path):
    f = open(path)
    data = f.read()
    return data

# Benchmark case 3 — logic bug
def is_adult(age):
    if age > 18:
        return True
    if age == 18:
        return True
    if age > 21:
        return True
    return False

# Benchmark case 4 — exception handling
def divide(a, b):
    try:
        return a / b
    except:
        pass

# Benchmark case 5 — complexity
def process(a, b, c, d, e, f):
    x = 0
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    x = a + b + c + d
    print(x)
    return x