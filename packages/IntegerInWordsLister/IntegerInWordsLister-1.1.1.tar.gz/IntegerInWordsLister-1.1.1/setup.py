from distutils.core import setup

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='IntegerInWordsLister',
    packages=['IntegerInWordsLister'],
    version='1.1.1',
    license='MIT',
    description='This module returns numbers to a list of words',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Amin Morakabi Sabet',
    author_email='vivaams@yahoo.com',
    url='https://github.com/vivaams/IntegerInWordsLister',
    project_urls={
        "Bug Tracker": "https://github.com/vivaams/IntegerInWordsLister/issues",
    },
    keywords=['integer', 'inwords'],
    install_requires=[
            'humanize',
        ],
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
)
