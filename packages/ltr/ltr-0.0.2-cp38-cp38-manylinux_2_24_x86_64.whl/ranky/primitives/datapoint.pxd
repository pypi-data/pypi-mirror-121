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
from libc.string cimport strtok
from libc.stdlib cimport atoi, strtof

from libcpp.vector cimport vector
from libcpp.string cimport string as cstr
from libcpp.string cimport npos

from cymem.cymem cimport Pool


cdef struct FeatureC:
    int id_
    float value

ctypedef vector[float] fvals_t
ctypedef vector[FeatureC*] features_t

cdef struct DataPointC:
    cstr id_
    cstr description
    float label
    features_t feature_values


cdef class DataPoint:
    cdef public int feature_count
    cdef public int known_features
    cdef public float last_eval
    cdef int max_feature, resize_step
    cdef Pool mem
    cdef DataPointC* c

    cdef float get_value(self, int feature_id) nogil

    cdef void __parse_svmlight(self, bytes svmlight) nogil except *

    cdef features_t __vals_to_feature(self, fvals_t features)
    cdef void __add_feature(self, FeatureC* ft) nogil except *

    @staticmethod
    cdef inline FeatureC _unsafe_split_dot_pair(char* dot_pair, const char* delimiter) nogil except *:
        """
        Split string by ':' char. Used in svmlight parsing. It's unsafe method because it doesn't treats
        cases like "foo:baz" strings. We consider that only numbers are passed in.
        :param dot_pair: 
        :return: 
        """
        cdef FeatureC * ft
        cdef char * id_
        cdef char * value

        id_ = strtok(dot_pair, delimiter)
        value = strtok(NULL, delimiter)

        if value == NULL:
            raise ValueError("Error in DataPoint::_unsafe_split_dot_pair: Invalid string")

        return FeatureC(atoi(id_),
                        strtof(value, NULL))


cdef inline cstr rtrim(const cstr s) nogil except *:
    cdef const char* whitespace = b" \n\r\t\f\v";
    cdef unsigned int end = s.find_last_not_of(whitespace)
    if end == npos:
        return cstr(b"")
    return s.substr(0, end+1)

cdef inline cstr ltrim(const cstr s) nogil except *:
    cdef const char* whitespace = b" \n\r\t\f\v";
    cdef unsigned int start = s.find_first_not_of(whitespace)
    if start == npos:
        return cstr(b"")
    return s.substr(start)

cdef inline cstr trim(const cstr s) nogil except *:
    return rtrim(ltrim(s))