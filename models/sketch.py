class Sketch:
    def __init__(self, *args, width, height, stitches, rows):
        self.sample = {
            "width": width, 
            "height": height, 
            "stitches": stitches,
            "rows": rows
        }
        self.convert_sample()

    def convert_sample(self):
        self.point_width = self.sample["stitches"] / self.sample["width"]
        self.point_height = self.sample["rows"] / self.sample["height"]
