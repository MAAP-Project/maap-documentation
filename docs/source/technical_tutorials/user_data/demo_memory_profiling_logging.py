from memory_profiler import profile

"""
... Code here
"""

fp=open('memory_profiler.log','w+')

@profile(stream=fp)

def my_function():
    # Include each line of the script which needs to be profiled
    # under this function
    
    return 0

if __name__ == "__main__":
    my_function()
    
    