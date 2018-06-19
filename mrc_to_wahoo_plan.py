from mrc.mrc import Mrc
import sys

class WahooInterval:
    def __init__(self, start_time, end_time, start_value, end_value):
        self.start_time = start_time
        self.end_time = end_time
        self.start_value = start_value
        self.end_value = end_value

    def duration_is_zero(self):
        if abs(self.end_time - self.start_time) < 0.1:
            return True

        return False

    def get_duration(self):
        return self.end_time - self.start_time

    def get_ramp_rate(self):
        if self.duration_is_zero():
            return 0.0
        return (self.end_value - self.start_value) / self.get_duration()

    def __str__(self):
        if self.duration_is_zero():
            return ""

        template = "=INTERVAL=\nPERCENT_FTP_HI={}{}\nMESG_DURATION_SEC>={}?EXIT\n\n"
        ramp_string = "@{:.6f}".format(self.get_ramp_rate()) if self.get_ramp_rate() != 0.0 else ""

        return template.format(self.start_value, ramp_string, int(self.get_duration()))


def get_wahoo_intervals(mrc):
    wahoo_intervals = []
    for index, data in enumerate(mrc.course_data[1:]):
        start_time = mrc.course_data[index][0] * 60
        end_time = data[0] * 60
        start_value = mrc.course_data[index][1]
        end_value = data[1]
        wahoo_intervals.append(WahooInterval(start_time, end_time, start_value, end_value))

    return wahoo_intervals

def mrc_to_wahoo_plan(mrc, name=None, description=None):
    header = "=HEADER=\n"

    if name is not None:
        header += "NAME={}\n".format(name)
    elif mrc.course_header.file_name is not None:
        header += "NAME={}\n".format(mrc.course_header.file_name)

    if description is not None:
        for line in textwrap.wrap(description, 96):
            header += "DESCRIPTION={} \n".format(line)
    elif mrc.course_header.description is not None:
        header += "DESCRIPTION={} \n".format(mrc.course_header.description)

    intervals = get_wahoo_intervals(mrc)
    intervals_string = "".join([str(interval) for interval in intervals])

    return "{}\n=STREAM=\n\n{}".format(header, intervals_string)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 mrc_to_wahoo_plan.py FILE")
        quit()

    filename = sys.argv[1]

    mrc = Mrc.load_mrc_file(filename)

    if mrc.course_header.data_types[1] != "PERCENT" and mrc.course_header.data_types[1] != "FTP":
        print("mrc has no PERCENT or FTP data type")
        quit()

    with open(filename.strip("mrc") + "plan", "w") as f:
        f.write(mrc_to_wahoo_plan(mrc))
