# int(), float(), bool(), str(), list(), dict()
a = int(10)  # 创建一个int类型的实例
b = 10
print(type(a))
print(isinstance(type(a), str))
# 类似其它语言的三目运算 a == b ? 5 : 6
b = 5 if a == b else 6
print(b)

float_1 = float(3.5)
bool_1 = bool(True)
str_1 = str("hello world")
list_1 = list()
dict_1 = dict()


# 自定义的类大写字母开头
class MyClass:
    pass


# <class '__main__.MyClass'>
print(MyClass)
# <__main__.MyClass object at 0x000001C6785680B8> 对象的创建
mc = MyClass()
print("id=", id(mc), "type=", type(mc), "value=", mc)
# 检查一个对象是否是一个类的实例
print("isinstance:", isinstance(mc, MyClass))

# 类也是一个对象，类就是一个创建对象的对象, 是一个type类型的对象<class 'type'>
print(id(MyClass), type(MyClass), MyClass)


class Person(object):
    def __init__(self):
        """
       双下划线开头和结尾的方法叫特殊方法(魔术方法)，不需要人为调用
       1.特殊方法什么时候调用
       2.特殊方法有什么作用
       """
        self.name = None
        self.age = 0

    def speak(self):
        print(self, "name=", self.name, "age=", self.age)

    def eat(self):
        pass


p1 = Person()
print(p1.name, p1.age)
p1.speak()
