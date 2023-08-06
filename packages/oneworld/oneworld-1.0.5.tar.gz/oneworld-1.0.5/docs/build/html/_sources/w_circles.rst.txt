Circles and lines
-----------------



A conveninet way to represent point geospatial data is by using circles, which
will allow us to represent the values of a point by means of its color and/or
size. To add circles to a `WebMap` object, we will use the `add_circles`
method of the object. First we need to create the `WebMap` object::

    import oneworld as ow
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)

Now we can use the `add_circles` method of that object::


    mymap.add_circles(latitude = [36.122288, 40.007984, 32.232845]
                      longitude = [-97.069263, -105.265457, -110.950172],
                      constant_size = True)

In this example we have added three circles to the map, specifying their
coordinates as two sequences of latitude and longitude values. Given that
we have also set the `constant_size` parameter to True, the circles will
retain its size regardless of the zoom level:

.. raw:: html

      <iframe src="_static/tut_circ1.html" height="345px" width="100%"></iframe>

`oneworld` also admits `pandas` DataFrames as inputs. In this case, we will
use the `data` parameter in the `add_circles` method to specify the DataFrame,
and the `latitude` and `longitude` parameters to state the name of the column
in the dataframe containing the latitude and longitude coordinates, 
respectively. To plot the map from the previous example using dataframes, 
we would simply::

    import pandas as pd
    coords = {'lat': [36.122288, 40.007984, 32.232845],
              'lon': [-97.069263, -105.265457, -110.950172]}
    df = pd.DataFrame.from_dict(coords)

    mymap.add_circles(latitude = 'lat', longitude = 'lon', data = df,
                      constant_size = True)

Dataframes are a convenient way to store and manipulate data that `oneworld`
can use to visualize that data. For example, we can use the values in one
of the dataframe's columns to color each circle (in this case we use a 
preloaded dataset packaged with `oneworld` for testing purposes only)::

    df = ow.load_dataset('conferences')

    mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
                      color = 'Conference', constant_size = True)

.. raw:: html

      <iframe src="_static/tut_circ2.html" height="345px" width="100%"></iframe>

We have used the values in the "Conferences" column of the dataframe to
color each circle. When using values to color elements, `oneworld`
automatically adds a legend colorbar to the map. The elements used to
color the nodes can be either categorical or numerical::

    df = ow.load_dataset('conferences')

    mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
                      color = 'Expenditures', palette = 'YlOrRd', n_colors = 6,
                      constant_size = True, legend_pos = 'bottomleft')

.. raw:: html

      <iframe src="_static/tut_circ3.html" height="345px" width="100%"></iframe>

Besides using the "Expenditures" column of the dataframe (which contains
numerical data), we have also requested the 'YlOrRd' palette of colors with
6 colors, and placed the colorbar on the bottom left of the map. We can also
represent numerical values in our map using the `size` parameter. When doing
so, the radius of each circle will be scaled to represent its 
corresponding numerical value::

    df = ow.load_dataset('conferences')

    mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
                      size = 'Expenditures', constant_size = True)

.. raw:: html

      <iframe src="_static/tut_circ4.html" height="345px" width="100%"></iframe>

Note that we have requested the circles to maintain a constant size independent
of the zoom level. 

If you don't like working with dataframes because you feel that they are not
pythonic enough, all these parameters accept lists and tuples as well. They
also accept a single value, which will be applied to all the circles.

Lines work in the same way, except that now we have to specify two sets of
coordinates, one set of latitudes and longitudes for the starting points of the
lines, and one set for the ending points::

     w.WebMap(center = [39,-96.8], zoom = 4)
     mymap.add_lines(latitude0 = [29.964007, 32.278847, 44.975352],
                     longitude0 = [-90.107465, -106.747831, -93.230973],
                     latitude1 = [40.278822, 40.852768, 34.069322],
                     longitude1 = [-111.715293, -96.689506, -118.442436],
                     color = ['Big East', 'SBC', 'Pac 12'],
                     size = [18, 10, 35])

.. raw:: html

      <iframe src="_static/tut_lin1.html" height="345px" width="100%"></iframe>
