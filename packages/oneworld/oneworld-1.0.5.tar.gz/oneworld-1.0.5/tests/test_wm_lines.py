'''Test WebMap lines'''
import oneworld as ow

def test_wm_lin():
    mymap = ow.WebMap(center = [39,-96.8], zoom = 4)
    mymap.add_lines(latitude0 = [29.964007, 32.278847, 44.975352],
                    longitude0 = [-90.107465, -106.747831, -93.230973],
                    latitude1 = [40.278822, 40.852768, 34.069322],
                    longitude1 = [-111.715293, -96.689506, -118.442436],
                    color = ['Big East', 'SBC', 'Pac 12'],
                    size = [18, 10, 35])
    mymap.savemap('webmap_lines.html')

if __name__ == "__main__":
    test_wm_lin()
