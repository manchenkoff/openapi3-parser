class Printable:
    """
    Base class to support printing object as a string value
    """

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return self.__repr__()


class Comparable:
    """
    Base class to support comparing two objects by their property values
    """

    def __eq__(self, o: 'Comparable') -> bool:
        return self.__dict__ == o.__dict__
