import numpy as np
import pandas as pd
import scipy as sc
from scipy.signal import argrelextrema


class TemporalPitchExtractor(object):
    """
    A computational model of the human's hearing pitch extraction stage, using the temporal model
    """

    def __init__(self):
        """
        Empty constructor. Fill with code if needed
        """
        pass

    def extract(self, spikes, sample_rate):
		channels_data = spikes
		number_of_channels = len(channels_data)
		number_of_points_in_channel = len(channels_data[0])
		lower_boundary = 0
		upper_boundary = int(number_of_points_in_channel/2)-1

		lmda = int(upper_boundary*1.5)
		dt = 1.0/sample_rate 
		step_tau = int((upper_boundary-lower_boundary)/50) ## was constant 1000 ## ensure that integer
		number_of_iterations = len(np.r_[lower_boundary:upper_boundary:step_tau]) ##(upper_boundary-lower_boundary)/step_tau
        
		# TODO: From the auditory nerve activity compute the autocorrelation of each nerve activity
		iteration = np.zeros(number_of_iterations)
		for i in range(number_of_iterations):
			for  j in range(number_of_channels):
				iteration[i] += integration(lower_boundary, upper_boundary, sample_rate, dt, channels_data, j, i*step_tau, lmda)
		
        # TODO: Sum these autocorrelation across nerves to construct the summary autocorrelation
		iteration = iteration/iteration[0] ##normalization
		
        # TODO: Extract the argument of the first non-zero peak in the autocorrelation
		peak_tau = step_tau*argrelextrema(iteration, np.greater)[0][iteration[argrelextrema(iteration, np.greater)[0]].argmax()]
		
        # TODO: Pitch matching maybe?

        # TODO: Return pitch estimate
        return 1.0/(peak_tau*dt)

	def acor(channels_data, channel_index, tau, t, t_current, lmda):
		"body of autocorrelation integral"
		return channels_data[channel_index,t_current]*channels_data[channel_index,t_current-tau]*np.exp((-t_current+t)*1.0/lmda)
		
	def integration(lower_boundary, upper_boundary, sample_rate, dt, channels_data, channel_index, tau, lmda):
		"trapezoidal integration of acor"
		result = acor(channels_data, channel_index, tau, upper_boundary, 0+tau, lmda)*dt/2.0 
		result = result + acor(channels_data, channel_index, tau, upper_boundary, upper_boundary+tau, lmda)*dt/2.0
		for i in range(1, int(round((upper_boundary-lower_boundary)/(sample_rate*dt*1.0))-1)):
			result = result + acor(channels_data, channel_index, tau, upper_boundary, i+tau, lmda)*dt*1.0 
		return result
