import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
    #In case the user enters a city that's not included in the initially defined CITY 
    #dictionary, a message will pop up and the input will be asked for again
        try:
            city = input('Enter a city:')
             
            if city.lower() not in CITY_DATA.keys():
                print('Sorry, that city is currently not available. Please enter another city')
            elif city.lower() in CITY_DATA.keys():
                break
        except:
            print('That\'s not a valid city')
            
    while True:
    #In case the user enters a month that's not included in the list months  
    #that contains the first 6 months of the year plus the 'all' option, a message 
    #will pop up and the input will be asked for again
            try:
                month = input('Enter the month you are interested in explore (all is also an option):')
                months = ['january', 'february', 'march', 'april', 'may', 'june','all']

                if month.lower() not in months:
                    print('Sorry, that month is currently not available. Please enter another month')
                elif month.lower() in months:
                    break
            except:
                print('That\'s not a valid month')
                
    while True:
    #In case the user enters a day that's not included in the list days  
    #that contains the 7 days of the week plus he all option, a message will pop 
    #up and the input will be asked for again
            try:
                day = input('Enter the day of the week you are interested in explore (all is also an option):')
                days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday', 'all']

                if day.lower() not in days:
                    print('Sorry, that day is not valid. Please enter another day')
                elif day.lower() in days:
                    break
            except:
                print('That\'s not a valid format')

    day = day.lower()
    month = month.lower()
    city = city.lower()
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable, thus, if a month is specified
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month']==month]
        
    # filter by day of week if applicable, thus, if a day is specified 
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    popular_month = df['month'].mode()[0]
    
    # display the most common day of week
    
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    
    print('The most popular month was: {}, while the most popular day was: {}, and finally, the most popular hour was  {}.'.format(popular_month,popular_day,popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
	
	
	
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    start_station = df['Start Station'].mode()[0]
    # display most commonly used end station
    end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Start-End Stations'] = df['Start Station'] + ' ending up in ' + df['End Station']
    popular_combo= df['Start-End Stations'].value_counts().index.tolist()[0]
    
    print('The most commonly used start station is: {}, the most commonly used end station is: {} and the most frequent combination of start-end stations is: {}.'.format(start_station,end_station,popular_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Travel Time'] = df['End Time'] - df['Start Time']
    Total_travel = df['Travel Time'].sum()
    

    # display mean travel time
    
    Mean_travel = df['Travel Time'].mean()
    
    print('The total travel time is: {} and the average travel time: {}.'.format(Total_travel, Mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    user1 = df['User Type'].value_counts().index.tolist()[0]
    user2 = df['User Type'].value_counts().index.tolist()[1]
    user1N=user_types[0]
    user2N=user_types[1]
    print('The number of {} users was {} and the number of {} users was {}.'.format(user1,user1N,user2,user2N))
    
    # Display counts of gender in case the Gender is available. 
    # In case it's not available, we won't compue the Birth stats either
    # as the information available for cities do not have one without the other. 
    # Another if condition could be required in case this changed.
    if 'Gender' in df.columns: 
        df['Gender'] = df['Gender'].fillna('Undetermined')
        Gender_types = df['Gender'].value_counts()
        Gender1 = df['Gender'].value_counts().index.tolist()[0]
        Gender2 = df['Gender'].value_counts().index.tolist()[1]
        Gender3 = df['Gender'].value_counts().index.tolist()[2]

        Gender1N=Gender_types[0]
        Gender2N=Gender_types[1]
        Gender3N=Gender_types[2]

        print('The number of {} users was {}, of {} users was {} and the number of {} gender users was {}.'.format(Gender1,Gender1N,Gender2,Gender2N,Gender3,Gender3N))


        # Display earliest, most recent, and most common year of birth
        df['Birth Year'] = df['Birth Year'].dropna()
        Common_Birth = df['Birth Year'].value_counts().index.tolist()[0]
        Early_Birth = df['Birth Year'].min()
        Latest_Birth = df['Birth Year'].max()
        print('The most common birth year registered is {}. The earliest is {} and the most recent {}.'.format(Common_Birth,Early_Birth,Latest_Birth))
    else:
        print('Gender and Birth Date information is not available for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        rawdata = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        i = 0
        while rawdata.lower() == 'yes':
            print(df[i:i+5])
            i += 5
            rawdata = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if rawdata.lower() != 'yes':
                break
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
