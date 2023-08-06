from setuptools import setup, find_packages



packages = find_packages()

setup(
    name='py-pcqq',
    version='1.0.3',
    url='https://github.com/DawnNights/py-pcqq',
    author='DawnNights',
    author_email='2224825532@qq.com',
    packages=packages,
    description=u'一个使用pcqq协议的简易python qqbot库',
    long_description='Python语言PCQQ协议的简单封装，详情请参考本人博客中的\ `这篇帖子 <http://blog.yeli.work/2021/09/11/py-pcqq/>`__\n',
    
)
