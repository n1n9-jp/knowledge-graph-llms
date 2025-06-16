# Import necessary modules
import streamlit as st
import streamlit.components.v1 as components  # For embedding custom HTML
from generate_knowledge_graph import generate_knowledge_graph, generate_csv_data
import pandas as pd

# Set up Streamlit page configuration
st.set_page_config(
    page_icon=None, 
    layout="wide",  # Use wide layout for better graph display
    initial_sidebar_state="auto", 
    menu_items=None
)

# Set the title of the app
st.title("Knowledge Graph From Text")

# Sidebar section for user input method
st.sidebar.title("Input document")
input_method = st.sidebar.radio(
    "Choose an input method:",
    ["Upload txt", "Input text"],  # Options for uploading a file or manually inputting text
)

# Case 1: User chooses to upload a .txt file
if input_method == "Upload txt":
    # File uploader widget in the sidebar
    uploaded_file = st.sidebar.file_uploader(label="Upload file", type=["txt"])
    
    if uploaded_file is not None:
        # Read the uploaded file content and decode it as UTF-8 text
        text = uploaded_file.read().decode("utf-8")
 
        # Button to generate the knowledge graph
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                # Call the function to generate the graph from the text
                net, graph_documents = generate_knowledge_graph(text)
                st.success("Knowledge graph generated successfully!")
                
                # Store graph documents in session state for CSV download
                st.session_state['graph_documents'] = graph_documents
                
                # Save the graph to an HTML file
                output_file = "knowledge_graph.html"
                net.save_graph(output_file) 

                # Store graph HTML content in session state
                HtmlFile = open(output_file, 'r', encoding='utf-8')
                graph_html = HtmlFile.read()
                st.session_state['graph_html'] = graph_html
                HtmlFile.close()
                
                # Display the graph
                components.html(graph_html, height=1000)
                
        # Add CSV download buttons if graph has been generated
        if 'graph_documents' in st.session_state:
            st.sidebar.markdown("---")
            st.sidebar.subheader("Download Graph Data")
            
            nodes_csv, edges_csv = generate_csv_data(st.session_state['graph_documents'])
            
            col1, col2 = st.sidebar.columns(2)
            with col1:
                st.download_button(
                    label="📊 Points CSV",
                    data=nodes_csv,
                    file_name="points.csv",
                    mime="text/csv",
                    key="download_nodes_1"
                )
            with col2:
                st.download_button(
                    label="🔗 Links CSV",
                    data=edges_csv,
                    file_name="links.csv",
                    mime="text/csv",
                    key="download_edges_1"
                )
            
            # Re-display the graph if it exists in session state
            if 'graph_html' in st.session_state:
                components.html(st.session_state['graph_html'], height=1000)

# Case 2: User chooses to directly input text
else:
    # Text area for manual input
    text = st.sidebar.text_area("Input text", height=300)

    if text:  # Check if the text area is not empty
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                # Call the function to generate the graph from the input text
                net, graph_documents = generate_knowledge_graph(text)
                st.success("Knowledge graph generated successfully!")
                
                # Store graph documents in session state for CSV download
                st.session_state['graph_documents'] = graph_documents
                
                # Save the graph to an HTML file
                output_file = "knowledge_graph.html"
                net.save_graph(output_file) 

                # Store graph HTML content in session state
                HtmlFile = open(output_file, 'r', encoding='utf-8')
                graph_html = HtmlFile.read()
                st.session_state['graph_html'] = graph_html
                HtmlFile.close()
                
                # Display the graph
                components.html(graph_html, height=1000)
                
        # Add CSV download buttons if graph has been generated
        if 'graph_documents' in st.session_state:
            st.sidebar.markdown("---")
            st.sidebar.subheader("Download Graph Data")
            
            nodes_csv, edges_csv = generate_csv_data(st.session_state['graph_documents'])
            
            col1, col2 = st.sidebar.columns(2)
            with col1:
                st.download_button(
                    label="📊 Points CSV",
                    data=nodes_csv,
                    file_name="points.csv",
                    mime="text/csv",
                    key="download_nodes_2"
                )
            with col2:
                st.download_button(
                    label="🔗 Links CSV",
                    data=edges_csv,
                    file_name="links.csv",
                    mime="text/csv",
                    key="download_edges_2"
                )
            
            # Re-display the graph if it exists in session state
            if 'graph_html' in st.session_state:
                components.html(st.session_state['graph_html'], height=1000)