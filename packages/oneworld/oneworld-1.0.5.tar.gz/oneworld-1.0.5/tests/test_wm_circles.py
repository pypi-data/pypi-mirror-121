'''Test WebMap circles'''
import oneworld as ow

def test_wm_circle():
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    df = ow.load_dataset('conferences')
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    mymap.add_circles(latitude = 'Lat', longitude = 'Long', data = df,
                      color = 'Conference', constant_size = True)
    mymap.savemap('webmap_circles.html')

if __name__ == "__main__":
    test_wm_circle()
