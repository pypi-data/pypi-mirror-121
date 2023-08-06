Getting started
---------------

Let's start by creating a `WebMap` object. We will specify the center
of the map as well as the initial zoom level (we will use the default values
for the rest of the parameters)::

    import oneworld as ow
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)

The `WebMap` object is a container for all the elements
that we will be adding to the map (think of it as the `figure` object in a
`matplotlib` plot). Now of course this doesn't show anything on our screens,
we have to save the map into an html file::

    mymap.savemap('Tutorial.html')

Now we can open this file with our favorite web browser, and we should see
something like this:

.. raw:: html

      <iframe src="_static/Tutorial.html" height="345px" width="100%"></iframe>

Now that we have created our `WebMap` object, let's add some elements to it.

.. note:: In all the examples of the following sections
          the `savemap` line is omitted for clarity.
