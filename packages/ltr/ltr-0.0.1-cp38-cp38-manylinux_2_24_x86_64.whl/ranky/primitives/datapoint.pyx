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

from cython.parallel import prange
from libc.stdlib cimport atoi, strtof
from libc.string cimport strcpy

from libcpp.algorithm cimport find
from libcpp.string cimport string as cstr
from libcpp.string cimport npos

from cymem.cymem cimport Pool

cdef class DataPoint:

    def __init__(self, bytes raw_datapoint):

        self.max_feature = 50
        self.resize_step = 25

        self.feature_count = 0
        self.known_features = 0
        self.last_eval = 0.0
        self.mem = Pool()

        self.c = <DataPointC*> self.mem.alloc(1, sizeof(DataPointC))
        self.c.label = 0.0
        self.c.feature_values = features_t(50, NULL)

        try:
            with nogil:
                self.__parse_svmlight(raw_datapoint)
        except:
            raise ValueError("Error in DataPoint::init() : Invalid svmlight string format.")

    @property
    def label(self):
        return self.c.label

    @property
    def description(self):
        return self.c.description

    @property
    def id_(self):
        return self.c.id_

    @property
    def features(self):
        return <list?> [(self.c.feature_values[i].id_, self.c.feature_values[i].value )
                        for i in range(self.known_features) if self.c.feature_values[i] != NULL]

    cdef float get_value(self, int feature_id) nogil:
        if self.c.feature_values[feature_id] == NULL:
            raise KeyError(f"Error in DataPoint::get_value() : Invalid feature_id: {feature_id}")
        return self.c.feature_values[feature_id].value

    cdef void __parse_svmlight(self, bytes svmlight) nogil except *:
        """
        Parse a string line following svmlight format into a features_t structure.
        :param svmlight: bytes string
        :return: vector of feature structure
        """
        cdef int last_feature
        cdef size_t pos
        cdef char commentary, spacing, ft_delimiter
        cdef cstr estr, token
        cdef FeatureC ft

        last_feature = -1

        with gil:
            estr = cstr(svmlight)

        commentary = b'#'
        spacing = b' '
        ft_delimiter = b':'

        # ---- treating commentaries ---- #
        pos = estr.find(commentary)
        if pos != npos:
            if pos + 1 < estr.length():
                self.c.description = trim(estr.substr(pos+1))

            estr = trim(estr.substr(0, pos))


        # ---- first occurrence: label  ----- #
        pos = estr.find(spacing)
        token = estr.substr(0, pos)

        self.c.label = strtof(token.c_str(), NULL)

        if self.c.label < 0:
            raise ValueError("Error in DataPoint::parse() : Label must be defined (>=0).")

        # ---- second occurrence: queryID  ----- #
        estr.erase(0, pos+1)
        pos = estr.find(spacing)
        token = estr.substr(0, pos)

        if token.find(b"qid") == npos:
            raise ValueError("Error in DataPoint::parse() : Query ID must be defined.")

        self.c.id_ = token

        # ----- next occurrences: feature values ---- #
        estr.erase(0, pos+1)
        pos = estr.find(spacing)


        while pos != npos:
            token = estr.substr(0, pos)

            ft = DataPoint._unsafe_split_dot_pair(<char*> token.c_str(), &ft_delimiter)
            self.__add_feature(&ft)

            estr.erase(0, pos + 1)
            pos = estr.find(spacing)

        if estr.find(ft_delimiter) != npos:
            ft = DataPoint._unsafe_split_dot_pair(<char *> estr.c_str(), &ft_delimiter)
            self.__add_feature(&ft)


    cdef void __add_feature(self, FeatureC* ft) nogil except *:
        if ft.id_ <= 0:
            raise ValueError("Error in DataPoint::parse() : Cannot use feature numbering less than or equal" + \
                             " to zero. Start your features at 1.")

        if ft.id_ >= self.max_feature:
            while ft.id_ >= self.max_feature:
                self.max_feature += self.resize_step
            self.c.feature_values.resize(self.max_feature, NULL)

        with gil:
            self.c.feature_values[ft.id_] = <FeatureC *> self.mem.alloc(1, sizeof(FeatureC))
            self.c.feature_values[ft.id_].id_ = ft.id_
            self.c.feature_values[ft.id_].value = ft.value

        self.known_features += 1

        if ft.id_ > self.feature_count:
            self.feature_count = ft.id_

        if ft.id_ > self.last_eval:
            self.last_eval = ft.id_


    cdef features_t __vals_to_feature(self, fvals_t features):
        """
        Convert fvals_t to features_t types.
        :param features: fvals_t vector of feature values
        :return: pair (id, val) for each feature.
        """
        cdef features_t fts
        cdef FeatureC* c

        fts = features_t(features.capacity() + 1)

        for i in range(features.capacity() + 1):
            c = <FeatureC*> self.mem.alloc(1, sizeof(FeatureC))
            c.id_ = i
            c.value = features[i]
            fts[i] = c

        return fts

    # todo: 2. melhorar esquema de parsing (tornar mais gen?rico)
    # todo: 3. ranklists.