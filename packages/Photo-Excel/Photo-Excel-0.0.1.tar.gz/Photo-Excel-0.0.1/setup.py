from setuptools import setup, find_packages

with open('F:\\my projects\\Python\\package\\Readme.md', 'r' , encoding='utf-8') as fh:
    long_description = fh.read()

# Setting up
setup(
    name="Photo-Excel",
    version='0.0.1',
    author="Yagav Akhilesh",
    author_email="yagav123456@gmail.com",
    description='Change Photos into a Excel file',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url= "https://github.com/yagav/PhotExcel",
    packages=['PhotExcel'],
    install_requires=['numpy', 'pandas', 'pillow'],
    keywords=['python','excel','photo converter', 'photo-excel', 'photo to excel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)