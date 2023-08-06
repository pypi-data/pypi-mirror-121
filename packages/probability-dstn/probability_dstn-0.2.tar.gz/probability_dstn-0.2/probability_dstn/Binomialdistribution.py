import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):

    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) number of trials
            
    """

    def __init__(self, p: float = .5, n: int = 20):
        self.prob = p
        self.n_trial = n
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
        

    def calculate_mean(self):

        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        mu = round((self.prob * self.n_trial),2)
        self.mean = mu
        return mu


    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """

        sigma = round((math.sqrt(self.n_trial * self.prob * (1 - self.prob))),2)
        self.std = sigma
        return sigma

    def __add__(self, other):

        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """

        try:
            assert self.prob == other.prob
        except AssertionError as error:
            raise error

        result = Binomial()

        result.n_trial = self.n_trial + other.n_trial
        result.prob = self.prob
        result.calculate_mean()
        result.calculate_stdev()
        
        return result

    def __repr__(self):

        return f"mean {self.mean}, standard deviation {self.std}, p {self.prob}, n {self.n_trial}" 

    def replace_stats_with_data(self):

        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """

        self.n_trial = len(self.data)
        self.prob = round((1.0 * sum(self.data) / len(self.data)),4)
        self.mean = self.calculate_mean()
        self.std = self.calculate_stdev()

        return self.prob, self.n_trial


    def plot_bar(self):

        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """

        plt.bar(x = ['0', '1'], height =[(1 - self.prob) * self.n_trial, self.prob * self.n_trial])
        plt.title('Barplot of Data')
        plt.xlabel('outcome')
        plt.ylabel('count')
        plt.show()


    def pdf (self, k: float):

        """Probability density function calculator for the binomial distribution.
        
        Args:
            x (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        a = math.factorial(self.n_trial) / (math.factorial(k) * (math.factorial(self.n_trial - k)))
        b = (self.prob ** k) * (1 - self.prob) ** (self.n_trial - k)

        return a * b

    
    
    def plot_bar_pdf (self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """

        x = [ ]
        y = [ ]

        for i in range (self.n_trial + 1):
            x.append(i)
            y.append(self.pdf(i))


        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')
        plt.show()