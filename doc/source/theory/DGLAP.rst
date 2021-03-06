Solving DGLAP
=============

We are solving the |DGLAP| equations given in x-space by

.. math::
    \frac{d}{d\ln(\mu_F^2)} \mathbf{f}(x,\mu_F^2) =
        \int\limits_x^1\!\frac{dy}{y}\, \mathbf{P}(x/y,a_s) \cdot \mathbf{f}(y,\mu_F^2)

with :math:`\mathbf P` the Altarelli-Parisi splitting functions (see :doc:`pQCD`).
In :doc:`Mellin space <Mellin>` the |DGLAP| equations are just differential equations:

.. math::
    \frac{d}{d\ln(\mu_F^2)} \tilde{\mathbf{f}}(\mu_F^2) = -\gamma(a_s) \cdot \tilde{\mathbf{f}}(\mu_F^2)

(Note the additional minus in the definition for :math:`\gamma`).

We change the evolution variable to the (monotonic) :ref:`theory/pQCD:strong coupling` :math:`a_s(\mu_F^2)`
and the equations to solve become

.. math::
    \frac{d}{da_s} \tilde{\mathbf{f}}(a_s)
        = \frac{d\ln(\mu_F^2)}{da_s} \cdot \frac{d \tilde{\mathbf{f}}(\mu_F^2)}{d\ln(\mu_F^2)} 
        = -\frac{\gamma(a_s)}{\beta(a_s)} \cdot \tilde{\mathbf{f}}(a_s)

This assumes the factorization scale :math:`\mu_F^2` (the inherit scale of the |PDF|) and the
renormalization scale :math:`\mu_R^2` (the inherit scale for the strong coupling) to be equal,
but tis constraint can however be lifted (see :ref:`theory/pQCD:scale variations`).

The (formal) solution can then be written in terms of an |EKO| :math:`\mathbf E` :cite:`Bonvini:2012sh`

