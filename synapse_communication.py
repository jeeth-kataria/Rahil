"""
Project Synapse Agent Communication Protocol

Handles inter-agent communication, task routing, and coordination
for the multi-agent business management system.
"""

import json
import time
import uuid
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AgentMessage:
    """Standardized message format for inter-agent communication."""
    
    def __init__(self, from_agent: str, to_agent: str, task: str, 
                 data: Dict[str, Any] = None, priority: str = "medium",
                 expected_outcome: str = None, callback_required: bool = False,
                 timeout: int = 30):
        self.message_id = str(uuid.uuid4())
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.task = task
        self.data = data or {}
        self.priority = priority
        self.expected_outcome = expected_outcome
        self.callback_required = callback_required
        self.timeout = timeout
        self.timestamp = datetime.now()
        self.status = "pending"
        self.response = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format."""
        return {
            "message_id": self.message_id,
            "from": self.from_agent,
            "to": self.to_agent,
            "task": self.task,
            "priority": self.priority,
            "data": self.data,
            "expected_outcome": self.expected_outcome,
            "callback_required": self.callback_required,
            "timeout": self.timeout,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status
        }


class SynapseMessageBus:
    """Central message bus for agent communication and coordination."""
    
    def __init__(self):
        self.message_queue = []
        self.agent_registry = {}
        self.message_history = []
        self.active_conversations = {}
        
    def register_agent(self, agent_name: str, agent_functions: Dict[str, Callable]):
        """Register an agent with its available functions."""
        self.agent_registry[agent_name] = {
            'functions': agent_functions,
            'status': 'active',
            'last_seen': datetime.now(),
            'message_count': 0
        }
        logger.info(f"Agent {agent_name} registered with {len(agent_functions)} functions")
    
    def send_message(self, message: AgentMessage) -> str:
        """Send a message to another agent."""
        if message.to_agent not in self.agent_registry:
            raise ValueError(f"Target agent {message.to_agent} not registered")
        
        self.message_queue.append(message)
        self.message_history.append(message)
        
        # Update agent statistics
        self.agent_registry[message.from_agent]['message_count'] += 1
        
        logger.info(f"Message sent from {message.from_agent} to {message.to_agent}: {message.task}")
        return message.message_id
    
    def process_message(self, message: AgentMessage) -> Dict[str, Any]:
        """Process a message by calling the appropriate agent function."""
        try:
            target_agent = self.agent_registry[message.to_agent]
            agent_functions = target_agent['functions']
            
            # Find the appropriate function for the task
            if message.task in agent_functions:
                function = agent_functions[message.task]
                result = function(**message.data)
                
                message.status = "completed"
                message.response = result
                
                return {
                    "success": True,
                    "result": result,
                    "message_id": message.message_id
                }
            else:
                message.status = "failed"
                return {
                    "success": False,
                    "error": f"Task {message.task} not available for agent {message.to_agent}",
                    "message_id": message.message_id
                }
                
        except Exception as e:
            message.status = "error"
            logger.error(f"Error processing message {message.message_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message_id": message.message_id
            }
    
    def broadcast_message(self, from_agent: str, task: str, data: Dict[str, Any], 
                         exclude_agents: List[str] = None) -> List[str]:
        """Broadcast a message to all registered agents."""
        exclude_agents = exclude_agents or [from_agent]
        message_ids = []
        
        for agent_name in self.agent_registry:
            if agent_name not in exclude_agents:
                message = AgentMessage(
                    from_agent=from_agent,
                    to_agent=agent_name,
                    task=task,
                    data=data,
                    priority="medium"
                )
                message_id = self.send_message(message)
                message_ids.append(message_id)
        
        return message_ids
    
    def get_agent_status(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status of specific agent or all agents."""
        if agent_name:
            if agent_name in self.agent_registry:
                return self.agent_registry[agent_name]
            else:
                return {"error": f"Agent {agent_name} not found"}
        
        return {
            "total_agents": len(self.agent_registry),
            "active_agents": len([a for a in self.agent_registry.values() if a['status'] == 'active']),
            "total_messages": len(self.message_history),
            "pending_messages": len([m for m in self.message_queue if m.status == 'pending']),
            "agents": self.agent_registry
        }
    
    def get_conversation_history(self, agent1: str, agent2: str) -> List[Dict[str, Any]]:
        """Get conversation history between two agents."""
        conversation = []
        for message in self.message_history:
            if ((message.from_agent == agent1 and message.to_agent == agent2) or
                (message.from_agent == agent2 and message.to_agent == agent1)):
                conversation.append(message.to_dict())
        
        return sorted(conversation, key=lambda x: x['timestamp'])


