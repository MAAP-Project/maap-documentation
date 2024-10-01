from memory_profiler import profile

@profile
def my_function():
    # Include each line of the script which needs to be profiled
    # under this function
    
    return 0

@profile
def my_other_function():
    # Include each line of the script which needs to be profiled
    # under this function
    
    return 0

def main():
    my_function()
    my_other_function()
    
    #...

if __name__ == "__main__":
    main()