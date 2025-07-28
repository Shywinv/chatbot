from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
import requests
import json
from datetime import datetime
from chatbot2.monitors import LlmMonitor, KnowledgeMonitor
#from crewai_tools import PDFSearchTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Chatbot2():
    """Chatbot2 crew"""
    def __init__(self):
        super().__init__()
        self.llm_model = "llama3.2:3b"
        self.embedding_model = "mxbai-embed-large"
        self.embedding_model_url="http://localhost:11434/api/embeddings"

        #set up pdf knowledge
        self.setup_knowledge()
        #self.setup_pdf_tool()
       
        #set up monitors for debugging
        self.knowledge_monitor = KnowledgeMonitor()
        self.llmMonitor= LlmMonitor()
        
    agents: List[BaseAgent]
    tasks: List[Task]    
    
    def setup_knowledge(self):
        self.pdf_source = PDFKnowledgeSource(
            file_paths=["pdfs/AMEX report.pdf"],
            metadata={
            "source": "AMEX", 
            "type": "report", 
            })
        print("Pdf Knowledge ready")

    def setup_pdf_tool(self):
        """Setup PDFSearchTool instead of knowledge sources"""
        pdf_path = "pdfs/AMEX report.pdf"
        # Create PDFSearchTool with Ollama
        self.pdf_tool = PDFSearchTool(
            pdf=pdf_path,
            config=dict(
                llm=dict(
                    provider="ollama",
                    config=dict(
                        model=self.llm_model,
                        # base_url= "http://localhost:11434/api"
                    )
                ),
                embedder=dict(
                    provider="ollama", 
                    config=dict(
                        model=self.embedding_model,
                        # base_url= self.embedding_model_url
                    )
                )
            )
        )

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            knowledge_sources=[self.pdf_source],
            # tools=[self.pdf_tool],
            embedder={ "provider": "ollama",
            "config": {
            "model": self.embedding_model,
            "url": self.embedding_model_url
            }}
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Chatbot2 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            # process=Process.sequential,
            verbose=True,
            memory=True,
            # process=Process.hierarchical, # In case you wanna uswhat about 2024e that instead https://docs.crewai.com/how-to/Hierarchical/
            embedder={ "provider": "ollama",
            "config": {
            "model": self.embedding_model,
            "url": self.embedding_model_url
            }}
        )
