from sqllineage.runner import LineageRunner

'''
数据血缘关系梳理工具：
1.开源工具sqllineage
    pip install sqllineage
    写代码
2.在线工具
https://sqlflow.gudusoft.com/#/
'''

sql = """

"""
result = LineageRunner(sql)
print(result)
# 打印result，会产出下面的信息
# Statements(#): 2
# Source Tables:
#    db1.table12
#    db2.table21
#    db2.table22
# Target Tables:
#    db3.table3
# Intermediate Tables:
#    db1.table11

# 也可以直接获取各个源表
for tbl in result.source_tables:
    print(tbl)
# db1.table12
# db2.table21
# db2.table22

# 目标表当然也是可以的
for tbl in result.target_tables:
    print(tbl)
# db3.table13

# 甚至还可以调用matplotlib绘制血缘图
result.draw()
