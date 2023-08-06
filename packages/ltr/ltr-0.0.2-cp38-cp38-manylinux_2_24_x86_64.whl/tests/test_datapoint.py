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
import pytest

from ranky.primitives import DataPoint


def test_valid_datapoint_parsing():
    raw_valid_dp = b"1 qid:1 1:0.32 2:0.123 3:4.23  #some description"
    raw_hashtag_dp = b"2 qid:2 1:1.42 2:3.223 5:1.23  #"
    raw_without_description_dp = b"0 qid:3 3:0.32 2:0.123 1:4.23"

    dp = DataPoint(raw_valid_dp)

    assert dp.description == b'some description'
    assert dp.label == 1.0
    assert dp.id_ == b'qid:1'
    for ft, truth in zip(dp.features, [(1, 0.320), (2, 0.123), (3, 4.230)]):
        assert ft[0] == truth[0]
        assert truth[1] == pytest.approx(ft[1])

    dp = DataPoint(raw_hashtag_dp)

    assert dp.description == b''
    assert dp.label == 2.0
    assert dp.id_ == b'qid:2'
    for ft, truth in zip(dp.features, [(1, 1.420), (2, 3.223), (5, 1.230)]):
        assert ft[0] == truth[0]
        assert truth[1] == pytest.approx(ft[1])

    dp = DataPoint(raw_without_description_dp)

    assert dp.description == b''
    assert dp.label == 0.0
    assert dp.id_ == b'qid:3'
    for ft, truth in zip(dp.features, [(1, 4.230), (2, 0.123), (3, 0.320)]):
        assert ft[0] == truth[0]
        assert truth[1] == pytest.approx(ft[1])


def test_invalid_datapoint_parsing():
    invalid_label = b"-1 qid:1 1:0.32 2:0.123 3:4.23  #some description"
    invalid_label2 = b"qid:1 1:0.32 2:0.123 3:4.23  #some description"
    invalid_qid = b"2 :2 1:1.42 2:3.223 5:1.23  #"
    invalid_qid2 = b"0 3 3:0.32 2:0.123 1:4.23"
    invalid_qid4 = b"0 3:0.32 2:0.123 1:4.23"
    invalid_format = b"0 qid:3 30.32 2 0.123 1:4.23"
    invalid_format2 = b"0 qid:3 30.32 2: 0.123 1:4.23"

    with pytest.raises(Exception):
        dp = DataPoint(invalid_label)

    with pytest.raises(Exception):
        dp = DataPoint(invalid_label2)

    with pytest.raises(Exception):
        dp = DataPoint(invalid_qid)

    with pytest.raises(Exception):
        dp = DataPoint(invalid_qid2)

    with pytest.raises(Exception):
        dp = DataPoint(invalid_qid4)

    with pytest.raises(Exception):
        dp = DataPoint(invalid_format)

    with pytest.raises(Exception):
        dp = DataPoint(invalid_format2)