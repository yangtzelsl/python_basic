import pymysql
import pandas as pd
from sqllineage.runner import LineageRunner
import datetime
from sqlalchemy import create_engine
import warnings

# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


if __name__ == "__main__":

    print("start time "+str(datetime.datetime.now()))
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='dolphinscheduler',
        charset='utf8'
    )

    cursor = conn.cursor()

    sql = """
        select distinct
            t4.name as project_name
            ,t1.name as process_name
            ,t3.name as task_name
            ,t3.sql_script as sql_script
        from (select code,name,project_code from dolphinscheduler.t_ds_process_definition where flag=1 and release_state=1 group by code,name,project_code) t1
        inner join (select distinct project_code,process_definition_code,pre_task_code,post_task_code from dolphinscheduler.t_ds_process_task_relation) t2
            on t1.project_code=t2.project_code and t1.code=t2.process_definition_code
        inner join (select code,name,project_code,json_extract(task_params,'$.sql') as sql_script from dolphinscheduler.t_ds_task_definition where flag=1 and task_type='SQL') t3
            on t1.project_code=t3.project_code and (t3.code=t2.pre_task_code or t3.code=t2.post_task_code)
        inner join dolphinscheduler.t_ds_project t4
            on t1.project_code=t4.code
        where t4.name <> 'test'
        ;
    """

    cursor.execute(sql)
    conn.commit()

    data = cursor.fetchall()
    print("fetch time "+str(datetime.datetime.now()))

    df = pd.DataFrame(columns=['sql_script', 'output'])

    # 组装成DataFrame
    all_project_name_list = []
    all_process_name_list = []
    all_task_name_list = []
    all_sql_script_list = []
    all_output_list = []
    for ele in data:
        project_name=ele[0]
        process_name=ele[1]
        task_name=ele[2]
        sql = eval(ele[3])
        try:
            result = LineageRunner(sql.replace("${db_para}", ''))
            source_tables_list = result.source_tables
            target_tables_list = result.target_tables

            if not target_tables_list:
                target_tables_list = ['']
            all_project_name_list.append(project_name)
            all_process_name_list.append(process_name)
            all_task_name_list.append(task_name)
            all_sql_script_list.append(sql)
            all_output_list.extend(target_tables_list)
        except Exception as e:
            print(sql)
            print(e)
    print("etl start time " + str(datetime.datetime.now()))
    df['project_name'] = all_project_name_list
    df['process_name'] = all_process_name_list
    df['task_name'] = all_task_name_list
    df['sql_script'] = all_sql_script_list
    df['output'] = all_output_list
    print("etl end time " + str(datetime.datetime.now()))

    # DataFrame写入Excel
    df.to_excel("t_ds_task_sql_script_relation.xlsx")

    # DataFrame写入MySQL
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/dolphinscheduler?charset=utf8')
    df.to_sql(name='t_ds_task_sql_script_relation', con=engine, if_exists='replace', index=False)

    print("end time " + str(datetime.datetime.now()))

    conn.close()
