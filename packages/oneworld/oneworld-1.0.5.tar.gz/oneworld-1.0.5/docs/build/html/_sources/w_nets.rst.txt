Networks
--------

A network is a collection of nodes connected by edges. In `oneworld`, nodes
are represented by circles, connected qith lines. We have two ways of
specify the connectivity: explicitly and by grouping. In both cases we will
need first to define the position of the nodes, and then their conenctivity
using one of the two methods. The most explicit way of doing it is to use
two sequences (lists, tuples or columns of a dataframe), one that will
contain the indexes of the starting nodes, and one that will contain the
indexes of the target nodes (note that, implicitly, each pair of elements
in the source and target sequences defines one edge). First of all we need
a new map::

    import oneworld as ow
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)

Now, for example, if in the
conferences dataset we wanted
to to connect the second and the third node,
the second and the fifth node and the fifth and the eight node we would::

    df = ow.load_dataset('conferences')
    mymap.add_network(latitude = 'Lat', longitude = 'Long', node_data = df,
                      source = [2, 2, 5], target = [3, 5, 8])

.. raw:: html

      <iframe src="_static/doc_net1.html" height="345px" width="100%"></iframe>

The second method of defining the connectivity is more specific and will only
be suitable for some maps. If we wanted to fully connect all nodes that have
the same value in a variable, we can use the `group_connect` parameter of
the method::

    df = ow.load_dataset('conferences')

    mymap.add_network(latitude = 'Lat', longitude = 'Long', node_data = df, 
                      group_connect = 'Conference')

.. raw:: html

      <iframe src="_static/doc_net2.html" height="345px" width="100%"></iframe>

In this map we have fully connected between themselves all the nodes that have 
the same value in the 'Conference' column of the dataframe. Note that 
`oneworld` has also colored nodes and edges according to the value in that 
column. If we want to explicitly define the characteristics for the nodes
and edges, we can use the `node_kwargs` and `edge_kwargs` of the method
(and optionally the `node_data` and `edge_data` parameters)::

     df_n = ow.load_dataset('conferences')
     df_e = ow.load_dataset('connections')

     mymap.add_network(latitude = 'Lat', longitude = 'Long', node_data = df_n,
                       source = 'Init', target = 'Final', edge_data = df_e,
                       node_kwargs = {'color': 'Conference',
                                      'constant_size': True},
                       edge_kwargs = {'size': 'Intensity'})

.. raw:: html

      <iframe src="_static/tut_net1.html" height="345px" width="100%"></iframe>
