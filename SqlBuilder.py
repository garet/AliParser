'''
Created on 25 окт. 2013 г.

@author: garet
'''

class SqlBuilder:
    def __init__(self, db, type_db, pref = '', debug = False):
        self.__db = db
        self.__pref = pref
        self.__debug = debug
        self.__type_db = type_db
        self.__sql = ''
        self.__start_where = False
        self.__count_params = 0
        self.__params = []
        self.__cursor = None
    
    def Select(self, columns = None):
        result = '*'
        if columns != None:
            result = ''
            for column in columns:
                if type(column) == dict:
                    while len(column) > 0:
                        item = column.popitem()
                        result += '{0} AS {1}, '.format(item[0], item[1])
                else:
                    result += '{0}, '.format(column)
            result = result.strip(', ')
        self.__sql += 'SELECT {0}\r'.format(result)
        return self
    
    def Update(self, table, columns = None):
        result = ''
        for key, value in columns.items():
            result += '{0}={1},'.format(key, '%s')
            self.__params.append(value)
            self.__count_params += 1
        result = result.strip(', ')
        
        sql_tmp = 'UPDATE {0} SET {1}'
        self.__sql += sql_tmp.format(self.__pref + table, result)
        return self
    
    def From(self, tables):
        result = ''
        if type(tables) == str:
            result = '{0}'.format(tables)
        elif type(tables) == list or type(tables) == tuple:
            for table in tables:
                if type(table) == dict:
                    while len(table) > 0:
                        item = table.popitem()
                        result += '{0} AS {1}, '.format(item[0], item[1])
                else:
                    result += '{0}, '.format(table)
            result = result.strip(', ')
        self.__sql += 'FROM {0} \r'.format(result)
        return self
    
    def OrderBy(self, params):
        str_params = ''
        if type(params) == str:
            str_params = params
        else:
            for param in params:
                str_params += '{0},'.format(param)
            str_params = str_params.strip(', ')
        self.__sql += 'ORDER BY {0}\r'.format(str_params)
        return self
    
    def InnerJoin(self, table, condict):
        self.__sql += 'INNER JOIN {0} ON {1}\r'.format(table, condict)
        return self
    
    def LeftJoin(self, table, condict):
        self.__sql += 'LEFT JOIN {0} ON {1}\r'.format(table, condict)
        return self
    
    def RightJoin(self, table, condict):
        self.__sql += 'RIGHT JOIN {0} ON {1}\r'.format(table, condict)
        return self
    
    def FullJoin(self, table, condict):
        self.__sql += 'FULL JOIN {0} ON {1}\r'.format(table, condict)
        return self
    
    def Delete(self, table):
        self.__sql += 'DELETE FROM {0}\r'.format(table)
        return self
    
    def Where(self, condict, param = None):
        if self.__start_where:
            self.__sql += 'AND {0} '.format(condict)
        else:
            self.__sql += 'WHERE \r{0} \r'.format(condict)
            self.__start_where = True
        if param != None:
            self.__count_params += 1
            self.__params.append(param)
        return self
    
    def WhereOr(self, condict, param = None):
        if self.__start_where:
            self.__sql += 'OR {0} '.format(condict)
        else:
            self.__sql += 'WHERE \r\t{0} \r'.format(condict)
            self.__start_where = True
        if param != None:
            self.__count_params += 1
            self.__params.append(param)
        return self
    
    def Insert(self, table, values):
        result = ''
        params = ''
        for key, value in values.items():
            result += '{0},'.format(key)
            params += '{0},'.format('%s')
            self.__params.append(value)
            self.__count_params += 1
        result = result.strip(', ')
        params = params.strip(', ')
        
        sql_tmp = 'INSERT INTO {0}({1}) VALUES ({2})'
        self.__sql += sql_tmp.format(self.__pref + table, result, params)
        return self
    
    def Limit(self, limit, offset = None):
        if type(limit) != int or type(offset) != int:
            raise 'SqlBuilder.Limit: Params might only Integer!'
        if offset != None:
            if self.__type_db != 'pg':
                self.__sql += 'LIMIT {0},{1} \r'.format(limit, offset)
            else:
                self.__sql += 'LIMIT {0} \r'.format(limit)
                self.__sql += 'OFFSET {0} \r'.format(offset)
        else:
            self.__sql += 'LIMIT {0} \r'.format(limit)
        return self
    
    def Execute(self, params = None):
        self.__sql = self.__sql.replace('{pref}', self.__pref).strip() + ';'
        if self.__debug:
            print(self.__sql)
            print()
        if len(params) > 0 and self.__count_params == 0:
            for param in params:
                self.__params.append(param)
                self.__count_params += 1
        if self.__cursor != None:
            self.__cursor.close()
        else:
            self.__cursor == None
        self.__cursor = self.__db.cursor()
        try:
            if self.__count_params > 0:
                self.__cursor.execute(self.__sql, self.__params)
            else:
                self.__cursor.execute(self.__sql)
        except Exception as e:
            print('Error: {0}'.format(e.args))
            self.__db.rollback()
            self.Clear()
            return False
        else:
            self.__db.commit()
            self.Clear()
        return True
    
    def Clear(self):
        self.__start_where = False
        self.__count_params = 0
        del(self.__params)
        self.__params = []
        self.__sql = ''
    
    def FetchOne(self):
        return self.__cursor.fetchone()
    
    def FetchMany(self, size = None):
        raise 'Not realise!'
        if size != None:
            return self.__cursor.fetchmany(size)
        else:
            return self.__cursor.fetchmany()
    
    def FetchAll(self):
        return self.__cursor.fetchall()
    
    def Commit(self):
        return self.__db.commit()