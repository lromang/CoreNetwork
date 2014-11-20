from urllib2 import Request, urlopen 
import json
import pandas as pd
from StringIO import StringIO
import numpy as np
import matplotlib.pyplot as plt

gmaps = googlemaps.Client(key='AIzaSyBIIo-O7IS74wWvJvX8g0CZqwg-xZe3PFY')


# Testing gmaps.directions
directions_result = gmaps.directions((19.388589,-99.207916),
									 (19.394499,-99.159765),
                                     region = "mx")

# Testing functions with multiple coordinates
# origins coordinates
origins = [(19.388589,-99.207916),
		   (19.338589,-99.237916),
		   (19.488589,-99.214916)]
# destinations coordinates
destinations = [(19.394499,-99.159765),
				(19.397699,-99.254765),
				(19.254499,-99.181765)]

# Extract the information given by gmaps
# and displays it as a data.frame
def fun_coords(origin, destination):
	result = {}
	directions_result = gmaps.directions(origin,
									     destination,
                                         region = "mx")
	# Getting directions
	directions = directions_result[ 0 ][ 'legs' ][ 0 ]
	# Gettin distance
	result['distance']   = directions[ 'distance'][ 'text' ]
	# Getting instructions
	steps      = directions[ 'steps' ]
	steps_df   = pd.DataFrame.from_dict( steps )
	coords     = pd.DataFrame( index = range(steps_df.shape[ 0 ]),
							   columns = ['start_lng',
							   			  'start_lat',
							   			  'end_lng',
							   			  'end_lat',
							   			  'distance',
							   			  'instruction'] )
	for i in range( steps_df.shape[ 0 ] ):
		coords[ 'start_lng' ][ i ]  = steps_df['start_location'][ i ]['lng']
		coords[ 'start_lat' ][ i ]  = steps_df['start_location'][ i ]['lat']
		coords[ 'end_lng' ][ i ]    = steps_df['end_location'][ i ]['lng']
		coords[ 'end_lat' ][ i ]    = steps_df['end_location'][ i ]['lat']
		coords[ 'distance'][ i ]    = steps_df['distance'][ i ]['text']
	        if  str(steps_df[ 'maneuver' ][ i ] ) == 'nan':
	        	coords[ 'instruction' ][ i ] = 'Continue'
	        else:
	    	    coords[ 'instruction' ][ i ] = steps_df['maneuver'][ i ]
	return coords	    	    

direction_matrix = fun_coords(origins[2], destinations[2])
# Same as coords but now it receives a list of coordinates
def list_coords( origins, destinations ):
	coordinates = []
	for i in range( len( origins ) ):
		coordinates.append( fun_coords( origins[ i ], destinations[ i ] ) )
		time.sleep(3)
	return coordinates
	
direction_matrix = list_coords(origins, destinations)

# Creates a dictionary with the coordinates of the matrix
# given by list_coords.
def fp_directions(direction_matrix):
	plot_directions  = {'long':[],'lat':[]}
	start = 0
	end   = 0
	for i in range(direction_matrix.shape[ 0 ]):
		if i % 2 == 0:
			plot_directions['long'].append(  direction_matrix['start_lng'][ start ] )
			plot_directions['lat'].append(  direction_matrix['start_lat'][ start ] )
			start = start + 1
		else:
			plot_directions['long'].append(  direction_matrix['end_lng'][ end ] )
			plot_directions['lat'].append(  direction_matrix['end_lat'][ end ] )
			end = end + 1
	plt.plot(plot_directions['long'],plot_directions['lat'])
	plt.show()
	return plot_directions

#plot results
final_directions = []
for i in range(len(direction_matrix)):
	final_directions.append( fp_directions( direction_matrix[ i ] ) )




