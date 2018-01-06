PyFaiss
![](https://readthedocs.org/projects/pygorithm/badge/?version=latest) ![](https://img.shields.io/badge/python%20-%202.7-brightgreen.svg)
========

**NOTE:To use this package must ensure has installed faiss lib**

## `Install`
- 使用该模块时，在项目的**[requirements.txt]**中添加
并使用命令行安装：

` /usr/local/bin/pip install -r requirements.txt`

- 或者通过单独安装

## `Include`
+ [train_index]

    训练faiss `index` 模块**TrainIndex**初始参数详解：

    class TrainIndex(kwargs):
    - `files`: (type `list`) 文档向量文件列表，注意：不是文件名，而是文档向量的绝对路径.
    - `vpath`: 文档向量读取路径，读取的数据应满足一定的前缀或者后缀规则(`prefix`, `suffix`).
    - `prefix`:文档向量文件名前缀，如 `vector_**`.
    - `suffix`:文档向量文件名后缀，如 `**_vector`.
    - `dpath`: `index`训练结果存储路径.
    - `iname`: `index`训练结果存储名称，默认为(`index.index`).
    - `direct`: 实例化`TrainIndex`时，直接使用默认提取的向量文件进行训练生成`index`，并返回.
    - `fpath`: 安装`faiss` 产生的编译文件(faiss.py,  swigfaiss.py, \_swigfaiss.so)存储路径，该模块运行必须导入这些相关文件.

+ [faiss_search]

    class FaissSearch(kwargs)
    两种传入方式，1. 直接传入index; 2. 传入index存储路径:
    - `index`:直接传入`index`文件;
    - `ipath`:读取`index`的路径(包含index的文件名，如：`/home/xxx/x/x.index`);
    - `fpath`:安装`faiss` 产生的编译文件(faiss.py,  swigfaiss.py, \_swigfaiss.so)存储路径，该模块运行必须导入这些相关文件.

    faiss搜索相关接口
    - `add()`:
    - `add_one()`:
    - `search()`:
    - `search_many()`:


## `Basic Usage`
```python
>>> from pyfaiss.train_index import TrainIndex
>>> vpath = u'/home/user/'
>>> prefix= u'vector_'
>>> fpath = '/home/user/'
>>> trainer = TrainIndex(vpath=vpath, prefix=prefix, fpath=fpath)
>>> files = trainer.files[:2]
>>> print files
>>> index = trainer.train(files)
>>> print index.ntotal
211897
```
