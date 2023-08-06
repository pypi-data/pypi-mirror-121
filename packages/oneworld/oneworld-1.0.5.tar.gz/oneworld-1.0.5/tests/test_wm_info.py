'''Test WebMap information panel'''
import oneworld as ow

def test_wm_info():
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    mymap.add_panel(title = "States of USA", width = '130px', height = '70px')
    df = ow.load_dataset('farms')
    info_l = ["<u>Name:</u><br />&nbsp;&nbsp;"+x for x in df["Name"]]
    mymap.add_choropleth(json_file = 'tests_data/us_states.json', 
                         json_key = 'GEOID',
                         geoid = 'FIPS', color = 'Region', data = df,
                         style_mouseover = {'color': '#636363'},
                         info_mouseover = info_l)
    mymap.savemap('webmap_info.html')

if __name__ == "__main__":
    test_wm_info()
