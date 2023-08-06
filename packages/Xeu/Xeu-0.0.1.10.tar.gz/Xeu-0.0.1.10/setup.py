# coding=utf-8

from setuptools import setup, find_packages


def readme():
    with open('./README', encoding="utf-8") as f:
        _long_description = f.read()
        return _long_description

packages=find_packages()

print('packages:', packages)

setup(
    name='Xeu',
    version="0.0.1.10",
    description=(
        """
            Xeu
        """
    ),
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=[],
    author='Jayson Leo',
    author_email='2835347017@qq.com',
    maintainer='Jayson Leo',
    maintainer_email='2835347017@qq.com',
    license='MIT License',

    platforms=["linux", 'windows'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'toml',
        'Tornado',
    ],
    packages=packages,
    entry_points={
        'console_scripts': [
            'xeu=Xeu.setup.script.manage:main'
        ]
    }
)