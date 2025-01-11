
from .sql_execution import QueryMixin

class QueryBase(QueryMixin):

    name = ""

    def names(self):

        # Return an empty list
        """
        Retrieve a list of all employees in the database.

        Returns:
            List[str]: A list of strings, each containing the full name of an employee.
        """
        return []

    def event_counts(self, id):
        """
        Retrieve the count of positive and negative events for a given id.

        Executes an SQL query to select and return the count of positive
        and negative events for the employee or team with an ID equal to the
        `id` argument. The query groups the results by `event_date` and sums
        the count of positive and negative events. The results are ordered by
        `event_date`.

        Args:
            id (int): The ID of the employee or team.

        Returns:
            pandas.DataFrame: A dataframe containing the count of positive
            and negative events for the employee or team as a pandas Series.
        """
        sql_query = f"""
                    SELECT event_date,
                           SUM(positive_events) AS positive_events,
                           SUM(negative_events) AS negative_events
                    FROM {self.name}
                    JOIN employee_events USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY event_date
                    ORDER BY event_date
                    """
        return self.pandas_query(sql_query)


    def notes(self, id):
        """
        Retrieve notes for a given ID.

        Executes an SQL query to select and return the note date and content
        from the `notes` table. The query joins the `notes` table with the
        table specified in the `name` class attribute, using the appropriate
        ID column. The results are filtered to only include the notes for
        the entity with an ID equal to the `id` argument.

        Args:
            id (int): The ID of the employee or team.

        Returns:
            pandas.DataFrame: A dataframe containing the note date and content.
        """

        sql_query = f"""
                    SELECT note_date, note
                    FROM notes
                    JOIN {self.name} USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    """
        return self.pandas_query(sql_query)