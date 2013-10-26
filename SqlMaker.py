'''
Created on 26 окт. 2013 г.

@author: garet
'''


class SqlMaker:
    def __init__(self):
        self.__sql = ''
        self.__params = []
        self.__count_params = 0
    
    def __str__(self):
        return self.__sql
    
    def DebugPrint(self):
        str_tmp = 'SQL: {0}\r'
        str_tmp += 'Count params: {1}\r'
        str_tmp += 'Params list: {2}'
        print(str_tmp.format(self.__sql, self.__count_params, self.__params))
    
    def Select(self, *args):
        result = ''
        for column in args:
            if type(column) != dict:
                if column == None:
                    raise Exception("SqlMaker: Argument 'Select' can`t be None.")
                result += '{0}, '.format(column)
                continue
            while len(column) > 0:
                item = column.popitem()
                result += '{0} AS {1}, '.format(item[0], item[1])
        result = result.strip(', ')
        if len(args) == 0:
            result = '*'
        self.__sql += 'SELECT {0}\r'.format(result)
        return self

    def From(self, *args):
        result = ''
        if len(args) == 0:
            raise Exception("SqlMaker: Argument 'From' can`t be None.")
        for table in args:
            if type(table) == dict:
                item = table.popitem()
                result += '{0} AS {1}, '.format(item[0], item[1])
            else:
                if table == None:
                    raise Exception("SqlMaker: Argument 'Select' can`t be None.")
                result += '{0}, '.format(table)
        result = result.strip(', ')
        self.__sql += 'FROM {0}\r'.format(result)
        return self

    def Update(self, table, *args):
        result = ''
        if len(args) == 0:
            raise Exception("SqlMaker: Counts arguments 'Update' is 0.")
        for item in args:
            if type(item) != dict:
                raise Exception("SqlMaker: Argument 'Update' can`t be not dict.")
            values = item.popitem()
            result += '{0} = {1}, '.format(values[0], '%s')
            self.__params.append(values[1])
            self.__count_params += 1
        result = result.strip(', ')
        sql_tmp = 'UPDATE {0} SET {1}\r'
        self.__sql += sql_tmp.format(table, result)
        return self


#obj = SqlMaker()
#obj.Update('table', 'a0', {'a1': 0}, {'a2': '111'})
#obj.DebugPrint()