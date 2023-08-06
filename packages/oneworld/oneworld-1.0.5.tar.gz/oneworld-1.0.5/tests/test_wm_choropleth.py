'''Test WebMap choropleth'''
import oneworld as ow

def test_wm_choro():
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    df = ow.load_dataset('farms')
    mymap.add_choropleth(json_file = 'tests_data/us_states.json',
                         geoid = 'FIPS', color = 'Land in farms', data = df,
                         json_key = 'GEOID', palette = 'YlOrRd', n_colors = 6)
    mymap.savemap('webmap_choropleth.html')

if __name__ == "__main__":
   test_wm_choro()
