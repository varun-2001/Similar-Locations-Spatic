import pandas
from geopy import distance
from geopy.geocoders import Nominatim

# Store the csv data in a dataframe for easier manipulation
locations = pandas.read_csv('assignment_data.csv')

geolocator = Nominatim(user_agent="assignment")

# Create copy of data to add the is_similar column
result = locations.copy()
result["is_similar"]=0

""" Calculates the minimum edits required to change one word 
to the other using Dynamic Programming """

def editDistance(loc1,loc2):
    m=len(loc1)
    n=len(loc2)

    # Create 2D DP table
    dp = [[0 for i in range(n+1)] for j in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            
            # if word1 is empty string, edit distance is length of other string
            if i==0:
                dp[i][j]=j
            elif j==0:
                dp[i][j]=i
            
            # if letter is equal, edits required is the minimum edits so far
            elif loc1[i-1] == loc2[j-1]:
                dp[i][j]=dp[i-1][j-1]
            
            # Minimum edits so far + 1 operation to change the letter
            else:
                dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])
    return dp[m][n]


for i in range(locations.shape[0]-1):
    lat1 = locations.iloc[i].latitude
    long1 = locations.iloc[i].longitude
    lat2 = locations.iloc[i+1].latitude
    long2 = locations.iloc[i+1].longitude

    # Calculate distance between every 2 points in metres using geopy
    d = distance.distance((lat1,long1),(lat2,long2)).meters

    #  if distance between points is less than 200m and edits required is less than 5, they are similar
    if (d<200) and editDistance(locations.loc[i,"name"],locations.loc[i+1,"name"])<5:
        result.loc[i,"is_similar"] = 1
        result.loc[i+1,"is_similar"] = 1
        
# write result into csv file
result.to_csv('result.csv',index=False)