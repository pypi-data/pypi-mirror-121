Information panel
-----------------

You can display information in a separate panel when hovering the mouse
over an added element by defining the `info_mouseover` parameter
when adding that element to the map. Let's create a map::

   import oneworld as ow
   mymap = ow.WebMap(center = [39,-96.8], zoom = 4)

Now let's add a choropleth to the map. When specifying the `info_mouseover` 
keyword upon adding items to the map, `oneworld` will also add a panel that
will display the specified info when the mouse is positionend above the
item added. The `info_mouseover` parameter accepts lists, tuples
and the name of a datframe column (if provided) as inputs::

   df = ow.load_dataset('farms')
   mymap.add_choropleth(json_file = 'us_states.json', json_key = 'GEOID',
                        geoid = 'FIPS', color = 'Region', data = df,
                        style_mouseover = {'color': '#636363'},
                        info_mouseover = 'Name')

.. raw:: html

      <iframe src="_static/tut_inf1.html" height="345px" width="100%"></iframe>

The `info_mouseover` parameter also accepts html format::

   mymap.add_panel(title = 'States of USA', width = '130px', height = '70px')

   df = ow.load_dataset('farms')
   info_l = ['<u>Name:</u><br />&nbsp;&nbsp;'+x for x in df['Name']]

   mymap.add_choropleth(json_file = 'us_states.json', json_key = 'GEOID',
                        geoid = 'FIPS', color = 'Region', data = df,
                        style_mouseover = {'color': '#636363'},
                        info_mouseover = info_l)

.. raw:: html

      <iframe src="_static/tut_inf2.html" height="345px" width="100%"></iframe>


In the last example, we have explicitly created the information panel, 
and manually set its title, width and height.
