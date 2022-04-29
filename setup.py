import setuptools

setuptools.setup(
    name="sort-reference",
    version="0.1.0",
    author="zhangkai",
    author_email="maple@forer.cn",
    description="Sort reference by cited order in docx file",
    url="https://github.com/Casxt/SortReference", 
    packages=["sort_reference"],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
    install_requires=['lxml>=4.8.0'],
)