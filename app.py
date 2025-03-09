import fitz  # PyMuPDF
import chromadb
import base64
import io
import streamlit as st
from openai import OpenAI

# OpenAI API key (Set this properly in your environment)
client = OpenAI()

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
try:
    chroma_client.delete_collection(name="pdf_content")
except:
    pass
collection = chroma_client.create_collection(name="pdf_content")



def encode_image(image):
    """Convert image to base64 for OpenAI Vision API."""
    return base64.b64encode(image.getvalue()).decode()


def describe_image(image):
    """Send image to OpenAI GPT-4o-Mini for description."""
    base64_image = encode_image(image)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Describe the attached image in JSON format."},
            {"role": "user", "content": [{"type": "image", "image": base64_image}]}
        ],
    )
    return response["choices"][0]["message"]["content"]


def parse_pdf(pdf_path):
    """Extract text and replace images with descriptions in-line."""
    doc = fitz.open(pdf_path)
    parsed_content = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")  # Extract text blocks (for positioning)
        images = page.get_images(full=True)  # Get images

        content_blocks = []  # To store ordered content (text + images)

        # Process text blocks first
        for block in blocks:
            block_text = block[4].strip()
            if block_text:
                content_blocks.append((block[1], "text", block_text))  # (y-position, type, content)

        # Process images
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = io.BytesIO(image_bytes)

            # Get image description
            description = describe_image(image)
            content_blocks.append((img[1], "image", f"[Page: {page_num+1}, Image {img_index+1}]: {description}"))

        # Sort all content (text + images) by y-coordinate to maintain order
        content_blocks.sort(key=lambda x: x[0])

        # Construct final content with images in correct places
        for block in content_blocks:
            parsed_content.append(block[2])
    return parsed_content


def store_in_vector_db(doc_id, content):
    """Store parsed content in ChromaDB."""
    collection.add(documents=content, ids=[f"{doc_id}_{i}" for i in range(len(content))])


def query_vector_db(query_text):
    """Query ChromaDB for relevant content."""
    results = collection.query(query_texts=[query_text], n_results=10)
    return results["documents"]





# Streamlit UI
st.title("📚 PDF Query System with ChromaDB & GPT-4o")
st.sidebar.header("Upload and Process PDF")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    # Save uploaded file
    pdf_path = f"./uploaded_{uploaded_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Parse and Index PDF
    st.sidebar.success("Processing PDF... This may take a while.")
    parsed_content = parse_pdf(pdf_path)
    store_in_vector_db(uploaded_file.name, parsed_content)
    st.sidebar.success("PDF Indexed Successfully!")

# Query input
query = st.text_input("🔎 Enter your query:")
if query:
    results = query_vector_db(query)
    st.subheader("🔍 Search Results:")
    for res in results:
        st.write(res)
