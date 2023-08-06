from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="serverrunner",
    version="1.0.3",
    description="A server runner for certant projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="palmtrww",
    author_email="palmtrww@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=find_packages(where='serverrunner'),
    entry_points={
        'console_scripts': [
            'runserver=serverrunner:__main__'
        ],
    },

)
