# Imports
import sys # Only needed for access to command line arguments
import DatabaseInterface

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
  QApplication,
  QMainWindow,
  QPushButton,
  QVBoxLayout,
  QLabel,
  QWidget,
  QTableWidget,
  QTableWidgetItem,
  QFormLayout,
  QComboBox,
  QSpinBox,
  QMessageBox
)



# Class: Main Menu
class MainMenu(QWidget):
  def __init__(self):
    super().__init__()
    
    # Setup
    self.setWindowTitle("Main Menu")
    self.setFixedSize(QSize(300, 200))
    
    
    # Buttons
    self.databaseViewButton = QPushButton("Database View")
    self.databaseViewButton.clicked.connect(self.openDatabaseView)
    self.itemChooserButton = QPushButton("Choose Items")
    self.itemChooserButton.clicked.connect(self.openItemChooserView)
    self.resetButton = QPushButton("Initialize/Reset Database")
    self.resetButton.clicked.connect(self.resetDatabase)
    
    
    # Layout
    self.outerVLayout = QVBoxLayout()
    self.outerVLayout.addWidget(self.databaseViewButton)
    self.outerVLayout.addWidget(self.itemChooserButton)
    self.outerVLayout.addWidget(self.resetButton)
    
    self.setLayout(self.outerVLayout)
    
    
  def openDatabaseView(self):
    self.w = DataBaseViewWindow()
    self.w.show()
    
    
  def openItemChooserView(self):
    self.w = ItemChooserWindow()
    self.w.show()
    
  
  def resetDatabase(self):
    result = DatabaseInterface.resetDatabase()
    
    notifDialog = QMessageBox(self)
    notifDialog.setWindowTitle("Status")
    notifDialog.setText(result)
    notifDialog.exec()
    
    

# Class: Main Window
class DataBaseViewWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    
    # Setup
    self.setWindowTitle("View a Table")
    self.setFixedSize(QSize(800, 400))
    
    
    # Labels
    self.label = QLabel()
    self.label.setWordWrap(True)
    
    
    # Test Boxes
    self.tableName = QComboBox()
    tableOutput = DatabaseInterface.getTables()
    tableList = []
    if tableOutput[0] == DatabaseInterface.successOutput:
      for item in tableOutput[1]:
        tableList.append(item[0])
      self.tableName.addItems(tableList)
    
    
    # Buttons
    self.button = QPushButton("Update!")
    self.button.clicked.connect(self.updateTable)
    
    
    # Table
    self.tableWidget = QTableWidget()
    self.tableWidget.setRowCount(5)
    self.tableWidget.setColumnCount(6)
    
    
    # Form
    self.formLayout = QFormLayout()
    self.formLayout.addRow("Table:", self.tableName)
    
    
    # Layout
    layout = QVBoxLayout()
    layout.addLayout(self.formLayout)
    layout.addWidget(self.button)
    layout.addWidget(self.tableWidget)
    
    container = QWidget()
    container.setLayout(layout)
    
    self.setCentralWidget(container)
      
  
  def updateTable(self):
    result = DatabaseInterface.selectAllData(self.tableName.currentText())
    
    
    if result[0] == DatabaseInterface.successOutput:
      result = result[1]
      
      self.tableWidget.setRowCount(0)
      self.tableWidget.setColumnCount(len(result[0]))
      
      for row_number, row_data in enumerate(result):
        self.tableWidget.insertRow(row_number)
        
        for column_number, data in enumerate(row_data):
          self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
              
    

# Class: Item Chooser Window    
class ItemChooserWindow(QWidget):
  def __init__(self):
    super().__init__()
    
    # Setup
    self.setWindowTitle("Item Chooser")
    self.setFixedSize(QSize(250,150))
    
    
    # Combo Boxes
    self.itemComboBox = QComboBox()
    itemOutput = DatabaseInterface.selectColumnData("items", "itemName")
    itemList = []
    if itemOutput[0] == DatabaseInterface.successOutput:
      for item in itemOutput[1]:
        itemList.append(item[0])
      self.itemComboBox.addItems(itemList)
      
      
    # Spin Boxes
    self.itemQuantitySpinner = QSpinBox()
    self.itemQuantitySpinner.setMinimum(-100000000)
    
    
    # Buttons
    self.confirmButton = QPushButton("Confirm!")
    self.confirmButton.clicked.connect(self.processOrder)
    
    
    # Form Layout
    self.mainFormLayout = QFormLayout()
    self.mainFormLayout.addRow("Item:", self.itemComboBox)
    self.mainFormLayout.addRow("Quantity:" , self.itemQuantitySpinner)
    
    
    # Layout
    self.outerVLayout = QVBoxLayout()
    self.outerVLayout.addLayout(self.mainFormLayout)
    self.outerVLayout.addWidget(self.confirmButton)
    
    self.setLayout(self.outerVLayout)
    
    
  def processOrder(self):
    itemName = self.itemComboBox.currentText()
    itemQuantity = self.itemQuantitySpinner.value()
    
    query = f'''UPDATE items SET itemStock = itemStock - {itemQuantity} WHERE itemName = "{itemName}"'''
    
    result = DatabaseInterface.executeQuery(query)
    
    notifDialog = QMessageBox(self)
    notifDialog.setWindowTitle("Status")
    notifDialog.setText(result)
    notifDialog.exec()
    
    
# One QApplication instance required per application.
# Passing in sys.argv to allow command line arguments.
app = QApplication(sys.argv)

window = MainMenu()
window.show()

# Start the event loop.
app.exec()

# After Exit