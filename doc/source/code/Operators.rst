Operator Classes
=================

The classes are nested as follows:

.. graphviz::
    :name: operators
    :caption: nesting of the operator classes: solid lines means "has many",
                dashed lines means "evolves into"
    :align: center

    digraph G {
        bgcolor = transparent

        node [shape=box]
        OperatorGrid [label="OperatorGrid"];
        OperatorMaster [label="OperatorMaster" ];
        test, test1 [style=invis];
        Operator [label="Operator" ];
        PhysicalOperator [label="PhysicalOperator"];
        OpMember [label="OpMember"];

        {rank=same OperatorMaster test test1}
        {rank=same Operator PhysicalOperator}

        OperatorGrid -> OperatorMaster;
        OperatorMaster -> Operator  [weight=1000];
        Operator -> OpMember;
        Operator -> PhysicalOperator [style=dashed len=10];
        PhysicalOperator -> OpMember
        OperatorMaster -> test -> test1 [style=invis];
        test1 -> PhysicalOperator [weight=1000 style=invis];
    }

- :class:`~eko.operator.grid.OperatorGrid`

    *  this is the master class which administrates all evolution kernel operator tasks
    *  it is instantiated once for each run
    *  it divides the given range of :math:`Q^2` into the necessary threshold crossings and
       creates a :class:`~eko.operator.grid.OperatorMaster` for each
    *  it recollects all necessary operators in the end to create the
       :class:`~eko.operator.physical.PhysicalOperator` following the instructions of
       :class:`~eko.flavours.FlavourTarget`

- :class:`~eko.operator.grid.OperatorMaster`

    * this represents a configuration for a fixed number of flavours
    * it creates an :class:`~eko.operator.Operator` for each final scale :math:`Q^2`

- :class:`~eko.operator.Operator`

    * this represents a configuration for a fixed final scale :math:`Q^2`
    * this class is only used *internally*
    * its :class:`~eko.operator.member.OpMember` are only valid in the current
      threshold area

- :class:`~eko.operator.physical.PhysicalOperator`

    * this is the exposed equivalent of :class:`~eko.operator.Operator`,
      i.e. it also lives at at fixed final scale
    * its :class:`~eko.operator.member.OpMember` are valid from the starting scale
      to the final scale

- :class:`~eko.operator.member.OpMember`

    * this represents a single evolution kernel operator
    * inside :class:`~eko.operator.Operator` they are in "raw" evolution basis, i.e.
      :math:`\tilde{\mathbf{E}}_S, \tilde{E}_{ns}^{\pm,v}`, and they never cross a threshold
    * inside :class:`~eko.operator.physical.PhysicalOperator` they are in "true" evolution
      basis, i.e. they evolve e.g. :math:`\tilde V, \tilde T_3` etc., so they are eventually
      a product of the "raw" basis (see :doc:`Matching Conditions </theory/Matching>`)