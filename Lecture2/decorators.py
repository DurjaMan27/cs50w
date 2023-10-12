# decorators are higher-order functions that can modify other functions

def announce(f):
    def wrapper():
        print("About to run the function..")
        f()
        print("Done with the function.")
    return wrapper

@announce # means that the following function now has a decorator around it
def hello():
    print("Hello, world!")

hello()