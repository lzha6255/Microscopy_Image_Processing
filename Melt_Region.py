"""Object Representing a particular melt region.
Fields:
    - id: A unique identifier for the melt region.
    - colour_id: An identifier for what colour the melt region should be coloured in. Takes on values in
    [0, n_colours-1].
    - n_colours: Number of colours available.
    - connections: Array of references to other connected melt regions. Melt regions can form a graph.
    - pixels: Array of arrays of length two indicating which image pixels belong to the melt region.
"""


class MeltRegion:
    def __init__(self, region_id, n_colours):
        self.id = region_id
        self.colour_id = 0              # Indicator for colouring of the melt region
        self.n_colours = n_colours
        self.connections = []           # Array of connected melt regions
        self.pixels = []                # Pixels over which this melt region exists

    def get_colour_id(self):
        return self.colour_id

    def get_id(self):
        return self.id

    def get_n_pixels(self):
        return len(self.pixels)

    def get_connectivity(self):
        return len(self.connections)

    def add_connection(self, melt_region):
        self.connections.append(melt_region)

    def set_pixels(self, pixels):
        # Deep copy
        for pixel in pixels:
            self.pixels.append(pixel.copy())

    # Goes through connected regions and sets colour_id to be different from each connected region.
    # This is possible by the four colour theorem
    def set_colour(self):
        # State of connected colours. Assume initially no connected melt regions
        connected = []
        for i in range(self.n_colours):
            connected.append(False)
        print(connected)
        # Go through connected regions and find which colours they have
        for connection in self.connections:
            connected[connection.get_colour_id()] = True
        # Set this region's colour to an unconnected colour
        distinct = False
        for i in range(len(connected)):
            if not connected[i]:
                self.colour_id = i
                distinct = True
        # If it is not possible to colour this region distinct from others, set colour_id to 0
        if not distinct:
            self.colour_id = 0
            print("Could not make a distinct colouring for region " + str(self.id))

    # Checks if this melt region is connected to one with a particular id
    def check_connectivity(self, region_id):
        for connection in self.connections:
            if region_id == connection.get_id():
                return True
        return False
