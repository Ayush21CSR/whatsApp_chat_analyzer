# Import necessary libraries
import streamlit as st
import preprocessor
import helper
import seaborn as sns
import matplotlib.pyplot as plt

# Set up the sidebar title for the app
st.sidebar.title("WhatsApp Chat Analyzer")

# File uploader widget in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read the uploaded file
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess the data to create a DataFrame
    df = preprocessor.preprocess(data)

    # Display the DataFrame in the main area of the app
    st.dataframe(df)

    # Fetch the unique list of users from the chat
    user_list = df['user'].unique().tolist()
    # Remove 'group_notification' from the list
    user_list.remove('group_notification')
    # Sort the user list and add 'Overall' at the beginning
    user_list.sort()
    user_list.insert(0, "Overall")

    # Dropdown to select a user for analysis
    selected_user = st.sidebar.selectbox("Show analysis of this person:", user_list)

    # Button to trigger the analysis
    if st.sidebar.button("Show Analysis"):

        # Fetch statistics for the selected user
        num_messages, words, no_media_msg, no_links = helper.fetch_stats(selected_user, df)

        # Display the top statistics
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(no_media_msg)

        with col4:
            st.header("Links Shared")
            st.title(no_links)

        # Monthly timeline plot
        st.title("Monthly Timeline:")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline plot
        st.title("Daily Timeline:")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='pink')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily activity map
        st.title("Daily Activity Map:")
        col1, col2 = st.columns(2)

        with col1:
            st.title("Most Busy Days:")
            busy_day = helper.week_activity_map(selected_user, df)
            st.dataframe(busy_day)
        with col2:
            st.title("Most Busy Days:")
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Monthly activity map
        st.title("Monthly Activity Map:")
        col1, col2 = st.columns(2)

        with col1:
            st.title("Most Busy Months:")
            busy_month = helper.month_activity_map(selected_user, df)
            st.dataframe(busy_month)
        with col2:
            st.title("Most Busy Months:")
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Weekly activity heatmap
        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Find the busiest users in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users:")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Generate and display word cloud
        st.title("Word Cloud:")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Display most common words
        st.title("Most Common Words:")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emojis")
        st.dataframe(emoji_df)
