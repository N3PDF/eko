Matching Conditions on Crossing Thresholds
==========================================

The :class:`~eko.flavours.FlavourTarget` class is used to provide a consistent transition in the Variable
Flavour Number Scheme (VFNS) of the :doc:`evolution distributions <FlavourBasis>` across the mass thresholds provided by
the :class:`~eko.thresholds.Threshold` class.
We denote the solution of the :doc:`DGLAP equation <DGLAP>` in :doc:`Mellin space <Mellin>` as

.. math ::
    \tilde{f_j}(Q^2_1)= \tilde E_{jk}(Q^2_1\leftarrow Q^2_0) \tilde{f_k}(Q^2_0)

For the singlet sector, we define the singlet evolution kernel matrix

.. math ::
    \ES{Q_1^2}{Q_0^2} = \begin{pmatrix}
        \tilde E_{qq} & \tilde E_{qg}\\
        \tilde E_{gq} & \tilde E_{gg}
    \end{pmatrix}(Q_1^2\leftarrow Q_0^2)

which is the only coupled system amongst the DGLAP equations.

Next, we list the matching conditions for the different evolution distributions up to LO.
Note, that the non-trivial matching of the discontinuities only enters at NNLO.

Zero Thresholds
---------------

Here, we consider :math:`m_{q}^2 < Q_0^2 < Q_1^2 < m_{q+1}^2` and we assume that
:math:`m_q` is the mass of the :math:`n_f`-th flavour. This configuration corresponds
effectivelyto a Fixed Flavour Number Scheme (FFNS).
Here all distributions simply evolve with their associated operator.
The singlet sector and the full valence distributions are given by

.. math ::
        \dSV{n_f}{Q_1^2} &= \ES{Q^2_1}{Q_0^2} \dSV{n_f}{Q_0^2}\\
        \dVf{n_f}{Q_1^2} &= \Ensv{Q^2_1}{Q_0^2} \dVf{n_f}{Q_0^2}

If the valence-like/singlet-like non-singlet distributions are already active,
they keep evolving from themselves

.. math ::
    \dVj{j}{n_f}{Q_1^2} &= \Ensm{Q^2_1}{Q_0^2} \dVj{j}{n_f}{Q_0^2} \\
    \dTj{j}{n_f}{Q_1^2} &= \Ensp{Q^2_1}{Q_0^2} \dTj{j}{n_f}{Q_0^2} \\
     &\text{for }j=3,\ldots, n_f^2-1

Otherwise, they are generated dynamically by the full valence distribution or the singlet
sector respectively

.. math ::
    \dVj{k}{n_f}{Q_1^2} &= \Ensv{Q^2_1}{Q_0^2} \dVf{n_f}{Q_0^2} \\
    \dTj{k}{n_f}{Q_1^2} &= \left(1, 0\right)\ES{Q_1^2}{Q_0^2}\dSV{n_f}{Q_0^2} \\
     &\text{for }k=(n_f+1)^2-1, \ldots, 35

and making the distributions thus linearly dependent :math:`V_k = V, T_k = \Sigma`
(as they should).

.. IC in FFNS
    S.S = P_qq
    S.g = P_qg
    g.S = P_gq
    g.g = P_gg
    V.V = NS_v
    V3.V3 = NS_m
    V8.V8 = NS_m
    T3.T3 = NS_p
    T8.T8 = NS_p
    c+.c+ = 1
    c-.c- = 1
.. IC in VFNS: q0 < q < mc
    S3.S3 = P_qq
    S.g = P_qg
    g.S = P_gq
    g.g = P_gg
    V.V = NS_v
    V3.V3 = NS_m
    V8.V8 = NS_m
    T3.T3 = NS_p
    T8.T8 = NS_p
    T15.S = P_qq
    T15.g = P_qg
    now add IC:
    T15.c+ = -3
    V15.c- = -3
.. IC in VFNS: q0 < mc < q:
    S.S = P_qq^4 @ P_qq^3 + P_qg^4 @ P_gq^3
    ...
    V.V = NS_v @ NS_v
    ...
    T15.S = NS_p^4 @ P_qq^3
    T15.g = NS_p^4 @ P_qg^3
    now add IC:
    T15.c+ = -3 NS_p^4

One Threshold
-------------

Here, we consider :math:`m_q^2 < Q_0^2 < m_{q+1}^2 < Q_1^2 < m_{q+2}^2` and we assume that
:math:`m_q` is the mass of the :math:`n_f`-th flavour.
The singlet sector and the full valence distributions are given by

.. math ::
    \dSV{n_f+1}{Q_1^2}    &= \ES{Q^2_1}{m_{q+1}^2} \ES{m_{q+1}^2}{Q_0^2} \dSV{n_f}{Q_0^2} \\
    \dVj{j}{n_f+1}{Q_1^2} &= \Ensv{Q^2_1}{m_{q+1}^2} \Ensv{m_{q+1}^2}{Q^2_0} \dVf{n_f}{Q_0^2}

If the valence-like/singlet-like non-singlet distributions have already been active before
the threshold, they keep evolving from themselves

