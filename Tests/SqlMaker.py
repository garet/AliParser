'''
Created on 26 окт. 2013 г.

@author: garet
'''

import unittest

from SqlMaker import *
  
  
class TestClassA(unittest.TestCase):
    def test_select_1(self):
        obj = SqlMaker()
        obj.Select('c1', 'c2', {'c3': 'column'})
        self.assertEqual('SELECT c1, c2, c3 AS column\r', str(obj))
        
    def test_select_2(self):
        obj = SqlMaker()
        obj.Select('c1', 'c2')
        self.assertEqual('SELECT c1, c2\r', str(obj))
        
    def test_select_3(self):
        obj = SqlMaker()
        obj.Select('c1')
        self.assertEqual('SELECT c1\r', str(obj))

    def test_select_4(self):
        obj = SqlMaker()
        obj.Select()
        self.assertEqual('SELECT *\r', str(obj))
        
    def test_select_5(self):
        obj = SqlMaker()
        obj.Select('c1', {'c2': 'column'}, 'c3')
        self.assertEqual('SELECT c1, c2 AS column, c3\r', str(obj))
        
    def test_select_6(self):
        obj = SqlMaker()
        self.assertRaises(Exception, obj.Select, 'c1', None)
        
    def test_select_7(self):
        obj = SqlMaker()
        self.assertRaises(Exception, obj.Select, None)
        
    def test_select_8(self):
        obj = SqlMaker()
        self.assertRaises(Exception, obj.Select, {'c2': 'column'}, None, 'c1')

    def test_from_1(self):
        obj = SqlMaker()
        obj.From('c1', 'c2')
        self.assertEqual('FROM c1, c2\r', str(obj))
        
    def test_from_2(self):
        obj = SqlMaker()
        obj.From('c1')
        self.assertEqual('FROM c1\r', str(obj))
        
    def test_from_3(self):
        obj = SqlMaker()
        obj.From('c1', 'c2', {'c3': 'a'})
        self.assertEqual('FROM c1, c2, c3 AS a\r', str(obj))
        
    def test_from_4(self):
        obj = SqlMaker()
        self.assertRaises(Exception, obj.From)
        
    def test_from_5(self):
        obj = SqlMaker()
        self.assertRaises(Exception, obj.From, None)
        
    def test_from_6(self):
        obj = SqlMaker()
        obj.From({'c3': 'a'})
        self.assertEqual('FROM c3 AS a\r', str(obj))
        
    def test_update_1(self):
        obj = SqlMaker()
        obj.Update('table', {'a1': 0})
        self.assertEqual('UPDATE table SET a1 = %s\r', str(obj))
        
    def test_update_2(self):
        obj = SqlMaker()
        obj.Update('table', {'a1': 0}, {'a2': 'asd'})
        self.assertEqual('UPDATE table SET a1 = %s, a2 = %s\r', str(obj))
        
    def test_update_3(self):
        obj = SqlMaker()
        self.assertRaises(Exception, obj.Update, 'table')
        
    def test_update_4(self):
        obj = SqlMaker()
        self.assertRaises(Exception, obj.Update, 'table', 'a1')

if __name__ == "__main__":
    unittest.main()
