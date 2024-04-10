import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified pastiche

    Here are some examples different Tones:
    - Formal: In the grand tapestry of literary imagination, there exists a tale that transcends the mundane confines of everyday existence, weaving threads of mystery, adventure, and profound insight. Set against the backdrop of an enchanting realm, this narrative unfurls with meticulous detail, inviting readers into a realm where the ordinary gives way to the extraordinary. Within these pages, characters of depth and complexity navigate the tumultuous waters of fate, their destinies intertwined in a delicate dance of circumstance and choice. As the story unfolds, themes of love, loss, and redemption emerge, resonating with universal truths that echo across time and space. Through masterful prose and evocative imagery, the author deftly guides the reader on a journey of discovery, illuminating the human condition with a brilliance that captivates the soul. Thus, in the annals of literature, this fictional saga stands as a testament to the enduring power of storytelling to inspire, enlighten, and enrich the lives of those who dare to embark upon its wondrous voyage.
    - Informal: Picture this: there's this amazing story that's like nothing you've ever read before. It's set in this totally magical place, and every little detail just sucks you right in. You've got these characters who are super real, dealing with all kinds of crazy stuff that life throws at them. Love, heartbreak, redemption – it's all there, hitting you right in the feels. And the way it's written, it's like the author's just grabbing your hand and taking you on this wild ride. It's one of those stories that sticks with you long after you've finished reading, reminding you of all the ups and downs of being human. Man, talk about a page-turner!  

    Example Sentences from each pastiche:
    - Sherlock Holmes: In the expansive repertoire of literary exploits, there resides a narrative that surpasses the pedestrian bounds of ordinary tales, weaving a tapestry of intrigue, adventure, and profound deduction. Set against the backdrop of a mesmerizing realm, this chronicle unfolds with meticulous precision, beckoning readers into a world where the commonplace yields to the extraordinary. Amidst its pages, characters of intricate depth and complexity traverse the treacherous pathways of destiny, their fates intricately intertwined in a delicate ballet of circumstance and choice. As the saga unfolds, themes of love, loss, and redemption emerge, resonating with universal truths that echo throughout time and space. Through the masterful arrangement of words and vivid imagery, the author deftly guides the reader on a journey of enlightenment, illuminating the intricacies of the human condition with a brilliance that captures the intellect. Thus, within the annals of literature, this tale stands as a testament to the enduring power of narrative to captivate, inspire, and elevate those who dare to embark upon its enigmatic odyssey.
    - Jar-Jar Binks: Meesa got dis here story for yousa, okeyday? Issa like, totally unlike anythin' yousa ever read befo'. Set in dis here magical place, it is, where every lil' ting jus' grabs yousa attention real good. Yousa got these characters, all real-like, dealin' with all sortsa crazy stuff life throws at them. Love, heartbreak, redemption, yousa name it - it's all dere, hittin' yousa right in da feels. And da way it's written, it's like da author's just takin' yousa by da hand and takin' yousa on dis wild, wild ride. It's one of dose stories that sticks wit yousa, long after yousa finished readin' it, remindin' yousa of all da ups and downs of bein' a Gungan. Mesa tellin' yousa, it's a real page-turner, okeyday!

    
    Below is the draft text, tone, and pastiche:
    DRAFT: {draft}
    TONE: {tone}
    PASTICHE: {pastiche}

    YOUR {pastiche} RESPONSE:
"""

#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["tone", "pastiche", "draft"],
    template=template,
)


#LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm


#Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Re-write your text as different characters.")

with col2:
    st.write("This is Kobus Kunz's first AI project")


#Input OpenAI API Key
st.markdown("## Enter Your OpenAI API Key")

def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()


# Input
st.markdown("## Enter the text you want to re-write")

# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_pastiche = st.selectbox(
        'Which pastiche would you like?',
        ('Sherlock Holmes', 'Jar-Jar Binks'))
    
def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()


    
    
# Output
st.markdown("### Your Re-written text:")

if draft_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_draft = prompt.format(
        tone=option_tone, 
        pastiche=option_pastiche, 
        draft=draft_input
    )

    improved_redaction = llm(prompt_with_draft)

    st.write(improved_redaction)