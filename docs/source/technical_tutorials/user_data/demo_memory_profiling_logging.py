from memory_profiler import profile

fp=open('memory_profiler.log','w+')
@profile(stream=fp)
def my_function():
    # Include each line of the script which needs to be profiled
    # under this function
    
    return 0

@profile(stream=fp)
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
    
    