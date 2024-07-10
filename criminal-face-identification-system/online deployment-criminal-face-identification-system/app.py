import json
import streamlit as st
from datetime import datetime
from utils import *
from mail import send_email

def app():
    
    st.title('criminal-face-identification-system')

    tab1, tab2 = st.columns([1, 1])
    
    with tab1:
        st.header('Report a Missing Criminal here')
        
        name = st.text_input('Enter Name')
        dob = st.date_input('Date of Birth', min_value=datetime(1900, 1, 1), max_value=datetime.now())
        date_of_missing = st.date_input('Select Date of Missing', min_value=datetime(1900, 1, 1), max_value=datetime.now())
        contact_email = st.text_input('Enter E-Mail for contact')
        mobile = st.text_input('Enter Mobile Number (10 digits)', max_chars=10)
        father_name = st.text_input('Enter Father\'s Name')
        mother_name = st.text_input('Enter Mother\'s Name')
        blood_group = st.selectbox('Select Blood Group', ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'Not known'])
        body_mark = st.text_input('Enter Body Mark')
        address = st.text_input('Enter Address')
        up_img = st.file_uploader('Upload the person image', type=['jpg', 'jpeg', 'png'])
        
        if st.button('Add Data'):
            try:
                with open('./database/data/details.json') as json_file:
                    json_decoded = json.load(json_file)

                if up_img is not None:
                    save_dir = f'./database/missing_persons/{name}.png'
                    with open(save_dir, 'wb') as f:
                        f.write(up_img.read())

                    json_decoded[name] = {
                        'dob': str(dob),
                        'date_of_missing': str(date_of_missing),
                        'contact_email': contact_email,
                        'mobile': mobile,
                        'father_name': father_name,
                        'mother_name': mother_name,
                        'blood_group': blood_group,
                        'body_mark': body_mark,
                        'address': address
                    }

                    with open('./database/data/details.json', 'w') as json_file:
                        json.dump(json_decoded, json_file)

                    encode_folder()

                    st.warning('Data Added Successfully')
            except Exception as e:
                st.error(f'Error Adding Data: {str(e)}')
                
    with tab2:
        st.header('Finding a Missing Criminal')
        
        if st.button('Start Camera'):
            try:
                match_status, name = detect()
                name = name.title()
                if match_status:
                    st.warning('Criminal Identified')

                    try:
                        json_file = open('./database/data/details.json')
                        json_obj = json.load(json_file)
                        person_info = json_obj.get(name, {})
                        con_email = person_info.get('contact_email', '')
                        lat, long = get_coordinates()

                        send_email(name, (lat, long), con_email)

                        json_file.close()

                    except Exception as e:
                        st.error(f'Error Sending Email: {str(e)}')
            except Exception as e:
                st.error(f'Error Starting Camera: {str(e)}')

if __name__=='__main__':
    app()


