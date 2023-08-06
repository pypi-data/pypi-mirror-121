from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-string-spliter',
    version='0.1',
    description='The purpose of this plugin is split any string',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Bartosz Dobrosielski`',
    author_email='bdobrosielski@edu.cdv.pl',
    packages=['tracardi_string_splitter'],
    install_requires=[
        'tracardi-plugin-sdk'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['tracardi', 'plugin'],
    python_requires=">=3.8",
    include_package_data=True
)