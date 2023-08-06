'''Test StaticMap choropleth'''
import oneworld as ow

def test_sm_choro():
   mymap = ow.StaticMap(view = [-125, -66.5, 21, 50],
                        central_longitude = -98.6,
                        projection = 'AlbersEqualArea')
   df = ow.load_dataset('farms')
   mymap.add_choropleth(shp_file = 'tests_data/us_state_20m.shp', data = df,
                        shp_key = 'GEOID', geoid = 'FIPS',
                        color = 'Land in farms',
                        palette = 'YlGn', n_colors = 8, edgecolor = 'grey')
   mymap.savemap('staticmap_choropleth.png')

if __name__ == "__main__":
    test_sm_choro()
