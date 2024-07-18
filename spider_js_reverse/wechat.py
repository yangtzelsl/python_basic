import execjs

# 1.实例化一个node对象
node = execjs.get()

# 2.js源文件编译
ctx = node.compile(open('./wechat.js', encoding='utf-8').read())

# 3.执行js函数
func_name = 'getPwd("{0}")'.format('123456')
pwd = ctx.eval(func_name)
print(pwd)