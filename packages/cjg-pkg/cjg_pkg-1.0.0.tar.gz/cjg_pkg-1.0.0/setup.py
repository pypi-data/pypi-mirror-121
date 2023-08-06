# coding: utf-8
from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='cjg_pkg',  # 包名，即自己自定义的报名
      version='1.0.0',  # 版本号，每次发布都要修改一次
      description='A small example package',
      long_description=long_description,
      author='jigang.chen',
      author_email='15252162668@163.com',
      url='https://github.com/chenjigang4167',
      install_requires=[],  # 存放依赖库，并指明依赖版本
      license='MIT License',
      packages=find_packages(),  # 要发布的包，多个包可以使用[a,b,c]定义指定包，不指定默认所有
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
