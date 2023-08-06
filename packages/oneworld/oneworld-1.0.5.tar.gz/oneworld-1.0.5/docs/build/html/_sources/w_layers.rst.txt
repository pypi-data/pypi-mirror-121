Layers: basemaps and overlays
-----------------------------

A basemap is a collection of tiles that will be used as a background image
in our map. We can add different sets of tiles to our map, but only one
set will be displayed at a time. In `oneworld`, basemaps are a type of
*layer* (the other type being `overlays`, more on that in a minute).
In the last section we did not
explicitly add any set of tiles to the map, 
so `oneworld` added the default basemap
for us. Let's start by creating the map object::

    import oneworld as ow
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)


Let's now add two basemaps, with a layer control panel so we can 
switch between the two basemaps::

    mymap.add_basemap(name = 'StreetMap', tiles = 'OSM')
    mymap.add_basemap(name = 'Terrain', tiles = 'Stamen_terrain')
    mymap.add_layer_control(collapsed = False)

After saving and opening the map, this is what we see:

.. raw:: html

      <iframe src="_static/tut_lay1.html" height="345px" width="100%"></iframe>

Given that we can only visualize one basemap at a time, the controls on the
layer control panel for basemaps are radio buttons. 

Another type of layer in `oneworld` is the `overlay`. Contrary to basemaps,
`overlays` do not display any image on the background, they are transparent.
More than one overlay can be displayed at a time, and their names appear
on the layer control panel next to check boxes. So, if they are transparent,
what is the use of having an overlay? well, some elements (like circles,
lines, etc.) can be added to layers (basemaps or overlays)
so that only the elements added to the active layers will be displayed.
Check out the next example where we have added circles to different layers,
including basemaps and overlays::

    mymap.add_layer_control(collapsed = False)

    mymap.add_basemap(name = 'No Reds', tiles = 'OSM')
    mymap.add_basemap(name = 'Reds', tiles = 'Stamen_watercolor')
    mymap.add_overlay(name = 'Blue')
    mymap.add_overlay(name = 'Purples')

    mymap.add_circles(latitude = [29.583058, 33.507507],
                      longitude = [-98.619407, -112.064633],
                      color = '#de2d26', size = 50000,
                      layer = 'Reds')
    mymap.add_circles(latitude = [40.007984],
                      longitude = [-105.265457],
                      color = '#3182bd', size = 50000,
                      layer = 'Blue')
    mymap.add_circles(latitude = [40.278822, 42.056887],
                      longitude = [-111.715293, -87.674991],
                      color = '#756bb1', size = 50000,
                      layer = 'Purples')

.. raw:: html

      <iframe src="_static/tut_lay2.html" height="345px" width="100%"></iframe>

If both `basemaps` and `overlays` are added to a map, the active `basemap` 
will always be displayed at the back of any active `overlay`. 

All added elements have a `layer` parameter that accepts a single value
(the name of a layer where all elements will be added to). Plus, circles
and lines also accept a list or tuple
or the name of a dataframe column containing the names of the layers
where each element will be added to::

   df = ow.load_dataset('conferences')

   mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
                     color = 'Expenditures', palette = 'YlOrRd',
                     constant_size = True, legend_pos = 'bottomleft',
                     layer = 'Conference')

In this example we haven't requested a layer control panel, but since we
added more than one layer to the map `oneworld` added it for us with
its default settings (hence why it is collapsed):

.. raw:: html

      <iframe src="_static/tut_lay3.html" height="345px" width="100%"></iframe>

Layers are a way of keeping maps organized in a tidy way when we add different
types of elements. The next example is a complex map packed with
information::

   mymap.add_layer_control(collapsed = False, position = 'topleft')

   mymap.add_basemap(name = 'Clear')
   mymap.add_basemap(name = 'Regions')
   mymap.add_basemap(name = 'Farms')

   df = ow.load_dataset('farms')
   mymap.add_choropleth(json_file = 'us_states.json',
                        geoid = 'FIPS', color = 'Region', data = df,
                        json_key = 'GEOID', layer = 'Regions')
   mymap.add_choropleth(json_file = 'us_states.json',
                        geoid = 'FIPS', color = 'Number of farms', data = df,
                        json_key = 'GEOID', palette = 'YlGn', layer = 'Farms')

   df = ow.load_dataset('conferences')
   mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
                     color = 'Expenditures', palette = 'RdBu',
                     constant_size = True, layer = 'Conference')

.. raw:: html

      <iframe src="_static/tut_lay4.html" height="345px" width="100%"></iframe>

Notice how the legend for the GeoJSON layers changes as we change
the active basemap. Also notice how `overlays` are always displayed on top of
`basemaps`.
