import streamlit as st
from openai import OpenAI
import re
import pandas as pd
from io import BytesIO
import datetime

def course_match_bot(user_info, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"User Information: {user_info}"
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in providing career choices and please give 1 recommendation"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def my_ambition(ambition_info, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"User Information: {ambition_info}"
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in giving motivation.Please give the 1 suitable career"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def character_bot(character_info, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"User Information: {character_info}"
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant in analysing user character.Please give about 5 scenarios for user to choose if it allign with him or not"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def finalize_character(character_info, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"User Personality: {', '.join(character_info)}"
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant in analysing user Personality based on their answer and give answer what kind of personality user have"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def create_excel_download(user_data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Create DataFrame for basic info
        basic_info = pd.DataFrame([{
            'Timestamp': user_data.get('timestamp', ''),
            'Subject': user_data.get('subject_like', ''),
            'Subject Opinion': user_data.get('like_not', ''),
            'Ambition': user_data.get('ambition', ''),
            'Character Description': user_data.get('character', ''),
            'Introvert/Extrovert': user_data.get('introvert_not', ''),
        }])
        basic_info.to_excel(writer, sheet_name='Basic Information', index=False)
        
        # Create DataFrame for suggestions and responses
        if user_data.get('scenario_responses'):
            scenarios_df = pd.DataFrame(user_data['scenario_responses'])
            scenarios_df.to_excel(writer, sheet_name='Scenario Responses', index=False)
        
        # Create DataFrame for AI recommendations
        recommendations = pd.DataFrame([{
            'Career Suggestions': user_data.get('career_suggestions', ''),
            'Ambition-Based Suggestion': user_data.get('ambition_suggestion', ''),
            'Final Character Analysis': user_data.get('final_character_analysis', '')
        }])
        recommendations.to_excel(writer, sheet_name='AI Recommendations', index=False)
    
    return output.getvalue()

if 'show_ambition' not in st.session_state:
    st.session_state.show_ambition = False
if 'show_character' not in st.session_state:
    st.session_state.show_character = False
if 'show_suggestion' not in st.session_state:
    st.session_state.show_suggestion = False
if 'character_suggestion' not in st.session_state:
    st.session_state.character_suggestion = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'scenario_responses': []
    }
# if 'previous_responses' not in st.session_state:
#     st.session_state.previous_responses = []

# Streamlit application
logo_url = "OIP.jpeg"
col1, col2 = st.columns([3, 1])
with col1:
    st.title("💬 Course Match Bot")
with col2:
    st.image(logo_url, width=100)

