from mrc.mrc import Mrc
import sys
import copy


def erg_to_mrc(erg):
    mrc = copy.deepcopy(erg)

    mrc.course_header.data_types[1] = "FTP"

    data = mrc.course_data[:]
    for index, value in enumerate(mrc.course_data):
        data[index][1] = int(round(value[1] * 100 / float(mrc.course_header.ftp)))
    mrc.course_data = data

    return mrc


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 erg_to_mrc.py FILE")
        quit()

    filename = sys.argv[1]

    erg = Mrc.load_mrc_file(filename)

    if erg.course_header.data_types[1] != "WATTS":
        print("erg has no WATTS data type")
        quit()

    mrc = erg_to_mrc(erg)
    mrc.save(filename.strip("erg") + "mrc")
