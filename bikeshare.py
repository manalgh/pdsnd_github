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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
            if city in CITY_DATA.keys():
                break
            else:
                print('Looks like you\'ve enterred an invalid city!!\n')
        except:
            continue

    user_filter = input('Would you like to filter the data by month, day, both, or not at all? Type \'none\' for no time filter\n').lower()

    if user_filter == 'month':
        while True:
            try:
                month = input('Which month - January, February, March, April, May, or June?\n').lower()
                day = 'all'
                if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                    break
                else:
                    print('Looks like you\'ve enterred an invalid month!!\n')
            except:
                continue

    elif user_filter == 'day':
        while True:
            try:
                month = 'all'
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
                if day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday']:
                    break
                else:
                    print('Looks like you\'ve enterred an invalid day!!\n')
            except:
                continue

    elif user_filter == 'both':
        while True:
            try:
                month = input('Which month - January, February, March, April, May, or June?\n').lower()
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
                if day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday'] and month in ['january', 'february', 'march', 'april', 'may', 'june']:
                    break
                else:
                    print('Looks like you\'ve enterred an invalid month or day!!\n')
            except:
                continue

    elif user_filter == 'none':
        month = 'all'
        day = 'all'

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
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
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
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month = months[df['month'].mode()[0]-1]
    print('Most common month:',common_month,'\n')

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day:',common_day,'\n')
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour:',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:',common_start_station,'\n')
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:',common_end_station,'\n')

    # display most frequent combination of start station and end station trip
    frequent_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most frequent combination of start station and end station trip\n',frequent_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time:',total_travel,'\n')
    # display mean travel time
    average_travel = df['Trip Duration'].mean()
    print('Average travel time:',average_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Counts of user types:\n',user_type,'\n')
    #Washington data does not have gender and birth year columns
    if city !='washington':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('Counts of gender:\n',gender,'\n')
        # Display earliest, most recent, and most common year of birth
        earliest_birthyear = df['Birth Year'].min()
        print('Earliest year of birth:\n',earliest_birthyear,'\n')
        recent_birthyear = df['Birth Year'].max()
        print('Most recent year of birth:\n',recent_birthyear,'\n')
        common_birthyear = df['Birth Year'].mode()[0]
        print('Most common year of birth:\n',common_birthyear)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # Asks user if they would like to view 5 rows of individual trip data
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data =='yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
