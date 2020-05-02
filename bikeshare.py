import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']


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
        city = (input('Would you like to see data for Chicago, New York or Washington? ')).lower()
        if city in ['chicago','new york', 'washington']:
            print ('{} selected \n'.format(city.title()))
            break
        else:
            print('Incorrect input, only Chicago, New York and Washington available')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        month_question = (input('Would you like to filter the data by month? Yes/No: ')).lower()
        if month_question == 'yes':
            month = (input('Please enter month between January and June: ')).lower()
            if month in ['january','february','march', 'april','may','june']:
                print ('{} selected \n'.format(month.title()))
                break
            else:
                print ('Enter the month as a string between january - june')
                continue
        elif month_question == 'no':
            month = 'all'
            print('all selected \n')
            break
        else:
            print('Select Yes/No')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_question = (input('Would you like to filter the data by day? Yes/No: ')).lower()
        if day_question == 'yes':
            day = (input('Please enter weekday between Monday and Sunday: ')).lower()
            if day in ['monday','tuesday','wednesday', 'thursday','friday','saturday','sunday']:
                print ('{} selected \n'.format(day.title()))
                break
            else:
                print('Enter the day between Monday - Sunday')
                continue
        elif day_question == 'no':
            day = 'all'
            print ('all selected \n')
            break
        else:
            print('Select Yes/No')
            continue

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
    # Loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # Converting start and end time to datetime, and creating new columns for month and day
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    #Filter for month if applicable
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        day = days.index(day.lower())

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = (df['month'].mode()[0])
    #Showing the output as monthname
    common_month = months[common_month-1].title()

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    #Showing the output as dayname
    common_day = days[common_day].title()

    # display the most common start hour
    common_hour = (df['Start Time'].dt.hour).mode()[0]

    print('Most common month: {} \nMost common day: {} \nMost common hour: {}'.format(common_month,common_day,common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    common_combination = (df['Start Station']+' >> '+df['End Station']).mode()[0]

    print('Most commonly used start station: {}'.format(common_start_station))
    print('Most commonly used end station: {}'.format(common_end_station))
    print('Most frequent combination: {}'.format(common_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())

    print ('Total travel time: {} seconds \nMean travel time: {} seconds'.format(total_travel_time, mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df.groupby(['User Type'])['User Type'].count()
    print(user_type_counts)
    # Display counts of gender
    try:
        gender_counts = df.groupby(['Gender'])['Gender'].count()
        print('\n',gender_counts)
    except KeyError:
        print('\nNo gender data to share')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = round(df['Birth Year'].min())
        most_recent_birth = round(df['Birth Year'].max())
        common_birth = round(df['Birth Year'].median())
        print('\nEarliest birth: {}\nMost recent birth: {}\nMost common birth year: {}'.format(earliest_birth,most_recent_birth,common_birth))
    except:
        print('\nno birth data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Giving the user an option to see raw data
        counter = 0
        while True:
            data_question = (input('Would you like to see the raw data? Yes/No: \n')).lower()
            rows_start = 5*counter
            rows_end = 5+5*counter
            # Showing the raw data by using dataframe. Removing unnecessary columns
            df2=df.set_index('Start Time')
            df2=df2.drop(['Unnamed: 0','month','day_of_week'],axis=1)
            if data_question == 'yes':
                counter += 1
                print('\n')
                print (df2[rows_start:rows_end])
            elif data_question =='no':
                break

        restart = input('\nWould you like to restart? Yes/No: \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
