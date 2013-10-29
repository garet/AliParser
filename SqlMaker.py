'''
Created on 26 окт. 2013 г.

@author: garet
'''

import psycopg2.extras


class SqlMaker:
    def __init__(self, conn, type_db, pref = '', debug = False):
        self.__sql = ''
        self.__params = []
        self.__count_params = 0
        self.__start_where = False
        self.__cursor = None
        self.__debug = debug
        self.__type_db = type_db
        self.__conn = conn
        self.__pref = pref
        
    def __str__(self):
        return self.__sql
    
    def DebugPrint(self):
        str_tmp = 'SQL: \r{0}\r'
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
    
    # Not tested
    def InnerJoin(self, table, condict):
        self.__sql += 'INNER JOIN {0} ON {1}\r'.format(table, condict)
        return self
    
    # Not tested
    def LeftJoin(self, table, condict):
        self.__sql += 'LEFT JOIN {0} ON {1}\r'.format(table, condict)
        return self
    
    # Not tested
    def RightJoin(self, table, condict):
        self.__sql += 'RIGHT JOIN {0} ON {1}\r'.format(table, condict)
        return self
    
    # Not tested
    def FullJoin(self, table, condict):
        self.__sql += 'FULL JOIN {0} ON {1}\r'.format(table, condict)
        return self
    
    # Not tested
    def Delete(self, table):
        self.__sql += 'DELETE FROM {0}\r'.format(table)
        return self
    
    # Not tested
    def Where(self, condict, param=None):
        if self.__start_where:
            self.__sql += 'AND {0}\r'.format(condict)
        else:
            self.__sql += 'WHERE \r{0}\r'.format(condict)
            self.__start_where = True
        if param != None:
            self.__count_params += 1
            self.__params.append(param)
        return self
    
    # Not tested
    def WhereOr(self, condict, param=None):
        if self.__start_where:
            self.__sql += 'OR {0}\r'.format(condict)
        else:
            self.__sql += 'WHERE \r{0}\r'.format(condict)
            self.__start_where = True
        if param != None:
            self.__count_params += 1
            self.__params.append(param)
        return self

    def Insert(self, table, *args):
        result = ''
        params = ''
        for arg in args:
            values = arg.popitem()
            result += '{0},'.format(values[0])
            params += '{0},'.format('%s')
            self.__params.append(values[1])
            self.__count_params += 1
        result = result.strip(', ')
        params = params.strip(', ')
        
        sql_tmp = 'INSERT INTO {0}({1}) VALUES ({2})'
        self.__sql += sql_tmp.format(table, result, params)
        return self

    def Execute(self, *args):
        self.__sql = self.__sql.replace('{pref}', self.__pref).strip() + ';'
        if self.__debug:
            print(self.__sql)
            print()
        #if len(args) > 0 and self.__count_params == 0:
        for param in args:
            self.__params.append(param)
            self.__count_params += 1
        if self.__cursor != None:
            self.__cursor.close()
        else:
            self.__cursor == None
        self.__cursor = self.__conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            if self.__count_params > 0:
                self.__cursor.execute(self.__sql, self.__params)
            else:
                self.__cursor.execute(self.__sql)
        except Exception as e:
            print('Error: {0}'.format(e.args))
            self.__conn.rollback()
            self.Clear()
            return False
        else:
            self.__conn.commit()
            self.Clear()
        return True
    
    def FetchOne(self):
        return self.__cursor.fetchone()

    def FetchAll(self):
        return self.__cursor.fetchall()

    def Clear(self):
        self.__start_where = False
        self.__count_params = 0
        del(self.__params)
        self.__params = []
        self.__sql = ''