"""
通过文件操作，我们可以将字符串写入到一个本地文件。但是，如果是一个对象(例如列表、字典、元组等)，就无
法直接写入到一个文件里，需要对这个对象进行序列化，然后才能写入到文件里。
设计一套协议，按照某种规则，把内存中的数据转换为字节序列，保存到文件，这就是序列化，反之，从文件的字
节序列恢复到内存中，就是反序列化。
对象---》字节序列 === 序列化
字节序列--》对象 ===反序列化
Python中提供了JSON这个模块用来实现数据的序列化和反序列化。
JSON模块
JSON(JavaScriptObjectNotation, JS对象简谱)是一种轻量级的数据交换标准。JSON的本质是字符串。
使用JSON实现序列化
JSON提供了dump和dumps方法，将一个对象进行序列化。
dumps方法的作用是把对象转换成为字符串，它本身不具备将数据写入到文件的功能。
"""


def dumps_func():
    import json
    file = open('names.txt', 'w')
    names = ['zhangsan', 'lisi', 'wangwu', 'jerry', 'henry', 'merry', 'chris']
    # file.write(names) 出错，不能直接将列表写入到文件里
    # 可以调用 json的dumps方法，传入一个对象参数
    result = json.dumps(names)
    # dumps 方法得到的结果是一个字符串
    print(type(result))  # <class 'str'>
    # 可以将字符串写入到文件里
    file.write(result)
    file.close()


def dump_func():
    import json
    file = open('names.txt', 'w')
    names = ['zhangsan', 'lisi', 'wangwu', 'jerry', 'henry', 'merry', 'chris']
    # dump方法可以接收一个文件参数，在将对象转换成为字符串的同时写入到文件里
    json.dump(names, file)
    file.close()


def loads_func():
    import json
    # 调用loads方法，传入一个字符串，可以将这个字符串加载成为Python对象
    result = json.loads('["zhangsan", "lisi", "wangwu", "jerry", "henry", "merry", "chris"]')
    print(type(result))  # <class 'list'>


def load_func():
    import json
    # 以可读方式打开一个文件
    file = open('names.txt', 'r')
    # 调用load方法，将文件里的内容加载成为一个Python对象
    result = json.load(file)
    print(result)
    file.close()

