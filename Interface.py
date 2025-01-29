import databaseInteraction as di

def printHelp():
    print("----------- User Help -----------")
    print("h -- view options")
    print("q -- quit program")
    print()
    print("1 -- Add new employee")
    print("2 -- View employee")
    print("3 -- Modify employee")
    print("4 -- Remove employee")
    print()
    print("5 -- Add new dependent")
    print("6 -- Remove dependent")
    print()
    print("7 -- Add new department")
    print("8 -- View department")
    print("9 -- Remove department")
    print()
    print("10 -- Add department location")
    print("11 -- Remove department location")

def main():
    usrInput : str = input("\nType 'h' to view options or enter the option: ")
    print()

    if(usrInput in ['h', 'help']):
        printHelp()
    elif(usrInput in ['q', 'quit']):
        exit()
    elif (usrInput == '1'):
        di.addEmployee()
    elif (usrInput == "2"):
        di.viewEmployee()
    elif (usrInput == '3'):
        di.modifyEmployee()
    elif (usrInput == '4'):
        di.removeEmployee()
    elif (usrInput == '5'):
        di.addDependent()
    elif (usrInput == '6'):
        di.removeDependent()
    elif (usrInput == '7'):
        di.addDepartment()
    elif (usrInput == '8'):
        di.viewDepartment()
    elif (usrInput == '9'):
        di.removeDepartment()
    elif (usrInput == '10'):
        di.addDeptLocation()
    elif (usrInput == '11'):
        di.removeDeptLocation()
    else:
        print("Unkown input\n")
        printHelp()

if __name__ == "__main__":
    print("* * *  Run using python3 -W ignore Interface.py to silence alchemy warnings  * * *")
    i = 0
    while True:
        main()