import os
import shutil
import re
from datetime import datetime
from PyPDF2 import PdfReader
from openpyxl import load_workbook
from docx import Document
import logging
import json
import google.generativeai as genai
import streamlit as st
import threading

# Initialize logging
logging.basicConfig(
    filename="file_organizer.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure Google Gemini API
genai.configure(api_key="YOUR_API_KEY")

def get_file_creation_date(file_path):
    """Get the creation date of a file."""
    creation_date = datetime.fromtimestamp(os.path.getctime(file_path))
    logging.debug(f"File {file_path} creation date: {creation_date}")
    return creation_date

def get_gemini_group(file_names, user_criteria):
    """Use Google Gemini to suggest groupings for files based on their names and criteria."""
    prompt = (
        "Organize the following list of file names into meaningful folder groups based on the provided criteria.\n"
        "Criteria: {criteria}\n"
        "Files: {files}\n\n"
        "Respond in JSON format with folder names as keys and lists of file names as values."
    ).format(criteria=user_criteria, files=', '.join(file_names))

    logging.debug(f"Sending prompt to Gemini API: {prompt}")
    model = genai.GenerativeModel("gemini-1.5-flash")

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            logging.debug(f"Gemini API raw response: {response}")
            raw_text = response.text.strip()

            if raw_text.startswith("```json") and raw_text.endswith("```"):
                raw_text = raw_text[7:-3].strip()

            parsed_response = json.loads(raw_text)
            logging.debug(f"Parsed response JSON: {parsed_response}")
            return parsed_response
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing Gemini response: {e}. Cleaned response text: {raw_text}")
        except Exception as e:
            logging.error(f"Error during Gemini API call: {e}")

        logging.info(f"Retrying Gemini API call ({attempt + 1}/3)...")

    logging.error("Failed to get a valid response from Gemini API after 3 attempts.")
    return {}

def move_file_with_user_assistance(src, dest):
    """Move a file with user assistance if the file is not found or there is an error."""
    while True:
        try:
            shutil.move(src, dest)
            logging.info(f"Moved {src} to {dest}")
            break
        except FileNotFoundError:
            logging.warning(f"File not found: {src}")
            new_path = input(f"File '{src}' not found. Provide the correct path or type 'skip': ")
            if new_path.lower() == 'skip':
                logging.info(f"Skipping file: {src}")
                break
            src = new_path
        except Exception as e:
            logging.error(f"Error moving file {src} to {dest}: {e}")
            break

def organize_files(source_dir, target_dir, user_criteria):
    """Organize files in the source directory based on criteria."""
    logging.info(f"Starting file organization from {source_dir} to {target_dir}")

    file_names = []
    file_paths = {}

    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_names.append(file)
            file_paths[file] = file_path
            logging.debug(f"Found file: {file_path}")

    gemini_groups = get_gemini_group(file_names, user_criteria)

    for folder, grouped_files in gemini_groups.items():
        target_folder = os.path.join(target_dir, folder)
        os.makedirs(target_folder, exist_ok=True)
        logging.info(f"Created directory: {target_folder}")

        for file in grouped_files:
            if file in file_paths:
                src = file_paths[file]
                dest = os.path.join(target_folder, file)
                move_file_with_user_assistance(src, dest)

def main():
    st.title("File Organizer with AI Assistance")
    st.write("Organize your files efficiently with AI-based suggestions.")

    st.info("**Note:** Please paste the full directory paths below. On macOS, open Finder, right-click the folder, hold 'Option' and select 'Copy' as Pathname'.")
    
    source_dir = st.text_input("Source Directory", placeholder="Enter the source directory path")
    target_dir = st.text_input("Target Directory", placeholder="Enter the target directory path")
    user_criteria = st.text_area("Organizational Criteria", placeholder="Define your organizational rules")

    if st.button("Start Organizing"):
        if not source_dir or not target_dir or not user_criteria:
            st.error("Please fill in all fields before starting the organization.")
        else:
            with st.spinner("Organizing files... Please wait."):
                threading.Thread(
                    target=organize_files, 
                    args=(source_dir, target_dir, user_criteria)
                ).start()
            st.success("File organization completed successfully!")

# To run this program, run "streamlit run file_organizer.py"
if __name__ == "__main__":
    logging.info("Starting Streamlit UI for file organization")
    main()