.. math::
    \tilde{\mathbf{f}}(a_s) &= \tilde{\mathbf{E}}(a_s \leftarrow a_s^0) \cdot \tilde{\mathbf{f}}(a_s^0)\\
    \tilde{\mathbf{E}}(a_s \leftarrow a_s^0) &= \mathcal P \exp\left[-\int\limits_{a_s^0}^{a_s} \frac{\gamma(a_s')}{\beta(a_s')} da_s' \right]

with :math:`\mathcal P` the path-ordering operator. In the non-singlet sector the equations decouple and
we do not need to worry about neither matrices nor the path-ordering.

Using :doc:`Interpolation <Interpolation>` on both the inital and final |PDF|, we can then discretize the
|EKO| in x-space and define :math:`{\mathbf{E}}_{k,j}` (represented by
:class:`~eko.operator.Operator`) by

.. math::
    {\mathbf{E}}_{k,j}(a_s \leftarrow a_s^0) = \mathcal{M}^{-1}\left[\tilde{\mathbf{E}}(a_s \leftarrow a_s^0)\tilde p_j\right](x_k)

Now, we can write the solution to |DGLAP| in a true matrix operator scheme and find

.. math::
    \mathbf{f}(x_k,a_s) = {\mathbf{E}}_{k,j}(a_s \leftarrow a_s^0) \mathbf{f}(x_j,a_s^0)

so the |EKO| is a rank-4 operator acting both in flavor and momentum fraction space. 

The issue of matching conditions when crossing flavor thresholds is dicussed in a seperate :doc:`document <Matching>`

Leading Order
-------------

Expanding the anomalous dimension :math:`\gamma(a_s)` and the beta function :math:`\beta(a_s)`
to |LO| we obtain the (exact) |EKO|:

.. math::
    \ln \tilde {\mathbf E}^{(0)}(a_s \leftarrow a_s^0) &= \gamma^{(0)}\int\limits_{a_s^0}^{a_s} \frac{da_s'}{\beta_0 a_s'} = \gamma^{(0)} \cdot j^{(0,0)}(a_s,a_s^0)\\
    j^{(0,0)}(a_s,a_s^0) &= \int\limits_{a_s^0}^{a_s} \frac{da_s'}{\beta_0 a_s'} = \frac{\ln(a_s/a_s^0)}{\beta_0}

In |LO| we always use the *exact* solution.

LO Non-Singlet Evolution
^^^^^^^^^^^^^^^^^^^^^^^^

We find

.. math::
    \frac{d}{da_s} \tilde f_{ns}^{(0)}(a_s) = \frac{\gamma_{ns}^{(0)}}{\beta_0 a_s}  \cdot \tilde f_{ns}^{(0)}(a_s)

with :math:`\gamma_{ns}^{(0)} = \gamma_{ns,+}^{(0)} = \gamma_{ns,-}^{(0)} = \gamma_{ns,v}^{(0)} = \gamma_{qq}^{(0)}`.

The |EKO| is then given by a simple exponential :cite:`Vogt:2004ns`

.. math::
    \tilde E^{(0)}_{ns}(a_s \leftarrow a_s^0) = \exp\left[\gamma_{ns}^{(0)} \ln(a_s/a_s^0)/\beta_0 \right]

LO Singlet Evolution
^^^^^^^^^^^^^^^^^^^^

We find

.. math::
    \frac{d}{da_s} \dSV{0}{a_s} = \frac{\gamma_S^{(0)}}{\beta_0 a_s} \cdot \dSV{0}{a_s}\,, \qquad
    \gamma_S^{(0)} = \begin{pmatrix}
                                \gamma_{qq}^{(0)} & \gamma_{qg}^{(0)}\\
                                \gamma_{gq}^{(0)} & \gamma_{gg}^{(0)}
                            \end{pmatrix}

In order to exponentiate the EKO, we decompose it
:math:`\ln \mathbf{\tilde E}^{(0)}_S = \lambda_+ {\mathbf e}_+ + \lambda_- {\mathbf e}_-` with
the eigenvalues :math:`\lambda_{\pm}` and the projectors :math:`\mathbf e_{\pm}` given by :cite:`Vogt:2004ns`

.. math::
    \lambda_{\pm} &= \frac 1 {2} \left( \ln \tilde E_{qq}^{(0)} + \ln \tilde E_{gg}^{(0)} \pm \sqrt{(\ln \tilde E_{qq}^{(0)}-\ln \tilde E_{gg}^{(0)})^2 + 4\ln \tilde E_{qg}^{(0)}\ln \tilde E_{gq}^{(0)}} \right)\\
    {\mathbf e}_{\pm} &= \frac{1}{\lambda_{\pm} - \lambda_{\mp}} \left( \ln \mathbf{\tilde E}^{(0)}_S  - \lambda_{\mp} \mathbf I \right)

with :math:`\mathbf I` the 2x2 identity matrix in flavor space and, e.g., :math:`\ln \tilde E_{qq}^{(0)} = \gamma_{qq}^{(0)}j^{(0,0)}(a_s,a_s^0)`.

The projectors obey the usual properties, i.e.

.. math::
    {\mathbf e}_{\pm} \cdot {\mathbf e}_{\pm} = {\mathbf e}_{\pm}\,,\quad {\mathbf e}_{\pm} \cdot {\mathbf e}_{\mp} = 0\,,\quad \ep + \em = \mathbf I

and thus the exponentiation becomes easier again.

The |EKO| is then given by

.. math::
    \ESk{0}{a_s}{a_s^0} = \ep \exp(\lambda_{+}) + \em \exp(\lambda_{-})

Next-to-Leading Order
---------------------

NLO Non-Singlet Evolution
^^^^^^^^^^^^^^^^^^^^^^^^^

We find

.. math::
    \frac{d}{da_s} \tilde f_{ns}^{(1)}(a_s) = \frac{\gamma_{ns}^{(0)} a_s + \gamma_{ns}^{(1)} a_s^2}{\beta_0 a_s^2 + \beta_1 a_s^3} \cdot \tilde f_{ns}^{(1)}(a_s)

with :math:`\gamma_{ns} \in \{\gamma_{ns,+},\gamma_{ns,-}=\gamma_{ns,v}\}`.

We obtain the (exact) |EKO| :cite:`RuizArriola:1998er,Vogt:2004ns,Bonvini:2012sh`:

.. math::
    \ln \tilde E^{(1)}_{ns}(a_s \leftarrow a_s^0) &= \gamma^{(0)} \cdot j^{(0,1)}(a_s,a_s^0) + \gamma^{(1)} \cdot j^{(1,1)}(a_s,a_s^0)\\
    j^{(1,1)}(a_s,a_s^0) &= \int\limits_{a_s^0}^{a_s}\!da_s'\,\frac{a_s'^2}{\beta_0 a_s'^2 + \beta_1 a_s'^3} = \frac{1}{\beta_1}\ln\left(\frac{1+b_1 a_s}{1+b_1 a_s^0}\right)\\
    j^{(0,1)}(a_s,a_s^0) &= \int\limits_{a_s^0}^{a_s}\!da_s'\,\frac{a_s'}{\beta_0 a_s'^2 + \beta_1 a_s'^3} = j^{(0,0)}(a_s,a_s^0) - b_1 j^{(1,1)}(a_s,a_s^0)

