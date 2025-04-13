import streamlit as st
import json
import pandas as pd

col1, col2 = st.columns([1, 8]) 

with col1:
    st.write()
    st.write()
    st.image("json.svg", width=100)  

with col2:
    st.title("JSON Parser")

def json_validator(json_str):
    json_str = json_str.strip()
    if not json_str:
        st.error("Error: JSON is empty")
        return False
    
    if not (json_str.startswith('{') or json_str.startswith('[')):
        st.error("Error: JSON must start with '{' or '['")
        return False
    
    stack = []
    in_string = False
    prev_char = ''
    invalid_symbols = {'@', '#', '$', '%', '^', '&', '*', '!', '~', '|', '\\'}
    arithmetic_operators = {'+', '-', '*', '/'}
    
    for char in json_str:
        if char == '"':
            in_string = not in_string
        elif char in "{[" and not in_string:
            stack.append(char)
        elif char in "}]" and not in_string:
            if not stack:
                st.error("Error: Mismatched brackets")
                return False
            last = stack.pop()
            if (char == "}" and last != "{") or (char == "]" and last != "["):
                st.error("Error: Mismatched brackets")
                return False
        
        if (not in_string) and (char in invalid_symbols):
            st.error(f"Error: Invalid symbol '{char}' in a number value")
            return False
            
        if (not in_string) and (char in arithmetic_operators):
            if char == '-' and prev_char in {':'}:
                continue
            st.error(f"Error: Invalid arithmetic operator '{char}' in JSON value")
            return False

        if prev_char in {':', ','} and char in {':', ','}:
            st.error("Error: Unwanted consecutive colons or commas")
            return False
        prev_char = char
    
    if stack:
        st.error("Error: Unclosed brackets in JSON")
        return False
    
    return True

def json_formatter(json_str):
    if not json_validator(json_str):
        return ""

    spaces = 0
    formatted_json = ""
    in_string = False

    for char in json_str:
        if char == '"':
            in_string = not in_string
        elif char in "{[" and not in_string:
            spaces += 1
            formatted_json += char + "\n" + "    " * spaces
            continue
        elif char in "}]" and not in_string:
            spaces -= 1
            formatted_json += "\n" + "    " * spaces + char
            continue
        elif char == "," and not in_string:
            formatted_json += char + "\n" + "    " * spaces
            continue

        formatted_json += char

    return formatted_json

def json_to_grid(json_str):
    if not json_validator(json_str):
        return
    
    try:
        data = json.loads(json_str)
        
        if isinstance(data, dict):
            array_data = None
            array_key = None
            top_level_data = {}
            
            for key, value in data.items():
                if isinstance(value, list) and value:
                    array_data = value
                    array_key = key
                else:
                    top_level_data[key] = value
            
            if array_data:
                df = pd.DataFrame(array_data)
                for key, value in top_level_data.items():
                    df[key] = value
                st.write(f"Grid for '{array_key}':")
                st.dataframe(df, use_container_width=True)
            else:
                df = pd.DataFrame(list(data.items()), columns=["Key", "Value"])
                st.write("Grid for key-value pairs:")
                st.dataframe(df, use_container_width=True)
        
        elif isinstance(data, list):
            if data:
                df = pd.DataFrame(data)
                st.write("Grid for array:")
                st.dataframe(df, use_container_width=True)
            else:
                st.error("Error: Empty array cannot be converted to grid")
        
        else:
            st.error("Error: JSON must be an object or array for grid display")
        
    except json.JSONDecodeError:
        st.error("Error: Unable to parse JSON for grid display")
    except Exception as e:
        st.error(f"Error creating grid: {str(e)}")

st.markdown("""
    <style>
        body {
            background-color: #1E1E1E;
            color: white;
        }
        .stApp {
            background-color: #1E1E1E;
        }
        .stTextArea>div>textarea {
            background-color: #333;
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            border: none;
            padding: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

st.write("Format, Validate, and Convert your JSON to Grid easily!")

json_input = st.text_area("Paste your JSON here:", height=200)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Format JSON"):
        formatted_json = json_formatter(json_input)
        st.text_area("Formatted JSON:", formatted_json, height=200)

with col2:
    if st.button("Validate JSON"):
        validation_result = json_validator(json_input)
        if validation_result:
            st.success("✅ JSON is valid!")
        else:
            st.error("❌ JSON is invalid. Check for errors.")

with col3:
    if st.button("Convert to Grid"):
        json_to_grid(json_input)

st.write("📌 **How It Works?**")
st.markdown("""
1️⃣ **Paste JSON** into the text area.
2️⃣ Click **Format** to beautify the JSON.
3️⃣ Click **Validate** to check for errors.
4️⃣ Click **Convert to Grid** to see data in grid format.
""")
st.write("")

st.write("🔧 **Why Use This Tool?**")
st.markdown("""
- 🚀 Debug JSON quickly
- 🔍 Ensure correct JSON format
- 📊 Visualize data in interactive grids
- 🎨 Clean and user-friendly interface
""")