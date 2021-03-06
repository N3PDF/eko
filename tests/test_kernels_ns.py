# -*- coding: utf-8 -*-
import numpy as np

from eko.kernels import non_singlet as ns
from eko import beta

methods = [
    "iterate-expanded",
    "decompose-expanded",
    "perturbative-expanded",
    "truncated",
    "ordered-truncated",
    "iterate-exact",
    "decompose-exact",
    "perturbative-exact",
]


def test_zero():
    """No evolution results in exp(0)"""
    nf = 3
    ev_op_iterations = 2
    gamma_ns = np.array([1, 1])
    for order in [0, 1]:
        for method in methods:
            np.testing.assert_allclose(
                ns.dispatcher(order, method, gamma_ns, 1.0, 1.0, nf, ev_op_iterations),
                1.0,
            )
            np.testing.assert_allclose(
                ns.dispatcher(
                    order, method, np.zeros(2), 2.0, 1.0, nf, ev_op_iterations
                ),
                1.0,
            )


def test_ode_lo():
    nf = 3
    ev_op_iterations = 10
    gamma_ns = np.random.rand(1)
    delta_a = -1e-6
    a0 = 0.3
    for a1 in [0.1, 0.2]:
        r = a1 * gamma_ns / (beta.beta(0, nf) * a1 ** 2)
        for method in methods:
            rhs = r * ns.dispatcher(0, method, gamma_ns, a1, a0, nf, ev_op_iterations)
            lhs = (
                ns.dispatcher(
                    0, method, gamma_ns, a1 + 0.5 * delta_a, a0, nf, ev_op_iterations
                )
                - ns.dispatcher(
                    0, method, gamma_ns, a1 - 0.5 * delta_a, a0, nf, ev_op_iterations
                )
            ) / delta_a
            np.testing.assert_allclose(lhs, rhs, atol=np.abs(delta_a))


# def test_ode_nlo():
#     nf = 3
#     ev_op_iterations = 10
#     gamma_ns = np.random.rand(2)
#     delta_a = -1e-6
#     a0 = 0.3
#     for a1 in [0.1, 0.2]:
#         r = (a1 * gamma_ns[0] + a1 ** 2 * gamma_ns[1]) / (
#             beta.beta(0, nf) * a1 ** 2 + beta.beta(1, nf) * a1 ** 3
#         )
#         for method in ["iterate-expanded"]:
#             rhs = r * ns.dispatcher(1, method, gamma_ns, a1, a0, nf, ev_op_iterations)
#             lhs = (
#                 ns.dispatcher(
#                     1, method, gamma_ns, a1 + 0.5 * delta_a, a0, nf, ev_op_iterations
#                 )
#                 - ns.dispatcher(
#                     1, method, gamma_ns, a1 - 0.5 * delta_a, a0, nf, ev_op_iterations
#                 )
#             ) / delta_a
#             np.testing.assert_allclose(lhs, rhs, atol=np.abs(delta_a))
