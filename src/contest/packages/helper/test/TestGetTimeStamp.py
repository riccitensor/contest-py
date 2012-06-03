from contest.packages.helper.getTimestamp import getTimestamp


import unittest

class GetTimeStampTest(unittest.TestCase):


    def testGetHourFromTimeStamp(self):
        """ @TODO: move this into a seperate unit Test for the getTimestamp Class but for now it is perfect here
        """
        timestamp = 4000
        binId = getTimestamp.gettimeStampIn_Hours(timestamp)
        self.assertEqual(binId, 1, "the conversion from timestamp to hour is wrong")

    def testGetTimestampFromHour(self):
        """ @TODO: move this into a seperate unit Test for the getTimestamp Class but for now it is perfect here
        """
        hour = 1
        val = 3600
        timestamp = getTimestamp.getTimeStampFromHours(hour)
        self.assertEqual(timestamp, val,
                         "the conversion from timestamp {0:1d} to hour {1:1d} is wrong".format(timestamp, val))

if __name__ == '__main__':
    unittest.main()
