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
    valid_city = ["Chicago", "New York City", "Washington"]
    city = ""
    while city not in valid_city:
        city = input("Hello! Would you like to see data for Chicago, New York City or Washington? ").title()
    print("Got it! We will check {} data.\n".format(city))

    # get user input for month (all, january, february, ... , june)
    valid_month = ["All","January", "February", "March", "April","May", "June", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    month = ""
    print("Which month of data would you like to analyze?")
    while month not in valid_month:
        month = input("You can only enter any month between January and June, or enter All: ").title()
    month_index = valid_month.index(month)
    if month_index > 6:
        month = valid_month[month_index-6]
    print("Alright! We will check {} data in {}.\n".format(month, city))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day = ["All","Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day = ""
    print("Which day of data would you like to analyze?")
    while day not in valid_day:
        day = input("You can only enter any day of the week in words. If you want whole week data, enter All: ").title()
    day_index = valid_day.index(day)
    if day_index > 7:
        day = valid_day[day_index-7]
    print("Alright! We will check {} data in {}.\n".format(day, city))

    print('-'*40)
    return city.lower(), month, day

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

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
        popular_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        print('Most Popular Month:', months[popular_month-1])

    # display the most common day of week
    if day == 'All':
        popular_day = df['day_of_week'].mode()[0]
        print('Most Popular day of the week: ', popular_day)

    # display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_Start_St = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', most_Start_St)
    # display most commonly used end station
    most_end_St = df['End Station'].mode()[0]
    print('Most commonly used end station: ', most_end_St)
    # display most frequent combination of start station and end station trip
    df['Start_to_end Station'] = df['Start Station'] + ' to ' + df['End Station']
    most_s_e_st = df['Start_to_end Station'].mode()[0]
    print('Most common trip is from ', most_s_e_st)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total duration of the selected month(s) and day(s) in seconds: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Average duration of the selected month(s) and day(s) in seconds: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Following are different types of users \n")
    print(user_types)

    if city != "washington":
    # Display counts of gender
        gender = df['Gender'].value_counts()
        print("\nFollowing are the gender counts of the users \n")
        print(gender)
    # Display earliest, most recent, and most common year of birth
        print("\nBelieve it or not, the oldest subscriber was born in", int(df['Birth Year'].min()))
        print("The youngest subscriber was born in", int(df['Birth Year'].max()))
        print("Most subscribers were born in", int(df['Birth Year'].mode()[0]))
    else:
        print("There is no gender or year of birth data in Washington")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_detail(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n\n')
    start_loc = 0
    while (view_data in ['yes', 'Yes', 'y', 'Y']):
        # print first 5 rows and the original columns of the .csv file without the added columns
        print(df.iloc[start_loc: start_loc+5, 0:df.shape[1]-4])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_detail(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'Yes', 'y', 'Y']:
            break

if __name__ == "__main__":
	main()
