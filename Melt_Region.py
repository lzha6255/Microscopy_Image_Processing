class MeltRegion:
    def __init__(self, id):
        self.id = id
        self.colour_id = 0              # Indicator for colouring of the melt region
        self.connections = []           # Array of connected melt regions

    def get_colour_id(self):
        return self.colour_id

    def add_connection(self, melt_region):
        self.connections.append(melt_region)

    # Goes through connected regions and sets colour_id to be different from each connected region.
    # This is possible by the four colour theorem
    def set_colour(self):
        # State of connected colours. Assume initially no connected melt regions
        connected = [False, False, False, False]
        for connection in self.connections:
            connected[connection.get_colour_id()] = True

        for i in range(len(connected)):
            if not connected[i]:
                self.colour_id = i
