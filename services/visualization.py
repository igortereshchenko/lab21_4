from domain.models import db, Users, Events, Options
import plotly
import plotly.graph_objs as go
import json


def user_distribution_pie(uuid):
    user = db.session.query(Events.event_id.label("event_id"),
                            db.func.count(Events.event_id).label("event_idCount")).filter(
        Events.event_id == uuid).group_by(
        Events.event_id).subquery()
    data = db.session.query(db.func.sum(user.c.event_idCount)
                            ).group_by(user.c.Event_name).all()
    pie_plot = [
        go.Pie(
            labels=[value[0] for value in data],
            values=[value[1] for value in data]
        )
    ]
    return json.dumps(pie_plot, cls=plotly.utils.PlotlyJSONEncoder)

def event_options_population_bar(name):
    data = db.session.query(Options.Place, db.func.count(Options.option_id)).join(
        Events, Events.event_id == Options.event_idFk
    ).filter(Events.Event_name == name).group_by(Options.Place).all()

    bar_plot = [
        go.Bar(
                x=[value[0] for value in data],
                y=[value[1] for value in data]
        )
    ]

    return json.dumps(bar_plot, cls=plotly.utils.PlotlyJSONEncoder)
