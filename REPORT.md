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

Nanobot gateway startup log:
```
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
MCP server 'lms': connected, 9 tools registered
Agent loop started
```
## Task 2B — Web client

-What can you do in this system?

-I'm nanobot, a helpful AI assistant with several capabilities:

## Core Functions
- **File Management**: Read, write, and edit files in the workspace
- **System Commands**: Execute shell commands safely with time limits
- **Web Tools**: Search the web and fetch content from URLs
- **Memory System**: Access long-term memory (MEMORY.md) and search history (HISTORY.md)

## Learning Management System (LMS) Skills
I can interact with course data to:
- List available labs and exercises
- Show pass rates, scores, and completion statistics
- Display learner performance and timelines
- Get group performance metrics
- Show top performers for specific labs

## Scheduling & Reminders
- Set up cron jobs for scheduled reminders
- Create recurring tasks
- Manage heartbeat tasks for periodic operations

## Interactive UI
On supported channels, I can present interactive choices when you need to select between options.

## Additional Capabilities
- Spawn subagents for complex background tasks
- Send messages with file attachments (images, documents, etc.)
- Access various specialized skills like structured UI and memory management

Is there something specific you'd like to explore or accomplish? I'm here to help!

-Which lab has the lowest pass rate?

-Based on my analysis of all the labs, I can now identify which lab has the lowest pass rate. Let me summarize what I found:

After checking all labs, Lab 02 has the lowest pass rate with a task that has a 0.0% pass rate:
- In Lab 02, the task "Optional 2: Make your VM a proxy" has an average score of 0.0% with 3 attempts.

There are also other low pass rates in different labs:
- Lab 01: "Optional: Plan skill development" with 20.0% pass rate
- Lab 02: "Optional 2: Make your VM a proxy" with 0.0% pass rate (lowest)
- Lab 03: "Task 3: Implement the learners endpoint" with 50.0% pass rate
- Lab 04: "Optional 1: CI/CD with GitHub Actions" with 33.8% pass rate

**Lab 02 has the lowest pass rate overall**, specifically the task "Optional 2: Make your VM a proxy" which has a 0.0% pass rate. This suggests this particular task is especially challenging for students.

## Task 3A — Structured logging

backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-01 HTTP/1.1" 200 OK
backend-1  | 2026-03-31 19:18:04,830 INFO [lms_backend.main] [main.py:62] [trace_id=1758c151c10c1b21e98b426e3895afa1 span_id=99322c66edd59ca0 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:18:04,831 INFO [lms_backend.auth] [auth.py:30] [trace_id=1758c151c10c1b21e98b426e3895afa1 span_id=99322c66edd59ca0 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-02 HTTP/1.1" 200 OK
backend-1  | 2026-03-31 19:18:04,859 INFO [lms_backend.main] [main.py:74] [trace_id=1758c151c10c1b21e98b426e3895afa1 span_id=99322c66edd59ca0 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-02 HTTP/1.1" 200
backend-1  | 2026-03-31 19:18:06,161 INFO [lms_backend.main] [main.py:62] [trace_id=e3b63bbdbed7de0b1499e3e65127f04e span_id=aff5e32e9cd0c8e3 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:18:06,161 INFO [lms_backend.auth] [auth.py:30] [trace_id=e3b63bbdbed7de0b1499e3e65127f04e span_id=aff5e32e9cd0c8e3 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-31 19:18:06,186 INFO [lms_backend.main] [main.py:74] [trace_id=e3b63bbdbed7de0b1499e3e65127f04e span_id=aff5e32e9cd0c8e3 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-03 HTTP/1.1" 200
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-03 HTTP/1.1" 200 OK
backend-1  | 2026-03-31 19:18:07,533 INFO [lms_backend.main] [main.py:62] [trace_id=073942bbad1b005c222c5cee93b4d25c span_id=7111d5c1ea598906 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:18:07,534 INFO [lms_backend.auth] [auth.py:30] [trace_id=073942bbad1b005c222c5cee93b4d25c span_id=7111d5c1ea598906 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-31 19:18:07,554 INFO [lms_backend.main] [main.py:74] [trace_id=073942bbad1b005c222c5cee93b4d25c span_id=7111d5c1ea598906 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-04 HTTP/1.1" 200
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-04 HTTP/1.1" 200 OK
backend-1  | 2026-03-31 19:18:08,910 INFO [lms_backend.main] [main.py:62] [trace_id=c00ccb31e4ba82ba08399aae0f2e43d0 span_id=95ade3f204c20f8d resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:18:08,910 INFO [lms_backend.auth] [auth.py:30] [trace_id=c00ccb31e4ba82ba08399aae0f2e43d0 span_id=95ade3f204c20f8d resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-05 HTTP/1.1" 200 OK
backend-1  | 2026-03-31 19:18:08,930 INFO [lms_backend.main] [main.py:74] [trace_id=c00ccb31e4ba82ba08399aae0f2e43d0 span_id=95ade3f204c20f8d resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-05 HTTP/1.1" 200
backend-1  | 2026-03-31 19:18:10,268 INFO [lms_backend.main] [main.py:62] [trace_id=9d8482093020fae9d075ec1125a05ff4 span_id=e92d8d35bb0baf27 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:18:10,269 INFO [lms_backend.auth] [auth.py:30] [trace_id=9d8482093020fae9d075ec1125a05ff4 span_id=e92d8d35bb0baf27 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-31 19:18:10,286 INFO [lms_backend.main] [main.py:74] [trace_id=9d8482093020fae9d075ec1125a05ff4 span_id=e92d8d35bb0baf27 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-06 HTTP/1.1" 200
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-06 HTTP/1.1" 200 OK
backend-1  | 2026-03-31 19:18:11,666 INFO [lms_backend.main] [main.py:62] [trace_id=884313dc3c41736c516f8ab670d2dcc7 span_id=93617b46711cc65d resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:18:11,667 INFO [lms_backend.auth] [auth.py:30] [trace_id=884313dc3c41736c516f8ab670d2dcc7 span_id=93617b46711cc65d resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-31 19:18:11,686 INFO [lms_backend.main] [main.py:74] [trace_id=884313dc3c41736c516f8ab670d2dcc7 span_id=93617b46711cc65d resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-07 HTTP/1.1" 200 OK
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-07 HTTP/1.1" 200
backend-1  | 2026-03-31 19:18:12,974 INFO [lms_backend.main] [main.py:62] [trace_id=cfa6865adf48372781e93743b3b1df1f span_id=713797922cac83fb resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:18:12,975 INFO [lms_backend.auth] [auth.py:30] [trace_id=cfa6865adf48372781e93743b3b1df1f span_id=713797922cac83fb resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-31 19:18:12,978 INFO [lms_backend.main] [main.py:74] [trace_id=cfa6865adf48372781e93743b3b1df1f span_id=713797922cac83fb resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-08 HTTP/1.1" 200
backend-1  | INFO:     172.18.0.9:54940 - "GET /analytics/pass-rates?lab=lab-08 HTTP/1.1" 200 OK
backend-1  | 2026-03-31 19:33:33,981 INFO [lms_backend.main] [main.py:62] [trace_id=65ab9df5e65eeabf4fde1cb6053e238d span_id=9c1903e59fd0a820 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:33:33,982 INFO [lms_backend.auth] [auth.py:30] [trace_id=65ab9df5e65eeabf4fde1cb6053e238d span_id=9c1903e59fd0a820 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-31 19:33:33,982 INFO [lms_backend.db.items] [items.py:16] [trace_id=65ab9df5e65eeabf4fde1cb6053e238d span_id=9c1903e59fd0a820 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-31 19:33:33,986 INFO [lms_backend.main] [main.py:74] [trace_id=65ab9df5e65eeabf4fde1cb6053e238d span_id=9c1903e59fd0a820 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.10:34444 - "GET /items/ HTTP/1.1" 200 OK
backend-1  | INFO:     172.18.0.10:34444 - "GET /items/ HTTP/1.1" 200
backend-1  | 2026-03-31 19:34:04,975 INFO [lms_backend.main] [main.py:62] [trace_id=8cea5b250b447589650c3f18e2d5aded span_id=1280cc69e73e4e82 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-03-31 19:34:04,977 INFO [lms_backend.auth] [auth.py:30] [trace_id=8cea5b250b447589650c3f18e2d5aded span_id=1280cc69e73e4e82 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-03-31 19:34:04,977 INFO [lms_backend.db.items] [items.py:16] [trace_id=8cea5b250b447589650c3f18e2d5aded span_id=1280cc69e73e4e82 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-31 19:34:04,983 ERROR [lms_backend.db.items] [items.py:23] [trace_id=8cea5b250b447589650c3f18e2d5aded span_id=1280cc69e73e4e82 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-03-31 19:34:04,983 WARNING [lms_backend.routers.items] [items.py:23] [trace_id=8cea5b250b447589650c3f18e2d5aded span_id=1280cc69e73e4e82 resource.service.name=Learning Management Service trace_sampled=True] - items_list_failed_as_not_found
	backend-1  | 2026-03-31 19:34:04,984 INFO [lms_backend.main] [main.py:74] [trace_id=8cea5b250b447589650c3f18e2d5aded span_id=1280cc69e73e4e82 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.18.0.10:45858 - "GET /items/ HTTP/1.1" 404 Not Found
backend-1  | INFO:     172.18.0.10:45858 - "GET /items/ HTTP/1.1" 404


## Task 3B — Traces

trace_id: 2f50c925b1b6af3f12db080f737bc413
span: GET /items/ http send
time: 2026-03-31T21:16:30.497617361Z
Query used to retrieve traces: curl "http://localhost:42011/select/logsql/query?query=_stream:{resource_attr:service.name=\"Learning Management Service"}&limit=2"

### Error trace
Trace captured after stopping postgres container.

Trace ID: `8cea5b250b447589650c3f18e2d5aded`
- Span: `GET /items/ http send` — database connection failed
- Error: `asyncpg.exceptions.InterfaceError: connection is closed`
- The error span appeared at the db_query step — postgres was unreachable.


## Task 3C — Observability MCP tools

Four MCP tools were added to a new `mcp-observability` server:
- `logs_search` — search VictoriaLogs with LogsQL query
- `logs_error_count` — count ERROR entries per service
- `traces_list` — list recent traces for a service from VictoriaTraces
- `traces_get` — fetch all spans for a specific trace ID

Skill file: `nanobot/workspace/skills/observability/SKILL.md`

### Agent response — normal conditions
> Question asked: "Any errors in the last hour?" 
Yes, there was 1 error in the Learning Management Service in the last hour. Here are the details:

**Error Summary:**
- **Type:** Database connection error
- **Description:** Connection to the PostgreSQL database was closed unexpectedly
- **Time:** 2026-03-31 19:34:04 UTC (about 1 hour 41 minutes ago)
- **Operation:** A SELECT query on the 'item' table failed

**Technical Details:**
The error occurred when the application tried to execute a database query to select items from the database. It appears the connection to the PostgreSQL database using asyncpg was closed during the operation.

Would you like me to check for any other services or get more detailed information about this error?



## Task 4A — Multi-step investigation

Based on the logs I've checked, the Learning Management Service is experiencing database connectivity issues. Here's what's happening:

**Root Cause:**
The service is failing to connect to its database due to DNS resolution problems. The error message "[Errno -2] Name or service not known" indicates that the application cannot locate the database server using its hostname.

**Timeline of Issues:**
- The service started having database connection issues around 19:34 today
- Initially, it was getting "connection is closed" errors
- More recently (as of 21:33), it's getting DNS resolution errors ("Name or service not known")
- These errors are preventing any database operations from completing successfully

**Impact:**
- The LMS backend is marked as "unhealthy"
- All attempts to retrieve data (like the list of labs) result in HTTP 404 errors
- Even the sync pipeline is failing with 500 internal server errors

**What Likely Happened:**
Either the database service has been moved/restarted with a different hostname, there's a network/DNS configuration issue, or the database service itself is down. The application can't resolve the database hostname to establish a connection, which means it can't serve any requests.

This is an infrastructure issue that would require attention from the system administrators to fix the networking configuration or restart the affected services.

## Task 4B — Proactive health check

I've checked the Learning Management Service and found that it's currently unhealthy. The system returned an HTTP 404 error, which indicates that the service endpoint cannot be reached. The item count is unknown due to this error.

This suggests there may be an issue with the LMS service that needs attention. Would you like me to try triggering the sync pipeline to potentially resolve this issue?



## Task 4C — Bug fix and recovery

**Root cause:** In `backend/src/lms_backend/routers/items.py`, the `get_items`
exception handler returned HTTP 404 for all exceptions including database
failures, hiding the real error.

**Fix:** Changed `status.HTTP_404_NOT_FOUND` to `status.HTTP_503_SERVICE_UNAVAILABLE`
and updated the log event name and detail message.

**Post-fix failure check:**
curl returned: {"detail":"Service temporarily unavailable"} (503)

**Healthy follow-up:**
've verified that your scheduled health check job is active:

- **Job**: "Check system health: Run obser" (ID: a65fb51e)
- **Schedule**: Every 2 minutes
- **Next run**: March 31, 2026 at 23:11:25 UTC (in about 2 minutes)

The health monitoring system is running as expected, checking for backend errors every 2 minutes and posting summaries to this chat.
