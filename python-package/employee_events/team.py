from .query_base import QueryBase

class Team(QueryBase):

    name = "team"

    def names(self):
        """
        Retrieve a list of all teams in the database.

        Executes an SQL query to select and return the team name and ID
        for all teams in the database.

        Returns:
            List[Tuple[str, int]]: A list of tuples, each containing the name and
            ID of a team.
        """
        sql_query = f"""
                    SELECT team_name, team_id
                    FROM {self.name}
                    """
        return self.query(sql_query)

    def username(self, id):


        """
        Retrieve a team's name based on their ID.

        Executes an SQL query to select and return the team name
        of the team with an ID equal to the `id` argument.

        Args:
            id (int): The ID of the team.

        Returns:
            List[Tuple[str]]: A list of tuples, each containing the name of the team as a string.
        """
        sql_query = f"""
                        SELECT team_name
                        FROM {self.name}
                        WHERE team_id = {id}
                    """
        return self.query(sql_query)

    def model_data(self, id):

        """
        Retrieve data for the machine learning model.

        Executes an SQL query to select and return the count of positive
        and negative events for each employee in the team with an ID equal to the
        `id` argument. The query groups the results by `employee_id` and returns
        the count of positive and negative events for each employee.

        Args:
            id (int): The ID of the team.

        Returns:
            pandas.DataFrame: A dataframe containing the count of positive
            and negative events for each employee as a pandas Series.
        """
        sql_query = f"""
            SELECT positive_events, negative_events
            FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM {self.name}
                JOIN employee_events
                    USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {id}
                GROUP BY employee_id
            )
        """
        return self.pandas_query(sql_query)