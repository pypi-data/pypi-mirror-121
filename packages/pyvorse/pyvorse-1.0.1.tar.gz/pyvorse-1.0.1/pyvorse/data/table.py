__all__ = ["Table", "Column", "Row"]

from pyvorse.core import basis
from pyvorse.data.positioned import poslist

class Column(basis):
    "Represents headers for tables"
    def __init__(self, name: str, align: int = 0, default = None):
        self.name = name
        self.align = align
        self.default = default
    
    def alignLeft(self):
        self.align = -1
    
    def alignCenter(self):
        self.align = 0
    
    def alignRight(self):
        self.align = 1
    
    def alignSwitch(self):
        self.align *= -1
    
    def setdefault(self, default):
        self.default = default

class Row(poslist, basis):
    "Represents datarow, positioned, based on dict, but behave like list"

class ColumnData(basis):
    "Contains all data about table row"
    def __init__(self, header: Column, *dataset):
        self.header = header
        self.data = dataset
    
    def __getitem__(self, index):
        return self.data[index]

class Table(basis):
    """Contains columns and rows. You can use functions as values and get items by .getsmart, function will be called
    with 3 arguments, link to table object, indexes for row and column. That allows dynamic calculated values, like summary."""
    def __init__(self, *columns: Column):
        super(Table, self).__init__()
        self.columns = [*columns]
        self.rows = []
    
    def cleardata(self):
        self.rows = []
    
    def clearall(self):
        self.cleardata()
        self.columns = []
    
    def append(self, row: Row):
        self.rows.append(row)
        return self
    
    def appends(self, *items, trigger=None):
        self.rows.append(Row(*items, trigger=trigger))
        return self
    
    def addheader(self, header: Column):
        self.columns.append(header)
    
    def adddefaultheader(self, name: str, align: int = 0, default=None):
        self.columns.append(Column(name, align, default))
    
    def getrow(self, index: int):
        return self.rows[index]
    
    def getheader(self, index: int):
        return self.columns[index]
    
    def getcolumn(self, index: int):
        res = []
        for row in self.rows:
            res.append(row.getor(index, self.columns[index].default))
        return ColumnData(self.columns[index], *res)
    
    def getitem(self, row, col):
        return self.rows[row].getor(col, self.columns[col].default)
    
    def setitem(self, row, col, value):
        self.rows[row][col] = value
        return self
    
    def delitem(self, row, col):
        return self.setitem(row, col, self.columns[col].default)
    
    def getdynamic(self, row, col):
        item = self.getitem(row, col)
        return item if not callable(item) else item(self, row, col)

    def __getitem__(self, index):
        return self.getcolumn(index)
