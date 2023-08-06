"""Great Assertions."""

# from .ga_dataframe import GADataFrame


class GASpark():
    """Great Assertions."""

    def __init__(self, df):
    #     """Great Assertions."""
    #     super().__init__(df)
        pass

    @property
    def get_row_count(self) -> int:
        """
        Calculate the row count.

        :returns: The row count value

        """
        return self.df.count()
