# SortReference

按照文献引用顺序对文献进行编号。

![效果图](img/demo.jpg?raw=true "demo")


## 支持的场景

请确保word中有且只有`[n]`这一种引用格式，`[1-3]`或 `[1,2,3]`等形式需要统一改写成`[1][2][3]`。

请确保word中所有形如`[n]`的字符串均代表引用，否则这些字符也会被计入引用而被错误的改写，如果有的话可以先把不代表引用的字符替换为其他格式比如`<n>`等到程序处理完后再改写回来。

## 使用方法

首先确保已经安装python3.6或更高版本。

1. 使用 pip 安装依赖

    ```
    python -m pip install sort_reference
    ```

2. 指定输入输出文件

    ```
    python -m sort_reference [input] [output] 
    ```
    如：`python -m sort_reference testcase/paper.docx testcase/processed_paper.docx`

3. 手动处理引用顺序

    最后的引用目录还无法使用程序自动排序，执行结束后手动排序一下即可。

## 报错处理

### 1. AssertionError: multi text blocks edit not support yet

![multi_text_blocks_error](img/multi_text_blocks_error.jpg?raw=true "multi_text_blocks_error")

**假设具体的报错内容是`total 2 text blocks in snippet: '12'`, 全文搜索找到每一处`[12]`, 删除其中的数字并重新输入一遍即可**

出现这个报错是因为一些引用的字符被word分到了多个不同的文字块中，具体来说，某一个`[12]`的字符被word分割为了`[1`和`2]`两个字符串，只是显示时看起来是连续的。此时删除字符并重新输入就可以保证新输入的字符在同一个文字块内了。

`testcase/paper_badcase.docx`中复现了这一错误，只需要重新输入一遍`12`就可以解决。

### 2. 论文导出pdf出现“错误!未找到引用源”
导出前使用`ctrl+a`和`ctrl+F11`禁用全局域更新，导出后`ctrl+a`和`ctrl+shift+F11`启用全局域更新即可。网络上有大量教程，可以自行搜索。理论上不是本程序导致的。