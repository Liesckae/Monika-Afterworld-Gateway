# 在这个python文件里你可以按照python3.X的写法写了，如果你的环境变量是python3.x的话...
# 当然python2.x还是可以用这个方法改的...改个版本号就行...因为python2是向下兼容的
# 这样设置的作用就是绕过DDLC超级古老的python2.7（我被折磨了好久），你如果还用python2.x那我的设计就被白费了（哭）

with open('test.txt', 'w',encoding='utf-8') as f:
        f.write('whis is a fucking test!')

    