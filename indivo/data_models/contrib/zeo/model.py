from indivo.models import Fact
from django.db import models

#note this is brute force, not attempting to use any of the indivo existing fields
#or to create special fields

class SleepStats(Fact):
	awakenings 			= models.IntegerField() #The number of times the individual woke up during the period
	awakeningsZqPoints 	= models.IntegerField() #The number of ZQ points due to awakenings
	bedTime 			= models.DateTimeField() #A ZeoDateTime object describing the bed time
	grouping 			= models.CharField(max_length = 10) #The SleepStatsGrouping Enum describing the method in which the data was averaged
	morningFeel 		= models.FloatField() # An integer from 1-5 describing how the user felt that morning (1=bad,5=great!)
	riseTime 			= models.DateTimeField() #A ZeoDateTime object describing the rise time
	startDate 			= models.DateField() #A ZeoDate object describing the start date for the SleepStats object
	timeInDeep 			= models.IntegerField() #The amount of time spent (in minutes) in deep sleep
	timeInDeepPercentage = models.FloatField() #The amount of time spent (in percentage of total) in deep sleep
	timeInDeepZqPoints  = models.IntegerField() #The number of ZQ points accounting for deep sleep
	timeInLight  		= models.IntegerField() #The amount of time spent (in minutes) in light sleep
	timeInLightPercentage  = models.FloatField() #The amount of time spent (in percentage of total) in light sleep
	timeInLightZqPoints = models.IntegerField() #The number of ZQ points accounting for light sleep
	timeInRem 			= models.IntegerField() #The amount of time spent (in minutes) in Rem sleep
	timeInRemPercentage = models.FloatField() #The amount of time spent (in percentage of total) in Rem sleep
	timeInRemZqPoints 	= models.IntegerField() #The number of ZQ points accounting for Rem sleep
	timeInWake  		= models.IntegerField() #The amount of time spent (in minutes) awake
	timeInWakePercentage = models.FloatField() #The amount of time spent (in percentage of total) awake
	timeInWakeZqPoints 	= models.IntegerField()  #The number of ZQ points accounting for being awake
	timeToZ 			= models.IntegerField()  #The amount of time (in minutes) it took to fall asleep
	totalZ 				= models.IntegerField()  #The total time asleep (in minutes)
	totalZZqPoints 		= models.IntegerField()  #The number of ZQ points accounting for Total Z
	zq 					= models.IntegerField()  #The overall ZQ score for this sleep period	
