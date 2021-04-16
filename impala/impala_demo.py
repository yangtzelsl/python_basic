from impala.dbapi import connect


def execute_query(query, cursor=None):
    try:
        impala_con = connect(host='10.132.45.35', port=21050, user='hui_liu', password='4c1@h6CmS')

        impala_cur = impala_con.cursor()
        impala_cur.execute(query,configuration=None)
        result = impala_cur if cursor else impala_cur.fetchall()

        impala_cur.close()

        return result
    except Exception as err:
        return None


if __name__ == '__main__':
    query = "show databases"
    result = execute_query(query)
    print(result)
