# cython: infer_types=True, c_string_type=bytes, cdivision=True
# distutils: language = c++
# Copyright (c) 2021 MatchUp Project (Marcos Pontes)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
import numpy as np
cimport numpy as np

from cython.parallel cimport prange

cdef class BordaCount:

    def __init__(self, *, n_threads = 4):
        """
        BordaCount initializer.
        """
        self.num_threads = n_threads
        self.num_documents = 0


    cdef long[:] rank_score(self, long[:] rank):
        """
        Generate BordaCount scores for a single rank.
        E.g. [1, 3, 5, 2, 4]  => [4, 1, 3, 0, 2]
        :param rank: rank of interest
        :param n_rows: number of rows in the rank
        :return: 
        """
        cdef int i
        cdef int n_rows = self.num_documents
        cdef bint error = 0
        cdef np.ndarray[long, mode='c'] borda_rank = np.zeros(n_rows, dtype=np.int64)

        for i in prange(n_rows, nogil=True, num_threads=self.num_threads):
            if rank[i]-1 < 0:
                error = 1
            else:
                borda_rank[rank[i]-1] = n_rows - (i+1)

        if error == 1:
            raise ValueError("Error in BordaCount::rank : Doc id's must be higher than 1")

        return borda_rank

    cdef long[:] fit(self, long[:, :] rankings):
        """
        Apply BordaCount with cython
        :param rankings: all rankings
        """
        cdef int i
        cdef int n_rows = self.num_documents
        cdef np.ndarray[long, mode='c', ndim=2] scores = np.zeros((n_rows, rankings.shape[1]), dtype=np.int64)
        cdef np.ndarray[long, mode='c', ndim=1] data = np.zeros(n_rows, dtype=np.int64)

        for i in range(rankings.shape[1]):
            scores[i, :] = self.rank_score(rankings[i, :])

        data = scores.sum(axis=0)

        return data.argsort() + 1


    def rank(self, long[:, :] rankings):
        """
        Main method of BordaCount process. Here, all rankings are compared and a new ranking is produced based on they.
        Important, each rank must be considered as ranking of ID's from 1 to Number of documents to be ranked.
        :param rankings: all rankings
        :return: final ranking list of ids (ndarray)
        """

        self.num_documents = rankings.shape[0]
        return np.asarray(self.fit(rankings))[::-1]


    def rank_by_id(self, list rankings):
        """
        List of strings for doc ids.
        :param rankings: List of rankings by docid str
        :return: final ranking list of docids (list)
        """
        cdef int nrank = len(rankings)
        cdef int ndoc = len(rankings[0])
        cdef object map_doc_ids = dict()
        cdef object map_ids_doc = dict()

        ndranks = np.zeros((nrank, ndoc), dtype=np.int64)

        if len(rankings) > 0:
            for i, docid in enumerate(rankings[0], start=1):
                map_doc_ids[docid] = i
                map_ids_doc[i] = docid

            for i, rank in enumerate(rankings):
                ndranks[i, :] = np.asarray([map_doc_ids[docid] for docid in rank])

            response = self.rank(ndranks)

            return [map_ids_doc[response[i]] for i in range(ndoc)]

        raise ValueError("Error in BordaCount::rank : You must provide some ranking")
