# ============================================================================
# FILE: langchain_agents.py
# ============================================================================

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
try:
    from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
except ImportError:
    try:
        from langchain.agents import create_tool_calling_agent
    except ImportError:
        # Fallback: try to import from the main agents module
        try:
            from langchain.agents.tool_calling_agent import create_tool_calling_agent
        except ImportError:
            # Try langchain-classic if available
            try:
                from langchain_classic.agents import create_tool_calling_agent
            except ImportError:
                # If all else fails, we'll use bind_tools approach
                create_tool_calling_agent = None

try:
    from langchain.agents import AgentExecutor
except ImportError:
    try:
        from langchain.agents.agent_executor import AgentExecutor
    except ImportError:
        try:
            from langchain_core.agents import AgentExecutor
        except ImportError:
            # Try langchain-classic if available
            try:
                from langchain_classic.agents import AgentExecutor
            except ImportError:
                raise ImportError(
                    "Could not import AgentExecutor. Please install langchain-classic: "
                    "pip install langchain-classic"
                )
from langchain_core.tools import Tool
from langchain_community.vectorstores import AstraDB
from dotenv import load_dotenv
import os
import json
import ast
import operator

load_dotenv()


# ============================================================================
# CALCULATOR TOOL
# ============================================================================

class Calculator:
    """Calculator tool for basic arithmetic operations"""
    
    @staticmethod
    def evaluate(expression: str) -> str:
        """Evaluate a mathematical expression"""
        try:
            operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
            }
            
            def eval_expr(node):
                if isinstance(node, ast.Num):
                    return node.n
                elif isinstance(node, ast.BinOp):
                    return operators[type(node.op)](
                        eval_expr(node.left), 
                        eval_expr(node.right)
                    )
                elif isinstance(node, ast.UnaryOp):
                    return operators[type(node.op)](eval_expr(node.operand))
                else:
                    raise TypeError(node)
            
            tree = ast.parse(expression, mode="eval")
            result = eval_expr(tree.body)
            formatted_result = f"{result:.6f}".rstrip("0").rstrip(".")
            return formatted_result
            
        except Exception as e:
            return f"Error: {str(e)}"


# Create calculator tool
calculator_tool = Tool(
    name="calculator",
    description="Evaluate basic arithmetic expressions. Input should be a string containing the expression like '4*4*(33/22)+12-20'",
    func=Calculator.evaluate
)


# ============================================================================
# MACRO RECOMMENDATION AGENT
# ============================================================================

class MacroAgent:
    """Agent for generating macro recommendations using Groq"""
    
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",  # Best free Groq model
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_template("""
Based on the following user profile, please calculate the recommended daily intake of protein (in grams), calories, fat (in grams), and carbohydrates (in grams) to achieve their goals. Ensure that the response is in JSON format with no additional explanations or text.

User Profile: {profile}

Goals: {goals}

Output Format:
Return the result in JSON format only, with the keys: "protein", "calories", "fat", and "carbs". Each key should have a numerical value. Do not include any additional text or explanations, only the JSON object.

Example:
{{"protein": 150, "calories": 2500, "fat": 70, "carbs": 300}}

Notes:
Ensure you do not include ```json ``` in the response, simply give me a valid json string with no formatting or display options.
        """)
        
        self.chain = self.prompt | self.llm
    
    def generate_macros(self, profile: dict, goals: list) -> dict:
        """Generate macro recommendations"""
        profile_str = self._dict_to_string(profile)
        goals_str = ", ".join(goals)
        
        response = self.chain.invoke({
            "profile": profile_str,
            "goals": goals_str
        })
        
        # Parse JSON response
        result_text = response.content.strip()
        # Remove markdown code blocks if present
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            # Fallback default values if parsing fails
            return {
                "protein": 150,
                "calories": 2500,
                "fat": 70,
                "carbs": 300
            }
    
    @staticmethod
    def _dict_to_string(obj, level=0):
        """Convert dict to readable string"""
        strings = []
        indent = "  " * level
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    nested = MacroAgent._dict_to_string(value, level + 1)
                    strings.append(f"{indent}{key}: {nested}")
                else:
                    strings.append(f"{indent}{key}: {value}")
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                nested = MacroAgent._dict_to_string(item, level + 1)
                strings.append(f"{indent}Item {idx + 1}: {nested}")
        else:
            strings.append(f"{indent}{obj}")
        
        return ", ".join(strings)


# ============================================================================
# ASK AI MULTI-AGENT SYSTEM
# ============================================================================

class AskAISystem:
    """Multi-agent system with conditional routing using Groq"""
    
    def __init__(self):
        # Initialize LLMs with Groq (FREE!)
        self.router_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.math_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.general_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Initialize vector store (AstraDB)
        self.vectorstore = None
        self._init_vectorstore()
        
        # Router prompt
        self.router_prompt = ChatPromptTemplate.from_template("""
You are a decision-making assistant, and your task is to respond with either "Yes" or "No" only—nothing else.

Here is the input: {question}

If the user is requesting anything that involves math, respond with "Yes."
If the user is asking a general question or making a request that does not involve math, respond with "No."
Your responses should be limited to "Yes" or "No" without any additional details or explanations.
        """)
        
        # Tool calling agent setup
        self._setup_tool_agent()
        
        # General agent prompt with chat history support
        self.general_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a highly experienced personal trainer and dietitian, an expert in health, nutrition, and fitness. You are speaking directly with {user_name}, and you should address them by name throughout the conversation to create a personalized experience.

