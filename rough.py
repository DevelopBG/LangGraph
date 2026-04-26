from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from pydantic import BaseModel,Field
import operator

load_dotenv()

# selelct a model that gives structured output
model = ChatOpenAI(model = "gpt-4o-mini") 

class EvaluationSchema(BaseModel):

    feedback: str = Field(description="Detailed feedback for the essay")
    score: int = Field(description= " Score out of 10", ge= 0, le=10)


structure_model = model.with_structured_output(EvaluationSchema)


essay = """
India has emerged as a significant player in the global development of artificial intelligence (AI), supported by its strong foundation in information technology, a large pool of skilled professionals, and a rapidly evolving digital ecosystem. Major IT companies such as Infosys, Tata Consultancy Services, and Wipro have enabled the country to transition smoothly into AI-driven innovation. At the policy level, initiatives led by NITI Aayog and programs like Digital India Initiative have created a strong infrastructure for AI adoption. India’s approach stands out for its emphasis on using AI for social good, including applications in healthcare, agriculture, and education, where technology is leveraged to address large-scale developmental challenges.

At the same time, India faces several challenges that must be addressed to fully realize its AI potential. Issues such as unequal access to digital resources, limited high-end research infrastructure, and concerns around data privacy and ethical AI governance remain critical. However, India’s vibrant startup ecosystem, particularly in cities like Bengaluru, Hyderabad, and Pune, continues to drive innovation and growth in the AI sector. As India expands its role in global AI discussions, it brings a unique perspective focused on inclusivity and scalability. With sustained investment and responsible policy frameworks, India is well-positioned to shape the future of AI in a way that balances technological advancement with societal benefit.
"""

class upscstate(TypedDict):

    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str

    individual_scores: Annotated[list[int], operator.add] # this line is very important. operator.add is the reducer merge multiple list into a single list
    avg_score: float


def evaluate_language(state: upscstate):

    prompt = f"Evaluate the languge quality of the following essay and provide a feedback and assign a score out of 10 \n {state['essay']}"

    output = structure_model.invoke(prompt)

    return {'language_feedback': output.feedback, 'individual_scores': output.score}


def evaluate_analysis(state: upscstate):

    prompt = f"Evaluate the depth of the analysis the following essay and provide a feedback and assign a score out of 10 \n {state['essay']}"

    output = structure_model.invoke(prompt)

    return {'analysis_feedback': output.feedback, 'individual_scores': output.score}

def evaluate_thought(state: upscstate):

    prompt = f"Evaluate the clarity of thought the following essay and provide a feedback and assign a score out of 10 \n {state['essay']}"

    output = structure_model.invoke(prompt)

    return {'clarity_feedback': output.feedback, 'individual_scores': output.score}


def final_evaluation(state: upscstate):

    # summary feedback
    prompt = f"Based on the following feedbacks, create a summarized feedback \n language feedback \n language feedback - {state["language_feedback"]} \n depth of analysis feedback - {state["analysis_feedback"]} \n clarity of thought feedback- {state["clarity_feedback"]}"

    final_feedback = model.invoke(prompt).content

    # average calculate

    avg_score = sum(state['individual_scores'])/len(state['individual_scores'])

    return {'overall_feedback':final_feedback, 'avg_score': avg_score}


graph = StateGraph(upscstate)

graph.add_node("evaluate_language",evaluate_language )
graph.add_node("evaluate_analysis",evaluate_analysis )
graph.add_node("evaluate_thought",evaluate_thought )
graph.add_node("final_evaluation",final_evaluation)

#edges

graph.add_edge(START,"evaluate_language")
graph.add_edge(START,"evaluate_analysis")
graph.add_edge(START,"evaluate_thought")

graph.add_edge("evaluate_language","final_evaluation")
graph.add_edge("evaluate_analysis","final_evaluation")
graph.add_edge("evaluate_thought","final_evaluation")

graph.add_edge("final_evaluation", END)

workflow  = graph.compile()


initial_state = {

    'essay':"hello"
}

final_out = workflow.invoke(initial_state)












