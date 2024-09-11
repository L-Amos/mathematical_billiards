from src import table, ball, utils

def main():
    allowed_geometries = ["rectangle", "elliptical", "stadium"]
    while True:
        geometry = input("Table Geometry (rectangle, elliptical or stadium): ")
        if geometry.lower() in allowed_geometries:
            break
    billiards_table = table.Table(geometry.lower())
    billiards_ball = ball.Ball(billiards_table)
    billiards_table.reflections = utils.input_test("Enter the number of collisions to see: ", positive=True)
    if geometry == "rectangle":
        billiards_table.rectangle_calc(billiards_ball)
    elif geometry == "elliptical":
        billiards_table.elliptical_calc(billiards_ball)
    else:
        billiards_table.stadium_calc(billiards_ball)
    billiards_table.plot(billiards_ball)

main()