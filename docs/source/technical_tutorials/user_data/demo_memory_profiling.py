from memory_profiler import profile

"""
... Code here
"""

@profile
def my_function():
    # Include each line of the script which needs to be profiled
    # under this function
    print("Hello, world!")
    
    return 0

if __name__ == "__main__":
    my_function()