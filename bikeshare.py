import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# create dictionary for cities and common (unambiguous) abbreviations and nicknames and possible typos (unambiguous if first 4 charaters correct)
chi_aliases = ['chicago', '1', 'chic', 'chi', 'windy city', 'the windy city', 'chi town', 'mud city']
nyc_aliases = ['new york city', '2', 'new ', 'nyc', 'ny', 'new york', 'big apple', 'gotham', 'gotham city', 'empire city']
was_aliases = ['washington', '3', 'wash', 'was', 'dc', 'capitol', 'capitol city']
# create a list of months and all
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all' ]
# create a list of weekdays and all
day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input('Please enter the city: Chicago (1) , New York City (2) or Washington (3): ')).lower()
    while True:
        if city in chi_aliases:
            city = chi_aliases[0]
            break
        elif city in nyc_aliases:
            city = nyc_aliases[0]
            break
        elif city in was_aliases:
            city = was_aliases[0]
            break
        print("\nNOK '{}' is not a valid input\n".format(city))
        city = str(input("Please input Chicago (1), New York City (2) or Washington (3): ")).lower()
    print("\nOK   >>> '{}' was selected <<<\n".format(city.title()))

    # TO DO: get user input for month (all, january, february, ... , june)
    mon_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Please enter the month: all, January, February, ... , June: ').lower()

    while month not in mon_list:
        print("\nNOK '{}' is not a valid input.".format(month))
        month = input("\n>> Please input all, or a month between January and June: \n").lower()
    if month in mon_list:
        print("\nOK   >>> '{}' is a valid input <<<\n".format(month.title()))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Please enter the day of the week: all, Monday, Tuesday, ... , Sunday: ').lower()
    while day.lower() not in day_list:
            print("\nNOK '{}' is not a valid input.".format(day))
            day = input("\nPlease input all, or a weekday name: \n").lower()
    if day in day_list:
        print("\nOK   >>> '{}' is a valid input <<<\n".format(day.title()))

    print('-'*40,'\n')
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int

        #integer = index +1
        month = months.index(month)+1

        # filter by month to create the new dataframe
        # filter the month out of the dataframe in the month column
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        # use the day argument input
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]

    # TO DO: display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print(" >> month: {} ({})\n >> day of week: {}\n >> start hour: {}".format(popular_month, months[popular_month-1].title(), popular_dow, popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40,'\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_s_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    popular_e_station = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + " to " + df['End Station']
    popular_route = df['Route'].mode()[0]

    print (" >> start station: {}\n >> end station: {}\n >> route: {}".format(popular_s_station, popular_e_station, popular_route))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    ttt is total travel time"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    ttt = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    # create df for travel time
    mean_travel_time = df['Trip Duration'].mode()[0]
    print (" >> total travel time: {} seconds --> {} minutes --> {} hours --> {} days\n >> mean travel time: {} seconds --> {} minutes".format(ttt, int(round(ttt/60,0)), round(ttt/3600,1), round(ttt/86400,2), mean_travel_time, round(mean_travel_time/60,1)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(user_type_count,"\n")
    if city != 'washington':
        # TO DO: Display counts of gender
        gender_count = df['Gender'].value_counts()

        # TO DO: Display earliest, most recent, and most common year of birth
        young = df['Birth Year'].max()
        old = df['Birth Year'].min()
        common_birth = df['Birth Year'].mode()[0]
        print(" >> The youngest user was born in {}\n >> The oldest user was born in {}\n >> The most common YOB is {}".format(int(young), int(old), int(common_birth)))
    else:
        print(" \n >> For {} there is no user data for gender or year of birth".format(city.title()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def viewer(df):
    """Displays individual trip data after positive user input."""
    view_data = input("Would you like to view 5 rows of individual trip data? Enter 'yes' or 'no'? ").lower()
    if view_data == 'yes':
        start_loc = 0
        while True:
            print(df.iloc[start_loc:start_loc + 5])
            print('-'*40)
            start_loc += 5
            view_display = input("\nDo you wish to continue? Press 'Enter' to continue input 'no' to exit ").lower()
            if view_display == 'no':
                print("\n >> You have ended viewing individual trip data")
                break
    else:
        print("\n >> You have skipped viewing individual trip data")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        viewer(df)

        restart = input('\nWould you like to restart? Enter yes to repeat or any key to exit.\n')
        if restart.lower() != 'yes':
            print("\n >>> You are exiting the program <<<\n")
            break
        else:
            print("\n >>> Restarting the program...\n")


if __name__ == "__main__":
	main()
