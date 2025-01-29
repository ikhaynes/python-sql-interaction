import pandas as pd
import mysql.connector
from mysql.connector import Error

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)

def helloWorld():
    print("Hello World!!")

def sqlGetResult(q, c):
    try:
        result = pd.read_sql(q, c)
        return result
    except Error as e:
        print("Error: ", e)
        return e

def openConnection():
    conn = mysql.connector.connect(
        user = 'root',
        password = 'password',
        host = 'localhost',
        database='COMPANY'
    )
    return conn
 
# ------------------------ ADD EMPLOYEE ------------------------
def addEmployee():
    conn = openConnection()
    cursor = conn.cursor()

    Fname : str = input("Enter employee first name: ")
    if (Fname in ['q', 'quit']):
        return
    Minit : str = input ("Enter employee middle initial: ")
    Lname : str= input("Enter employee last name: ")
    ssn : int = input("Enter employee ssn: ")
    Bdate : str = input("Enter employee birth date (YYYY-MM-DD): ")
    Address : str = input("Enter employee address: ")
    Sex : str = input("Enter employee sex: ")
    Salary : int = input("Enter employee salary: ")
    SuperSsn : int = input("Enter employee supervisor's ssn: ")
    Dno : int = input("Enter employee Department #: ")
    print()

    query = f"""
        INSERT INTO EMPLOYEE (Fname, Minit, Lname, 
        Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno)
        Values('{Fname}', '{Minit}', '{Lname}', {ssn}, '{Bdate}', 
        '{Address}', '{Sex}', {Salary}, {SuperSsn}, {Dno});"""

    try:
        cursor.execute(query)
        conn.commit()
        print()
        print("{} {}. {} added to EMPLOYEE".format(Fname, Minit, Lname))
        print()
    except Error as e:
        print()
        print("Error: ", e)
        print()

    conn.close()
    return

# ------------------------ VIEW EMPLOYEE ------------------------
def viewEmployee():
    conn = openConnection()
    
    # doesn't show data for dependents, include in another table?
    ssn = input("Enter employee ssn: ")
    if (ssn in ['q', 'quit']):
        return

    query = f"""
        SELECT E.*, T.Mgr_Fname, T.Mgr_Minit, T.Mgr_Lname, 
        T.Dname, D.Dependent_name FROM EMPLOYEE AS E LEFT JOIN 
        (SELECT Fname AS Mgr_Fname, Minit AS Mgr_Minit, 
        Lname AS Mgr_Lname, Ssn, Dname FROM EMPLOYEE AS S 
        JOIN DEPARTMENT AS D ON S.Ssn = D.Mgr_ssn) AS T 
        ON E.Super_ssn = T.Ssn LEFT JOIN DEPENDENT AS D ON 
        D.Essn = E.Ssn WHERE E.Ssn = {ssn};"""
    
    result = sqlGetResult(query, conn)
    print(result)
    print()

    conn.close()
    return


# ------------------------ MODIFY EMPLOYEE ------------------------
def modifyEmployee():

    conn = openConnection()
    cursor = conn.cursor()
    ssn = input("Enter ssn of employee to modify: ")
    if (ssn in ['q', 'quit']):
        return

    # lock row
    q1 = "BEGIN;"
    cursor.execute(q1)
    # cursor.execute(q2)

    query = f"""
        SELECT * FROM EMPLOYEE WHERE Ssn = {ssn} FOR UPDATE;"""
    print(sqlGetResult(query, conn) )
    print()

    # update item
    updateColumn = input("Enter column to update (Address, Sex, Salary, Super_ssn, Dno): ")
    print()
    updateValue = input("Enter the new value: ")
    print()

    query = f"""
        UPDATE EMPLOYEE SET 
        {updateColumn} = '{updateValue}' 
        WHERE Ssn = {ssn};"""
    cursor.execute(query)

    # unlock row
    cursor.execute("COMMIT;")
    
    print("Employee '{}' updated to '{}'".format(updateColumn, updateValue) )
    conn.close()
    return


