Styles
------

Almost all added elements in a `WebMap` object, including circles, lines, 
networks and
polygons accept a `style` parameter in the form of a dictionary, 
which defines aesthetic items common
to all added elements. Note that, when defined, keywords defined in this 
parameter override those in the `color` and `size` parameters. After creating
the map object::

   import oneworld as ow
   mymap = ow.WebMap(center = [39,-96.8], zoom = 4) 

We can add some circles and define their basic style along with a variable
color::

   df = ow.load_dataset('conferences')
   mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
                     color = 'Conference', constant_size = True,
                     style = {'color': '#636363', 'fillOpacity': 1.0})

.. raw:: html

      <iframe src="_static/tut_sty1.html" height="345px" width="100%"></iframe>

For a full list of customizable aesthetic variables, please see the
`leaflet styles`_. All these added elements can also change the style when
the mouse is hovered above each one of them, using the `style_mouseover`
parameter::

   df = ow.load_dataset("farms")
   mymap.add_choropleth(json_file = "us_states.json", json_key = "GEOID",
                        geoid = "FIPS", color = "Region", data = df,
                        style = {'weight': 1, 'color' : '#636363',
                                 'fillOpacity': 0.6},
                        style_mouseover = {'weight': 5, 'color': '#000000',
                                           'fillColor': '#bdbdbd',
                                           'fillOpacity': 1})

When the mouse is hovered over an element, its style changes to that defined
in `style_mouseover`. When the mouse moves away from the element, its style
changes back to that specified in the `style` parameter (and the `color`
and `size` parameters if defined):

.. raw:: html

      <iframe src="_static/tut_sty2.html" height="345px" width="100%"></iframe>

When adding networks, you can also define the styles of the neighboring nodes
of the node that is being hovered, as well as the connecting edges, using
the `connect_mouseover` parameter. If used, `connect_mouseover` must be a list
or a tuple, the first element of which must be the style of the neighboring 
nodes, and the second must be the style of the connecting edges::

   df = ow.load_dataset("conferences")
   mymap.add_network(latitude = 'Lat', longitude = 'Long', node_data = df,
                     group_connect = 'Conference',
                     edge_kwargs = {'style': {'weight': 0}},
                     node_kwargs = {'style_mouseover': {'color': '#636363'},
                                    'constant_size': True},
                     connect_mouseover = [{'color': '#636363'}, {'weight': 3}])

.. raw:: html

      <iframe src="_static/tut_sty3.html" height="345px" width="100%"></iframe>

.. seealso::
      
      `leaflet styles`_

.. _leaflet styles: https://leafletjs.com/reference-1.6.0.html#path

