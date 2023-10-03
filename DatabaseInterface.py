# Imports
import sqlite3

successOutput = "Success!"
failureOutput = "Error!"

def connectToServer():
  try:
    connection = sqlite3.connect("itemsdb.db")
    
    return [successOutput, connection]
  
  except:
    return [failureOutput]
  
  
def selectAllData(tableName):
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
      
    cursor.execute(f'''SELECT * FROM {tableName}''')

    result = cursor.fetchall()
    
    conn[1].close()
    return [successOutput, result]
 
  except:
    return [failureOutput]


def getTables():
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
      
    cursor.execute('''SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';''')
    result = cursor.fetchall()
    
    conn[1].close()
    return [successOutput, result]
 
  except:
    return [failureOutput]
  
  
def selectColumnData(tableName, columnName):
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
      
    cursor.execute(f'''SELECT {columnName} FROM {tableName};''')

    result = cursor.fetchall()
    
    conn[1].close()
    return [successOutput, result]

  except:
    return [failureOutput]
  
  
def executeQuery(query):
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
    
    cursor.execute(query)
    
    conn[1].commit()
    
    conn[1].close()
    return successOutput

  except:
    return failureOutput
  
  
def resetDatabase():
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
    
    cursor.execute('''DROP TABLE IF EXISTS items''')
    cursor.execute('''CREATE TABLE items(itemID INTEGER PRIMARY KEY AUTOINCREMENT, itemName VARCHAR(40) NOT NULL, itemStock INTEGER NOT NULL)''')
    cursor.execute('''INSERT INTO items (itemName, itemStock) VALUES ('Apples', 200)''')
    cursor.execute('''INSERT INTO items (itemName, itemStock) VALUES ('Bananas', 100)''')
    cursor.execute('''INSERT INTO items (itemName, itemStock) VALUES ('Oranges', 50)''')
    
    conn[1].commit()
    
    conn[1].close()
      
    return successOutput
  
  except:
    return failureOutput