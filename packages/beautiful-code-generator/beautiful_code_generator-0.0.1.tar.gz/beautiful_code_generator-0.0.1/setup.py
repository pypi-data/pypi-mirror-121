from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Simple tools that generates beautiful code'
LONG_DESCRIPTION = 'Simple tools to generate beautiful code. The format of such code is combination of 2 adjectives and names'

setup(
    name="beautiful_code_generator",
    version=VERSION,
    author="Johny Utah",
    author_email="jones.hovercraft2020@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    keywords=['python', 'beautiful code generator', 'code generator'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
