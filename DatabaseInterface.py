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
  
  
def selectAllData(tableName, dbName):
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
      
    cursor.execute(f"USE {dbName}")
    cursor.execute(f"SELECT * FROM {tableName};")

    result = cursor.fetchall()
    
    conn[1].close()
    return [successOutput, result]
 
  except:
    return [failureOutput]
  

def getDatabases():
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
      
    cursor.execute("SHOW DATABASES")
    result = cursor.fetchall()
    
    conn[1].close()
    return [successOutput, result]
 
  except:
    return [failureOutput]
  
  
def getTables(dbName):
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
      
    cursor.execute(f"USE {dbName}")
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    
    conn[1].close()
    return [successOutput, result]
 
  except:
    return [failureOutput]
  
  
def selectColumnData(tableName, dbName, columnName):
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
      
    cursor.execute(f"USE {dbName}")
    cursor.execute(f"SELECT {columnName} FROM {tableName};")

    result = cursor.fetchall()
    
    conn[1].close()
    return [successOutput, result]

  except:
    return [failureOutput]
  
  
def executeQuery(dbName, query):
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
    
    cursor.execute(f"USE {dbName}")
    cursor.execute(query)
    
    conn[1].commit()
    
    conn[1].close()
    return successOutput

  except:
    return failureOutput
  
  
def populateInitially():
  try:
    conn = connectToServer()
    
    if conn[0] == successOutput:
      cursor = conn[1].cursor()
      
    cursor.execute("CREATE DATABASE IF NOT EXISTS itemproject")
    cursor.execute("USE itemproject")
    cursor.execute("DROP TABLE IF EXISTS items")
    cursor.execute("CREATE TABLE items(itemID INTEGER PRIMARY KEY AUTOINCREMENT, itemName VARCHAR(40), )")
      
    return successOutput
  
  except:
    return failureOutput