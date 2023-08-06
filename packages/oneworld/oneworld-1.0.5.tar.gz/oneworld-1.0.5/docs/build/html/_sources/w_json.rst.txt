GeoJSON files and choropleths
-----------------------------

GeoJSON files are containers for a collection of geographical *features*,
each feature containing the coordinates of each vertex of a polygon and
additional infomation regarding the geographical area encompassed inside
that polygon. Let's start by cr4eating a map to which we will add
the polygons of a GeoJSON file::

    import oneworld as ow
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    
We can add the polygons of a GeoJSON file to the map using
the `add_geojson` method::

    mymap.add_geojson(json_file = 'us_states.json')

In this example we have added the contents of the file 'us_states.json', which
are a collection of polygons representing the area of each of the states
in the United States of America:

.. raw:: html

      <iframe src="_static/tut_js1.html" height="345px" width="100%"></iframe>

We can also select a subset of the *features* in the file. In the next example,
we add to the map only those *features* whose "NAME" property matches
"Nebraska"::

    mymap.add_geojson(json_file = 'us_states.json', 
                      subset = 'Nebraska', subset_key = 'NAME')

.. raw:: html

      <iframe src="_static/tut_js2.html" height="345px" width="100%"></iframe>

As we did with the circles and lines, we can color each polygon in the file
according to some value, thus creating a choropleth. In this case we will
use the `add_choropleth` method of the map object, supplying the values
that we want to use to color each polygon in the same way we did the cricles
and lines (list, tuple or column of a dataframe). We will use another
sequence to identify each polygon according to the value of a given
property of its *feature*::

    df = ow.load_dataset('farms')
    mymap.add_choropleth(json_file = 'us_states.json',
                         geoid = 'FIPS', color = 'Region', data = df,
                         json_key = 'GEOID')

In this map we have used the "GEOID" property of each *feature* to uniquely
identify it. Then we have told the `add_choropleth` method to look in
the "FIPS" column of the dataframe for those values, and finally color
the *feature* according to the value found on the corresponding "Region"
column of the dataframe:

.. raw:: html

      <iframe src="_static/doc_chor.html" height="345px" width="100%"></iframe>

Like in the `add_circles` and `add_lines` methods, the `color` parameter
in the `add_choropleth` method accepts both categorical and numeric values::

   df = ow.load_dataset('farms')
   mymap.add_choropleth(json_file = 'us_states.json',
                        geoid = 'FIPS', color = 'Land in farms', data = df,
                        json_key = 'GEOID', palette = 'YlOrRd', n_colors = 6)

.. raw:: html

      <iframe src="_static/tut_js3.html" height="345px" width="100%"></iframe>

