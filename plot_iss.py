"""
Script to create an interactive plot displaying the users location relative to
the international space station (ISS). Plot loads as html in default browser.
"""
import requests
import datetime
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import geocoder

def get_user_location():
    """Get user location by IP address"""
    return geocoder.ip('me').latlng
    
def get_iss_location():
    """Get ISS location (last 1.5hrs) from NASA API"""
    current_time = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    start_time = (datetime.datetime.now() - datetime.timedelta(hours=1.5)).strftime("%Y%m%dT%H%M%SZ")
    
    api_key = "DEMO_KEY"
    api_base = "https://sscweb.sci.gsfc.nasa.gov/WS/sscr/2"
    short_path = f"/locations/iss/{start_time},{current_time}/gse"
    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    
    response = requests.get(api_base + short_path, headers=headers)
    coords = response.json()["Result"]["Data"][1][0]["Coordinates"][1][0]
    timestamps = [y[11:16] for x,y in response.json()["Result"]["Data"][1][0]["Time"][1]]
    iss_lat = coords["Latitude"][1]#[-1]
    iss_lon = coords["Longitude"][1]#[-1]
    
    iss_data = pd.DataFrame({
            "Object":"ISS",
            "Size":200,
            "Latitude":iss_lat,
            "Longitude":iss_lon,
            "Time":timestamps
          }
    )
    
    return iss_data

def main():
    """Plot user and ISS locations on a world map"""
    # Get location data
    iss_data = get_iss_location()
    user_lat, user_lon = get_user_location()
    
    user_data = iss_data.copy()
    user_data["Latitude"] = user_lat
    user_data["Longitude"] = user_lon
    user_data["Size"] = 20
    user_data["Object"] = "You!"
    
    # Put data into df
    location_data = pd.concat([iss_data, user_data])
        
    # Plotting
    fig = px.scatter_geo(location_data, lat="Latitude", lon="Longitude",
                         color="Object",
                         hover_name="Object",
                         hover_data=["Time", "Latitude", "Longitude"],
                         size="Size",
                         animation_frame="Time",
                         animation_group="Object",
                         projection="orthographic")        
    plot(fig)
    
    # Would be cool to change shape of scatter dot to ISS
    # https://upload.wikimedia.org/wikipedia/commons/d/d0/International_Space_Station.svg

if __name__ == "__main__":
    main()
