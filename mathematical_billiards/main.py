import sys
from mathematical_billiards import table, ball, utils

def main():
    allowed_geometries = ["rectangle", "elliptical", "stadium"]
    while True:
        geometry = input("Table Geometry (rectangle, elliptical or stadium): ")
        if geometry.lower() in allowed_geometries:
            break
        elif geometry.lower() == "q":
            sys.exit()
    if geometry.lower() == "rectangle":
        width = utils.input_test("Table width (positive integer): ", positive=True)
        height = utils.input_test("Table height (positive integer): ", positive=True)
    elif geometry.lower() == "elliptical":
        while True:
            width = utils.input_test("Table semi-major axis (positive integer): ", positive=True)
            height = utils.input_test("Table sami-minor axis (positive integer): ", positive=True)
            if width >= height:
                break    
            print("Error: semi-major axis must be larger than semi-minor axis. ")
    else:
        width = utils.input_test("Central width (positive integer): ", positive=True)
        height = utils.input_test("Central height (positive integer): ", positive=True)
    billiards_table = table.Table(geometry.lower(), width, height)
    x = utils.input_test("Enter starting x position: ", integer=False)
    y = utils.input_test("Enter starting y position: ", integer=False)
    while True:
            if billiards_table.geometry == "rectangle":
                if abs(x) <= billiards_table.dims[0]/2 and abs(y) <= billiards_table.dims[1]/2:
                    break
            elif billiards_table.geometry == "elliptical":
                if (x/billiards_table.dims[0])**2 + (y/billiards_table.dims[1])**2 <= 1:
                    break
            else:
                if abs(x) <= billiards_table.dims[0]/2 and abs(y) <= billiards_table.dims[1]/2:
                    if not ((x > billiards_table.dims[0]/2 and x-billiards_table.dims[0]/2 > np.sqrt((billiards_table.dims[1]/2)**2-y**2)) or (x < billiards_table.dims[0]/2 and x+billiards_table.dims[0]/2 < -np.sqrt((billiards_table.dims[1]/2)**2-y**2))):
                        break
            print('Error: not on the table')
    angle = utils.input_test("Enter starting angle in degrees: ", integer=False)
    billiards_ball = ball.Ball(billiards_table, x, y, angle)
    billiards_table.reflections = utils.input_test("Enter the number of collisions to see: ", positive=True)
    if geometry == "rectangle":
        billiards_table.rectangle_calc(billiards_ball)
    elif geometry == "elliptical":
        billiards_table.elliptical_calc(billiards_ball)
    else:
        billiards_table.stadium_calc(billiards_ball)
    billiards_table.plot(billiards_ball)