#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# simplicial_test -- a python module to realize simplicial degree-size sequences
#
# Copyright (C) 2020-2021 Tzu-Chi Yen <tzuchi.yen@colorado.edu>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from simplicial_test import Test, compute_joint_seq, if_facets_simplicial
import pickle

many_small_cases = pickle.load(open("datasets/multiple_small_test_cases.pickle", "rb"))


def test_batch_dataset():
    for degs, sizes in many_small_cases:
        st = Test(degs, sizes)
        is_simplicial, facets = st.is_simplicial()
        assert is_simplicial is True, print(degs, sizes)
        joint_seqs = compute_joint_seq(facets)
        assert if_facets_simplicial(facets) is True
        assert joint_seqs[0] == sorted(degs, reverse=True)
        assert joint_seqs[1] == sorted(sizes, reverse=True)
