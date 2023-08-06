'''Test WebMap simple map'''
import oneworld as ow

def test_wm():
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    mymap.savemap('webmap_map.html')

if __name__ == "__main__":
   test_wm()
