'''Test WebMap network'''
import oneworld as ow

def test_wm_net():
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    df = ow.load_dataset('conferences')
    mymap.add_network(latitude = 'Lat', longitude = 'Long', node_data = df,
                      group_connect = 'Conference',
                      edge_kwargs = {'style': {'weight': 0}},
                      node_kwargs = {'style_mouseover': {'color': '#636363'},
                                     'constant_size': True},
                      connect_mouseover = [{'color': '#636363'}, {'weight': 3}])
    mymap.savemap('webmap_network.html')

if __name__ == "__main__":
    test_wm_net()
