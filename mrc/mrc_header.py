import re

class MrcHeader:
    __slots__ = "version", "units", "ftp", "description", "file_name", "data_types"

    def __str__(self):
        output = "[COURSE HEADER]\n"

        if self.version is not None:
            output += "VERSION = {}\n".format(self.version)
        if self.units is not None:
            output += "UNITS = {}\n".format(self.units)
        if self.ftp is not None:
            output += "FTP = {}\n".format(self.ftp)
        if self.description is not None:
            output += "DESCRIPTION = {}\n".format(self.description)
        if self.file_name is not None:
            output += "FILE NAME = {}\n".format(self.file_name)
        if self.data_types is not None:
            output += "{}\n".format(" ".join(self.data_types))
        output += "[END COURSE HEADER]\n"

        return output


    @classmethod
    def from_raw_course_header(cls, raw_course_header):
        header = MrcHeader()

        for slot, expression in [
                ("version", r'VERSION *= *(?P<value>.+)'),
                ("units", r'UNITS *= *(?P<value>.+)'),
                ("description", r'DESCRIPTION *= *(?P<value>.+)'),
                ("file_name", r'FILE NAME *= *(?P<value>.+)'),
                ("data_types", r'\n(?P<value>[A-Z \t]*)(?:\n|$)'),
                ("ftp", r'FTP *= *(?P<value>.+)'),
            ]:
            m = re.search(expression, raw_course_header)
            if m is not None:
                if slot == "data_types":
                    data = re.findall(r"[A-Z]+", m.group('value'))
                    if data[0] != "MINUTES":
                        raise ValueError("First data type must be MINUTES, found {} instead".format(data[0]))
                    setattr(header, slot, data)
                else:
                    setattr(header, slot, m.group('value'))

        for slot in cls.__slots__:
            try:
                header.__getattribute__(slot)
            except:
                setattr(header, slot, None)

        return header
