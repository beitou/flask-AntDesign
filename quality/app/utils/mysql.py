
import pymysql


class Mysql():

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        host = "172.16.0.115"
        if 'host' in kwargs and kwargs['host']:
            host = kwargs['host']

        user = "app"
        if 'user' in kwargs and kwargs['user']:
            user = kwargs['user']

        password = "Yc)E7aqYU6)AjW"
        if 'password' in kwargs and kwargs['password']:
            password = kwargs['password']

        database = None
        if 'database' in kwargs and kwargs['database']:
            database = kwargs['database']

        charset = "utf8"
        if 'charset' in kwargs and kwargs['charset']:
            charset = kwargs['charset']

        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def create(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        # 如果指定数据库则选中数据库
        if 'database' in kwargs and kwargs['database']:
            self.conn.select_db(kwargs.pop('database'))

        # 插入数据必须指定插入到那个表中
        if 'table' not in kwargs or not kwargs['table']:
            return None
        table = kwargs.pop('table')

        # 如果没有要插入的数据或要插入的数据不是字典类型
        if 'data' not in kwargs and not kwargs['data'] and not isinstance(kwargs['data'], dict):
            return None

        fields = ",".join(kwargs['data'].keys())
        values = [str(value) for value in kwargs['data'].values()]
        values = "'" + "', '".join(values) + "'"
        sql = "insert into {0} ({1}) values ({2});".format(table, fields, values)
        print(sql)

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except pymysql.err.IntegrityError as error:
            print(error)
        self.conn.commit()
        count = cursor.rowcount
        cursor.close()
        return count

    def delete(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        # 如果指定数据库则选中数据库
        if 'database' in kwargs and kwargs['database']:
            self.conn.select_db(kwargs['database'])
        sql = "delete from {table}".format(**kwargs)

        # 如果限制查询条件则填充sql语句
        if 'where' in kwargs and kwargs['where']:
            terms = []
            for key, val in kwargs['where']['terms'].items():
                terms.append(" {0}='{1}' ".format(key, val))
            # 多个查询条件时会存在logic属性，此时用logic拼接，logic是and或or
            if 'logic' in kwargs['where'] and kwargs['where']['logic']:
                logic = kwargs['where']['logic']
            else:
                logic = ""
            condition = logic.join(terms)
            sql += " where {0}".format(condition.strip())

        print(sql)

        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        count = cursor.rowcount
        cursor.close()
        return count

    def update(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        # 如果指定数据库则选中数据库
        if 'database' in kwargs and kwargs['database']:
            self.conn.select_db(kwargs['database'])

        if 'table' not in kwargs:
            raise Exception("need table！")

        sql = "update {table}".format(**kwargs)

        # 设置更新的内容
        if 'set' in kwargs and kwargs['set']:
            terms = []
            for key, val in kwargs['set']['terms'].items():
                terms.append(" {0}='{1}' ".format(key, val))
            content = ",".join(terms)
            sql += " set {0}".format(content.strip())

        # 如果限制查询条件则填充sql语句
        if 'where' in kwargs and kwargs['where']:
            terms = []
            for key, val in kwargs['where']['terms'].items():
                terms.append(" {0}='{1}' ".format(key, val))
            # 多个查询条件时会存在logic属性，此时用logic拼接，logic是and或or
            if 'logic' in kwargs['where'] and kwargs['where']['logic']:
                logic = kwargs['where']['logic']
            else:
                logic = ""
            condition = logic.join(terms)
            sql += " where {0}".format(condition.strip())

        print(sql)

        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        count = cursor.rowcount
        cursor.close()
        return count

    def search(self, **kwargs):
        """
        :param database:
        :return:
        """
        # 如果指定数据库则选中数据库
        if 'database' in kwargs and kwargs['database']:
            self.conn.select_db(kwargs['database'])

        if 'table' not in kwargs:
            raise Exception("need table！")

        if 'fields' in kwargs and kwargs['fields']:
            sql = "select {fields} from {table}".format(**kwargs)
        else:
            sql = "select * from {table}".format(**kwargs)

        # 如果限制查询条件则填充sql语句
        if 'where' in kwargs and kwargs['where']:
            terms = []
            for key, val in kwargs['where']['terms'].items():
                if key == 'great':
                    for key, val in kwargs['where']['terms']['great'].items():
                        terms.append(" {0}>'{1}' ".format(key, val))
                    continue
                if key == 'less':
                    for key, val in kwargs['where']['terms']['less'].items():
                        terms.append(" {0}<'{1}' ".format(key, val))
                    continue
                terms.append(" {0}='{1}' ".format(key, val))
            # 多个查询条件时会存在logic属性，此时用logic拼接，logic是and或or
            if 'logic' in kwargs['where'] and kwargs['where']['logic']:
                logic = kwargs['where']['logic']
            else:
                logic = ""
            condition = logic.join(terms)
            sql += " where {0}".format(condition.strip())

        # 如果携带翻页参数则对其赋值，否则页码为0
        try:
            page = int(kwargs.get('page', 0))
        except TypeError:
            page = 0

        # 如果限制页码大小则对其赋值，否则限制为20
        try:
            size = int(kwargs.get('size', 20))
        except TypeError:
            size = 20

        if 'order' in kwargs:
            order = kwargs.get('order', 'id')
            reverse = kwargs.get('reverse', 'asc') #desc
            sql += " order by {0} {1}".format(order, reverse)

        # 拼接limit限制条件
        sql += " limit {0}, {1}".format(page*size, size)

        print(sql)

        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return results

    def count(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        self.conn.select_db(kwargs.get("database", "quality"))
        sql = "select * from {table}".format(**kwargs)
        print(sql)

        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        results = cursor.rowcount

        cursor.close()
        return results

    def __del__(self):
        self.conn.close()  # 关闭连接，释放内存


if __name__ == '__main__':
    filter = {
        "database": "insurance",
        "table": "ins_questionnaire",
        "fields": "finish_id,id,user_id,last_name,user_mobile,leads_sn",
        "condition": "finish_id is not null",
        "page": 1,
    }
    mysql = Mysql()
    mysql.search(**filter)
    # filter = {
    #     "database": "insurance",
    #     "table": "ins_questionnaire"
    # }
    # print(mysql.count(**filter))
