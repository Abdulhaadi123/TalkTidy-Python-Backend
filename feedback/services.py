import os
from groq import Groq
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

load_dotenv()

class GroqService:
    def __init__(self):
        # Initialize Groq client & model
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
  
        # Wrap it in LangChain’s ChatGroq interface
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=self.model
        )
        
        # 👉 Ultra-catchy prompt: emoji-rich, UI-style bullets—no paragraphs
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
You are the 🎤 **Presentation Maestro**! 🥳  
Deliver **emoji-rich**, **one-line**, **sparkling** tips—**no paragraphs**.  
Cover these five pillars:
1. Content clarity & organization  
2. Visual elements & impact  
3. Key message delivery  
4. Audience engagement  
5. Areas for improvement  

Use this format exactly:

🔹 **[Clarity]**: ✨ Crisp headlines  
🎨 **[Visuals]**: 🌈 Bold colors  
🔑 **[Message]**: 💥 Hit the core  
👥 **[Engagement]**: ❓ Ask a question  
🛠️ **[Improve]**: 🚀 Add next step  

• Keep each tip under 8 words  
• End with an action-oriented verb or emoji flair  
"""),
            ("user", "{content}")
        ])
        
        # Build the chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def get_presentation_feedback(self, content: str) -> str:
        """
        Run the chain on the given presentation content.
        Returns ultra-catchy, emoji-driven bullet feedback.
        """
        try:
            return self.chain.run(content=content)
        except Exception as e:
            return f"Error generating feedback: {e}"
