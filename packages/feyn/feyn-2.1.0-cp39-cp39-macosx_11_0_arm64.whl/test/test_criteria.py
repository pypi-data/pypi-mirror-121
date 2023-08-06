import unittest
import numpy as np
import pandas as pd
import warnings

import feyn
from feyn._context import Context
from feyn._program import Program
from feyn.criteria._bootstrap import _assign_qcells_by_bootstrap
from feyn.criteria._clustering import _assign_qcells_by_clustering


class TestCriteria(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"x": ["a", "a", "b", "c"], "y": [1, 2, 3, 4]})

    def test_aic_computes(self):
        loss_value = 1e4
        param_count = 10
        n_samples = 100

        aic = feyn.criteria.aic(loss_value, param_count, n_samples)

        self.assertAlmostEqual(aic, 941, 0)

    def test_bic_computes(self):
        loss_value = 1e4
        param_count = 10
        n_samples = 100

        bic = feyn.criteria.bic(loss_value, param_count, n_samples)

        self.assertAlmostEqual(bic, 967, 0)

    def test_outside_math_domain_of_log_computes(self):
        loss_value = 0
        param_count = 10
        n_samples = 100

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", r"divide by zero encountered in log")
            bic = feyn.criteria.bic(loss_value, param_count, n_samples)
            aic = feyn.criteria.aic(loss_value, param_count, n_samples)

        assert bic == -np.inf
        assert aic == -np.inf

    def test_structural_diversity(self):
        ### Define test models
        features, self.output = list("abcde"), "output"
        ctx = Context()
        ctx.registers += features
        _, qcodes = ctx.query_to_codes("y", "'a'+'c'")
        p1 = Program(qcodes, -1, autopad=True)
        m1 = ctx.to_model(p1, self.output)
        _, qcodes = ctx.query_to_codes("y", "'a'*'c'")
        p2 = Program(qcodes, -1, autopad=True)
        m2 = ctx.to_model(p2, self.output)
        _, qcodes = ctx.query_to_codes("y", "'b'*'c'")
        p3 = Program(qcodes, -1, autopad=True)
        m3 = ctx.to_model(p3, self.output)
        models = [m1, m2, m3]
        # Assign dummy loss and bic values
        for m in models:
            m.bic = feyn.criteria.bic(
                loss_value=0.1, param_count=m._paramcount, n_samples=10
            )

        ### Compute structural diversity metric scores
        average_structural_diversity_difference_scores = (
            feyn.criteria._structural._compute_average_structural_diversity_difference_scores(
                models
            )
        )
        self.assertAlmostEqual(average_structural_diversity_difference_scores[0], 1.5)
        self.assertAlmostEqual(average_structural_diversity_difference_scores[1], 1.0)
        self.assertAlmostEqual(average_structural_diversity_difference_scores[2], 1.5)

        ### Apply criterion
        # Expecting m2 to be last in sorted order
        models_sorted = feyn.criteria._sort_by_structural_diversity(models)
        self.assertEqual(m2, models_sorted[-1])

    def test_qcell_assignment_by_clustering(self):
        num_qcells_to_assign_total = 20
        priority_number = 10
        qid_to_sample_priorities = _assign_qcells_by_clustering(
            self.df,
            priority_number=priority_number,
            num_qcells_to_assign_total=num_qcells_to_assign_total,
            max_num_clusters=2,
        )

        self.assertEqual(
            len(qid_to_sample_priorities.keys()), num_qcells_to_assign_total
        )
        self.assertEqual(len(set(qid_to_sample_priorities[0])), 2)

        print(qid_to_sample_priorities)

    def test_qcells_assignment_by_bootstrap(self):
        num_qcells_to_assign_total = 20

        qid_to_sample_priorities = _assign_qcells_by_bootstrap(
            self.df, num_qcells_to_assign_total=num_qcells_to_assign_total
        )

        self.assertEqual(
            len(qid_to_sample_priorities.keys()), num_qcells_to_assign_total
        )

        print(qid_to_sample_priorities)
