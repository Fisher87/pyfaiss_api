#!usr/bin/env python
# coding=utf8

import os
import sys
import numpy as np

#from .faiss_utils import faiss

class FaissSearch(object):
    """
    intent to seach similar news from faiss index.

    @param:`index_path`: which index to search.
    @param:`callback`  : future extension. 
           get vector func, different index different func.   
    """
    def __init__(self, **kwargs):
        self.index    = None
        self.callback = None
        if kwargs.has_key('index'):
            self.index = kwargs['index']
        if not self.index and all(k in kwargs for k in ['ipath', 'fpath']):
            fpath = kwargs.get('fpath')
            try:
                import faiss
            except ImportError:
                sys.path.insert(0, fpath)
                import faiss
            ipath = kwargs.get('ipath')
            self.index = faiss.read_index(ipath)

        assert self.index is not None

    @staticmethod
    def read_index(ipath, fpath='./'):
        """
        @param: fpath: faiss file path.
        """
        try:
            import faiss
        except ImportError:
            sys.path.insert(0, fpath)
            import faiss
        return faiss.read_index(ipath)

    @staticmethod
    def write_index(index, fpath='./', savepath='./', index_name='index.index'):
        try:
            import faiss
        except ImportError:
            sys.path.insert(0, fpath)
            import faiss
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        index_name = savepath + index_name
        faiss.write_index(index, index_name)

    def add_one(self, item_vector, **kwargs):
        """
        only to add vector to index.
        @param: `text`   : type `str`, search text.
        @param: **kwargs : other params
            `try_time` : try the most time to get vector server.
            `id`:type  : `ndarray` or `list`, which to add in faiss
                         index.
            `add_with_ids`: flag, indicate whether to add with user-
                         defined ids. 
        """
        if not all(k in kwargs for k in ('id', 'add_with_ids')):
            import warnings
            warnings.warn(
        """
        if use faiss `add_with_ids` functions, field `id`, 
        `add_with_ids` must in parameters kwargs at the same
        time.
        """)

        if not isinstance(item_vector, np.ndarray):
            raise ValueError('vector must `numpy.ndarray` type, not %s.' % type(item_vector))
        if len(item_vector.shape) < 2:
            item_vector = item_vector.reshape([1,item_vector.shape[0]]).astype('float32')
        if not kwargs.get('add_with_ids', False):
            self.index.add(item_vector)
            return 
        if not kwargs.has_key('id'):
            raise KeyError('use add_with_ids must provied `id`')
        id = kwargs.get('id')
        if not isinstance(id, np.ndarray):
            id = np.array(id).astype('int')

        self.index.add_with_ids(item_vector, id)
        return 

    def add_many(self, item_vectors, **kwargs):
        """
        add clust vectors to index.
        """
        if not all(k in kwargs for k in ('ids', 'add_with_ids')):
            import warnings
            warnings.warn(
        """
        if use faiss `add_with_ids` functions, field `ids`, 
        `add_with_ids` must in parameters kwargs at the same
        time.
        """)
        if not isinstance(item_vectors, np.ndarray):
            raise ValueError('vector must `numpy.ndarray` type, not %s.' % type(item_vectors))
        assert len(item_vectors.shape) == 2
        if not kwargs.get('add_with_ids', False):
            self.index.add(item_vectors)
            return 
        if not kwargs.has_key('ids'):
            raise KeyError('use add_with_ids must provied `ids`')
        ids = kwargs.get('ids')
        if not isinstance(ids, np.ndarray):
            ids = np.array(ids).astype('int')
        assert len(ids.shape) == 1
        assert item_vectors.shape[0] == ids.shape[0]

        self.index.add_with_ids(item_vectors, ids)
        return 

    def search_one(self, item_vector, **kwargs):
        """
        @param: `text`   : type `str`, search text.
        @param: **kwargs : other params
            `k`:return most 'k' nearnest search result.
            `try_time`:try the most time to get vector server.
            `add`: flag, after search add new vector to index, then
                   return the search result.
        """
        if not isinstance(item_vector, np.ndarray):
            raise ValueError('vector must `numpy.ndarray` type, not %s.' % type(item_vector))
        if len(item_vector.shape) < 2:
            item_vector = item_vector.reshape([1,item_vector.shape[0]]).astype('float32')
        add = False
        search_len = kwargs.get('k', 100)
        D, I = self.index.search(item_vector, search_len)
        if u'add' in kwargs:
            add = kwargs.get('add')
        if add:
            self.add_one(item_vector, **kwargs)
        return (D, I)

    def search_many(self, item_vectors, **kwargs):
        """
        @param: `texts`  : type `list`, search text list.
        @param: **kwargs : other params
            `k`:return most 'k' nearnest search result.
            `try_time`:try the most time to get vector server
        """
        
        if not isinstance(item_vectors, np.ndarray):
            raise ValueError('vector must `numpy.ndarray` type, not %s.' % type(item_vectors))
        assert len(item_vectors.shape) == 2
        add_many = False
        search_len = kwargs.get('k', 100)
        D, I = self.index.search(item_vectors, search_len)
        if u'add_many' in kwargs:
            add_many = kwargs.get('add_many')
        if add_many:
            self.add_many(item_vectors, **kwargs)
        return (D, I)

    def remove_ids(self, ids):
        """
        intent to remove ids from index.
        """
        pass


