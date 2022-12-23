import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

valid_monthes = ['all','january', 'february', 'march', 'april', 'may', 'june']
Valid_days = ['all' ,'saturday' , 'sunday', 'monday' , 'tuesday' , 'wednesday' , 'thursday' , 'friday' ]



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
        city = input("please type one of this three cities (chicago, new york city, washington) : ")
        if city.lower() in CITY_DATA:
            break
        else:
            print('You entered not valid city name \n' )
            continue
    print("\n")   
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("which month you want to filter with for example january, february, ... , june or type 'all' for no month filter :  ")
        if month.lower() in valid_monthes:
            break
        else:
            print('You entered not valid value for month name \n' )
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\n")
    while True:
        day = input("which day of the week you want to filter with for example sunday,monday, ... friday or type 'all' for no day filter : ")
        if day.lower() in Valid_days:
            break
        else:
            print('You entered not valid value for day name \n' )
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
    # load from file
    file_name= CITY_DATA[city]
    df = pd.read_csv(file_name)
    
   # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # get month from the Start Time column to create an month name column
    df['month'] = df['Start Time'].dt.month_name()

    # get day from the Start Time column to create an day name column
    df['day'] = df['Start Time'].dt.day_name()

    # get hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # get the Start Station AND End Station column to create an  start_to_end new column
    df['start_to_end'] = df['Start Station'].str.cat(df['End Station'], sep=' --> ')
    
     # filter by the month name
    if month != 'all':
        df = df[ df['month'] == month.title() ]

    # filter by day of the week name
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (dataframe) df - dataframe of data that needs to analyze 
    Returns:
        Nothing
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month


    common_month = df['month'].mode()[0]
    print("The most common month is :", common_month)

    # display the most common day of week
    common_day = df['day'].mode()[0]
    print("The most common day is :", common_day)


    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("The most common start hour is :", common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (dataframe) df - dataframe of data that needs to analyze
    Returns:
        Nothing
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start_station is :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combination = df['start_to_end'].mode()[0];
    print('The most combination of start to end station trip is: ',most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        (dataframe) df - dataframe of data that needs to analyze
    Returns:
        Nothing
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("The total of travel time is :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("the mean of travel time is : ", mean_travel)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,current_city):
    """Displays statistics on bikeshare users.
    Args:
        (dataframe) df - dataframe of data that needs to analyze
        (string) current_city - current city that needs to analyze
    Returns:
        Nothing
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types =df['User Type'].value_counts()
    print("The counts of user types is : ",user_types)

    # Display counts of gender
    if 'Gender'  in df.columns:
        print("\n")
        gender_types =df['Gender'].value_counts()
        print("The counts of gender types is : ",gender_types)
    else:
       print("\n")
       print('Sorry, {} has no column called "Gender" informations'.format(current_city))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year'  in df.columns:
        print("\n")
        earliest=int(df['Birth Year'].min())
        most_recent=int(df['Birth Year'].max())
        most_common_year=int(df['Birth Year'].mode())
        print('Earliest user year of birth is: ',earliest)
        print('Recent user year of birth is: ',most_recent)
        print('Most common user year of birth is: ',most_common_year)
    else:
       print("\n")
       print('Sorry, {} has no column called "Birth Year" informations'.format(current_city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(city):
    """Show 5 records from the selected city.
    Asks user to type if he wants to show raw data or not

    Args:
        (dataframe) df - dataframe of data that needs to analyze
    Returns:
        Nothing
    """
    df = pd.read_csv(CITY_DATA[city])
    allowed_answers = ['no','yes']
    inputs = ''

    #counter to use later in displaying raw data with df.head() method
    i = 0

    #prompt the user if they want to see 5 lines of raw data,
    while inputs not in allowed_answers:
        print("\nDo you want show first 5 records?")
        print("\nPlease type: Yes or No\n")
        inputs = input().lower()

        #show first 5 records of data
        if inputs == "yes":
            print(df.head())
        elif inputs not in allowed_answers:
            print("\nPlease choose yes or no.")

    #Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration,
    while inputs == 'yes':
        print("\nShow More Data?\n")
        i += 5
        inputs = input().lower()
        #If yes -> display more 5 records, else -> break
        if inputs == "yes":
             print(df[i:i+5])
        elif inputs != "yes":
             break

    print('-'*40)

def main():
    while True:
        
        # for testing         
        # city = 'washington'
        # month = 'january'
        # day = 'monday'
        
        city, month, day = get_filters()

        df = load_data(city.lower(), month.lower(), day.lower())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        display_data(city.lower())
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
