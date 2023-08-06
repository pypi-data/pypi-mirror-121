import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):

	def __init__(self,p=0.5,n=25):

		self.p=p
		self.n=n

		Distribution.__init__(self,self.calculate_mean(),self.calculate_stdev())

		data_list=[]
		self.data = list(data_list)


	
	def calculate_mean(self):

		self.mean = float(self.p*self.n)

		return self.mean

	def calculate_stdev(self):

		self.stdev = float(math.sqrt(self.n*self.p*(1-self.p)))

		return self.stdev

	def replace_stats_with_data(self):

		#Distribution.read_data_file(self, file_name)
	
		counter =[]
		for nums in self.data:
			if nums==1:
				counter.append(nums)
		self.p = (len(counter)/len(self.data))
		self.n = len(self.data)
		self.mean = self.calculate_mean()
		self.stdev=self.calculate_stdev()

		return self.p, self.n

	def plot_bar(self):


		plt.bar(self.data)
		plt.title('Bar chart of Data')
		plt.xlabel('data')
		plt.ylabel('count')	

	def pdf(self,k):

		a=math.factorial(self.n)/(math.factorial(self.n-k)*math.factorial(k))
		b= (self.p**k )*(1-self.p)**(self.n - k)

		return a*b
	
	def plot_histogram_pdf(self):
		k0 = min(self.data)
		kn = max(self.data)
		x = []
		y = []
		for i in range(len(self.data)):
			x.append(self.pdf(i))
			y.append(self.pdf(x))
		
		fig, axes = plt.subplots(2,sharex=True)
		fig.subplots_adjust(hspace=.5)
		axes[0].bar(self.data, density=True)
		axes[0].set_title('Binomial Histogram of Data')
		axes[0].set_ylabel('Density')

		axes[1].plot(x, y)
		axes[1].set_title('Binomial Distribution for \n Sample Mean and Sample Standard Deviation')
		axes[0].set_ylabel('Density')
		plt.show()

		return x,y

	def __add__(self,other):

		try:
			assert self.p == other.p, 'p values are not equal'

		except AssertionError as error:
			raise

		result = Binomial()
		result.p = (self.p + other.p)/2
		result.n = sum([self.n, other.n])
		result.calculate_mean()
		result.calculate_stdev()

		return result

	def __repr__(self):

		return("mean {}, standard deviation {}, p {}, n {}".format(self.mean,self.stdev,self.p,self.n))
