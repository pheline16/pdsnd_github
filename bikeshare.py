import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day of week to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()#.replace(' ', '_')
        if city not in CITY_DATA:
            print('Oops!, The day you\'ve entered seems an invalid input! Try again.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    #('Would you like to filter the data by month, day, both or not at all?')
    while True:
        month = input('Name the month you wanna filter by or enter all to apply no filter by month: ').lower()
        if month in months:
            month = months.index(month) + 1
            break
        elif month != 'all':
            print('Oops!, The day you\'ve entered seems an invalid input! Try again.')
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Name the day you wanna filter by or enter all to apply no filter by day: ').lower()
        if day in days:
             day = days.index(day)
             break
        elif day != 'all':
            print('Oops!, The day you\'ve entered seems an invalid input! Try again.')
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
    df = pd.read_csv(CITY_DATA[city])

    while True:
        if month != 'all':
            df['month'] = pd.to_datetime(df['Start Time'])
            df['month'] = df['month'].dt.month
            df = df[df['month'] == month]
        break

    while True:
        if day != 'all':
            df['day'] = pd.to_datetime(df['Start Time'])
            df['day'] = df['day'].dt.dayofweek
            df = df[df['day'] == day]
        break

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time']= pd.to_datetime(df['Start Time'])


    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('The most common month: ', popular_month)


    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of the week: ', popular_day)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count_start = (df['Start Station'].values == popular_start_station).sum()
    print('The most popular start station is', popular_start_station, 'with a count of ', count_start)



    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    count_end = (df['End Station'].values == popular_end_station).sum()
    print('The most popular end station is ', popular_end_station, 'with a count of ', count_end)


    # TO DO: display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
   # count_combination = (df.groupby(['Lake Shore Dr & Monroe St', 'Streeter Dr & Grand Ave'])).count()
    print('The most popular combination of start station and end station trip is ', popular_combination)#, count_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['travel'] =  pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    print('The total travel time was ', df['travel'].sum())


    # TO DO: display mean travel time
    #df['mean_travel'] =  pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    print('The mean travel time was ', df['travel'].mean())




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('These user types exist and have the following count\n',user_types)


    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('These gender exist and have the following count\n',gender)

        # TO DO: Display earliest, most recent, and most common year of birth
        print('The earliest year of birth was', int(df['Birth Year'].min()))
        print('The most recent year of birth was', int(df['Birth Year'].max()))
        print('The most common year of birth was', int(df['Birth Year'].value_counts().idxmax()))

    except KeyError:
        print("\nNo data for gender and age available")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    while True:
        display = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        start_loc = 0
        while display == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            display = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        break





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        #if city != 'washington':
        user_stats(df)
        display_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
