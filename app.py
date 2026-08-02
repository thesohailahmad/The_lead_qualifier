import streamlit as st
import csv
import io
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv

# Load your API keys securely
load_dotenv()

# --- UI SETUP ---
st.title("🚀 The Lead Qualifier Agent")
st.write("Upload a CSV file containing an 'email' column. The AI will research each company and qualify them based on your strict criteria.")

# File Uploader
uploaded_file = st.file_uploader("Upload your leads.csv file", type=["csv"])

# This block runs when the user clicks the button
if st.button("Qualify Leads"):
    
    if uploaded_file is not None:
        
        # Display a loading spinner while the AI sets up
        with st.spinner("Initializing AI and processing leads. This might take a minute..."):
            
            # 1. SETUP THE AI
            model = init_chat_model(model="gemini-3.5-flash", model_provider="google_genai", temperature=0.0)
            search_tool = TavilySearch(max_results=1)
            
            agent = create_agent(
                model=model,
                tools=[search_tool],
                system_prompt=(
                    "You are a strict lead qualifier. Use the search tool to find out what the company does. "
                    "We ONLY want to sell to Software or Technology companies. "
                    "Respond strictly with 'YES' or 'NO', followed by a one-sentence reason."
                )
            )

            # 2. READ THE UPLOADED FILE
            # Decode the uploaded web file into text that the csv library can read
            decoded_file = uploaded_file.getvalue().decode("utf-8").splitlines()
            reader = csv.reader(decoded_file)
            
            # Skip the header row
            next(reader) 
            
            # We will store the successful "YES" leads in this list
            qualified_leads = []
            
            # Create an empty placeholder on the webpage to show live updates
            progress_text = st.empty()
            
            # 3. LOOP THROUGH THE LEADS
            for row in reader:
                # Skip empty rows if any exist
                if not row: 
                    continue
                
                email = row[0]
                
                # Extract the company name safely
                email_parts = email.split('@')
                if len(email_parts) < 2:
                    continue  # Skip if it's not a valid email format
                    
                domain = email_parts[1]
                domain_parts = domain.split('.')
                company_name = domain_parts[0]
                
                # Update the webpage to show which company is currently being researched
                progress_text.write(f"🔍 Evaluating: **{company_name}**...")
                
                # Ask the AI
                question = HumanMessage(content=f"Search for {company_name} and qualify them.")
                response = agent.invoke({"messages": [question]})
                
                # Clean the output
                raw_content = response['messages'][-1].content
                if type(raw_content) == list:
                    clean_decision = raw_content[0]['text']
                else:
                    clean_decision = raw_content
                    
                # 4. FILTER AND DISPLAY LIVE RESULTS
                if "YES" in clean_decision:
                    # st.success creates a nice green box on the web page
                    st.success(f"✅ **{company_name}** ({email})\n\n{clean_decision}")
                    qualified_leads.append([email, company_name, clean_decision])
                else:
                    # st.warning creates a yellow box for unqualified leads
                    st.warning(f"❌ **{company_name}** ({email})\n\n{clean_decision}")

            # Clear the loading text when finished
            progress_text.write("✨ **Evaluation Complete!**")
            
            # 5. CREATE THE DOWNLOAD BUTTON
            if len(qualified_leads) > 0:
                st.subheader("🎉 Your Qualified Leads are Ready!")
                
                # Instead of writing to a local file, we write to computer memory (io.StringIO)
                # so the web browser can download it securely.
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["Email", "Company", "Decision"])
                writer.writerows(qualified_leads)
                csv_data = output.getvalue()
                
                # Streamlit's built-in download button creates the CSV file for the user
                st.download_button(
                    label="⬇️ Download Qualified Leads (CSV)",
                    data=csv_data,
                    file_name="qualified_leads.csv",
                    mime="text/csv"
                )
            else:
                st.info("No qualified leads were found in this batch.")
                
    else:
        st.error("Please upload a CSV file before clicking the button.")