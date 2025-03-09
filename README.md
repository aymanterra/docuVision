# docuVision
Document with images querying

---

### **📄 PDF Vision Query**  
**AI-powered PDF parser and search tool using GPT-4o & ChromaDB**  

---

## **📝 About the Project**  
📚 **PDF Vision Query** is a tool that:  
✅ Parses PDFs to extract text & detect images  
✅ Uses **GPT-4o** to generate descriptions for images  
✅ Stores processed content in **ChromaDB** (vector database)  
✅ Allows users to **query** the indexed content via a **Streamlit UI**  

🔍 **Use Case**: Quickly search and retrieve insights from PDFs, even if they contain images.  

---

## **🚀 Installation**  
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/aymanterra/docuVision.git
cd docuVision
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```
(Ensure you have **Python 3.8+** installed)

### **3️⃣ Store OpenAI API Key Securely**
Instead of using `.env`, store your API key in Streamlit’s **secrets manager**:

1. **Create a secrets file**:
   ```bash
   mkdir -p .streamlit && touch .streamlit/secrets.toml
   ```

2. **Edit `.streamlit/secrets.toml`** and add:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key"
   ```

Or set it as an environment variable:  
```bash
export OPENAI_API_KEY=your_openai_api_key
```

---

## **▶️ How to Run**
### **1️⃣ Start the Streamlit App**
```bash
streamlit run app.py
```

### **2️⃣ Upload a PDF**
- Click **Browse files** on the sidebar  
- Select a **PDF file** to process  
- Wait for **parsing & indexing** to complete  

### **3️⃣ Query the Document**
- Enter your **question** in the search box  
- View AI-powered **search results**  

---

## **🛠 Features**
✅ **AI-Powered Image Descriptions** – Uses GPT-4o to describe images  
✅ **Full-Text Search** – Retrieve PDF content instantly  
✅ **Vector Database** – Stores data efficiently in **ChromaDB**  
✅ **User-Friendly UI** – Query via a **Streamlit** interface  
