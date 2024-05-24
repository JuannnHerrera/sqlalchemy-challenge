from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Database Setup
try:
    engine = create_engine('sqlite:///D:/ASU_Bootcamp_Anaconda/Module 10 Challenge/SurfsUp/Resources/hawaii.sqlite')
    Base = automap_base()
    Base.prepare(autoload_with=engine)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    app.logger.debug("Database connected successfully.")
except Exception as e:
    app.logger.error(f"Error connecting to the database: {e}")

@app.route("/")
def welcome():
    app.logger.debug("Welcome route accessed")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/&lt;start&gt;<br/>"
        f"/api/v1.0/start_end_date/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    try:
        app.logger.debug("Precipitation route accessed")
        one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
        app.logger.debug(f"Retrieved {len(precipitation_data)} records from the database.")
        precip_dict = {date: prcp for date, prcp in precipitation_data}
        return jsonify(precip_dict)
    except Exception as e:
        app.logger.error(f"Error in precipitation route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1.0/stations")
def stations():
    try:
        app.logger.debug("Stations route accessed")
        stations = session.query(Station.station).all()
        stations_list = [station[0] for station in stations]
        return jsonify(stations_list)
    except Exception as e:
        app.logger.error(f"Error in stations route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1.0/tobs")
def tobs():
    try:
        app.logger.debug("TOBS route accessed")
        one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year_ago).all()
        app.logger.debug(f"Retrieved {len(tobs_data)} records from the database.")
        tobs_list = [tobs for date, tobs in tobs_data]
        return jsonify(tobs_list)
    except Exception as e:
        app.logger.error(f"Error in TOBS route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1.0/start_date/<start>")
def start_date(start):
    try:
        app.logger.debug(f"Start date route accessed with start={start}")
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
        temp_dict = {
            "Min Temp": temp_stats[0][0],
            "Avg Temp": temp_stats[0][1],
            "Max Temp": temp_stats[0][2]
        }
        return jsonify(temp_dict)
    except Exception as e:
        app.logger.error(f"Error in start_date route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1.0/start_end_date/<start>/<end>")
def start_end_date(start, end):
    try:
        app.logger.debug(f"Start/End date route accessed with start={start} and end={end}")
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end, '%Y-%m-%d')
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        temp_dict = {
            "Min Temp": temp_stats[0][0],
            "Avg Temp": temp_stats[0][1],
            "Max Temp": temp_stats[0][2]
        }
        return jsonify(temp_dict)
    except Exception as e:
        app.logger.error(f"Error in start_end_date route: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
