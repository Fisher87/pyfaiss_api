#!/usr/bin/env python
# coding=utf-8

"""
pyfaiss.train_faiss.
----------------------------------------------------
  this module intend to train faiss index object.
input vector path or vector files, and index output
path. Then return the trained index object to dest-
ination path.
----------------------------------------------------
"""

import os
import sys
import time
import logging
import warnings
import numpy as np

from mylogging.namedlogger import NamedLogger

#from faiss_utils import faiss

class TrainIndex(object):
    def __init__(self, **kwargs):
        """
        :param files: from which files to get vectors.
        :param vpath: from where to get all vector files, note this files 
                      name should startswith `vector_`.
        :param dpath: where trained index object to save.
        :param iname: trained index saved as iname.
        :param fpath: faiss built files path. from where to import faiss
                      modules.
        :param direct:when instance TrainIndex object direct to train.
        """
        self.files  = []
        self.vpath  = ''
        self.dpath  = ''
        self.iname  = ''
        self.fpath  = ''
        self.direct = False
        self.index  = None
        if not any([u'files' in kwargs, u'vpath' in kwargs]):
            Error = 'Must need anyone key in (`files`, `vpath`)'
            raise KeyError(Error)

        if u'files' in kwargs:
            self.files = kwargs.get('files')
        if u'vpath' in kwargs:
            self.vpath = kwargs.get('vpath')
            self.prefix= kwargs.get('prefix', '\1')
            self.suffix= kwargs.get('suffix', '\1')
            self.fix   = {'prefix':self.prefix} or {'suffix':self.suffix}
        if self.vpath:
            if self.files:
                Warn = ('Input `files` and `vpath` at the same time, input '
                        'files list will be replaced by vpath select files.')
                warnings.warn(Warn)
            self.files = self._get_files()
        if u'fpath' in kwargs:
            self.fpath = kwargs.get('fpath')

        #: index object save path
        if u'dpath' in kwargs:
            self.dpath = kwargs.get('dpath')
            if u'iname' not in kwargs:
                Warn = ('NO `iname` input, the index object will save as '
                        'default name [index.index]')
                warnings.warn(Warn)
            self.iname = kwargs.get('iname', 'index.index')
        self.logger = kwargs.get('logger', '') or logging.getLogger(__file__)
        if u'direct' in kwargs:
            self.direct = kwargs.get('direct')
        if self.direct:
            self.index = self.train(self.files)

    
    def _get_files(self):
        """ select files from vpath """

        if 'prefix' in self.fix:
            _files = [file for file in os.listdir(self.vpath) if \
                     file.startswith(self.fix['prefix'])]
        else:
            _files = [file for file in os.listdir(self.vpath) if \
                     file.endswith(self.fix['suffix'])]
        files = [os.path.join(self.vpath, _) for _ in _files]
        return files

    @staticmethod
    def _generate_npvectors(files):
        """
        intend from vector files to generate numpy matrixs.
        NOTE:this files not only filenames, is a list about
        file absoult path.

        :param files: type `list`: vector files absoulte path. 
        @rtype: numpy matrix.
        """
        count = 0
        allvectors = list()
        for file in files:
            with open(file, 'r') as fopen:
                vectorlines = fopen.readlines()
                count += len(vectorlines)
                allvectors.extend(vectorlines)
        npvectors = np.zeros(shape=[count, 102]).astype('float32')
        for i, line in enumerate(allvectors):
            l = np.array([float(_) for _ in line.strip().split(' ')]).astype('float32')
            npvectors[i] = l

        return npvectors

    def train(self, files):
        """ train index """

        npvectors = self._generate_npvectors(files)

        #: npvectors[0:2] save docvector ids' number, 
        #: and [2:] save docvetor true infos.
        vectors   = npvectors[:, 2:].astype('float32')
        vectorids = npvectors[:, :2]
        vector_ids= vectorids[:, 0].astype('int') * 10000 + vectorids[:, 1].astype('int')

        try:
            from faiss_utils import faiss
        except ImportError:
            if not self.fpath:
                Error = ('Can not import faiss, need to put faiss build files to '
                         './faiss_utils or input ref fpath.')
                raise ImportError(Error)
            sys.path.insert(0, self.fpath)
            import faiss

        index = faiss.index_factory(100, "PCA80, IVF1024, Flat")
        start = time.time()
        self.logger.info('start to train index')
        index.train(vectors)
        index.add_with_ids(vectors, vector_ids)

        if self.dpath:
            self.logger.info('write index to %r as name: %r' % 
                                                 (self.dpath, self.iname))
            dfile = os.path.join(self.dpath, self.iname)
            faiss.write_index(index, dfile)

        self.logger.info('train index cost time:{0}'.format(time.time()-start))
        return index

if __name__ == '__main__':
    logger = NamedLogger('index_train')
    trainer = TrainIndex(vpath='/home/yulianghua/gitlab/wechat_marking_system/title_vectors',
                         prefix='vector_', 
                         fpath = '/home/yulianghua/github/faiss', 
                         direct=True,
                         #files = ['/home/yulianghua/gitlab/news_extract/wechat/vectors/vector_20170819'], 
                         #dpath='/home/yulianghua',
                         #iname='test.index',
                         logger=logger)
    index = trainer.index
    
    #files = trainer.files[:2]
    #print files
    #index = trainer.train(files)
    print 'index ntotal', index.ntotal

        
