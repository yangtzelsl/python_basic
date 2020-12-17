# 1.创建字典
# 键必须独一无二，但值则不必
dict_common = {'ob1': 'computer', 'ob2': 'mouse', 'ob3': 'printer'}
dict_list = {'yangrong': ['23', 'IT'], "xiaohei": ['22', 'dota']}
dict_dict = {'yangrong': {"age": "23", "job": "IT"}, "xiaohei": {"'age':'22','job':'dota'"}}

# 2.访问字典里的值
for key in dict_common:
    print(key, dict_common[key])

# 3.修改字典
dict_common['ob1'] = 'book'
print(dict_common)

# 4.删除字典
# del dict['ob1'] 删单一的元素
# dict.clear() 删除字典中所有元素，删除后访问会返回空字典 {}
# del dict1 删除整个字典，删除后访问字典会抛出异常 NameError: name 'dict1' is not defined

# 5.更新字典
# update()方法可以用来将一个字典的内容添加到另外一个字典中
dict1 = {'ob1': 'computer', 'ob2': 'mouse'}
dict2 = {'ob3': 'printer'}
dict1.update(dict2)
print(dict1)

# 6.映射类型相关的函数
print(dict(x=1, y=2))
dict8 = dict(x=1, y=2)
print(dict8)
dict9 = dict(**dict8)
print(dict9)
dict10 = dict8.copy()
print(dict10)

# 7.字典键的特性
# 字典值可以没有限制地取任何python对象，既可以是标准的对象，也可以是用户定义的，但键不行。
# 两个重要的点需要记住：
# 1）不允许同一个键出现两次。创建时如果同一个键被赋值两次，后一个值会被记住
# 2）键必须不可变，所以可以用数，字符串或元组充当，用列表就不行

# 8.字典内置函数&方法
# Python字典包含了以下内置函数：
# 1、cmp(dict1, dict2)：比较两个字典元素。(python3后不可用)
# 2、len(dict)：计算字典元素个数，即键的总数。
# 3、str(dict)：输出字典可打印的字符串。
# 4、type(variable)：返回输入的变量类型，如果变量是字典就返回字典类型。

# Python字典包含了以下内置方法：
# 1、radiansdict.clear()：删除字典内所有元素
# 2、radiansdict.copy()：返回一个字典的浅复制
# 3、radiansdict.fromkeys()：创建一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值
# 4、radiansdict.get(key, default=None)：返回指定键的值，如果值不在字典中返回default值
# 5、radiansdict.has_key(key)：如果键在字典dict里返回true，否则返回false
# 6、radiansdict.items()：以列表返回可遍历的(键, 值) 元组数组
# 7、radiansdict.keys()：以列表返回一个字典所有的键
# 8、radiansdict.setdefault(key, default=None)：和get()类似, 但如果键不已经存在于字典中，将会添加键并将值设为default
# 9、radiansdict.update(dict2)：把字典dict2的键/值对更新到dict里
# 10、radiansdict.values()：以列表返回字典中的所有值

# 访问dict中没有的对应key的项目
# 如果字典window_counts中没有key==char的项，
# 则get()函数返回0，此时将在字典window_counts创建一个新的项。
window_counts = {}
window_counts['char'] = window_counts.get('char', 0)
print(window_counts)

