class Distribution:

    """ Generic distribution class for calculating and 
		visualizing a probability distribution.
	
		Attributes:
			mean (float) representing the mean value of the distribution
			stdev (float) representing the standard deviation of the distribution
			data_list (list of floats) a list of floats extracted from the data file
			"""
    def __init__(self, mu =0,  sigma=1):
        self.mean = mu
        self.std = sigma
        self.data = []

    def read_data_file(self, file_name, sample=True):

        """Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute.
				
		Args:
			file_name (string): name of a file to read from
		
		Returns:
			None
		
		"""

        with open(file_name) as f:
            datalist = []
            line = f.readline()
            while line:
                datalist.append(int(line))
                line = f.readline()
        f.close()

        self.data = datalist
        


