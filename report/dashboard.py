from fasthtml.common import *
import matplotlib.pyplot as plt
from employee_events import Employee, Team

from utils import load_model

from base_components import Dropdown, BaseComponent, Radio, MatplotlibViz, DataTable

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):

    def build_component(self, entity_id, model, *args, **kwargs):
        """
        Build the component for the ReportDropdown.

        Parameters
        ----------
        entity_id : int
            The id of the entity to build the component for.
        model : Model
            The model to use for building the component.
        *args : tuple
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        fasthtml.common.Select
            A Select element representing the dropdown component.
        """

        self.label = model.name
        return super().build_component(entity_id, model, *args, **kwargs)

    def component_data(self, entity_id, model, *args, **kwargs):
        """
        Retrieve a list of all employees in the database.

        Parameters
        ----------
        entity_id : int
            The id of the entity to retrieve names for
        model : Model
            The model to use for retrieving names

        Returns
        -------
        List[str]: A list of strings, each containing the full name of an employee.
        """
        return model.names()


class Header(BaseComponent):
    def build_component(self, entity_id, model, *args, **kwargs):
        """
        Build a fasthtml H1 object containing the model's name attribute.

        Parameters
        ----------
        entity_id : int
            The id of the entity to build the component for
        model : Model
            The model to use for building the component

        Returns
        -------
        fasthtml.common.H1
            A fasthtml H1 object containing the model's name attribute
        """
        return H1(model.name)



class LineChart(MatplotlibViz):
    def visualization(self, asset_id, model, *args, **kwargs):
        """
        Retrieve event counts for a given asset id and model.

        Parameters
        ----------
        asset_id : int
            The id of the asset to retrieve event counts for
        model : Model
            The model to use for retrieving event counts

        Returns
        -------
        matplotlib.figure.Figure
            A matplotlib figure object containing a line chart of the
            cumulative event counts for the asset over time
        """
        df = model.event_counts(asset_id)

        # Use the pandas .fillna method to fill nulls with 0
        df = df.fillna(0)

        # User the pandas .set_index method to set
        # the date column as the index
        df = df.set_index("event_date")

        # Sort the index
        df = df.sort_index()

        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        df = df.cumsum()

        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        df.columns = ["Positive", "Negative"]

        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        figure_object, ax = plt.subplots()

        # call the .plot method for the
        # cumulative counts dataframe
        df.plot(ax=ax)

        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax)

        # Set title and labels for x and y axis
        ax.set_title("Events of the Employees", fontsize=22)
        ax.set_xlabel("Date", fontsize=15)
        ax.set_ylabel("Cumulative Events (Count)", fontsize=17)
        return figure_object



class BarChart(MatplotlibViz):

    predictor = load_model()

    def visualization(self, asset_id, model, *args, **kwargs):
        """
        This method is responsible for generating a bar chart
        of the predicted risk of an asset.

        Parameters
        ----------
        asset_id : int
            The id of the asset to retrieve event counts for
        model : Model
            The model to use for retrieving event counts

        Returns
        -------
        matplotlib.figure.Figure
            A matplotlib figure object containing a bar chart of the
            predicted risk of the asset
        """

        data = model.model_data(asset_id)

        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        probas = self.predictor.predict_proba(data)

        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        probas = probas[:, 1]

        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        if model.name == "team":
            pred = probas.mean()

        # Otherwise set `pred` to the first value
        # of the predict_proba output
        else:
            pred = probas[0]

        # Initialize a matplotlib subplot
        figure_object, ax = plt.subplots()

        # Run the following code unchanged
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax)
        return figure_object


class Visualizations(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    children = [LineChart(), BarChart()]

    # Leave this line unchanged
    outer_div_type = Div(cls="grid")


class NotesTable(DataTable):

    def component_data(self, entity_id, model, *args, **kwargs):
        """
        Return the notes for a given entity_id using the model argument.

        Parameters
        ----------
        entity_id : int
            The id of the entity to retrieve notes for
        model : Model
            The model to use for retrieving notes

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the notes for the given entity_id
        """
        return model.notes(entity_id)


class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector",
        ),
        ReportDropdown(id="selector", name="user-selection"),
    ]



class Report(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing initialized instances
    # of the header, dashboard filters,
    # data visualizations, and notes table
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


# Initialize a fasthtml app
app = FastHTML()

# Initialize the `Report` class
report = Report()


@app.get("/")
def home():
    """
    Generates the default report for Employee #1.

    This route serves as the homepage of the application and
    generates a fasthtml combined component report. The report
    includes a header, a form to select a team or employee, a
    line and bar chart, and a table of notes.

    Initially, the report is generated for Employee #1 by default,
    as the QueryBase class is abstract and cannot be used directly.

    Returns:
        A fasthtml combined component report for Employee #1.
    """

    return report("1", Employee())


@app.get("/employee/{iid:str}")
def employee_report(iid: str):
    """
    Generates a report for the given employee ID.

    The report is a fasthtml combined component that includes
    a header, a form to select a team or employee, a line and bar
    chart, and a table of notes.

    The employee ID is passed as a path parameter in the URL.

    Example: /employee/1
    """
    return report(iid, Employee())


@app.get("/team/{iid:str}")
def team_report(iid: str):
    """
    Generates a report for the given team ID.

    The report is a fasthtml combined component that includes
    a header, a form to select a team or employee, a line and bar
    chart, and a table of notes.

    The team ID is passed as a path parameter in the URL.

    Example: /team/1

    :param iid: The ID of the team to generate the report for
    :type iid: str
    :return: The HTML for the report
    :rtype: str
    """
    return report(iid, Team())


# Keep the below code unchanged!
@app.get("/update_dropdown{r}")
def update_dropdown(r):
    """
    Endpoint that updates the dropdown menu in the dashboard filters.

    When the radio button is changed, this endpoint is called with
    the new value of the radio button as a query parameter.

    The endpoint returns the HTML for the updated dropdown menu.
    """
    dropdown = DashboardFilters.children[1]
    print("PARAM", r.query_params["profile_type"])
    if r.query_params["profile_type"] == "Team":
        return dropdown(None, Team())
    elif r.query_params["profile_type"] == "Employee":
        return dropdown(None, Employee())


@app.post("/update_data")
async def update_data(r):
    """
    This endpoint is used to update the current report being viewed.

    It handles POST requests and expects to receive a form containing
    a "profile_type" and a "user-selection". The "profile_type" is
    a string that should be either "Employee" or "Team", and the
    "user-selection" is a string that should be the ID of the
    employee or team to view.

    The function will redirect to the appropriate page based on the
    provided form data.
    """
    from fasthtml.common import RedirectResponse

    data = await r.form()
    profile_type = data._dict["profile_type"]
    id = data._dict["user-selection"]
    if profile_type == "Employee":
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == "Team":
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()
