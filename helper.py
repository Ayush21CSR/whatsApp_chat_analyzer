# Import necessary libraries
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
from urlextract import URLExtract
import emoji

# Initialize URL extractor
extract = URLExtract()

def fetch_stats(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Calculate the number of messages
    num_messages = df.shape[0]

    # Calculate the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Calculate the number of media messages
    no_media_msg = df[df['message'] == '<Media omitted>'].shape[0]

    # Calculate the number of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), no_media_msg, len(links)

def most_busy_users(df):
    # Find the top users by message count
    x = df['user'].value_counts().head()

    # Calculate the percentage of messages per user
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    df = df.rename(columns={'percent': 'user_name', 'count': 'percent'})

    return x, df

def create_wordcloud(selected_user, df):
    # Read stop words for word cloud
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Generate the word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user, df):
    # Read stop words for common words analysis
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()
    stop_words = stop_words.split('\n')

    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create a list of words excluding stop words and media messages
    temp = df[df['message'] != '<Media omitted>']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Get the most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Count the emojis used
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    # Create a DataFrame with emoji counts
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by year and month to create a timeline
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create a new column combining year and month for display
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by date to create a daily timeline
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by day name to create a weekly activity map
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by month name to create a monthly activity map
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create a heatmap for user activity based on day name and period
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