class AgentCoordinator:
    """Coordinates complex multi-agent workflows and task delegation."""
    
    def __init__(self, message_bus: SynapseMessageBus):
        self.message_bus = message_bus
        self.workflow_templates = self._initialize_workflows()
        self.active_workflows = {}
    
    def _initialize_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Initialize predefined workflow templates."""
        return {
            "strategic_analysis": {
                "description": "Comprehensive strategic analysis workflow",
                "steps": [
                    {"agent": "ceo_agent", "task": "market_analysis", "depends_on": []},
                    {"agent": "financial_agent", "task": "financial_modeling", "depends_on": ["ceo_agent"]},
                    {"agent": "revenue_agent", "task": "revenue_forecast", "depends_on": ["ceo_agent"]},
                    {"agent": "operations_agent", "task": "capacity_analysis", "depends_on": ["revenue_agent"]},
                    {"agent": "hr_agent", "task": "talent_assessment", "depends_on": ["operations_agent"]}
                ],
                "consolidation_agent": "ceo_agent"
            },
            
            "budget_planning": {
                "description": "Annual budget planning workflow",
                "steps": [
                    {"agent": "financial_agent", "task": "budget_framework", "depends_on": []},
                    {"agent": "revenue_agent", "task": "revenue_projections", "depends_on": []},
                    {"agent": "operations_agent", "task": "operational_budget", "depends_on": ["financial_agent"]},
                    {"agent": "hr_agent", "task": "hr_budget", "depends_on": ["financial_agent"]},
                    {"agent": "ceo_agent", "task": "budget_approval", "depends_on": ["revenue_agent", "operations_agent", "hr_agent"]}
                ],
                "consolidation_agent": "financial_agent"
            },
            
            "performance_review": {
                "description": "Quarterly performance review workflow",
                "steps": [
                    {"agent": "financial_agent", "task": "financial_performance", "depends_on": []},
                    {"agent": "revenue_agent", "task": "sales_performance", "depends_on": []},
                    {"agent": "operations_agent", "task": "operational_performance", "depends_on": []},
                    {"agent": "hr_agent", "task": "talent_performance", "depends_on": []},
                    {"agent": "ceo_agent", "task": "strategic_review", "depends_on": ["financial_agent", "revenue_agent", "operations_agent", "hr_agent"]}
                ],
                "consolidation_agent": "ceo_agent"
            }
        }
    
    def execute_workflow(self, workflow_name: str, input_data: Dict[str, Any]) -> str:
        """Execute a predefined workflow."""
        if workflow_name not in self.workflow_templates:
            raise ValueError(f"Workflow {workflow_name} not found")
        
        workflow_id = str(uuid.uuid4())
        workflow = self.workflow_templates[workflow_name].copy()
        workflow['id'] = workflow_id
        workflow['status'] = 'running'
        workflow['start_time'] = datetime.now()
        workflow['input_data'] = input_data
        workflow['results'] = {}
        
        self.active_workflows[workflow_id] = workflow
        
        # Execute workflow steps
        self._execute_workflow_steps(workflow_id)
        
        return workflow_id
    
    def _execute_workflow_steps(self, workflow_id: str):
        """Execute the steps of a workflow in dependency order."""
        workflow = self.active_workflows[workflow_id]
        completed_steps = set()
        
        while len(completed_steps) < len(workflow['steps']):
            for step in workflow['steps']:
                step_id = f"{step['agent']}_{step['task']}"
                
                if step_id in completed_steps:
                    continue
                
                # Check if dependencies are met
                dependencies_met = all(
                    f"{dep}_task" in completed_steps 
                    for dep in step['depends_on']
                )
                
                if dependencies_met:
                    # Execute step
                    message = AgentMessage(
                        from_agent="orchestrator_agent",
                        to_agent=step['agent'],
                        task=step['task'],
                        data=workflow['input_data'],
                        priority="high"
                    )
                    
                    message_id = self.message_bus.send_message(message)
                    result = self.message_bus.process_message(message)
                    
                    workflow['results'][step_id] = result
                    completed_steps.add(step_id)
                    
                    logger.info(f"Completed workflow step: {step_id}")
        
        workflow['status'] = 'completed'
        workflow['end_time'] = datetime.now()
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the status of a running workflow."""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "status": workflow['status'],
            "progress": len(workflow['results']) / len(workflow['steps']),
            "start_time": workflow['start_time'].isoformat(),
            "results": workflow['results']
        }


# Global instances
message_bus = SynapseMessageBus()
coordinator = AgentCoordinator(message_bus)
