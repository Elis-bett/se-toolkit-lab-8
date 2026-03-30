# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

1

🐈 nanobot
The agentic loop is the iterative reasoning and action cycle that AI     
agents use to accomplish tasks. It typically follows this pattern:       

 1 Observe — Gather information about the current state (read files,     
   check outputs, recall context)                                        
 2 Think — Reason about what to do next based on goals and observations  
 3 Act — Execute a tool or action (write files, run commands, call APIs) 
 4 Repeat — Observe the results and continue until the goal is achieved  

This loop enables agents to:                                             

 • Break complex tasks into steps                                        
 • Adapt based on feedback from previous actions                         
 • Handle uncertainty by iteratively refining their approach             
 • Use tools effectively to interact with the environment                

It's the core mechanism that distinguishes agentic AI (which can take    
autonomous actions) from standard chatbots (which only respond to        
prompts). 


2

You: "What labs are available in our LMS?"

🐈 nanobot
I'll help you find information about available labs in your LMS. Let me  
explore the workspace to see what's configured.                          

🐈 nanobot
Based on the LMS (Learning Management System) in this workspace, here are
the available labs:                                                      

Lab Structure                                                            

This is Lab 8 — "The Agent is the Interface" from the SE Toolkit course. 
The lab focuses on building an AI agent (nanobot) as a natural-language  
interface to the LMS.                                                    

Required Tasks:                                                          

 1 Task 1: Set Up the Agent — install nanobot, configure Qwen API, add   
   MCP tools, write skill prompt                                         
 2 Task 2: Deploy and Connect a Web Client — Dockerize nanobot, add      
   WebSocket channel + Flutter chat UI                                   
 3 Task 3: Give the Agent New Eyes — explore observability data, write   
   log/trace MCP tools                                                   
 4 Task 4: Diagnose a Failure and Make the Agent Proactive — investigate 
   a failure, schedule health checks, fix a planted bug                  

Optional Tasks:                                                          

 1 Task 1: Add a Telegram Bot Client — same agent, different interface   

Lab Components:                                                          

 • LMS Backend: FastAPI application with endpoints for items,            
   interactions, and learners                                            
 • Database: PostgreSQL with seeded data                                 
 • Frontend: React dashboard + Flutter web chat UI                       
 • Agent: nanobot (lightweight AI agent framework)                       
 • Observability: OpenTelemetry Collector, VictoriaLogs, VictoriaTraces  
 • Infrastructure: Docker Compose, Caddy reverse proxy                   

You can find the full setup instructions in:                             

 • lab/setup/setup-simple.md — for quick start                           
 • lab/setup/setup-full.md — for first-time setup                        

Would you like me to help you get started with any specific task?   

## Task 1B — Agent with LMS tools

🐈 nanobot
Here are the available labs:                                             

 1 Lab 01 – Products, Architecture & Roles                               
 2 Lab 02 — Run, Fix, and Deploy a Backend Service                       
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy               
 4 Lab 04 — Testing, Front-end, and AI Agents                            
 5 Lab 05 — Data Pipeline and Analytics Dashboard                        
 6 Lab 06 — Build Your Own Agent                                         
 7 Lab 07 — Build a Client with an AI Coding Agent                       
 8 lab-08                                                                

Would you like more details about any specific lab, such as pass rates,  
completion rates, or top learners?    


🐈 nanobot
Based on the codebase, here's the LMS (Learning Management System) architecture:                                                                                         

Overview                                                                                                                                                                 

The LMS is a FastAPI-based backend service that manages learning labs, learner data, and interaction analytics. It's designed to be queried by various clients, including
a React dashboard, Swagger UI, and AI agents like nanobot.                                                                                                               

Core Components                                                                                                                                                          

1. Backend API (backend/src/lms_backend/)                                                                                                                                

 • Framework: FastAPI with async support                                                                                                                                 
 • Database: PostgreSQL with async SQLAlchemy (SQLModel)                                                                                                                 
 • Authentication: API key-based (verify_api_key)                                                                                                                        
 • Observability: OpenTelemetry integration for logs and traces                                                                                                          

2. Data Model                                                                                                                                                            

 • Items: Labs and tasks (hierarchical structure with parent_id)                                                                                                         
 • Learners: Student records with external IDs and group assignments                                                                                                     
 • InteractionLogs: Submission records linking learners to items with scores and timestamps                                                                              

3. API Routers                                                                                                                                                           

                                                                                        
 Router         Endpoint         Purpose                                                
 ────────────────────────────────────────────────────────────────────────────────────── 
 /items         CRUD operations  Manage labs and tasks                                  
 /learners      GET, POST        List and register learners                             
 /interactions  (optional)       Record learner submissions                             
 /analytics     Various queries  Pass rates, timelines, group performance, top learners 
 /pipeline      Sync operations  ETL pipeline triggers                                  
                                                                                        

4. Analytics Endpoints                                                                                                                                                   

The /analytics router provides aggregated queries:                                                                                                                       

 • GET /scores — Score distribution histogram (0-25, 26-50, 51-75, 76-100)                                                                                               
 • GET /pass-rates — Average score and attempt count per task                                                                                                            
 • GET /timeline — Submissions per day                                                                                                                                   
 • GET /groups — Average score and student count per group                                                                                                               
 • GET /completion-rate — Percentage of learners who passed (score ≥ 60)                                                                                                 
 • GET /top-learners — Top learners by average score                                                                                                                     

5. ETL Pipeline                                                                                                                                                          

 • Populates interaction data from external sources                                                                                                                      
 • Syncs learner and item records                                                                                                                                        
 • Triggered via /pipeline endpoint                                                                                                                                      

System Architecture (from Lab 8)                                                                                                                                         

                                                                                                                                                                         
 [Browser]            [Telegram, optional]                                                                                                                               
     \                       /                                                                                                                                           
      \                     /                                                                                                                                            
       +---- [Nanobot Agent] ---- [LLM]                                                                                                                                  
                  |                                                                                                                                                      
          +-------+-------+                                                                                                                                              
          |               |                                                                                                                                              
    [LMS Tools]   [Observability Tools]                                                                                                                                  
          |               |                                                                                                                                              
    [LMS Backend]    [Logs / Traces]                                                                                                                                     
          |                                                                                                                                                              
     [Postgres]                                                                                                                                                          
                                                                                                                                                                         

Key Features                                                                                                                                                             

 • Async-first: Uses asyncpg and async sessions throughout                                                                                                               
 • CORS-enabled: Configured for web client access                                                                                                                        
 • Error handling: Global exception handler with traceback details                                                                                                       
 • Request logging: Middleware logs all requests with duration                                                                                                           
 • API key protection: All endpoints require authentication                                                                                                              

The LMS is designed as a data layer that AI agents can query through natural language, turning complex SQL aggregations into conversational answers like "Which lab has  
the lowest pass rate?" or "Show me submissions from the last hour."          

## Task 1C — Skill prompt

🐈 nanobot
I can see these labs available:                                          

 1 Lab 01 – Products, Architecture & Roles                               
 2 Lab 02 — Run, Fix, and Deploy a Backend Service                       
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy               
 4 Lab 04 — Testing, Front-end, and AI Agents                            
 5 Lab 05 — Data Pipeline and Analytics Dashboard                        
 6 Lab 06 — Build Your Own Agent                                         
 7 Lab 07 — Build a Client with an AI Coding Agent                       
 8 lab-08                                                                

Which lab would you like to see the scores for?                          


## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
