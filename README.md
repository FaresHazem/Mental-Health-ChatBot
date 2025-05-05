# Retrieval-Augmented Generation (RAG) Chatbot 🚀

## Project Overview 📚
This project implements a Retrieval-Augmented Generation (RAG) chatbot designed to answer user questions using information from real-world websites and documents in the domain of **mental health**. The chatbot combines document retrieval with a generative model to provide accurate and context-aware responses. Unlike existing frameworks like LangChain, this project is built from scratch to demonstrate a deeper understanding of the RAG architecture.

## Project Presentation 🎥

You can view the project presentation here: [Mental Health Chatbot Presentation (Canva)](https://www.canva.com/design/DAGmk_75QPE/vLpF77pP7h-MCkuCiPbKMw/view?utm_content=DAGmk_75QPE&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h6cf34f083a)

## Project Goal 🎯
The goal of this project is to create a chatbot that:
- 🧠 Collects and understands domain-specific content.
- 🔍 Retrieves relevant information for a user’s question.
- ✍️ Uses a language model to generate informative responses.

## Chosen Topic and Use Case 💡

The chosen topic for this project is **Mental Health**, and the use case is to provide a chatbot that answers questions related to mental health topics such as anxiety, depression, and available treatments. This chatbot aims to raise awareness and provide accessible, reliable information to users in need.

## Project Phases 🛠️

### Phase 1: Choose a Domain and Use Case 🌐
- **Domain**: Mental Health
- **Use Case**: The chatbot answers questions related to mental health topics, such as anxiety, depression, and available treatments. This is valuable for raising awareness and providing accessible information to users.

### Phase 2: Collect Data 📄
- **Description**: Reliable websites and documents about mental health were scraped using tools like `trafilatura`.
- **Output**: A `.csv` file containing over 20,000 words of content.

### Phase 3: Preprocess and Chunk the Text ✂️
- **Description**: The collected text was cleaned to remove HTML, punctuation, and irrelevant content. It was then split into smaller chunks of 200–500 words for efficient processing.
- **Output**: A cleaned and chunked dataset ready for embedding.

### Phase 4: Embed the Chunks 🧩
- **Description**: A sentence embedding model (`all-MiniLM-L6-v2`) was used to convert text chunks into numerical vectors, enabling semantic understanding.
- **Output**: A set of vector representations for the text chunks.

### Phase 5: Create a Vector Store 🗂️
- **Description**: The vectors were stored in a FAISS index, allowing efficient retrieval of the most relevant chunks for a given query.
- **Output**: A searchable FAISS index containing the embedded content.

### Phase 6: Build the RAG System 🤖
- **Description**: The system accepts a user question, embeds it, retrieves the top 3–5 most relevant text chunks, and passes them along with the question to a language model to generate an answer.
- **Output**: A script that processes user questions and returns context-aware answers.

### Phase 7: Build a Chat Interface (Bonus) 💬
- **Description**: A user-friendly interface was created using `Streamlit`, allowing users to interact with the chatbot by typing questions and receiving responses.
- **Output**: A fully functional chatbot interface.

## Project Structure 🗃️
```
data/
	chunk_metadata.csv
	cleaned_chunk_metadata.csv
	cleaned_chunked_data.csv
	mental_health_data.csv
Embeddings/
	embeddings.npy
models/
	mental_health_index.faiss
scripts/
	1) Collect_Data.py
	2) Preprocess_and_Chunk_the_Text.py
	3) Embed_the_Chunks.py
	4) Create_a_Vector_Store.py
	5) Clean_and_Save_the_Data.py
	6) Build_the_RAG_System.py
	7) Build_Chat_Interface.py
```

## How to Run the Project 🏃‍♂️
1. **Setup**:
   - Install the required Python libraries: `pip install -r requirements.txt`.
   - Ensure the `data`, `models`, and `Embeddings` directories are populated as described above.

2. **Run the Scripts**:
   - Execute the scripts in the `scripts/` directory sequentially to build the chatbot.

3. **Launch the Interface**:
   - Run `7) Build_Chat_Interface.py` using `streamlit run "scripts/7) Build_Chat_Interface.py"`.

## Key Features ✨
- **Custom RAG Implementation**: Built without relying on external frameworks like LangChain.
- **Domain-Specific Knowledge**: Focused on mental health to provide accurate and helpful responses.
- **Efficient Retrieval**: Uses FAISS for fast and accurate vector-based search.
- **User-Friendly Interface**: Streamlit-based interface for seamless interaction.

## Future Enhancements 🔮
- Expand the dataset to include more diverse mental health topics.
- Integrate additional language models for improved response quality.
- Add multilingual support to reach a broader audience.

## Test Report 🧪

The project includes a `Test_Report.md` file, which contains a detailed test report with sample questions and the chatbot's responses. This report demonstrates the chatbot's capabilities and provides insights into its functionality. It serves as a reference for understanding how the chatbot handles various queries related to mental health.

## Team Members 👥
- Fares Hazem (ID: 20221443356)
- Ali Ashraf (ID: 2103106)
- Ahmed Dawood (ID: 20221454408)
- Ahmed Yousri (ID: 2103108)
- Khalid Mansour (ID: 20221320444)