Note that we recover the |LO| solution:

.. math::
    \ln \tilde E^{(1)}_{ns}(a_s \leftarrow a_s^0) = \ln \tilde E^{(0)}_{ns}(a_s \leftarrow a_s^0) + j^{(1,1)}(a_s,a_s^0)(\gamma^{(1)} - b_1 \gamma^{(0)})

In |NLO| we provide different strategies to define the |EKO|:

- ``method in ['iterate-exact', 'decompose-exact', 'perturbative-exact']``: use the *exact* solution as defined above
- ``method in ['iterate-expanded', 'decompose-expanded', 'perturbative-expanded']``: use the *exact* |LO| solution and substitute
  :math:`j^{(1,1)}(a_s,a_s^0) \to j^{(1,1)}_{exp}(a_s,a_s^0) = \frac 1 {\beta_0}(a_s - a_s^0)`
  and :math:`j^{(0,1)}(a_s,a_s^0) \to j^{(0,1)}_{exp}(a_s,a_s^0) = j^{(0,0)}(a_s,a_s^0) - b_1 j^{(1,1)}_{exp}(a_s,a_s^0)`
- ``method = 'ordered-truncated'``: expanding the *argument* of the exponential of the new term but keeping the order we obtain:

.. math::
    \tilde E^{(1)}_{ns}(a_s \leftarrow a_s^0) = \tilde E^{(0)}_{ns}(a_s \leftarrow a_s^0) \frac{1 + a_s/\beta_0 (\gamma_{ns}^{(1)} - b_1 \gamma_{ns}^{(0)})}{1 + a_s^0/\beta_0 (\gamma_{ns}^{(1)} - b_1 \gamma_{ns}^{(0)})}

- ``method = 'truncated'``: expanding the *whole* exponential of the new term we obtain:

.. math::
    \tilde E^{(1)}_{ns}(a_s \leftarrow a_s^0) = \tilde E^{(0)}_{ns}(a_s \leftarrow a_s^0) \left[1 + (a_s - a_s^0)/\beta_0 (\gamma_{ns}^{(1)} - b_1 \gamma_{ns}^{(0)}) \right]

NLO Singlet Evolution
^^^^^^^^^^^^^^^^^^^^^

We find

.. math::
    \frac{d}{da_s} \dSV{1}{a_s} = \frac{\gamma_{S}^{(0)} a_s + \gamma_{S}^{(1)} a_s^2}{\beta_0 a_s^2 + \beta_1 a_s^3} \cdot \dSV{1}{a_s}

with :math:`\gamma_{S}^{(0)} \gamma_{S}^{(1)} \neq \gamma_{S}^{(1)} \gamma_{S}^{(0)}`.

Here the strategies are:

- for ``method in ['iterate-exact', 'iterate-expanded']`` we use a discretized path-ordering :cite:`Bonvini:2012sh`:

.. math::
    \ESk{1}{a_s}{a_s^0} = \prod\limits_{k=n}^{0} \ESk{1}{a_s^{k+1}}{a_s^{k}}\quad \text{with} a_s^{n+1} = a_s

