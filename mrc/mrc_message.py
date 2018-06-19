class MrcMessage:
    def __init__(self, time, content, duration):
        self.time = time
        self.content = content
        self.duration = duration

    def __str__(self):
        return "time: {}\ncontent: {}\nduration: {}".format(self.time,
                                                            self.content,
                                                            self.duration)

    @classmethod
    def from_raw_course_text(cls, raw_course_text):
        splitted = raw_course_text.strip().split("\t")
        return cls(int(splitted[0]), splitted[1], int(splitted[2]))
