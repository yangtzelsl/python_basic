# 1.创建列表：把逗号分隔的不同的数据项使用方括号括起来
list_a = [1, 2, 3, 'James', 'Paul']
print(list_a)

list_b = [i for i in range(10)]  # 左闭右开
print(list_b)

# 2.添加元素：
# list.append() ：尾部新增元素
# list.insert()：插入元素
# list.insert(index, object)  参数一：index 位置， 参数二：object
# list.extend()：扩展列表  list.extend(tablelist)，左右与 + 类似
# + 号用于组合列表， list1+list2
# * 号用于重复列表

# 3.访问列表元素
# 通过索引下标

# 4.顺序遍历，迭代：
# for循环 遍历元素
list_num = [1, 2, 3, 4, 5]
for i in list_num:
    print(i)
# for循环和enumerate()函数实现，同时输出索引值和元素内容
list_country = ['中国', '美国', '英国', '俄罗斯']
for index, item in enumerate(list_country):
    print(index + 1, item)

# 5.删除元素：
# list.remove(object)：参数object 如有重复元素，只会删除最靠前的
# list.pop(index)： 默认为删除最后一个元素，index -- 可选参数，要移除列表元素的对应索引值，
# del list[index] ：可以删除整个列表或指定元素或者列表切片，list删除后无法访问。

# 6.排序和反转：
# list.reverse() ：列表元素反转
# list.sort()：排序，sort有三个默认参数 cmp=None,key=None,reverse=False 因此可以制定排序参数

# 7.列表切片：
# 列表的位置，或索引，第一个索引是0，第二个索引是1，反向从-1开始
L = ['spam', 'Spam', 'SPAM!', 'Sam', 'Paul', 'Kate']
print(L[2])  # 'SPAM!'  读取列表中第三个元素
print(L[-2])  # 'Paul'  读取列表中倒数第二个元素
print(L[1:])  # ['Spam',  'SPAM!', 'Sam', 'Paul','Kate'] 从第二个元素开始截取列表
print(L[1:4:2])  # ['Spam', 'Sam']  从第二个元素开始到底到第五个元素，每两个元素选取一个

# 8.列表操作常用函数和方法：
# 列表操作包含以下函数:
# cmp(list1, list2)：比较两个列表的元素 (python3已丢弃)
# len(list)：列表中元素个数
# max(list)：返回列表元素最大值
# min(list)：返回列表元素最小值
# list(seq)：将元组转换为列表
# tuple(seq)：将列表转换为元祖
# sorted(list)：排序列表元素顺序

# 列表操作常用操作包含以下方法:
# list.append(obj)：在列表末尾添加新的对象
# list.count(obj)：统计某个元素在列表中出现的次数
# list.extend(seq)：在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
# list.index(obj)：从列表中找出某个值第一个匹配项的索引位置
# list.insert(index, obj)：将对象插入列表
# list.pop(obj=list[-1])：移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
# list.remove(obj)：移除列表中某个值的第一个匹配项
# list.reverse()：反向列表中元素
# list.sort([func])：对原列表进行排序
# list.clear()：  清空列表  (python3.0)
