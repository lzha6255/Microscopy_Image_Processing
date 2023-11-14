class MeltRegion:
    def __init__(self, id, n_colours):
        self.id = id
        self.colour_id = 0              # Indicator for colouring of the melt region
        self.n_colours = n_colours
        self.connections = []           # Array of connected melt regions

    def get_colour_id(self):
        return self.colour_id

    def get_id(self):
        return self.id

    def add_connection(self, melt_region):
        self.connections.append(melt_region)

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
    def check_connectivity(self, id):
        for connection in self.connections:
            if id == connection.get_id():
                return True
        return False
