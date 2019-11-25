from domain.models import db, Vendors
import plotly
import plotly.graph_objs as go
import json

def visualization_data():
    data = db.session.query(Vendors.vendor_name,
                            db.func.count(Vendors.balance).label("VendorsQuantity")
                            ).join(Vendors, Vendors.vendor_name == Vendors.vendor_name).group_by(Vendors.balance).all()

    bar = [
        go.Bar(
            x=[value[0] for value in data],
            y=[value[1] for value in data]
        )
    ]

    return json.dumps(bar, cls=plotly.utils.PlotlyJSONEncoder)