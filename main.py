import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Access the API key (ollama does not need)
groq_api_key = os.getenv("GROQ_API_KEY")

### Models
#Groq 8B model
groq_llama8b_llm = ChatGroq(
    temperature = 0,
    model_name = 'llama3-8b-8192',
    api_key = groq_api_key
)
#Groq 70B model
groq_llama70b_llm = ChatGroq(
    temperature = 0,
    model_name = 'llama3-70b-8192',
    api_key = groq_api_key
)


##### Input #######

user_prompt = input("Enter coding task:")

############# AGENTS #################
# 1
rewriter = Agent(
    role = "Task Refinement Specialist",
    goal = """My aim is to enhance the sophistication and detail of prompts without expanding into new subject areas.
    I will assist in refining the language and depth of inquiry while maintaining the original focus. I will never do anything else than refine the user input.
    I wont try to find any solutions to tasks. I wont start coding.""",
    backstory = "I am well experienced to articulate and rewrite prompts.",
    llm = groq_llama8b_llm,
    verbose = True,
    allow_delegation = False
)
# 2
project_planner = Agent(
    role = "System Designer",
    goal = "My job is to make a comprehensive plan for the task at hand. I will find the most effective solution for the coding tasks. I will never write the code.",
    backstory = "I am a skilled project planner, blends coding prowess with strategic thinking, excelling in crafting meticulous plans for diverse tech projects.",
    llm = groq_llama8b_llm,
    verbose = True,
    allow_delegation = False
)
# 3
plan_critic = Agent(
    role = "Quality Assurance Auditor",
    goal = "My primary goal is to meticulously scrutinize project plans, seeking out any inaccuracies, inconsistencies, or potential pitfalls. With a keen eye for detail and a sharp analytical mind, I aim to identify and pinpoint flaws within the plan, offering constructive criticism to ensure its accuracy, feasibility, and effectiveness. By challenging assumptions and highlighting areas of concern, I play a crucial role in driving refinement and improvement, ultimately contributing to the project's success",
    backstory = "I am a perceptive project critic with a knack for pinpointing flaws in plans. With a sharp eye for detail, I meticulously evaluate project strategies, offering insightful critiques to drive improvement.",
    llm = groq_llama8b_llm,
    verbose = True,
    allow_delegation = False
)
# 4
senior_coder = Agent(
    role = "Senior Coding Architect",
    goal = "I aims to meticulously translate project plans into flawless code implementations, ensuring the seamless execution of complex technical solutions.",
    backstory = "My journey into the world of coding began at a young age, fueled by a fascination with technology and a natural aptitude for problem-solving. As I delved deeper into the realm of computer science, I quickly distinguished himself as a prodigious talent, earning recognition for his exceptional coding skills and meticulous attention to detail.",
    llm = groq_llama8b_llm,
    verbose = True,
    allow_delegation = False
)
# 5
coder_critic = Agent(
    role = "Code Review Specialist",
    goal = "My primary goal is to meticulously scrutinize project plans, seeking out any inaccuracies, inconsistencies, or potential pitfalls. With a keen eye for detail and a sharp analytical mind, I aim to identify and pinpoint flaws within the plan, offering constructive criticism to ensure its accuracy, feasibility, and effectiveness. By challenging assumptions and highlighting areas of concern, I play a crucial role in driving refinement and improvement, ultimately contributing to the project's success",
    backstory = "I am a perceptive project critic with a knack for pinpointing flaws in plans. With a sharp eye for detail, I meticulously evaluate project strategies, offering insightful critiques to drive improvement.",
    llm = groq_llama8b_llm,
    verbose = True,
    allow_delegation = False
)
# 6
summarize_agent = Agent(
    role = "Content Summarization Specialist",
    goal = "To provide concise and accurate summaries of code and project plans, ensuring key details are communicated effectively.",
    backstory = "As software projects grow in complexity, there is a need for clear and concise communication of codebases and project plans. The rise of agile methodologies and distributed teams further emphasizes the importance of efficient communication. This agent was developed to meet the demand for summarizing technical content, bridging the gap between detailed documentation and high-level overviews.",
    llm = groq_llama8b_llm,
    verbose = True,
    allow_delegation = False
)

############# TASKS #################

rewrite_user_prompt = Task(
    description = f"Rewrite the query: {user_prompt}",
    agent = rewriter,
    expected_output = "Rewrite the user prompt and find the core question what is asked. Never change the topic."
)

project_plan = Task(
    description = f"Find the best plan for the task based on the query: {rewrite_user_prompt}",
    agent = project_planner, 
    expected_output = "Find the best plan for the task."
)

project_plan_critic = Task(
    description = f"""Find the flaws and bugs from the given project plan. Pinpoint the failures and give as an output what should be changed to improve the structure.
    Ask myself a question can this be done better. Here is the given code for the task: {project_plan}""",
    agent = plan_critic, 
    expected_output = "Find the best coding plan for the task."
)

project_plan_2 = Task(
    description = f"Take into account the critic given here: {project_plan_critic}. Find new better plan given new insights.",
    agent = project_planner, 
    expected_output = "Find the best plan for the task."
)

coding = Task(
    description = f"""Find the best way to code the given task: {rewrite_user_prompt}. 
    Remember than you need to follow the plan: {project_plan_2}. Get your hands dirty and code.""",
    agent = senior_coder, 
    expected_output = "Find the best coding solution of this task. I will include the plan without any changes."
)

coding_critic_task = Task(
    description = f"""Find the flaws and bugs from the code. Pinpoint the failures and give as an output what should be changed to improve the structure and the code.
    Ask myself a question can this be done better. Offer constructive feedback and suggestions for optimization, with the aim of enhancing the overall quality and effectiveness of the code. Here is the code: {coding}""",
    agent = coder_critic, 
    expected_output = "Find the best coding plan for the task."
)

coding_2 = Task(
    description = f"""Take into consideration the feedback given in the task: {coding_critic_task}.
    Polish the original code from the task: {coding}.
    Ensure the code is fully ready to be delivered to a client who is willing to pay for it. Address any unknowns with your absolute best knowledge.
    For example, if the user asks for a game, do not forget to implement user controls. Include randomness if the game requires that.
    """,
    agent = senior_coder,
    expected_output = "Provide the final, polished code solution for the task, with no additional commentary. Ensure the code is well-structured and ready for client delivery."
)

summarize = Task(
    description = f"""I will deliver the fully functioning code and the project plan so that the user can have detailed view of the plan.
    Here is detailed code: {coding_2}
    and here is detailed plan {project_plan_2}.
    """,
    agent = summarize_agent,
    expected_output = "I am expected to deliver the code and summarize the plan."
)

######## CREW ###########

crew = Crew(
    agents = [rewriter, project_planner, plan_critic, senior_coder, coder_critic, summarize_agent],
    tasks = [rewrite_user_prompt, project_plan, project_plan_critic, project_plan_2, coding, coding_critic_task, coding_2, summarize],
    verbose = 2,
    process = Process.sequential
)

# Run crew
output = crew.kickoff()