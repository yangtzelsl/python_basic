# input()函数
# 该函数用来获取用户的输入
# input()调用后，程序会立即暂停，等待用户输入
#   用户输入完内容以后，点击回车程序才会继续向下执行
#   用户输入完成以后，其所输入的的内容会以返回值得形式返回
#   注意：input()的返回值是一个字符串
#   input()函数中可以设置一个字符串作为参数，这个字符串将会作为提示文字显示
a = input('请输入任意内容：')
print('用户输入的内容是:',a)
# input()也可以用于暂时阻止程序结束

# 获取用户输入的用户名
username = input('请输入你的用户名:')
# 判断用户名是否是admin
if username == 'admin' :
    print('欢迎管理员光临！')