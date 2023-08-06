import pyodbc

def get_pti(username, password):
    return pyodbc.connect(
        'DSN=get_pti; UID='+ username +'; PWD=' + password + '; Directory=T:\Sage\Sage 100 Standard\MAS90; Prefix=T:\Sage\Sage 100 Standard\MAS90\SY, T:\Sage\Sage 100 Standard\MAS90\==\; ViewDLL=T:\Sage\Sage 100 Standard\MAS90\Home; Company=PTI; LogFile=\PVXODBC.LOG; DirtyReads=1; BurstMode=1; StripTrailingSpaces=1;',
        autocommit=True)

def get_cdu(username, password):
    return pyodbc.connect(
        'DSN=get_cdu; UID='+ username +'; PWD=' + password + '; Directory=Z:\Sage\Sage 100 Standard\MAS90; Prefix=Z:\Sage\Sage 100 Standard\MAS90\SY, Z:\Sage\Sage 100 Standard\MAS90\==\; ViewDLL=Z:\Sage\Sage 100 Standard\MAS90\Home; Company=CDU; LogFile=\PVXODBC.LOG; DirtyReads=1; BurstMode=1; StripTrailingSpaces=1;',
        autocommit=True)

def get_cyc(username, password):
    return pyodbc.connect(
        'DSN=cyc_test; UID='+ username +'; PWD=' + password + '; Directory=D:\CYC1028\CYC\Sage\Sage 100 Standard\MAS90; Prefix=D:\CYC1028\CYC\Sage\Sage 100 Standard\MAS90\SY, D:\CYC1028\CYC\Sage\Sage 100 Standard\MAS90\==\; ViewDLL=D:\CYC1028\CYC\Sage\Sage 100 Standard\MAS90\HOME; Company=CYC; LogFile=\PVXODBC.LOG; DirtyReads=1; BurstMode=1; StripTrailingSpaces=1;',
        autocommit=True)



