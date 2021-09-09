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
    print("Hello! Let's explore some US bikeshare data!")
    
    
    # Get user input for city (chicago, new york city, washington).
    # Make sure the Input is valid
    cities = ('chicago' , 'new york city' , 'washington')
    while True:
        city = input("PLEASE ENTER CITY NAME 'Chicago, New York city or Washington': ")
        city = city.lower().strip()
        if city not in cities:
            print("Invalid city....PLEASE TRY AGAIN!")
        else:
            break
    print(f"You choose {city.title()}")
    
    
    # Get user input for month (all, january, february, ... , june)
    # Make sure the Input is valid 
    months = ('all', 'january' , 'february' , 'march' , 'april' , 'may' , 'june')
    while True:
        month = input("PLEASE ENTER MONTH 'from january to june' or 'all': ")
        month = month.lower().strip()
        if month not in months:
            print("Invalid month....PLEASE TRY AGAIN!")
        else:
            break   
    print(f"You choose {month.title()}")
            
    
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    # Make sure the Input is valid
    days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    while True:
        day = input("PLEASE ENTER DAY or 'all': ")
        day = day.lower().strip()
        if day not in days:
            print("Invalid day....PLEASE TRY AGAIN!")
        else:
            break
    print(f"You choose {day.title()}")
    
    print('-'*40)
    return city , month , day


def load_data(city, month, day): 
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Reading CSV File 
    df = pd.read_csv(CITY_DATA[city])
    
    # Change Start Time colomn to datetime in Pandas
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Create a new coloumns 'month' , 'day_of_week' and 'hour' then get the data from 'Start Time' colomn
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    
    # Add a new coloumn 'Start to End Station' to save each trip from start to end
    df['Trip Stations'] = 'From ' + df['Start Station'] + ' to ' + df['End Station']
    
    return df


def time_stats(df): 
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Very impotant note : 'month' coloumn is the number of month
    # Display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    index_of_most_common_month = df['month'].mode()[0]
    most_common_month = months[index_of_most_common_month - 1]
    print(f'Most common month is : {most_common_month.upper()} .')

    # Very impotant note : 'day_of_week' coloumn is the name of day
    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f'Most common day of week is : {most_common_day.upper()} .')
        

    # TDisplay the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print(f'Most common start hour is : {most_common_start_hour} .')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df): 
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station *From 'Start Station' coloumn*
    most_common_start_station = df['Start Station'].mode()[0]
    print(f'Most common start station is : {most_common_start_station} .')

    # Display most commonly used end station *From 'End Station' coloumn*
    most_common_end_station = df['End Station'].mode()[0]
    print(f'Most common end station is : {most_common_end_station} .')

    # Display most frequent combination of start station and end station trip *From 'Trip Stations' coloumn*
    most_common_trip_stations = df['Trip Stations'].mode()[0]
    print(f'Most common trip stations is : {most_common_trip_stations} .')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df): 
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time *From 'Trip Duration' coloumn*
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time = {total_travel_time / 60.00} min")

    # Display mean travel time *From 'Trip Duration' coloumn*
    # df.describe() ==> [0] == count , [1] == mean , [2] == std
    mean_travel_time = df['Trip Duration'].describe()[1]
    print(f"Mean travel time = {mean_travel_time / 60.00} min")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df): 
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types *From 'User Type' coloumn*
    # df['User Type'].value_counts() ==> [0] == Subscriber , [1] == Customer , [2] == Dependent
    subscriber = df['User Type'].value_counts()[0]
    customer = df['User Type'].value_counts()[1]
    #dependent = df['User Type'].value_counts()[2]
    print(f"Number of SUBSCRIBERS : {subscriber} ")
    print(f"Number of CUSTOMERS : {customer} ")
    #print("Number of DEPENDENT : {} \n".format(dependent))
    
    
    # Just if city is 'Chicago' or 'New york city'
    # Display counts of gender *From 'Gender' coloumn*
    # df['Gender'].value_counts() ==> [0] == male , [1] == female
    if 'Gender' in df:
        male   = df['Gender'].value_counts()[0]
        female = df['Gender'].value_counts()[1]
        print(f"Number of MALES : {male}")
        print(f"Number of FEMALES : {female} \n")
        
        
    # Just if city is 'Chicago' or 'New york city'
    # Display earliest, most recent, and most common year of birth *From 'Birth Year' coloumn*
    # df['Birth Year'].describe() ==> [3] == min , [7] == max 
    if 'Birth Year' in df:
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        youngest = df['Birth Year'].describe()[7]
        oldest   = df['Birth Year'].describe()[3]
        print(f"Most common year of birth : {most_common_year_of_birth}")
        print(f"Earliest year of birth : {oldest}")
        print(f"Most recent year of birth : {youngest}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(city):
    print("Random raw data is available to check...\n")
    repeat = 'yes'
    while repeat == 'yes':
        for chunk in pd.read_csv(CITY_DATA[city] , chunksize = 5):
            print(chunk)
            repeat = input("Do you want too check another raw data? 'yes or no' ")
            if repeat == 'no':
                break;
       
 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(city)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
