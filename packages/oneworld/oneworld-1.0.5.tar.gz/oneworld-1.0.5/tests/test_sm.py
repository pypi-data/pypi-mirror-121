'''Simple StaticMap test'''
import oneworld as ow

def test_sm():
    mymap = ow.StaticMap(view = [-125, -66.5, 20, 50],
                         central_longitude = -98.6,
                         projection = 'AlbersEqualArea',
                         inner_borders = ['USA'])
    myinsert = ow.StaticMap(position = [0, 0, 0.3, 0.3], create_fig = False,
                            view = [-175, -130, 50, 73],
                            central_longitude = -150,
                            projection = 'AlbersEqualArea',
                            inner_borders = ['USA'])
    mymap.savemap('staticmap_map.png')

if __name__ == "__main__":
    test_sm()
