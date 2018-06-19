from mrc.mrc_header import MrcHeader
from mrc.mrc_message import MrcMessage
from mrc.mrc_interval import MrcInterval


class Mrc:
    def __init__(self, raw_mrc):
        self.raw_mrc = raw_mrc
        self.course_header = self.parse_course_header()
        self.course_data = self.parse_course_data()
        self.course_text = self.parse_course_text()
        self.interval_data = self.parse_interval_data()

    def parse_course_header(self):
        raw_header = self.get_raw_course_header()
        return MrcHeader.from_raw_course_header(raw_header)

    def parse_course_data(self):
        raw_course_data = self.get_raw_course_data()
        data = []

        for line in raw_course_data.split("\n"):
            splitted_line = line.split()
            if len(splitted_line) != len(self.course_header.data_types):
                raise ValueError

            data.append([float(value) for value in splitted_line])
        return data

    def parse_course_text(self):
        raw_course_text = self.get_raw_course_text()

        messages = []

        for line in raw_course_text.split("\n"):
            try:
                messages.append(MrcMessage.from_raw_course_text(line))
            except ValueError:
                print("Could not parse Interval: {}".format(line))

        return messages

    def parse_interval_data(self):
        raw_interval_data = self.get_raw_interval_data()

        intervals = []

        for line in raw_interval_data.split("\n"):
            try:
                intervals.append(MrcInterval.from_raw_interval_data(line))
            except ValueError:
                print("Could not parse Interval: {}".format(line))
        return intervals

    def get_between(self, start, end):
        a = self.raw_mrc.find(start)
        b = self.raw_mrc.find(end, a + len(start))

        if a == -1 or b == -1:
            return ""

        return self.raw_mrc[a + len(start):b].strip()

    def get_raw_course_header(self):
        START = "[COURSE HEADER]"
        END = "[END COURSE HEADER]"
        return self.get_between(START, END)

    def get_raw_course_data(self):
        START = "[COURSE DATA]"
        END = "[END COURSE DATA]"
        return self.get_between(START, END)

    def get_raw_course_text(self):
        START = "[COURSE TEXT]"
        END = "[END COURSE TEXT]"
        return self.get_between(START, END)

    def get_raw_interval_data(self):
        START = "[INTERVAL DATA]"
        END = "[END INTERVAL DATA]"
        return self.get_between(START, END)

    def get_raw_mode_data(self):
        START = "[MODE DATA]"
        END = "[END MODE DATA]"
        return self.get_between(START, END)

    def __str__(self):
        output = "{}\n".format(self.course_header)

        output += "[COURSE DATA]\n"
        for data in self.course_data:
            data = [str(value) for value in data]
            output += "{}\n".format("\t".join(data))
        output += "[END COURSE DATA]\n\n"

        output += "[COURSE TEXT]\n"
        for message in self.course_text:
            output += "{}\t{}\t{}\n".format(
                message.time,
                message.content,
                message.duration
            )
        output += "[END COURSE TEXT]\n\n"

        output += "[INTERVAL DATA]\n"
        for interval in self.interval_data:
            output += "{}\n".format(interval)
        output += "[END INTERVAL DATA]\n\n"

        return output

    @classmethod
    def load_mrc_file(cls, filename):
        with open(filename, "r") as f:
            raw_mrc = f.read()
        return cls(raw_mrc)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))

if __name__ == "__main__":
    mrc = Mrc.load_mrc_file("Avalanche Spire.mrc")
    print(mrc)
