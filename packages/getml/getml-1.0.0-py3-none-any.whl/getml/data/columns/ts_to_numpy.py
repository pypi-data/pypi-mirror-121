
# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Transform time stamp to numpy array
"""

import datetime

import numpy as np

def _ts_to_numpy(mat):

    def is_proper_ts(time_stamp):
        return (not np.isnan(time_stamp)) and (not np.isinf(time_stamp))

    def to_datetime(time_stamp):
        if time_stamp < 0.0:
            return datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=time_stamp)
        return datetime.datetime.utcfromtimestamp(time_stamp)

    shape = mat.shape
    
    mat = [
        np.datetime64(to_datetime(ts))
        if is_proper_ts(ts)
        else np.nan
        for ts in mat.ravel().tolist()
    ]
    
    mat = np.asarray(mat)

    return mat.reshape(shape[0], shape[1])
