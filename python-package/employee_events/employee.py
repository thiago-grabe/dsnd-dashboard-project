from .query_base import QueryBase

class Employee(QueryBase):

    name = "employee"

    def names(self):
        """
        Retrieve a list of all employees in the database.

        Executes an SQL query to select and return a list of tuples,
        where each tuple contains:
        1. The employee's full name (constructed by concatenating
        the first name and last name with a space in between).
        2. The employee's ID.

        Returns:
            List[Tuple[str, int]]: A list of tuples, each containing
            the full name and ID of an employee.
        """

        sql_query = """
                       SELECT first_name || ' ' || last_name AS full_name, employee_id
                       FROM employee
                """
        return self.query(sql_query)


    def username(self, id):
        """
        Retrieve an employee's full name based on their ID.

        Executes an SQL query to select and return the full name
        of the employee with an ID equal to the `id` argument.

        Args:
            id (int): The ID of the employee.

        Returns:
            List[Tuple[str]]: A list of tuples, each containing
            the full name of the employee as a string.
        """
        sql_query = f"""
                    SELECT first_name || ' ' || last_name AS full_name
                    FROM employee
                    WHERE employee_id = {id}
                """
        return self.query(sql_query)
    
    def model_data(self, id):

        """
        Retrieve data for the machine learning model.

        Executes an SQL query to select and return the count of positive
        and negative events for the employee with an ID equal to the `id`
        argument.

        Args:
            id (int): The ID of the employee.

        Returns:
            pandas.DataFrame: A dataframe containing the count of positive
            and negative events for the employee as a pandas Series.
        """
        sql_query = f"""
               SELECT SUM(positive_events) AS positive_events,
                      SUM(negative_events) AS negative_events
               FROM {self.name}
               JOIN employee_events USING({self.name}_id)
               WHERE {self.name}.{self.name}_id = {id}
           """

        return self.pandas_query(sql_query)