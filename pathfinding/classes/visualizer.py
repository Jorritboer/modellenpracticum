
class Visualizer:
    #path: found path
    #geotransform: (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size)
    def __init__(self, path) -> None:
        self.path = path
        self.geotransform:list
        pass

    def array_index_to_coordinates(
        self,

        array_index_to_transform: list,

        geotransform: list,

    ) -> list:

        """

        Change index values of a raster (combined with geotransform) to real coordinates.

        Example: (306, 886) should become (174768.627, 451001.5161999986) given (174615.377, 451444.7661999986)

        Follow these steps:

        1. Use upper left coordinates

        2. add difference in x, but consider tile-size (default 0.5x0.5),

        3. Take the centre of the tile



        Note that in different coordinate systems, y_size can be negative (even though one might not expect it),

        there an abs() is used

        """

        upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size = geotransform



        real_coordinates = []

        for y_index, x_index in array_index_to_transform:

            x = upper_left_x + ((x_index * x_size) + (x_size / 2))

            y = upper_left_y - abs(((y_index * y_size) + (y_size / 2)))

            real_coordinates.append((x, y))

        return real_coordinates


    def getGEOJSON(self):
        f = open("path.json", "a")
        f.write( "{\n \"TYPE\": \"LineString\",\"coordinates\": [")
        for coord in self.array_index_to_coordinates(self.path,self.geotransform):
            f.write("  ",coord)        
        f.write(" ]}")