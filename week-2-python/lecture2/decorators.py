# Functional Programming: decorators


# Define a function called "announce" that takes a function as an argument.
def announce(f):
    # Define an inner function called "wrapper" that will be returned by the "announce" function.
    def wrapper():
        # Print a message before running the function passed as an argument.
        print("About to run the function...")
        # Call the function passed as an argument.
        f()
        # Print a message after running the function passed as an argument.
        print("Done with the function.")

    # Return the inner function "wrapper".
    return wrapper


# Use the "@" symbol followed by the function name "announce" as a decorator to modify the behavior of the "hello" function.
@announce
# Define a function called "hello".
def hello():
    # Print the message "Hello, world!".
    print("Hello, world!")


# Call the modified "hello" function.
hello()
