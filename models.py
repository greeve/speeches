class Conference:

    LANGUAGES = [
        'eng',
        'hun',
    ]

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        self.languages = self.LANGUAGES
        self.sessions = []

    @classmethod
    def from_config(cls, config=None):
        if not config:
            return
        c = cls()
        return c


class Session:

    DAYS = [
        'sat',
        'sun',
    ]

    TIME_CODES = [
        'am',
        'pm',
        'ps',
    ]

    TIMES = [
        'morning',
        'afternoon',
        'priesthood',
    ]

    def __init__(self):
        self.day = None
        self.time_code = None
        self.time = None
        self.name = None
        self.talks = []


class Talk:
    def __init__(self):
        self.speaker = None
        self.title = None
        self.content = None


def main():
    pass

if __name__ == '__main__':
    main()
