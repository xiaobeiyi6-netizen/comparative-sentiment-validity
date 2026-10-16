# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Tiny deterministic algebra checks; no results in these tests come from study participants."""
import unittest
class TestReversalIdentity(unittest.TestCase):
    def test_signed_misclassification_identity(self):
        for tp,fn,fp,tn in [(7,3,2,8),(4,6,1,9),(0,5,5,0)]:
            n=tp+fn+fp+tn
            p=(tp+fn)/n;q=(tp+fp)/n
            fpr=fp/(fp+tn);fnr=fn/(tp+fn)
            self.assertAlmostEqual(q-p,(1-p)*fpr-p*fnr)
    def test_pairwise_reversal_when_bias_exceeds_gap(self):
        true_a,true_b=.8,.6; pred_a,pred_b=.2,.5
        self.assertTrue((true_a-true_b)*(pred_a-pred_b)<0)
    def test_pair_tie_is_not_strict_reversal(self):
        self.assertFalse((.8-.6)*(.3-.3)<0)
if __name__=='__main__':unittest.main()

