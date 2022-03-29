# Import Flask
from flask import Flask, jsonify

# Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite:///hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)
measurement = base.classes.measurement
station = base.classes.station

# create our session (link) from Python to the DB
# Flask
app = Flask(__name__)

# Routes
@app.route('/')
def welcome():
    """List all available api routes."""
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start (enter as YYYY-mm-DD)<br/>'
        f'/api/v1.0/start/end (enter as YYYY-mm-DD/YYYY-mm-DD)'

    )

# Precipitation Route
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    one_year_from_last = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    data_precip_score = session.query(measurement.date, measurement.prcp).\
                        filter(measurement.date >= one_year_from_last).\
                        order_by(measurement.date).all()
    # Convert into dict
    prcp_data_list = dict(data_precip_score)
    session.close()
    # Return JSON of dict
    return jsonify(prcp_data_list)

# Station Route
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    # Query all stations
    all_stations = session.query(station.station, station.name).all()
    # Convert stations into list
    station_list = list(all_stations)
    session.close()
    # Return JSON for station list
    return jsonify(station_list)

# TOBs Route
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    one_year_from_last = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Query the last 12 months of temperature observation data
    year_temp = session.query(measurement.station, measurement.tobs).\
                filter(measurement.date >= one_year_from_last).\
                order_by(measurement.date).all()
    # Convert to list
    tobs_data = list(year_temp)
    session.close()
    # Return JSON for tobs list
    return jsonify(tobs_data)

# Start Route
@app.route('/api/v1.0/<start>')
def start_date(start):
    session = Session(engine)

    start_date = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).\
                filter(measurement.date >= start).\
                group_by(measurement.date).all()
    # Convert to list
    start_date_list = list(start_date)
    session.close()
    # Return JSON for list
    return jsonify(start_date_list)


# Start-End Route
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    start_end_date = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                    filter(measurement.date >= start).\
                    filter(measurement.date <= end).\
                    group_by(measurement.date).all()
    # Convert to list
    start_end_date_list = list(start_end_date)
    # Return JSON for list
    return jsonify(start_end_date_list)

# Main behavior
if __name__ == '__main__':
    app.run(debug=True)