class MrcInterval:
    def __init__(self, start_time, end_time, name):
        self.start_time = start_time
        self.end_time = end_time
        self.name = name

    def __str__(self):
        return "{}\t{}\t{}".format(self.start_time, self.end_time, self.name)

    @classmethod
    def from_raw_interval_data(cls, raw_interval_data):
        splitted = raw_interval_data.strip().split("\t")
        if len(splitted) >= 3:
            start_time, end_time, name = splitted[:3]
        else:
            raise ValueError()
        return cls(int(start_time), int(end_time), name)
