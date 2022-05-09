import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sort-reference",
    version="0.1.2",
    author="casxt",
    author_email="maple@forer.cn",
    description="Sort reference by cited order in docx file",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Casxt/SortReference", 
    packages=["sort_reference"],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['lxml>=4.8.0'],
)