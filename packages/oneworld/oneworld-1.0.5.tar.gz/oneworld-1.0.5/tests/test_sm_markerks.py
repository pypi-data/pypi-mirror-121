'''Test StaticMap markers'''
import oneworld as ow

def test_sm_mark():
    mymap = ow.StaticMap(view = [-125, -66.5, 21, 50],
                         central_longitude = -98.6,
                         projection = 'AlbersEqualArea',
                         inner_borders = ['USA'])
    df = ow.load_dataset('conferences')
    mymap.add_markers(latitude = 'Lat', longitude = 'Long', data = df,
                      color = 'Conference', palette = 'Set2', n_colors = 6,
                      size = 'Expenditures', sizes = (10, 25),
                      marker = '*', legend_pos = 'center right')
    mymap.savemap('staticmap_markers.png')

if __name__ == "__main__":
    test_sm_mark()
