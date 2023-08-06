import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup


def read(fname):
    """
        定义一个read方法，用来读取目录下的长描述
        我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
        你也可以不用这个方法，自己手动写内容即可，
        PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = 'study_pypi_zbr'
"""
    一般放包的名字
"""

PACKAGES = ['somefuncs',]
"""
包含的包，可以是多个，这是个列表
"""

DESCRIPTION = 'this is a test for upload pypi'
"""
关于这个包的描述
"""

LONG_DESCRIPTION = read('README.rst')
"""
参见read方法说明
"""

KEYWORDS = 'test python package'
"""
关于当前包的一些关键字，方便PyPI进行分类
"""

AUTHOR = 'zhangbaorui'
"""
作者
"""

AUTHOR_EMAIL = '1220302613@qq.com'
"""
作者的邮箱
"""

URL = 'https://pypi.org/manage/projects/'
"""
这个包的项目地址，可以是自己的地址，也可以是pypi上的地址
"""

VERSION = '1.0.1'
"""
当前包的版本
"""

LICENSE = "MIT"
"""
授权方式，可以是MIT的方式，你可以换成其他方式
"""

platforms = ['linux/Windows']
classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.7',
]

install_requires = [
    'numpy>=1.11.1',
    'pandas>=0.19.0'
]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=classifiers,
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
    install_requires=install_requires,
    platforms=platforms,
)
