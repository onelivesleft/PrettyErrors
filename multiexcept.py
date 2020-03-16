
try:
    myval = [1,2]
    print(myval[3])
except:
    try:
        print(foo)
    except:
        print("First exception")
        raise OSError