# ------------------------ REMOVE EMPLOYEE ------------------------
def removeEmployee():
    conn = openConnection()
    cursor = conn.cursor()
    ssn = input("Enter ssn of employee to delete: ")
    if (ssn in ['q', 'quit']):
        return
    cursor.execute("BEGIN;")
    
    query = f"""SELECT * FROM EMPLOYEE WHERE Ssn = {ssn} FOR UPDATE;"""
    print(sqlGetResult(query, conn))
    print()

    confirm = input("Confirm removal (y/n): ")
    print()
    if (confirm in ['y', 'yes']):
        query = f"""DELETE FROM EMPLOYEE WHERE Ssn = {ssn};"""
        try:
            cursor.execute(query)
            print("Employee ({}) removed".format(ssn))
        except Error as e:
            print("Error: ", e)
    
    cursor.execute("COMMIT;")
    return


# ------------------------ ADD DEPENDENT ------------------------
def addDependent():
    conn = openConnection()
    cursor = conn.cursor()

    Essn : int = input("Enter employee ssn: ")
    if (Essn in ['q', 'quit']):
        return
    
    q1 = f"""
        SELECT * FROM DEPENDENT WHERE Essn = {Essn} FOR UPDATE"""
    try:
        r1 = pd.read_sql(q1, conn)
        if (r1.empty):
            print()
            print("Employee has no dependents")
            print()
        else:
            print()
            print(r1)
            print()
    except Error as e:
        print("Error: ", e)

    dependentName : str = input("Enter dependent's name: ")
    Sex : str = input("Enter dependent's sex: ")
    Bdate : str = input("Enter dependent's birth date (YYYY-MM-DD): ")
    relationship : str = input("Enter dependent's relationship to employee: ")

    query = f"""
        INSERT INTO DEPENDENT (Essn, Dependent_name, Sex, 
        Bdate, Relationship) Values({Essn}, '{dependentName}', 
        '{Sex}', '{Bdate}', '{relationship}');"""

    try:
        cursor.execute(query)
        conn.commit()
        print("{} added to DEPENDENT".format(dependentName))
    except Error as e:
        print("Error: ", e)

    conn.close()
    return

# ------------------------ REMOVE DEPENDENT ------------------------
def removeDependent():
    conn = openConnection()
    cursor = conn.cursor()
    ssn = input("Enter employee ssn: ")
    if (ssn in ['q', 'quit']):
        return
    cursor.execute("BEGIN;")
    
    query = f"""SELECT * FROM DEPENDENT WHERE Essn = {ssn} FOR UPDATE;"""
    r1 = sqlGetResult(query, conn)
    if (r1.empty):
        print("Employee has no dependents")
        print()
    else:
        print(r1)
        name = input("Enter name of dependent to be removed: ")
        confirm = input("Confirm removal of {} (y/n): ".format(name))
        print()
        if (confirm in ['y', 'yes']):
            query = f"""
                DELETE FROM DEPENDENT WHERE Essn = {ssn} 
                AND Dependent_name = '{name}';"""
            try:
                cursor.execute(query)
                print("Dependent ({}) removed".format(name))
            except Error as e:
                print("Error: ", e)
    print()
    cursor.execute("COMMIT;")

# ------------------------ ADD DEPARTMENT ------------------------
def addDepartment():
    conn = openConnection()
    cursor = conn.cursor()

    Dname : str = input("Enter department name: ")
    if (Dname in ['q', 'quit']):
        return
    Dnumber : int = input("Enter department number: ")
    mgrSsn : int = input("Enter manager ssn: ")
    mgrStart : str = input("Enter manager start date (YYYY-MM-DD): ")

    query = f"""
        INSERT INTO DEPARTMENT (Dname, Dnumber, 
        Mgr_ssn, Mgr_start_date) Values('{Dname}', 
        {Dnumber}, {mgrSsn}, '{mgrStart}');"""  

    try:
        cursor.execute(query)
        conn.commit()
        print("{} added to DEPARTMENT".format(Dname))
    except Error as e:
        print("Error: ", e)

    conn.close() 
    return 

