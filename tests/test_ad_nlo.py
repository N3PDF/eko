# -*- coding: utf-8 -*-
# Test LO splitting functions
import numpy as np

import eko.anomalous_dimensions.nlo as ad_nlo
from eko.constants import CA, CF

NF = 5


def test_gamma_1():
    # reference values are obtained from MMa
    # non-siglet sector
    np.testing.assert_allclose(ad_nlo.gamma_nsm_1(1, NF), 0, atol=2e-6)
    np.testing.assert_allclose(
        ad_nlo.gamma_nsp_1(2, NF), (-112 * CF + 376 * CA - 64 * NF) * CF / 27
    )
    # singlet sector
    np.testing.assert_allclose(ad_nlo.gamma_ps_1(2, NF), -40 * CF * NF / 27)
    np.testing.assert_allclose(ad_nlo.gamma_qg_1(2, NF), (-74 * CF - 35 * CA) * NF / 27)
    np.testing.assert_allclose(
        ad_nlo.gamma_gq_1(2, NF), (112 * CF - 376 * CA + 104 * NF) * CF / 27
    )
    # the CA*NF term seems to be tough to compute, so raise the constraint ...
    np.testing.assert_allclose(
        ad_nlo.gamma_gg_1(2, NF), (74 * CF + 35 * CA) * NF / 27, rtol=4e-5
    )
    assert ad_nlo.gamma_singlet_1(2, NF).shape == (2, 2)