.. math ::
    \dVj{j}{n_f+1}{Q_1^2} &= \Ensm{Q^2_1}{m_{q+1}^2}\Ensm{m_{q+1}^2}{Q_0^2} \dVj{j}{n_f}{Q_0^2}\\
    \dTj{j}{n_f+1}{Q_1^2} &= \Ensp{Q^2_1}{m_{q+1}^2}\Ensp{m_{q+1}^2}{Q_0^2} \dTj{j}{n_f}{Q_0^2}\\
     &\text{for }j=3,\ldots, n_f^2-1

The two distributions which become active after crossing the threshold are generated
dynamically up to the threshold and then set themselves apart:

.. math ::
    \dVj{j'}{n_f+1}{Q_1^2} &= \Ensm{Q^2_1}{m_{q+1}^2}\Ensv{m_{q+1}^2}{Q_0^2} \dVf{n_f}{Q_0^2} \\
    \dTj{j'}{n_f+1}{Q_1^2} &= \Ensp{Q^2_1}{m_{q+1}^2}\left(1,0\right)\ES{m_{q+1}^2}{Q_0^2} \dSV{n_f}{Q_0^2} \\
     & \text{for }j'=(n_f+1)^2-1

The remaining distributions are generated again purely dynamically:

.. math ::
    \dVj{k}{n_f+1}{Q_1^2} &= \Ensv{Q^2_1}{m_{q+1}^2}\Ensv{m_{q+1}^2}{Q_0^2} \dVf{n_f}{Q_0^2} \\
    \dTj{k}{n_f+1}{Q_1^2} &= \left(1, 0\right)\ES{Q_1^2}{m_{q+1}^2}\ES{m_{q+1}^2}{Q_0^2}\dSV{n_f}{Q_0^2} \\
     & \text{for }k=(n_f+2)^2-1, \ldots, 35

Two Thresholds
--------------

Here, we consider :math:`m_q^2 < Q_0^2 < m_{q+1}^2 < m_{q+2}^2 < Q_1^2 < m_{q+3}^2` and we assume that
:math:`m_q` is the mass of the :math:`n_f`-th flavour.
The singlet sector and the full valence distributions are given by

.. math ::
    \dSV{n_f+2}{Q_1^2}    &= \ES{Q^2_1}{m_{q+2}^2} \ES{m_{q+2}^2}{m_{q+1}^2} \ES{m_{q+1}^2}{Q_0^2} \dSV{n_f}{Q_0^2} \\
    \dVj{j}{n_f+2}{Q_1^2} &= \Ensv{Q^2_1}{m_{q+2}^2} \Ensv{m_{q+2}^2}{m_{q+1}^2} \Ensv{m_{q+1}^2}{Q^2_0} \dVf{n_f}{Q_0^2}

If the valence-like/singlet-like non-singlet distributions have already been active before
the threshold, they keep evolving from themselves

.. math ::
    \dVj{j}{n_f+2}{Q_1^2} &= \Ensm{Q^2_1}{m_{q+2}^2}\Ensm{m_{q+2}^2}{m_{q+1}^2}\Ensm{m_{q+1}^2}{Q_0^2} \dVj{j}{n_f}{Q_0^2}\\
    \dTj{j}{n_f+2}{Q_1^2} &= \Ensp{Q^2_1}{m_{q+2}^2}\Ensp{m_{q+2}^2}{m_{q+1}^2}\Ensp{m_{q+1}^2}{Q_0^2} \dTj{j}{n_f}{Q_0^2}\\
     &\text{for }j=3,\ldots, n_f^2-1

The two distributions which become active after crossing the *first* threshold are generated
dynamically up to the first threshold and then set themselves apart:

.. math ::
    \dVj{j'}{n_f+2}{Q_1^2} &= \Ensm{Q^2_1}{m_{q+2}^2}\Ensm{m_{q+2}^2}{m_{q+1}^2}\Ensv{m_{q+1}^2}{Q_0^2} \dVf{n_f}{Q_0^2} \\
    \dTj{j'}{n_f+2}{Q_1^2} &= \Ensp{Q^2_1}{m_{q+2}^2}\Ensp{m_{q+2}^2}{m_{q+1}^2}\left(1,0\right)\ES{m_{q+1}^2}{Q_0^2} \dSV{n_f}{Q_0^2} \\
     & \text{for }j'=(n_f+1)^2-1

The two distributions which become active after crossing the *second* threshold are generated
dynamically up to the second threshold and then set themselves apart:

.. math ::
    \dVj{j''}{n_f+2}{Q_1^2} &= \Ensm{Q^2_1}{m_{q+2}^2}\Ensv{m_{q+2}^2}{m_{q+1}^2}\Ensv{m_{q+1}^2}{Q_0^2} \dVf{n_f}{Q_0^2} \\
    \dTj{j''}{n_f+2}{Q_1^2} &= \Ensp{Q^2_1}{m_{q+2}^2}\left(1,0\right)\ES{m_{q+2}^2}{m_{q+1}^2} \ES{m_{q+1}^2}{Q_0^2} \dSV{n_f}{Q_0^2} \\
     & \text{for }j''=(n_f+2)^2-1

If there is a distributions remaining it is generated again purely dynamically:

.. math ::
    \dVj{k}{n_f+2}{Q_1^2} &= \Ensv{Q^2_1}{m_{q+2}^2}\Ensv{m_{q+2}^2}{m_{q+1}^2}\Ensv{m_{q+1}^2}{Q_0^2} \dVf{n_f}{Q_0^2} \\
    \dTj{k}{n_f+2}{Q_1^2} &= \left(1, 0\right)\ES{Q_1^2}{m_{q+2}^2}\ES{m_{q+2}^2}{m_{q+1}^2}\ES{m_{q+1}^2}{Q_0^2}\dSV{n_f}{Q_0^2} \\
     & \text{for }k=(n_f+3)^2-1

Three Thresholds
----------------

Here, we consider :math:`0 < Q_0^2 < m_{c}^2 < m_{b}^2 < m_{t}^2 < Q_1^2 < \infty`.
The singlet sector and the full valence distributions are given by

.. math ::
    \dSV{6}{Q_1^2} &=       \ES{Q^2_1}{m_{t}^2} \ES{m_t^2}{m_{b}^2} \\
                   & \quad  \ES{m_b^2}{m_{c}^2} \ES{m_{c}^2}{Q_0^2} \dSV{3}{Q_0^2} \\
    \dVj{j}{6}{Q_1^2} &=      \Ensv{Q^2_1}{m_{t}^2}   \Ensv{m_{t}^2}{m_{b}^2} \\
                      & \quad \Ensv{m_{b}^2}{m_{c}^2} \Ensv{m_{c}^2}{Q^2_0} \dVf{3}{Q_0^2}

The valence-like/singlet-like non-singlet distributions containing flavours up to strange,
they keep evolving from themselves

.. math ::
    \dVj{j}{6}{Q_1^2} &=      \Ensm{Q^2_1}{m_{t}^2}   \Ensm{m_{t}^2}{m_{b}^2} \\
                      & \quad \Ensm{m_{b}^2}{m_{c}^2} \Ensm{m_{c}^2}{Q_0^2} \dVj{j}{3}{Q_0^2} \\
    \dTj{j}{6}{Q_1^2} &=      \Ensp{Q^2_1}{m_{t}^2}   \Ensp{m_t^2}{m_{qb}^2} \\
                      & \quad \Ensp{m_{b}^2}{m_{c}^2} \Ensp{m_{c}^2}{Q_0^2} \dTj{j}{3}{Q_0^2} \\
     &\text{for }j=3,8

The two distributions containing charm are generated dynamically up to the first threshold
and then set themselves apart:

.. math ::
    \dVj{15}{6}{Q_1^2} &=      \Ensm{Q^2_1}{m_{t}^2}   \Ensm{m_{t}^2}{m_{b}^2} \\
                       & \quad \Ensm{m_{b}^2}{m_{c}^2} \Ensv{m_{c}^2}{Q_0^2} \dVf{3}{Q_0^2} \\
    \dTj{15}{6}{Q_1^2} &=      \Ensp{Q^2_1}{m_{t}^2} \Ensp{m_{t}^2}{m_{b}^2} \\
                       & \quad \Ensp{m_{b}^2}{m_{c}^2} \left(1,0\right)\ES{m_{c}^2}{Q_0^2} \dSV{3}{Q_0^2}

The two distributions containing bottom are generated dynamically up to the second threshold
and then set themselves apart:

.. math ::
    \dVj{24}{6}{Q_1^2} &=      \Ensm{Q^2_1}{m_{t}^2}   \Ensm{m_{t}^2}{m_{b}^2} \\
                       & \quad \Ensv{m_{b}^2}{m_{c}^2} \Ensv{m_{c}^2}{Q_0^2} \dVf{3}{Q_0^2} \\
    \dTj{24}{6}{Q_1^2} &=      \Ensp{Q^2_1}{m_{t}^2} \Ensp{m_{t}^2}{m_{b}^2} \\
                       & \quad \left(1,0\right) \ES{m_{b}^2}{m_{c}^2} \ES{m_{c}^2}{Q_0^2} \dSV{3}{Q_0^2}

The two distributions containing top are generated dynamically up to the third threshold
and then set themselves apart:

.. math ::
    \dVj{35}{6}{Q_1^2} &=      \Ensm{Q^2_1}{m_{t}^2}   \Ensv{m_{t}^2}{m_{b}^2} \\
                       & \quad \Ensv{m_{b}^2}{m_{c}^2} \Ensv{m_{c}^2}{Q_0^2} \dVf{3}{Q_0^2} \\
    \dTj{35}{6}{Q_1^2} &=      \Ensp{Q^2_1}{m_{t}^2} \left(1,0\right) \ES{m_{t}^2}{m_{b}^2} \\
                       & \quad \ES{m_{b}^2}{m_{c}^2} \ES{m_{c}^2}{Q_0^2} \dSV{3}{Q_0^2}