# Display previous responses if they exist
# if st.session_state.previous_responses:
#     with st.expander("View Previous Responses", expanded=False):
#         for idx, response in enumerate(st.session_state.previous_responses, 1):
#             st.write(f"### Response {idx}")
#             st.write(f"**Timestamp:** {response['timestamp']}")
#             st.write(f"**Subject:** {response['subject_like']}")
#             st.write(f"**Opinion:** {response['like_not']}")
#             if 'career_suggestions' in response:
#                 st.write("**Career Suggestions:**")
#                 st.write(response['career_suggestions'])
#             if 'ambition' in response:
#                 st.write(f"**Ambition:** {response['ambition']}")
#             if 'ambition_suggestion' in response:
#                 st.write("**Ambition-Based Suggestion:**")
#                 st.write(response['ambition_suggestion'])
#             if 'character' in response:
#                 st.write(f"**Character Description:** {response['character']}")
#                 st.write(f"**Personality Type:** {response['introvert_not']}")
#             if 'scenario_responses' in response:
#                 st.write("**Scenario Responses:**")
#                 for scenario in response['scenario_responses']:
#                     st.write(f"- **Scenario:** {scenario['Scenario']}")
#                     st.write(f"  **Response:** {scenario['Response']}")
#             if 'final_character_analysis' in response:
#                 st.write("**Final Character Analysis:**")
#                 st.write(response['final_character_analysis'])
#             st.markdown("---")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    st.write("Get personalized career suggestions based on your interests and strengths.")

    # First Form - Career Suggestion
    with st.form(key="career_suggestion_form"):
        subject_like = st.text_input("Tell me about yourself. What subject do you like in school and do well?")
        like_not = st.radio("Do you like it?", ["I Like but I don't do well", "I don't like but I do well", "I like and I do well", "I have no interest at all"])
        submit_button = st.form_submit_button(label="Enter")

        if submit_button and subject_like and like_not:
            user_info = f"Subject the user likes: {subject_like}, Do I like the subject?: {like_not}"
            suggestions = course_match_bot(user_info, openai_api_key)
            st.write("Here are some career suggestions for you:")
            st.write(suggestions)
            st.session_state.show_ambition = True
            st.session_state.user_data.update({
                'subject_like': subject_like,
                'like_not': like_not,
                'career_suggestions': suggestions
            })

    # Second Form - Ambition
    if st.session_state.show_ambition:
        with st.form(key="ambition_form"):
            ambition = st.text_input("What are your career ambitions or goals?")
            submit_button_ambition = st.form_submit_button(label="Submit Ambition")

            if submit_button_ambition and ambition:
                ambition_info = f"Type of ambition the user want:{ambition}, The subject the user choose: {st.session_state.user_data['subject_like']}, User Opinion on the subject: {st.session_state.user_data['like_not']}"
                ambi_suggestion = my_ambition(ambition_info, openai_api_key)
                st.write("Based on your ambition this is the new career that we will propose:")
                st.write(ambi_suggestion)
                st.session_state.show_character = True
                st.session_state.user_data.update({
                    'ambition': ambition,
                    'ambition_suggestion': ambi_suggestion
                })

    # Third Form - Character
    if st.session_state.show_character:
        with st.form(key="character_form"):
            character = st.text_input("Can you describe your character")
            introvert_not = st.radio("Are you an introvert or extrovert", ["I am an Introvert", "I am an Extrovert"])
            submit_button_character = st.form_submit_button(label="Submit your character")

            if submit_button_character and character:
                character_info = f"This is what I think my character is like: {character}, I am a {introvert_not}"
                st.session_state.character_suggestion = character_bot(character_info, openai_api_key)
                st.session_state.show_suggestion = True
                st.session_state.user_data.update({
                    'character': character,
                    'introvert_not': introvert_not
                })

    # Fourth Form - Suggestions
    if st.session_state.show_suggestion and st.session_state.character_suggestion:
        with st.form(key="suggestion_form"):
            responses_array = []
            st.write("Based on your character, here are some scenarios for you to consider:")

            suggestions = re.split(r"\d+\.\s", st.session_state.character_suggestion)[1:]
            scenario_responses = []

            for i, suggestion in enumerate(suggestions, start=1):
                st.write(f"{i}. {suggestion}")
                user_response = st.text_input(f"Your thoughts on suggestion {i}:", key=f"suggestion_input_{i}")
                responses_array.append(user_response)
                if user_response:
                    scenario_responses.append({
                        'Scenario': suggestion.strip(),
                        'Response': user_response
                    })

            submit_button_suggestion = st.form_submit_button(label="Submit your answer")

            if submit_button_suggestion and all(responses_array):
                fcharacter_suggestion = finalize_character(responses_array, openai_api_key)
                st.write("Our Opinion:")
                st.write(fcharacter_suggestion)
                
                # Update session state with final data
                st.session_state.user_data.update({
                    'scenario_responses': scenario_responses,
                    'final_character_analysis': fcharacter_suggestion
                })
                
                # Add current response to previous responses
                # st.session_state.previous_responses.append(st.session_state.user_data.copy())
                
                # Set a flag to show the download button
                st.session_state.show_download = True

        # Place the download button outside the form
        if hasattr(st.session_state, 'show_download') and st.session_state.show_download:
            # Create download button for current response
            excel_data = create_excel_download(st.session_state.user_data)
            st.download_button(
                label="Download Current Results as Excel",
                data=excel_data,
                file_name=f"career_assessment_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # # Create download button for all responses
            # if len(st.session_state.previous_responses) > 1:
            #     all_excel_data = create_excel_download({
            #         'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #         'responses': st.session_state.previous_responses
            #     })
            #     st.download_button(
            #         label="Download All Results as Excel",
            #         data=all_excel_data,
            #         file_name=f"all_career_assessments_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            #     )

            # # Add a button to start a new assessment
            # if st.button("Start New Assessment"):
            #     # Reset session state for new assessment
            #     st.session_state.user_data = {
            #         'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #         'scenario_responses': []
            #     }
            #     st.session_state.show_ambition = False
            #     st.session_state.show_character = False
            #     st.session_state.show_suggestion = False
            #     st.session_state.character_suggestion = None
            #     st.session_state.show_download = False
            #     st.experimental_rerun()