IMPORTANT: Always use {user_name}'s name when responding. Make your responses feel personal and tailored specifically to them.

Here is {user_name}'s complete profile information:
{profile}

Additional Notes/Facts about {user_name}: {notes}

Remember the conversation history to provide context-aware responses. Always refer to {user_name} by name and use their specific information (age, weight, height, goals, etc.) to give personalized advice."""),
            ("placeholder", "{chat_history}"),
            ("human", "{user_question}"),
        ])
    
    def _init_vectorstore(self):
        """Initialize AstraDB vector store"""
        try:
            self.vectorstore = AstraDB(
                token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
                api_endpoint=os.getenv("ASTRA_ENDPOINT"),
                collection_name="notes",
                embedding=None  # Using Astra Vectorize
            )
        except Exception as e:
            print(f"Warning: Could not initialize vector store: {e}")
    
    def _setup_tool_agent(self):
        """Set up the tool calling agent"""
        tool_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that can use the tools provided to answer questions. You are speaking with {user_name}, and you should address them by name to create a personalized experience.

IMPORTANT: Always use {user_name}'s name when responding. Make your responses feel personal and tailored specifically to them.

Here is {user_name}'s complete profile information:
{profile}

Additional Notes/Facts about {user_name}: {notes}

Use the tools available to help {user_name} with their questions. Always refer to {user_name} by name and incorporate their specific information when providing answers."""),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        if create_tool_calling_agent is not None:
            self.tool_agent = create_tool_calling_agent(
                self.math_llm,
                [calculator_tool],
                tool_prompt
            )
        else:
            # Fallback: try create_react_agent or use LLM with bound tools
            try:
                from langchain.agents import create_react_agent
                from langchain import hub
                try:
                    # Try to use the default react prompt
                    prompt = hub.pull("hwchase17/react")
                except:
                    # Use a simple prompt if hub is not available
                    prompt = tool_prompt
                
                self.tool_agent = create_react_agent(
                    self.math_llm,
                    [calculator_tool],
                    prompt
                )
            except ImportError:
                # Last resort: use LLM with bound tools (simpler approach)
                # This requires a different executor setup
                self.tool_agent = self.math_llm.bind_tools([calculator_tool])
                # Note: This approach may require different executor logic
                raise ImportError(
                    "Could not import create_tool_calling_agent or create_react_agent. "
                    "Please ensure you have a compatible version of langchain installed."
                )
        
        self.tool_executor = AgentExecutor(
            agent=self.tool_agent,
            tools=[calculator_tool],
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=15
        )
    
    def _route_question(self, question: str) -> bool:
        """Route question to determine if it needs math tools"""
        router_chain = self.router_prompt | self.router_llm
        response = router_chain.invoke({"question": question})
        return "yes" in response.content.lower()
    
    def _get_relevant_notes(self, question: str, user_id: int) -> str:
        """Retrieve relevant notes from vector store or database"""
        if not self.vectorstore:
            # Fallback: get notes directly from database
            return self._get_notes_from_db(user_id)
        
        try:
            # Search for relevant notes using vector search
            docs = self.vectorstore.similarity_search(
                question,
                k=4,
                filter={"user_id": user_id}
            )
            
            # Format notes
            notes_text = "\n".join([doc.page_content for doc in docs])
            return notes_text
        except Exception as e:
            print(f"Error retrieving notes from vector store: {e}")
            # Fallback: get notes directly from database
            return self._get_notes_from_db(user_id)
    
    def _get_notes_from_db(self, user_id: int) -> str:
        """Get notes directly from database as fallback"""
        try:
            from db import notes_collection
            notes = list(notes_collection.find({"user_id": {"$eq": user_id}}))
            # Get the most recent notes (limit to 4)
            notes = sorted(notes, key=lambda x: x.get("metadata", {}).get("injested", ""), reverse=True)[:4]
            notes_text = "\n".join([note.get("text", "") for note in notes])
            return notes_text
        except Exception as e:
            print(f"Error retrieving notes from database: {e}")
            return ""
    
    def ask(self, question: str, profile: dict, user_id: int = 1, chat_history: list = None) -> str:
        """Main entry point for asking questions
        
        Args:
            question: User's question
            profile: User profile dictionary
            user_id: User ID
            chat_history: List of tuples in format [("human", "user message"), ("ai", "ai response"), ...]
        """
        if chat_history is None:
            chat_history = []
        
        # Get user's name from profile, default to "there" if not set
        user_name = profile.get("general", {}).get("name", "").strip()
        if not user_name:
            user_name = "there"  # Fallback if name is not set
        
        # Get relevant notes
        notes = self._get_relevant_notes(question, user_id)
        profile_str = MacroAgent._dict_to_string(profile)
        
        # Route the question
        needs_math = self._route_question(question)
        
        if needs_math:
            # Use tool calling agent
            result = self.tool_executor.invoke({
                "input": question,
                "profile": profile_str,
                "notes": notes,
                "chat_history": chat_history,
                "user_name": user_name
            })
            return result["output"]
        else:
            # Use general agent
            general_chain = self.general_prompt | self.general_llm
            response = general_chain.invoke({
                "profile": profile_str,
                "user_question": question,
                "notes": notes,
                "chat_history": chat_history,
                "user_name": user_name
            })
            return response.content
