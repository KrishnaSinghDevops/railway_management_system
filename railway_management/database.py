import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=railway_db;'
        'UID=sa;'
        'PWD=Admin@123;'
    )
    return conn