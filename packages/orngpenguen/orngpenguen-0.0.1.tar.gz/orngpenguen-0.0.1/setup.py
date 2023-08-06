from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='orngpenguen',
    version='0.0.1',
    description='Password Hasher with a key',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Mert Alperen Beşer',
    author_email='mertbeser77@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='hash',
    packages=find_packages(),
    install_requires=['bitarray==2.3.4']
)