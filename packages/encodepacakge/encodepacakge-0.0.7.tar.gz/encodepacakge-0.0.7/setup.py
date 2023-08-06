from setuptools import setup, find_packages

#with open("readme.md", "r") as fh:
#    long_description = fh.read()

setup(
    name='encodepacakge',  
    version='0.0.7',
    author="uptownaravi",
    author_email="uptownaravi@gmail.com",
    description="encode string with given template",
    #long_description_content_type="text/markdown",
    url="https://github.com/uptownaravi/encoder",
    package_dir={"": "encoder"},
    packages=find_packages(where="encoder"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
