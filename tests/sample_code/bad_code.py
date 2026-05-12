# tests/sample_code/bad_code.py

def calculate(a, b, c, d, e, f, g):  
    x = 10  # unused variable
    
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:  
                    return a + b
    
    try:
        result = a / b
    except:  
        pass
    
    print("done") 
    
    return a + b