import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/ends<br/>"
    )

@app.route("/api/v1.0/station")
def station():
    """Return a list of all station"""
    # Query all station
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation names"""
    # Query all passengers
    results = session.query(Measurement).all()
    
    all_precipitation = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict['date'] = precipitation.date
        precipitation_dict['prcp'] = precipitation.prcp        
        all_precipitation.append(precipitation_dict)
        #print(all_precipitation)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/tobs")
def tobs():    
    results = session.query(Measurement.station, func.count(Measurement.tobs).label('tobs')).\
          filter(Measurement.date >= '2016-01-01').\
          filter(Measurement.date <= '2016-12-31').\
          group_by(Measurement.station).all()
    all_tobs = []
    for sta in results:
        observation_dict = {}
        observation_dict['station'] = sta.station
        observation_dict['tobs'] = sta.tobs        
        all_tobs.append(observation_dict)
   
    return jsonify(all_tobs) 

@app.route("/api/v1.0/<start_date>")
def start_summary_tobs(start_date): 
    results = session.query(Measurement.station,\
            func.min(Measurement.tobs).label('TMIN'),\
            func.max(Measurement.tobs).label('TMAX'),\
            func.avg(Measurement.tobs).label('TAVG')).\
            filter(Measurement.date >= start_date).\
            group_by(Measurement.station).all()
    print(results)
    all_start_summary_tobs = []
    for start_summary_tobs in results:
        start_tob_dict = {}
        start_tob_dict['station'] = start_summary_tobs.station
        start_tob_dict['TMIN'] = str(start_summary_tobs.TMIN)
        start_tob_dict['TMAX'] = str(start_summary_tobs.TMAX)
        start_tob_dict['TAVG'] = str(start_summary_tobs.TAVG)
        
        all_start_summary_tobs.append(start_tob_dict)

    return jsonify(all_start_summary_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def summary_tobs(start_date, end_date): 
    results = session.query(Measurement.station,\
            func.min(Measurement.tobs).label('TMIN'),\
            func.max(Measurement.tobs).label('TMAX'),\
            func.avg(Measurement.tobs).label('TAVG')).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).\
            group_by(Measurement.station).all()
    print(results)
    all_summary_tobs = []
    for summary_tobs in results:
        tob_dict = {}
        tob_dict['station'] = summary_tobs.station
        tob_dict['TMIN'] = str(summary_tobs.TMIN)
        tob_dict['TMAX'] = str(summary_tobs.TMAX)
        tob_dict['TAVG'] = str(summary_tobs.TAVG)
        
        all_summary_tobs.append(tob_dict)

    return jsonify(all_summary_tobs)

if __name__ == '__main__':
    app.run(debug=True)

