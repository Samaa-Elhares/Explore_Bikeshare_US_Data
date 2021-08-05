import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
days_list = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_check, month_check, days_check = False, False, False 
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        if not city_check:
            city = input('Would you like to see data for New York, Chicago, or Washington?\n')
            city = city.lower()
            if city not in CITY_DATA:
                print('City not found please choose one of these:New York, Chicago, or Washington\n ')
                continue 
            else:
                city_check = True

        # get user input for month (all, january, february, ... , june)                
        if not month_check:
            month = input('Please choose a month to filter the data by:\nJanuary, February, March, April, May, June, or All to explore all months\n')
            month = month.title()
            if month not in month_list:
                print('Month not found, Please enter a valid month')
                continue
            else:
                month_check = True

        # get user input for day of week (all, monday, tuesday, ... sunday)        
        if not days_check:
            day = input('Please choose a day to filter the data by:\n Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday,or All to explore all days\n')
            day = day.title()
            if day not in days_list:
                print('Day not found, Please choose a valid day')
                continue
            else:
                break

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()
    
    df = pd.read_csv(CITY_DATA.get(city), parse_dates=['Start Time', 'End Time'])
    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Day'] = df['Start Time'].dt.day_name()
    df['Start hour'] =df['Start Time'].dt.hour

    if month != "All":
        df = df[df['Start Month'] == month]

    if day != "All":
        df = df[df['Start Day'] == day]


    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
        most_common_month = df['Start Month'].dropna()
        if most_common_month.empty:
            print('No common month found, Please refilter your data')
        else:
            most_common_month = most_common_month.mode()[0]
            print('Most common month is: {}'.format(most_common_month))
    else:
        print('Select All to get the most common month instead of {}'.format(month))

    # display the most common day of week
    if day == 'All':
        most_common_day = df['Start Day'].dropna()
        if most_common_day.empty:
            print('No common day found, Please refilter your data')
        else:
            most_common_day = most_common_day.mode()[0]
            print('Most common day is: {}'.format(most_common_day))
    else:
        print('Select All to get the most common day instead of {}'.format(day))

    # display the most common start hour
    most_common_hour = df['Start hour'].dropna()
    if most_common_hour.empty:
        print('No common start hour found, Please refilter your data')
    else:
        most_common_hour = most_common_hour.mode()[0]
        print('Most common start hour is: {}'.format(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station']
    if most_common_start_station.empty:
        print('No common start station found')
    else:
        most_common_start_station = most_common_start_station.value_counts().idxmax()  
        print('Most common start station is: {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station']
    if most_common_end_station.empty:
        print('No common end station found')
    else:
        most_common_end_station = most_common_end_station.value_counts().idxmax() 
        print('Most common end station is: {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_frequent_startend_station = df[['Start Station','End Station']].dropna()
    if most_frequent_startend_station.empty:
        print('No frequent combination of start station and end station found')
    else:
        most_frequent_startend_station = most_frequent_startend_station.groupby(
            ['Start Station','End Station']).size().sort_values(ascending=False)
        trip_count = most_frequent_startend_station.iloc[0]
        stations = most_frequent_startend_station[most_frequent_startend_station == trip_count].index[0]
        start_station, end_station = stations
        print('most frequent start station is: {} and end station is: {} which were part of trips: {} times'
            .format(start_station, end_station, trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    available_time = df['Trip Duration'].dropna()
    if available_time.empty:
        print('No data found')
    else:
        total_time = available_time.sum()
        print('Total travel time in seconds is: {}'.format(total_time))

        # display mean travel time
        mean_travel_time = available_time.mean()
        print('Mean travel time in seconds is: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].dropna()
    if user_type.empty:
        print('No data available')
    else:
        user_type = user_type.value_counts()
        print('user type info: {}'.format(user_type))

    # Display counts of gender
    if 'Gender' in df:
        user_gender = df['Gender'].dropna()
        if user_gender.empty:
            print('No data available')
        else:
            user_gender = user_gender.value_counts()
            print('user gender info: {}'.format(user_gender))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_year = df['Birth Year'].dropna()
        if birth_year.empty:
            print('No data available')
        else:
            user_birth_year = df['Birth Year'].dropna()
            if user_birth_year.empty:
                print('No data available')
            else:
                earliest_birth_year = user_birth_year.min()
                print('Earliest birth year is: {}'.format(int(earliest_birth_year)))
                most_recent_birth_year = user_birth_year.max()
                print('Most recent birth year is: {}'.format(int(most_recent_birth_year)))
                most_common_birth_year = user_birth_year.mode()[0]
                print('Most common birth year is: {}'.format(int(most_common_birth_year))) 


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
# Show data raw, 5 raws at a time
def show_raw_data(df):
    choice = input('Would you like to see the raw data? type Yes or NO: ')
    count = 0
    if choice.lower() == 'yes':
        for raw in df.iterrows():
            print(raw)
            count += 1
            if count != 0 and count % 5 == 0:
                choice = input('Would you like to see the raw data? type Yes or NO: ')
                if choice.lower() != 'yes':
                    break
            
                


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
