from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ptodbc',
    version='0.0.1',
    description='get odbc with username and password',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Zheng Xu',
    author_email='chizetas@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Pioneer Tools odbc',
    packages=find_packages(),
    install_requires=['']
)