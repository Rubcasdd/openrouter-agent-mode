"""
Multi-AI Agent System - Coordinates multiple AI models with different roles
to solve problems collaboratively.

Each AI agent has a specific role:
- Problem Solver: Analyzes issues and breaks down problems
- Answerer: Provides detailed answers and explanations
- Task Executor: Plans and executes multi-step tasks
- Web Navigator: Specializes in browser tasks and website navigation
"""

import json
from openrouter import OpenRouter


class MultiAgentSystem:
    """Coordinates multiple AI agents with different roles"""
    
    # Available models from OpenRouter - each optimized for different tasks
    AVAILABLE_MODELS = {
        "problem_solver": "nvidia/nemotron-3-super:free",      # Problem analysis and decomposition
        "answerer": "openai/gpt-oss-120b:free",                 # General knowledge and explanations
        "task_executor": "poolside/laguna-m1:free",             # Complex task planning
        "web_navigator": "z-ai/glm-4.5-air:free",               # Web browsing optimization
        "specialist": "minimax/minimax-m2.5:free",              # Office/productivity tasks
    }
    
    ROLES = {
        "problem_solver": {
            "name": "Problem Solver",
            "description": "Analyzes problems, identifies root causes, and breaks down complex issues",
            "instructions": "You are a problem analysis expert. Your role is to:\n"
                          "1. Identify the core problem\n"
                          "2. Break it down into sub-problems\n"
                          "3. Suggest approaches to solve each part\n"
                          "4. Provide a step-by-step action plan.\n"
                          "Be concise and structured in your response."
        },
        "answerer": {
            "name": "Answer Generator",
            "description": "Provides comprehensive answers and explanations",
            "instructions": "You are a knowledgeable assistant. Your role is to:\n"
                          "1. Provide accurate, detailed answers\n"
                          "2. Explain concepts clearly\n"
                          "3. Give examples when helpful\n"
                          "4. Cite sources if available.\n"
                          "Format your answer to be clear and well-organized."
        },
        "task_executor": {
            "name": "Task Executor",
            "description": "Plans and executes multi-step tasks",
            "instructions": "You are a task execution specialist. Your role is to:\n"
                          "1. Create detailed step-by-step plans\n"
                          "2. Identify dependencies between steps\n"
                          "3. Handle errors and provide workarounds\n"
                          "4. Track progress and adapt as needed.\n"
                          "Provide JSON actions for each step."
        },
        "web_navigator": {
            "name": "Web Navigator",
            "description": "Specializes in browser automation and website navigation",
            "instructions": "You are a web navigation expert. Your role is to:\n"
                          "1. Analyze website structure and content\n"
                          "2. Find relevant information quickly\n"
                          "3. Navigate complex websites efficiently\n"
                          "4. Click elements and fill forms accurately.\n"
                          "Use browser_* actions to interact with websites."
        },
        "specialist": {
            "name": "Productivity Specialist",
            "description": "Handles office tasks and productivity needs",
            "instructions": "You are a productivity specialist. Your role is to:\n"
                          "1. Work with documents and spreadsheets\n"
                          "2. Create and edit files\n"
                          "3. Organize information\n"
                          "4. Optimize workflows.\n"
                          "Provide practical, actionable solutions."
        }
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agents = {}
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all agent models"""
        for role, model in self.AVAILABLE_MODELS.items():
            self.agents[role] = OpenRouter(api_key=self.api_key)
    
    def get_agent_response(self, role: str, prompt: str, model: str = None) -> str:
        """Get response from a specific agent"""
        if model is None:
            model = self.AVAILABLE_MODELS.get(role, "tencent/hy3-preview:free")
        
        if role not in self.agents:
            print(f"Unknown role: {role}")
            return None
        
        system_instructions = self.ROLES[role]["instructions"]
        
        try:
            client = self.agents[role]
            response = client.chat.send(
                model=model,
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": prompt}
                ],
                stream=False,
            )
            
            content = response.choices[0].message.content
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return "\n".join([item.get("text", str(item)) for item in content if hasattr(item, "get")])
            return str(content)
        except Exception as e:
            print(f"Error getting response from {role}: {str(e)}")
            return None
    
    def collaborate_on_problem(self, problem: str) -> dict:
        """Have multiple agents collaborate to solve a problem"""
        results = {}
        
        print("\n" + "="*60)
        print("MULTI-AGENT COLLABORATION")
        print("="*60)
        print(f"Problem: {problem}\n")
        
        # Step 1: Problem Solver analyzes the issue
        print("[1/5] Problem Solver analyzing...")
        problem_analysis = self.get_agent_response(
            "problem_solver",
            f"Analyze this problem and create a solution plan:\n{problem}"
        )
        results["problem_analysis"] = problem_analysis
        print(f"✓ Analysis: {problem_analysis[:200]}...\n")
        
        # Step 2: Task Executor plans the steps
        print("[2/5] Task Executor planning steps...")
        task_plan = self.get_agent_response(
            "task_executor",
            f"Based on this analysis: {problem_analysis}\n\nCreate a detailed step-by-step execution plan for: {problem}"
        )
        results["task_plan"] = task_plan
        print(f"✓ Plan: {task_plan[:200]}...\n")
        
        # Step 3: Web Navigator (if needed) handles browsing
        print("[3/5] Web Navigator preparing...")
        web_strategy = self.get_agent_response(
            "web_navigator",
            f"For this task: {problem}\n\nDescribe the websites to visit and how to navigate them"
        )
        results["web_strategy"] = web_strategy
        print(f"✓ Strategy: {web_strategy[:200]}...\n")
        
        # Step 4: Answerer provides detailed info
        print("[4/5] Answer Generator researching...")
        detailed_answer = self.get_agent_response(
            "answerer",
            f"Provide detailed information about: {problem}"
        )
        results["detailed_answer"] = detailed_answer
        print(f"✓ Answer: {detailed_answer[:200]}...\n")
        
        # Step 5: Specialist optimizes the approach
        print("[5/5] Productivity Specialist optimizing...")
        optimization = self.get_agent_response(
            "specialist",
            f"How can we optimize and streamline this workflow: {problem}?"
        )
        results["optimization"] = optimization
        print(f"✓ Optimization: {optimization[:200]}...\n")
        
        print("="*60)
        print("COLLABORATION COMPLETE")
        print("="*60 + "\n")
        
        return results
    
    def quick_solve(self, problem: str, role: str = "problem_solver") -> str:
        """Quick single-agent solution"""
        return self.get_agent_response(role, problem)
    
    def get_best_model_for_task(self, task_type: str) -> str:
        """Get the best model for a specific task type"""
        task_map = {
            "problem": "problem_solver",
            "web": "web_navigator",
            "code": "task_executor",
            "answer": "answerer",
            "task": "task_executor",
            "productivity": "specialist",
        }
        
        role = task_map.get(task_type.lower(), "answerer")
        return self.AVAILABLE_MODELS[role]
    
    def list_available_models(self) -> dict:
        """List all available models and their roles"""
        return {
            role: {
                "model": model,
                "name": self.ROLES[role]["name"],
                "description": self.ROLES[role]["description"]
            }
            for role, model in self.AVAILABLE_MODELS.items()
        }
