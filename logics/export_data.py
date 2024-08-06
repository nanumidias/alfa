import streamlit as st
import pandas as pd
import io
import xlsxwriter


from logics.fetch_google_analytics_data import *

from logics.load_data import google_api_data_load
from logics.load_data import facebook_api_data_load
from logics.load_data import google_analytics_data_load
from logics.load_data import facebook_ads_data_load
from logics.load_data import instagram_data_load


from logics.utilis import load_google_api
from logics.utilis import facebook_apis_tokens

from logics.date_range import date_range_for_ads


from facebook_business.api import FacebookAdsApi

access_token            = st.secrets["access_tokens"]["user_access_token"]
instagram_user_id       = st.secrets["instagram"]["instagram_user_id"]

(page_access_token, user_access_token, 
 page_id, adaccount_account_id, adaccount_id) = facebook_apis_tokens()
FacebookAdsApi.init(access_token= page_access_token)

def export_data(start_date, end_date):
    (page_access_token, user_access_token, 
    page_id, adaccount_account_id, adaccount_id) = facebook_apis_tokens()
    selected_range       = date_range_for_ads()
    # GOOGLE ADS
    client, property_id, dimensions, metrics = load_google_api()
    google_ads_data_, total_google_ads_data_ = google_api_data_load(start_date, end_date, client, property_id)
    google_ads_data  = pd.DataFrame(google_ads_data_)
    # GOOGLE ANALYTICS
    data_, rose_pie_data_, eventCount_data_, sunbrust_data_ = google_analytics_data_load(client, property_id, start_date, end_date)
    google_analytics            = pd.DataFrame(data_)
    # FACEBOOK ADS DATA
    ads_insights_, ada_account =  facebook_ads_data_load(user_access_token, adaccount_account_id, adaccount_id, selected_range)
    ads_insights  = pd.DataFrame(ads_insights_)
    # FACEBOOK DATA
    (
    page_insights, dates, page_post_engagements, 
    page_impressions, page_impressions_unique, 
    page_fans, unique_page_fan, page_follows, 
    page_views, page_negative_feedback_unique, 
    page_impressions_viral, 
    page_fan_adds_by_paid_non_paid_unique, 
    page_daily_follows_unique, page_daily_unfollows_unique, 
    page_impressions_by_age_gender_unique, 
    page_impressions_organic_unique_v2, 
    page_impressions_paid, post_reactions, 
    page_fans_country, page_fan_adds, 
    page_fan_removes)  = facebook_api_data_load(page_id, start_date, end_date)
    facebook_data_dictionary = {                            
                            'dates': dates,
                            'page_post_engagements':              page_post_engagements,
                            'page_impressions':                   page_impressions,
                            'page_impressions_unique':            page_impressions_unique,
                            'page_fans':                          page_fans,
                            'page_daily_follows_unique':          page_daily_follows_unique,
                            'page_daily_unfollows_unique':        page_daily_unfollows_unique,
                            'page_impressions_organic_unique_v2': page_impressions_organic_unique_v2,
                            'page_impressions_paid ':             page_impressions_paid ,
                            'post_reactions':                     post_reactions ,
                            'page_fan_adds':                      page_fan_adds,
                            'page_fan_removes':                   page_fan_removes,
                        }
    

    # Find the maximum length of the arrays
    max_length = max(len(v) for v in facebook_data_dictionary.values())
    # Pad the shorter arrays with None
    for key in facebook_data_dictionary:
        if len(facebook_data_dictionary[key]) < max_length:
            facebook_data_dictionary[key].extend([None] * (max_length - len(facebook_data_dictionary[key])))



    facebook_dictionary     = pd.DataFrame(facebook_data_dictionary)
    page_fans_country_data  = pd.DataFrame(page_fans_country)
    combine_facebook_data   = pd.concat([facebook_dictionary, 
                                       page_follows, page_views,
                                       page_negative_feedback_unique, page_impressions_viral,
                                       page_fan_adds_by_paid_non_paid_unique,
                                       page_impressions_by_age_gender_unique,
                                       page_fans_country_data], axis=1)
    # INSTAGRAM DATA
    (
    insta_dates, ig_insights_by_total_values, 
    impressions_values, reach_values, 
    profile_views_values, follower_count_values, 
    email_contacts, phone_call_clicks, 
    text_message_clicks, get_directions_clicks, 
    website_clicks
    ) = instagram_data_load(instagram_user_id, access_token, start_date, end_date)
    instagram_data_dictionary_ = {                            
                            'dates':                 insta_dates,
                            'impressions_values':    impressions_values,
                            'reach_values':          reach_values,
                            'profile_views_values':  profile_views_values,
                            'follower_count_values': follower_count_values,
                            'email_contacts':        email_contacts,
                            'phone_call_clicks':     phone_call_clicks,
                            'text_message_clicks':   text_message_clicks,
                            'get_directions_clicks': get_directions_clicks,
                            'website_clicks':        website_clicks,
                        }
    instagram_data_dictionary  = pd.DataFrame(instagram_data_dictionary_)





    def create_excel_file():
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Write each DataFrame to a different worksheet
            combine_facebook_data.to_excel(writer, sheet_name='Facebook', index=False)
            ads_insights.to_excel(writer, sheet_name='Facebook Ads', index=False)
            google_analytics.to_excel(writer, sheet_name='Google Analytics', index=False)
            google_ads_data.to_excel(writer, sheet_name='Google Ads', index=False)
            instagram_data_dictionary.to_excel(writer, sheet_name='Instagram', index=False)
            
            # Access the workbook and worksheets
            workbook  = writer.book
            worksheets = {
                'Facebook': writer.sheets['Facebook'],
                'Facebook Ads': writer.sheets['Facebook Ads'],
                'Google Analytics': writer.sheets['Google Analytics'],
                'Google Ads': writer.sheets['Google Ads'],
                'Instagram': writer.sheets['Instagram'],
            }
            
            # Set the column width for each worksheet
            # Excel column width unit: 1 unit = 1/256th of the width of the zero character
            # Approximate conversion: 300 pixels ≈ 40 Excel column width units
            column_width = 40
            
            for sheet_name, worksheet in worksheets.items():
                if sheet_name == 'Facebook':
                    num_columns = len(combine_facebook_data.columns)
                elif sheet_name == 'Facebook Ads':
                    num_columns = len(ads_insights.columns)
                elif sheet_name == 'Google Analytics':
                    num_columns = len(google_analytics.columns)
                elif sheet_name == 'Google Ads':
                    num_columns = len(google_ads_data.columns)
                elif sheet_name == 'Instagram':
                    num_columns = len(instagram_data_dictionary.columns)
                
                for col_num in range(num_columns):
                    worksheet.set_column(col_num, col_num, column_width)
                    
        output.seek(0)
        return output

    # Sidebar success message and download button
    st.sidebar.success("Data Export Successfully")

    try:
        excel_data = create_excel_file()
        st.sidebar.download_button(label='Click here to download',
                                data=excel_data,
                                file_name='Export_Data.xlsx',
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")



    # def create_excel_file():
    #     output = io.BytesIO()
    #     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    #         combine_facebook_data.to_excel(writer, sheet_name='Facebook', index=False)
    #         ads_insights.to_excel(writer, sheet_name='Facebook Ads', index=False)
    #         google_analytics.to_excel(writer, sheet_name='Google Anaytics', index=False)
    #         google_ads_data.to_excel(writer, sheet_name='Google Ads', index=False)
    #         instagram_data_dictionary.to_excel(writer, sheet_name='Instagram', index=False)
    #     output.seek(0)
    #     return output
    
    # st.sidebar.success("Data Export Successfully")

    # excel_data = create_excel_file()
    # st.sidebar.download_button(label='Click here to download',
    #                    data=excel_data,
    #                    file_name='Export_Data.xlsx',
    #                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


