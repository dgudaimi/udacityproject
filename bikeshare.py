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
        try:
            city = int(input('Please select number the city you would like to draw data from ( 1: Chicago, 2: NYC, 3: Washington): '))
            if city == 1:
                city = 'chicago'
                break
            elif city == 2:
                city = 'new york city'
                break
            elif city == 3:
                city = 'washington'
                break
            else:
                print('The number you entered is invalid')
        except ValueError:
            print('Invalid input, please try again.')
        #print(city)
    while True:
        try:
            month = input('Please select the month you would like to draw data from (All, 1: Jan, 2: Feb, 3: Mar, 4: Apr, 5: May, 6: Jun: ').title()
            if month == 'All':
                break
            elif int(month) < 7 and int(month) >=0:
                break
            else:
                print('Invalid input, please try again.')
        except ValueError:
            print('Invalid input, please try again.')     
    while True:
        try:
            day = input('Please select the day you would like to draw data from (All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday): ').title()
            if day in ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
                break
            else:
                print('Invalid input, please try again.')     

        except ValueError:
            print('Invalid input, please try again.')    

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'All':
        months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    print('Common month: ', int(df['month'].mean()))
    print('Common day: ', df['day_of_week'].describe())
    print('Common hour: ', int(df['hour'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    start_station = df.groupby('Start Station')['Start Station'].count()
    print(df['Start Station'].describe())
    print('Most frequent station: ' , start_station.max())
    # TO DO: display most commonly used start station
    #print(start_station)
    #start_station = start_station.max()
    #print(start_station)

    # TO DO: display most commonly used end station
    print(df['End Station'].describe())
    end_station = df.groupby('End Station')['End Station'].count()
    print('Most frequent end station: ',end_station.max())

#    print(end_station.head(1))


    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Combo'] = df['Start Station'] + ' ' + df['End Station']
    start_end_station = df.groupby('Start End Combo')['Start End Combo'].count()
    print(df['Start End Combo'].describe())
    print('Most frequent combo: ',start_end_station.max())
    #print(start_end_station.head(1))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time: ', (df['Trip Duration'].sum())/60, 'minutes.' ) 


    # TO DO: display mean travel time
    print('Average travel time: ', (df['Trip Duration'].mean())/60, 'minutes.' ) 
    #mean_travel = df['Trip duration'].mean()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df.groupby('User Type')['User Type'].count()
    print(user_type)

    # TO DO: Display counts of gender
    #print(df['Gender'].describe())
    if city != 'washington':
        gender = df.groupby('Gender')['Gender'].count()
        print(gender)
    # TO DO: Display earliest, most recent, and most common year of birth
        print('earliest: ', df['Birth Year'].min())
        print('recent: ', df['Birth Year'].max())
        print('common: ', df['Birth Year'].mean())

    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_lines(df):
    """Asks user if they would like to view raw data, displaying 5 lines at a time, iterating every time a user requests more lines. Breaks if user selects anything but 'yes' """
    i = 5
    while True:
        view = input('Would you like to view data on the above statistics? Enter yes to preceed, any other key to exit: ').lower()
        if view != 'yes':
            break
        else:
            print(df.iloc[:i])
            i=i+5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print_lines(df)
        #print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        #print_lines(df)


        restart = input('\nWould you like to restart? Enter yes to continue, any other key to stop: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
