from enginelib.errors import Error


class NoPractitionerError(Error):
    def __init__(self, message="Error: no Practitioner found on claim or claim line"):
        super().__init__(message)


class TooManyPractitionersError(Error):
    def __init__(self, message="Error: too many Practitioners found on claim line"):
        super().__init__(message)
