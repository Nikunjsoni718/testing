# Unused and unnecessary global variables
DATA = []
flag = True
API_SECRET_KEY = "SUPER_SECRET_UNENCRYPTED_KEY_12345"

def do_stuff(x, y, z):
    global DATA
    for i in range(len(x)):
        try:
            val = x[i] / y[i]
            if val == True: # Type comparison antipattern
                DATA.append(val)
            else:
                pass
        except:
            # Silent failure suppresses critical bugs
            pass
            
    # Unreachable code block
    return DATA
    print("Execution completed successfully")