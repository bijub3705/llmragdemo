import streamlit as st
from langchain.schema import(SystemMessage, HumanMessage, AIMessage)
from llm import query

def init_page() -> None:
  st.set_page_config(
    page_title="History Chatbot"
  )
  st.header("History Chatbot")
  st.sidebar.title("Options")

def init_messages() -> None:
  clear_button = st.sidebar.button("Clear Conversation", key="clear")
  if clear_button or "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages = [
      SystemMessage(
        content="""You are a helpful AI assistant. Reply your answer in based on following information.
        
        The history of the lands that became the United States began with the arrival of the first people in the Americas around 15,000 BC. Numerous indigenous cultures formed, and many saw transformations in the 16th century away from more densely populated lifestyles and towards reorganized polities elsewhere. The European colonization of the Americas began in the late 15th century, although most colonies in what would later become the United States were settled after 1600. By the 1760s, the thirteen British colonies contained 2.5 million people and were established along the Atlantic Coast east of the Appalachian Mountains. The Southern Colonies built an agricultural system on slave labor, enslaving millions from Africa for this purpose. After defeating France, the British government imposed a series of taxes, including the Stamp Act of 1765, rejecting the colonists' constitutional argument that new taxes needed their approval. Resistance to these taxes, especially the Boston Tea Party in 1773, led to Parliament issuing punitive laws designed to end self-government. Armed conflict began in Massachusetts in 1775.
        In 1776, in Philadelphia, the Second Continental Congress declared the independence of the colonies as the United States of America. Led by General George Washington, it won the Revolutionary War. The Paris peace treaty of 1783 established the borders of the new sovereign state. The Articles of Confederation established a central government, but it was ineffectual at providing stability as it could not collect taxes and had no executive officer. A convention wrote a new Constitution that was adopted in 1789 and a Bill of Rights was added in 1791 to guarantee inalienable rights. With Washington as the first president and Alexander Hamilton his chief adviser, a strong central government was created. Purchase of the Louisiana Territory from France in 1803 doubled the size of the United States.
        Encouraged by the notion of manifest destiny, the United States expanded to the Pacific Coast. While the nation was large in terms of area, its population in 1790 was only four million. Westward expansion was driven by a quest for inexpensive land for yeoman farmers and slave owners. The expansion of slavery was increasingly controversial and fueled political and constitutional battles, which were resolved by compromises. Slavery was abolished in all states north of the Mason–Dixon line by 1804, but states in the south continued the institution, to support the kinds of large scale agriculture that dominated the southern economy. Precipitated by the election of Abraham Lincoln as president in 1860, the Civil War began as the southern states seceded from the Union to form their own pro-slavery country, the Confederate States of America. The defeat of the Confederates in 1865 led to the abolition of slavery. In the Reconstruction era following the war, legal and voting rights were extended to freed male slaves. The national government emerged much stronger, and gained explicit duty to protect individual rights. However, when white southern Democrats regained their political power in the South in 1877, often by paramilitary suppression of voting, they passed Jim Crow laws to maintain white supremacy, as well as new state constitutions that legalized discrimination based on race and prevented most African Americans from participating in public life.
        The United States became the world's leading industrial power at the turn of the 20th century, due to an outburst of entrepreneurship and industrialization and the arrival of millions of immigrant workers and farmers. A national railroad network was completed and large-scale mines and factories were established. Mass dissatisfaction with corruption, inefficiency, and traditional politics stimulated the Progressive movement, from the 1890s to the 1920s, leading to reforms, including the federal income tax, direct election of Senators, granting of citizenship to many indigenous people, alcohol prohibition, and women's suffrage. Initially neutral during World War I, the United States declared war on Germany in 1917 and funded the Allied victory the following year. After the prosperous Roaring Twenties, the Wall Street Crash of 1929 marked the onset of the decade-long worldwide Great Depression. President Franklin D. Roosevelt implemented his New Deal programs, including relief for the unemployed, support for farmers, social security, and a minimum wage. The New Deal defined modern American liberalism.[1] Following the Japanese attack on Pearl Harbor, the United States entered World War II and financed the Allied war effort, and helped defeat Nazi Germany and Fascist Italy in the European theater. Its involvement culminated in using newly invented American nuclear weapons on Hiroshima and Nagasaki to defeat Imperial Japan in the Pacific War.
        The United States and the Soviet Union emerged as rival superpowers in the aftermath of World War II. During the Cold War, the two countries confronted each other indirectly in the arms race, the Space Race, propaganda campaigns, and proxy wars. In the 1960s, in large part due to the strength of the civil rights movement, another wave of social reforms was enacted which enforced the constitutional rights of voting and freedom of movement to African Americans. In the 1980s, Ronald Reagan's presidency realigned American politics towards reductions in taxes and regulations. The Cold War ended when the Soviet Union was dissolved in 1991, leaving the United States as the world's sole superpower. Foreign policy after the Cold War has often focused on many conflicts in the Middle East, especially after the September 11 attacks. Early in the 21st century, the United States experienced the Great Recession and the COVID-19 pandemic, which had a negative effect on communities.
        
        """
      )
    ]

def get_answer(prompt) -> str:
  return query(prompt)

def get_current_prompt()-> None:
    prompt = ""
    messages = st.session_state.get("messages", [])
    for message in messages: 
        if isinstance(message, SystemMessage):
            prompt += message.content
            prompt += "\n"
        elif isinstance(message, AIMessage):
            prompt += "Answer :" +message.content
            prompt += "\n"
        elif isinstance(message, HumanMessage):
            prompt += "Question :" +message.content
            prompt += "\n"
    return prompt

def main() -> None:
  init_page()
  init_messages()

  if user_input := st.chat_input("Input your history question!"):
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.spinner("Bot is typing ..."):
      updated_prompt = get_current_prompt()
      answer = get_answer(updated_prompt)
      print(answer)
    st.session_state.messages.append(AIMessage(content=answer))

    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
             with st.chat_message("user"):
                st.markdown(message.content)

if __name__ == "__main__":
  main()