where the order of the product is such that later |EKO| are to the left and

.. math::
    \ESk{1}{a_s^{k+1}}{a_s^{k}} &= \exp\left(-\frac{\gamma(a_s^{k+1/2})}{\beta(a_s^{k+1/2})} \Delta a_s \right) \\
    a_s^{k+1/2} &= a_0 + \left(k+ \frac 1 2\right) \Delta a_s\\
    \Delta a_s &= \frac{a_s - a_s^0}{n + 1}

using the projector algebra from |LO| to exponentiate the single steps.

- for ``method in ['decompose-exact', 'decompose-expanded']``: use the exact or the approximate exact
  integrals from the non-singlet sector and then decompose :math:`\ln \tilde{\mathbf E}^{(1)}` - 
  this will neglect the non-commutativity of the singlet matrices.

- for ``method in ['perturbative-exact', 'perturbative-expanded', 'ordered-truncated', 'truncated']``
  we seek for an perturbative solution around the (exact) leading order operator:

We set :cite:`Vogt:2004ns`

.. math::
    \frac{d}{da_s} \dSV{1}{a_s} = \frac{\mathbf R (a_s)}{a_s} \cdot \dSV{1}{a_s}\,, \quad
    \mathbf R (a_s) = \sum\limits_{k=0} a_s^k \mathbf R_{k}

where in |NLO| we find

.. math::
    \mathbf R_0 = \gamma_{S}^{(0)}/\beta_0\,,\quad
    \mathbf R_1 = \gamma_{S}^{(1)}/\beta_0 - b_1 \gamma_{S}^{(0)}

and for the higher coefficients

- ``method = 'perturbative-exact'``: :math:`\mathbf R_k = - b_1 \mathbf R_{k-1}\,\text{for}\,k>1`
- ``method = 'perturbative-expanded'``: :math:`\mathbf R_k = 0\,\text{for}\,k>1`

We make an ansatz for the solution

.. math::
    \ESk{1}{a_s}{a_s^0} = \mathbf U (a_s) \ESk{0}{a_s}{a_s^0} {\mathbf U}^{-1} (a_s^0), \quad
    \mathbf U (a_s) = \mathbf I + \sum\limits_{k=1} a_s^k \mathbf U_k

Inserting this ansatz into the differential equation and sorting by powers of :math:`a_s`, we
obtain a recursive set of commutator relations for the evolution operator coefficients
:math:`\mathbf U_k`:

.. math::
    [\mathbf U_1, \mathbf R_0] &= \mathbf R_1 - \mathbf U_1\\
    [\mathbf U_k, \mathbf R_0] &= \mathbf R_k + \sum\limits_{j=1}^{k-1} \mathbf R_{k-j} \mathbf U_j - k \mathbf U_k = \mathbf{R}_k' - k \mathbf U_k\,,k>1

Multiplying these equations with :math:`\mathbf e_{\pm}` from left and right and using the identity

.. math::
    \mathbf U_k = \em \mathbf U_k \em + \em \mathbf U_k \ep + \ep \mathbf U_k \em + \ep \mathbf U_k \ep

we obtain the :math:`\mathbf U_k`:

.. math::
    \mathbf U_k = \frac{ \em \mathbf{R}_k' \em + \ep \mathbf{R}_k' \ep } k + \frac{\ep \mathbf{R}_k' \em}{r_- - r_+ + k} + \frac{\em \mathbf{R}_k' \ep}{r_+ - r_- + k}

So the strategies are

- ``method in ['perturbative-exact', 'perturbative-expanded']``: approximate the full evolution
  operator :math:`\mathbf U(a_s)` with an expansion up to ``ev_op_max_order``
- ``method in ['ordered-truncated', 'truncated']``: truncate the evolution operator :math:`\mathbf U(a_s)` and use

.. math::
    \ESk{1}{a_s}{a_s^0} = \ESk{0}{a_s}{a_s^0} + a_s \mathbf U_1 \ESk{0}{a_s}{a_s^0} - a_s^0 \ESk{0}{a_s}{a_s^0} \mathbf U_1