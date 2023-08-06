from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ezdatabase',
    version='0.0.1',
    description='A simple database wrapper for Python',
    author='JJTV',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    license='MIT',
    classifiers=classifiers,
    keywords=["database wrapper", "ezdatabase", "easydatabase", "easy database", "repl.it database"],
    packages=find_packages(),
    install_requires=['']
)