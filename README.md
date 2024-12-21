# 📂 AI-Powered File Organizer

## 🚀 **Why I Made This**
Managing and organizing files manually can be a tedious and time-consuming task, especially when dealing with a large number of files with varying formats, names, and purposes. Traditional manual organization often results in cluttered directories, misplaced files, and wasted productivity. This project aims to address this problem by leveraging AI to intelligently analyze file names, metadata, and user criteria to organize files efficiently into logical groups.

---

## 🤖 **Project Overview**
This project provides an AI-powered file organization tool that uses Google's Gemini 1.5 flash model to suggest folder groupings based on user-defined criteria and file metadata. The project features a user-friendly web interface powered by **Streamlit**, where users can specify:

- **Source Directory:** Where the files are currently stored.
- **Target Directory:** Where the organized files will be moved.
- **Organizational Criteria:** Custom rules for organizing files, such as grouping by file type, date, or specific keywords.

The AI processes the given criteria and generates folder structures and file mappings, which are then executed automatically.

---

## 🛠️ **How to Test the Project**

Follow these steps to set up and test the project locally:

### **1. Clone the Repository**
```bash
git clone https://github.com/micah1crandell/ai-file-organizer.git
cd your-repo
```

### **2. Install Dependencies**
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### **3. Setup Gemini API Key**
Replace `YOUR_API_KEY` in the code with your valid Gemini API key.

### **4. Start the Streamlit App**
```bash
streamlit run file_organizer.py
```

### **5. Test the Application**
- The repository includes two directories:
  - **SourceDirectory:** Pre-filled with sample files.
  - **TargetDirectory:** Destination for organized files.

- In the Streamlit app:
   1. Enter the full paths of `SourceDirectory` and `TargetDirectory`.
   2. Define your organizational criteria (e.g., group by file type, date, or keywords).
   3. Click **Start Organizing**.

The application will process the files based on your criteria and organize them into the `TargetDirectory`.

---

## 🧠 **Example Organizational Criteria**
- "Group all financial documents into a `Finance` folder."
- "Place all images into an `Images` folder."

The AI will process these rules and intelligently categorize files.

---

## 📑 **Technologies Used**
- **Python**
- **Streamlit** (UI Framework)
- **Google Gemini API**
- **PyPDF2**, **openpyxl**, **python-docx** (File Parsing Libraries)

---

## 🤝 **Contributing**
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

## 📜 **License**
This project is licensed under the MIT License.

---

## 📝 **Acknowledgements**
- Google for the Gemini API.
- Streamlit for the powerful and easy-to-use UI framework.

---

Feel free to open an issue or discussion for any questions or improvements!

