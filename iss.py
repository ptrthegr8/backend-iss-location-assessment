#!/usr/bin/env python

"""ISS Location Finder

Program obtains a list of the astronauts who are currently in space.
It prints their full names, the spacecraft they are currently on board,
and the total number of astronauts in space

This program also retrives current geographic coordinates (lat/lon) of
the space station, along with a timestamp.

In addition, it creates a graphics screen with the world map background image
that displays the ISS's location, Indianapolis's location,
and the time when ISS would pass over Indianapolis.
"""

import requests
import sys
import turtle
import time


def get_info(url, params=None):
    res = requests.get(url) if params is None else requests.get(
        url, params=params)
    try:
        res.raise_for_status()
        return res.json()
    except Exception as exc:
        print 'Problem Encountered: %s' % exc
        sys.exit(1)


def display_astros(json_dict):
    """Returns concatenated string of ISS Astronaut info
    given JSON dict from API call
    """

    container = ''
    container += 'Number of Astronauts:' + str(json_dict.get('number')) + '\n'
    for data in json_dict.get('people'):
        container += ('Spacecraft:' + data.get(
            'craft') + '---' + 'Name:' + data.get('name') + '\n')
    return container


def display_geocoords(json_dict):
    """Returns tuple of ISS's latitude, longitude, and timestamp given
    JSON dict from API response
    """

    for data in json_dict.values():
        if isinstance(data, dict):
            return (float(data.get('latitude')), float(data.get('longitude')),
                    time.ctime(json_dict.get('timestamp')))


def display_graphics(iss_coords, indy_info=None):
    """Displays graphics with world map. Shows ISS's and Indianapolis's locations.
    Also displays next time ISS will pass over Indianapolis
    """

    indy_arrival = indy_info.get('time')
    indy_lat = indy_info.get('indy_coords').get('lat')
    indy_lon = indy_info.get('indy_coords').get('lon')
    x_coord = iss_coords[1]
    y_coord = iss_coords[0]
    iss = 'iss.gif'
    win = turtle.Screen()
    win.setup(width=720, height=360, startx=0, starty=0)
    win.bgpic(picname='./map.gif')
    win.setworldcoordinates(-180, -90, 180, 90)
    win.addshape(iss)
    my_turtle = turtle.Turtle(iss)
    indy = turtle.Turtle()
    indy.shape('circle')
    indy.color('yellow')
    indy.resizemode('user')
    indy.shapesize(0.2)
    indy.penup()
    indy.goto(indy_lon, indy_lat)
    indy.write(indy_arrival, align='right', font=('Arial', 10, 'bold'))
    my_turtle.penup()
    my_turtle.goto(x_coord, y_coord)
    win.exitonclick()


def get_indy():
    """Returns a dict with ISS arrival time to Indianapolis's location,
    and Indianapolis's Latitude and Longitude.
    """

    lat, lon = 39.7684, -86.1581
    indy_coords = {'lat': lat, 'lon': lon}
    res = get_info('http://api.open-notify.org/iss-pass.json',
                   params=indy_coords)
    return {'time': time.ctime(res.values()[2][0].get('risetime')),
            'indy_coords': indy_coords}


def main():
    """Prints all ISS info and displays turtle graphics for ISS and 
    Indianapolis
    """

    astros_api = 'http://api.open-notify.org/astros.json'
    geocoords_api = 'http://api.open-notify.org/iss-now.json'
    iss_coords = get_info(geocoords_api)
    indy_info = get_indy()
    print '\n'
    print display_astros(get_info(astros_api))
    print 'Lat: {}'.format(display_geocoords(iss_coords)[0]),
    print 'Lon: {}'.format(display_geocoords(iss_coords)[1]),
    print 'Time: {}'.format(display_geocoords(iss_coords)[2]),
    print '\n'
    display_graphics(display_geocoords(iss_coords), indy_info=indy_info)


if __name__ == '__main__':
    main()
