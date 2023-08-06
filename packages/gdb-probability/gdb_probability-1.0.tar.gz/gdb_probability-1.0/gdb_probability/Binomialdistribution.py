from math import sqrt, factorial
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
        n (int) the total number of trials
    """
    
    def __init__(self, prob=.5, size=20):           
        self.p = prob
        self.n = size

        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())



    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
                
        avg = self.p * self.n
        self.mean = avg
        return self.mean



    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        stddev = sqrt(self.n * self.p * (1 - self.p))
        self.stdev = stddev

        return self.stdev
        
        
        
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        
        
        self.n = len(self.data)
        self.p = 1.0 * sum(self.data)/len(self.data)

        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

        return self.p, self.n


        
    def plot_bar(self):

        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        
        x = self.data
        y = x.value_counts()
        plt.figure(figsize = (10, 5))

        plt.bar(x, y, color = 'indigo', width = 0.4)
        
        plt.xlabel('0 = tails, 1 = heads')
        plt.ylabel('Count')
        plt.title('Coin Flip')

        plt.show()
    

        
    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        
        a = factorial(self.n) / (factorial(k) * (factorial(self.n - k)))
        b = (self.p ** k) * (1 - self.p) ** (self.n - k)

        return a * b



    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
    
        x = []
        y = []
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))
        
        plt.bar(x, y, color = 'blue', width = 0.4)
        plt.xlabel('Outcomes')
        plt.ylabel('Probability of Outcomes')
        plt.title('Distribution of Outcomes')

        plt.show()

        return x, y



                
    def __add__(self, other):

        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

                
        result = Binomial()
        result.n = self.n + other.n
        result.p = self.p
        result.calculate_mean()
        result.calculate_stdev()

        return result
        


    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
        
    
        return f'mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n{self.n}'