# ------------------------ VIEW DEPARTMENT ------------------------
def viewDepartment():
    conn = openConnection()

    Dnumber : int = input("Enter department number: ")
    if (Dnumber in ['q', 'quit']):
        return

    query = f"""
        SELECT T.Dname, E.Fname, E.Minit, E.Lname, T.Dlocation
        FROM EMPLOYEE AS E JOIN (SELECT Dname, D.Dnumber, Mgr_ssn, 
        Dlocation FROM DEPARTMENT AS D LEFT JOIN DEPT_LOCATIONS 
        AS L ON D.Dnumber = L.Dnumber) AS T ON E.Ssn = T.Mgr_ssn 
        WHERE T.Dnumber = {Dnumber}"""
    
    result = sqlGetResult(query, conn)
    if (result.empty):
        print()
        print("There are no departments with number {}".format(Dnumber))
        print()
    else:
        print()
        print(result)
        print()

    conn.close()
    return

# ------------------------ REMOVE DEPARTMENT ------------------------
def removeDepartment():
    conn = openConnection()
    cursor = conn.cursor()

    Dnumber : int = input("Enter department number: ")
    if (Dnumber in ['q', 'quit']):
        return

    query = f"""SELECT * FROM DEPARTMENT WHERE Dnumber = {Dnumber} FOR UPDATE;"""
    
    r1 = sqlGetResult(query, conn)
    if (r1.empty):
        print("There are no departments with number {}".format(Dnumber))
        print()
    else:
        print(r1)
        confirm = input("Confirm removal of Department {} (y/n): ".format(Dnumber))
        print()
        if (confirm.lower() in ['y', 'yes']):
            query = f"""DELETE FROM DEPARTMENT WHERE Dnumber = {Dnumber};"""
            try:
                cursor.execute(query)
                conn.commit()
                print("Department ({}) removed".format(Dnumber))
            except Error as e:
                print("Error: ", e)
            print()
    conn.close()
    return

# ------------------------ ADD DEPARTMENT LOCATION------------------------
def addDeptLocation():
    conn = openConnection()
    cursor = conn.cursor()

    Dnumber : int = input("Enter department number: ")
    if (Dnumber in ['q', 'quit']):
        return

    query = f"""SELECT * FROM DEPT_LOCATIONS WHERE Dnumber = {Dnumber} FOR UPDATE;"""
    r1 = sqlGetResult(query, conn)

    if (r1.empty):
        print()
        print("There are no locations for department {}".format(Dnumber))
        print()
    else:
        print()
        print(r1)
        print()
        
    loc : str = input("Enter new department location: ")

    query = f"""
        INSERT INTO DEPT_LOCATIONS (Dnumber, Dlocation) 
        Values({Dnumber}, '{loc}');""" 
    cursor.execute(query)
    conn.commit()
    print("{} added for Department number {}".format(loc, Dnumber))
    conn.close()
    return

# ------------------------ REMOVE DEPARTMENT LOCATION------------------------
def removeDeptLocation():
    conn = openConnection()
    cursor = conn.cursor()

    Dnumber : int = input("Enter department number: ")
    if (Dnumber in ['q', 'quit']):
        return

    query = f"""SELECT * FROM DEPT_LOCATIONS WHERE Dnumber = {Dnumber} FOR UPDATE;"""
    
    r1 = sqlGetResult(query, conn)
    if (r1.empty):
        print()
        print("There are no locations for department {}".format(Dnumber))
        print()
    else:
        print(r1)
        Dlocation : str = input("Enter location to remove: ")
        confirm = input("Confirm removal of ocation {} (y/n): ".format(Dlocation))

        if (confirm.lower() in ['y', 'yes']):
            query = f"""
                DELETE FROM DEPT_LOCATIONS WHERE 
                Dnumber = {Dnumber} AND Dlocation = '{Dlocation}';"""
            try:
                cursor.execute(query)
                conn.commit()
                print()
                print("Location ({}) removed".format(Dlocation))
            except Error as e:
                print("Error: ", e)
    conn.close()
    return


if __name__ == "__main__":
    # addEmployee() # working 
    # viewEmployee() # working 
    # modifyEmployee() # working 
    # removeEmployee() # working 

    # addDependent() # working
    # removeDependent() # working

    # addDepartment() # working 
    # viewDepartment() # working
    # removeDepartment() # working 

    # addDeptLocation() # working
    # removeDeptLocation() # working
    
    print("Run using python3 -W ignore Interface.py")
