# # coding: utf-8
# import codecs
# import os
# import sys

# # try:
# from setuptools import setup
# # except:
# #     from distutils.core import setup

# """
# 打包的用的setup必须引入，
# """

# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
 

# import sys
# if sys.version_info < (2, 5):
#     sys.exit('Python 3.6 or greater is required.')
 
 
# with open('README.md', 'rb') as fp:
#     readme = fp.read()
 
# # 版本号，自己随便写
# VERSION = "1.0.0"

# LICENSE = "MIT"

 
# setup(
#     name='model_builder',
#     version=VERSION,
#     description=(
#         '在搭建模型时必要的基础函数'
#     ),
#     long_description=readme,
#     author='ivey',
#     author_email='iveyzhang@outlook.com',
#     license=LICENSE,
#     py_mudoles=['model_builder'],
#     packages=['model_builder'],
#     platforms=["all"],
#     url='None',
#     install_requires=[  
#         'pandas',  
#         'numpy' 
#         ],  
#     classifiers=[
#         'Development Status :: 1 - Beta',
#         'Operating System :: Windows',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: BSD License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: Implementation',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: 3.8',
#         'Topic :: Software Development :: Libraries'
#     ],
# )


# # URL 你这个包的项目地址，如果有，给一个吧，没有你直接填写在PyPI你这个包的地址也是可以的
# # INSTALL_REQUIRES 模块所依赖的python模块
# # 以上字段不需要都包含


from setuptools import setup, find_packages

setup(
    name='ivtest',
    version='0.0.2',
    description='my test',
    author='ivey',
    author_email='iveyzhang@outlook.com',
    py_modules=["ivtest"],
    packages=['ivtest'],
    license='MIT',
    platform='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['pandas', 'numpy']
)