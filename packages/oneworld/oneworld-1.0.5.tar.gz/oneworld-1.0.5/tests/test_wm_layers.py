'''Test WebMap layers'''
import oneworld as ow

def test_wm_lay():
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    mymap.add_layer_control(collapsed = False, position = 'topleft')

    mymap.add_basemap(name = 'Clear')
    mymap.add_basemap(name = 'Regions')
    mymap.add_basemap(name = 'Farms')

    df = ow.load_dataset('farms')
    mymap.add_choropleth(json_file = 'tests_data/us_states.json',
                         geoid = 'FIPS', color = 'Region', data = df,
                         json_key = 'GEOID', layer = 'Regions')
    mymap.add_choropleth(json_file = 'tests_data/us_states.json',
                         geoid = 'FIPS', color = 'Number of farms', data = df,
                         json_key = 'GEOID', palette = 'YlGn', layer = 'Farms')

    df = ow.load_dataset('conferences')
    mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
                      color = 'Expenditures', palette = 'RdBu',
                      constant_size = True, layer = 'Conference')
    mymap.savemap('webmap_layers.html')

if __name__ == "__main__":
    test_wm_lay()
