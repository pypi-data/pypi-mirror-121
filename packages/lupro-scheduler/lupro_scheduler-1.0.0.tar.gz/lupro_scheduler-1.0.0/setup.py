from distutils.core import setup
from setuptools import find_packages
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='lupro_scheduler',  # 包名
      version='1.0.0',  # 版本号
      description='Lupro Scheduler is a synchronous task chain scheduler support sweeper, multi-thread, multi-process synchronous communication.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='ShengXin Lu',
      author_email='luxuncang@qq.com',
      url='https://github.com/luxuncang/lupro_scheduler',
      install_requires=['gevent'],
      license='MIT',
      packages=find_packages(),
      include_package_data = True,
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )