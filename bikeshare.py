#optimize start comment

import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_valid_input(prompt, valid_options):
    """
    Helper function to get valid input from the user.

    Args:
        prompt (str): The input prompt for the user.
        valid_options (list): List of valid options.

    Returns:
        str: User's input (lowercase and stripped).
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print('Invalid input, please try again.')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = list(CITY_DATA.keys())
    city = get_valid_input('Let\'s begin by choosing a city! Which city would you like to explore: '
                           'Chicago, New York City, or Washington?\n\n', cities)

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = get_valid_input(f'\nWhich month are you interested in analyzing for in {city.title()}? '
                            f'You have the option to select from January, February, March, April, May, June and All.\n\n',
                            months)

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = get_valid_input('\nLastly... What day of the week?\n\n', days)

    print('-' * 40)
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
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Week_Day'] = df['Start Time'].dt.weekday

    if month != 'all':
        df = df[df['Month'] == month.index(month) + 1]

    if day != 'all':
        df = df[df['Week_Day'] == day.index(day)]

    return df


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()

    if 'Start Time' not in df.columns:
        print(f'No start time data for {city.title()} data')
    else:
        print('\nCalculating The Most Frequent Times of Travel...\n')

        # Display the most common month
        mode_month = df['Month'].mode()[0]
        print(f'Most common month to start a trip: {mode_month}')

        # Display the most common day of week
        mode_day_of_week = df['Week_Day'].mode()[0]
        print(f'Most day of the week to start a trip: {mode_day_of_week}')

        # Display the most common start hour
        mode_start_hour = df['Start Time'].dt.hour.mode()[0]
        print(f'Most common hour to start a trip: {mode_start_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""
    start_time = time.time()
    if 'Start Time' not in df.columns:
        print(f'No start time in {city.title()} data')
    else:
        print('\nCalculating The Most Popular Stations and Trip...\n')

        mode_start_station = df['Start Station'].mode()[0]
        print(f'Most common station to start a trip from: {mode_start_station}')

        mode_end_station = df['End Station'].mode()[0]
        print(f'Most commonly used station to end a trip: {mode_end_station}')

        df['Combined_Station'] = df['Start Station'] + ' and ' + df['End Station']
        frequent_start_and_end = df['Combined_Station'].mode()[0]
        print(f'Most frequent combination of start station and end station trip: {frequent_start_and_end}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""
    start_time = time.time()

    if 'Start Time' not in df:
        print(f'No start time in {city.title()} data')
    else:
        print('\nCalculating Trip Duration...\n')

        total_time_travel = df['Trip Duration'].sum()
        print(f'Total travel time: {total_time_travel}')

        mean_travel_time = df['Trip Duration'].mean()
        print(f'Mean travel time: {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' not in df.columns:
        print(f'No data for user type in {city.title()}')
    else:
        user_type_count = df['User Type'].values

        subscriber_user_type = (user_type_count == 'Subscriber').sum()
        print(f'Number of subscriber: {subscriber_user_type}')

        customer_user_type = (user_type_count == 'Customer').sum()
        print(f'Number of customer: {customer_user_type}\n')

    if 'Gender' not in df.columns:
        print(f'No data for gender in {city.title()}')
        print(f'No data for birth year in {city.title()}')
    else:
        gender_count = df['Gender'].values
        male = (gender_count == 'Male').sum()
        female = (gender_count == 'Female').sum()
        print(f'The number of male users: {male}')
        print(f'The number of female user: {female}')

        earliest_birth_year = round(df['Birth Year'].min())
        print('\n')
        print(f'Earliest year of birth: {earliest_birth_year}')

        recent_birth_year = round(df['Birth Year'].max())
        print(f'Recent year of birth: {recent_birth_year}')

        mode_birth_year = round(df['Birth Year'].mode()[0])
        print(f'Most common year of birth: {mode_birth_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_data(df):
    i = 0

    while True:
        data = input("\nDo you want to view 5 lines of raw data? Please enter 'yes' or 'no'?\n\n")
        if data.lower() == 'yes' or data.lower() == 'y':
            print(df[i:i + 5])

            # increase index by 5
            i = i + 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes' or 'y':
            break
        print('\n\n')


if __name__ == "__main__":
    main()

#optimize end comment
#The end