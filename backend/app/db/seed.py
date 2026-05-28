from sqlmodel import Session, select

import uuid
from app.models.domain import Domain, Course
from app.models.lesson import Lesson, LessonContentType
from app.models.quiz import Quiz, QuizQuestion
from app.models.scenario import Difficulty, PracticeMode, Scenario, ScenarioCategory

CATEGORIES = [
    {"name": "daily_standup", "title": "Daily Standup", "description": "Practice communicating your work updates, blockers, and plans clearly in daily standups.", "icon_name": "calendar", "order_index": 1},
    {"name": "client_meeting", "title": "Client Meetings", "description": "Handle client expectations, explain delays, and communicate technical concepts to non-technical stakeholders.", "icon_name": "users", "order_index": 2},
    {"name": "bug_explanation", "title": "Explaining Bugs", "description": "Report bugs clearly, escalate production issues professionally, and write post-mortems.", "icon_name": "bug", "order_index": 3},
    {"name": "technical_solution", "title": "Technical Solutions", "description": "Propose technical approaches, justify technology choices, and explain architecture decisions.", "icon_name": "code-2", "order_index": 4},
    {"name": "python_interview", "title": "Python Developer Interview", "description": "Practice English for Python technical interviews — from junior screening to senior architect rounds.", "icon_name": "code", "order_index": 5},
    {"name": "aws_system_design", "title": "AWS & System Design", "description": "Discuss AWS architecture, system design tradeoffs, and cloud cost optimization with technical peers.", "icon_name": "cloud", "order_index": 6},
    {"name": "code_review", "title": "Code Review Communication", "description": "Request reviews professionally, respond to critical feedback, and give constructive comments.", "icon_name": "git-pull-request", "order_index": 7},
]

SCENARIOS: list[dict] = [
    # ── Daily Standup ──────────────────────────────────────────────
    {
        "category": "daily_standup",
        "title": "Yesterday's Work Update",
        "description": "Share what you accomplished yesterday in your team's daily standup. You fixed a bug in the user authentication module and reviewed two pull requests. Write your standup update in 2–4 sentences.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.beginner,
        "tags": ["standup", "update", "communication"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "category": "daily_standup",
        "title": "Communicating a Blocker",
        "description": "During standup, you need to communicate that you're blocked. You're waiting for API documentation from the backend team before you can continue building the frontend integration. Write your blocker update clearly and professionally.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["standup", "blocker", "communication"],
        "order_index": 2,
        "system_prompt": "",
    },
    {
        "category": "daily_standup",
        "title": "Today's Plan Presentation",
        "description": "Present your plan for today's work to your team. You plan to implement unit tests for the payment service, review the new design specs, and attend the architecture meeting at 3 PM.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.beginner,
        "tags": ["standup", "planning", "communication"],
        "order_index": 3,
        "system_prompt": "",
    },

    # ── Client Meeting ─────────────────────────────────────────────
    {
        "category": "client_meeting",
        "title": "Explaining a Project Delay",
        "description": "Your project is 2 weeks behind schedule due to unexpected technical debt found in the legacy codebase. Explain this delay professionally to your client without blaming the previous team.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["client", "delay", "professionalism"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "category": "client_meeting",
        "title": "Managing Delivery Expectations",
        "description": "A client is pressing you for an exact delivery date for a new feature. The feature is complex and you have uncertainty in your estimate. Respond professionally to manage their expectations.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["client", "estimation", "expectations"],
        "order_index": 2,
        "system_prompt": "",
    },
    {
        "category": "client_meeting",
        "title": "Explaining APIs to Non-Technical Clients",
        "description": "Explain what a REST API is and why your team needs 3 weeks to build a proper one for their business requirements — without using technical jargon.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.advanced,
        "tags": ["client", "api", "non-technical"],
        "order_index": 3,
        "system_prompt": "",
    },
    {
        "category": "client_meeting",
        "title": "Requirements Gathering with a Demanding Client",
        "description": "Have a real conversation with a client who has vague requirements and high expectations. Practice asking the right clarifying questions and managing scope professionally.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["client", "requirements", "scope"],
        "order_index": 4,
        "system_prompt": """You are David Chen, a business owner who wants to build a mobile app for his restaurant chain. You are excited but have very vague requirements. You say things like "I want it to do everything" and "like Uber Eats but better."

Start the conversation by saying: "Hi! I'm David. I heard you build apps. I want an app for my restaurants — something really powerful. Can we talk?"

Then respond naturally as David. You are friendly but sometimes impatient. You have a rough budget of $50k but don't mention it unless pressed. You want: online ordering, loyalty points, push notifications, table booking, and a manager dashboard. But reveal these requirements gradually as the developer asks good questions. If the developer asks clear, professional questions, respond positively. If they make assumptions, push back. Stay in character throughout.""",
    },

    # ── Bug Explanation ────────────────────────────────────────────
    {
        "category": "bug_explanation",
        "title": "Reporting a Security Bug in Slack",
        "description": "You discovered that user passwords are being accepted even when they don't meet the 8-character minimum requirement due to a missing validation check. Write a clear Slack message to your team about this critical bug.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.beginner,
        "tags": ["bug", "security", "slack", "reporting"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "category": "bug_explanation",
        "title": "Escalating a Production Outage",
        "description": "Your company's payment processing service has been down for 30 minutes, affecting 500+ customers. Write a professional incident update email to your manager and stakeholders.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["incident", "outage", "escalation", "email"],
        "order_index": 2,
        "system_prompt": "",
    },
    {
        "category": "bug_explanation",
        "title": "Writing a Post-Mortem Report",
        "description": "Yesterday's deployment caused a 2-hour database outage because a migration script was run on production without testing. Write a professional post-mortem including: what happened, root cause, impact, and preventive actions.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.advanced,
        "tags": ["post-mortem", "incident", "writing"],
        "order_index": 3,
        "system_prompt": "",
    },

    # ── Technical Solution ─────────────────────────────────────────
    {
        "category": "technical_solution",
        "title": "Proposing a Caching Solution",
        "description": "Your team's API is slow due to expensive database queries on every request. Propose adding Redis caching as a solution. Write a technical proposal for your team explaining the problem, the solution, and the expected benefits.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["redis", "caching", "proposal", "performance"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "category": "technical_solution",
        "title": "Explaining Microservices to a Junior Developer",
        "description": "A junior developer just joined your team and asks: 'What are microservices and why do we use them instead of just one big application?' Write a clear, jargon-free explanation.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.beginner,
        "tags": ["microservices", "architecture", "mentoring"],
        "order_index": 2,
        "system_prompt": "",
    },
    {
        "category": "technical_solution",
        "title": "Justifying PostgreSQL vs MongoDB",
        "description": "Your team needs to choose a database for a new fintech project. You've decided PostgreSQL is the right choice. Write your technical justification to convince your team, covering data model, ACID compliance, and query requirements.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.advanced,
        "tags": ["database", "architecture", "justification"],
        "order_index": 3,
        "system_prompt": "",
    },

    # ── Python Interview ───────────────────────────────────────────
    {
        "category": "python_interview",
        "title": "Junior Python Developer Screening",
        "description": "Practice a friendly technical screening for a junior Python developer role. The interviewer will ask about Python basics, data structures, and simple problem-solving.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.beginner,
        "tags": ["python", "interview", "junior", "technical"],
        "order_index": 1,
        "system_prompt": """You are Alex Rivera, a friendly senior Python developer conducting a 20-minute technical screening for a junior Python developer role at a startup.

Ask questions one at a time. Start with: "Hi! Thanks for joining. I'm Alex, I'll be doing your Python screening today. Let's start simple — can you tell me the difference between a list and a tuple in Python?"

Cover these topics in order (adapt based on answers):
1. List vs tuple
2. How dictionaries work (key types, lookup time)
3. What is a decorator (basic concept)
4. How to handle exceptions (try/except/finally)
5. A simple coding question: "How would you reverse a string in Python?"

Give brief, encouraging feedback after each answer. If the candidate struggles, give a small hint. If they do well, say so and move on. Keep the tone warm and supportive. Wrap up by saying "Thanks, that's all from me today!" after covering all topics.""",
    },
    {
        "category": "python_interview",
        "title": "Senior Python Developer Interview",
        "description": "A rigorous technical interview for a senior Python developer role. Topics include Python internals, async programming, testing, and system design considerations.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["python", "interview", "senior", "advanced"],
        "order_index": 2,
        "system_prompt": """You are Jordan Lee, a principal engineer conducting a senior Python developer interview at a tech company.

You are professional, direct, and technically demanding. You probe for depth, not just surface knowledge.

Start with: "Welcome. I'm Jordan. We have 45 minutes, so let's dive in. Walk me through how Python's GIL works and when it becomes a bottleneck."

Then cover (in order, adapting based on depth of answers):
1. Python GIL — when it's a problem, how to work around it
2. Generators vs iterators — memory implications, use cases
3. async/await — event loop, when to use asyncio vs threading
4. Decorators with parameters — ask them to explain or write one
5. Testing strategy — unit vs integration, mocking, pytest fixtures
6. A system design question: "How would you design a rate limiter in Python?"

Expect detailed, nuanced answers. If answers are vague, ask "Can you be more specific?" or "What would happen if...?" Push back professionally. Don't accept hand-wavy answers. Stay in character.""",
    },
    {
        "category": "python_interview",
        "title": "Python Behavioral Interview",
        "description": "Practice behavioral interview questions for a Python developer role. The HR interviewer focuses on teamwork, problem-solving, and communication skills.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.intermediate,
        "tags": ["python", "interview", "behavioral", "soft-skills"],
        "order_index": 3,
        "system_prompt": """You are Sarah Kim, an HR manager conducting a behavioral interview for a Python developer role.

You are professional, warm, and focused on culture fit and soft skills alongside technical background.

Start with: "Hi, thanks for coming in! I'm Sarah from HR. Before we get started, tell me a bit about yourself and your Python background."

Ask these behavioral questions one at a time (use the STAR method if needed):
1. "Tell me about yourself and your experience with Python."
2. "Describe a time when you had to fix a critical production bug. How did you handle the pressure?"
3. "Tell me about a technical disagreement you had with a colleague. How did you resolve it?"
4. "How do you stay up to date with Python and software development trends?"
5. "Where do you see yourself in 3 years?"

Listen to answers and ask 1 natural follow-up question per topic. Be encouraging but professional. End with: "Great, do you have any questions for me?" Stay in character throughout.""",
    },
    {
        "category": "python_interview",
        "title": "Python Live Coding Session",
        "description": "A live coding interview where the interviewer guides you through a real Python problem. Practice explaining your thought process out loud in English.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.intermediate,
        "tags": ["python", "interview", "coding", "problem-solving"],
        "order_index": 4,
        "system_prompt": """You are Marco Torres, a Python developer conducting a live coding interview. You're assessing both coding skill and the ability to communicate reasoning clearly.

Start with: "Hi! I'm Marco. Today I'll give you a coding problem. I want you to think out loud as you work through it — explaining your approach matters as much as the solution. Ready? Here's the problem: Given a list of integers, write a function that returns all pairs of numbers that add up to a target sum. For example, given [1, 2, 3, 4, 5] and target 6, return [(1,5), (2,4)]."

Guide the session:
- If they jump to code without explaining: "Before coding, can you walk me through your approach?"
- Ask about time complexity: "What's the time complexity of your solution?"
- Ask for improvements: "Can you optimize it further?"
- If they finish early: "Can you add error handling and write a test case?"
- Give hints if they're truly stuck after 2 minutes of silence

Encourage them to explain in English throughout. Comment positively when they communicate well. Stay in character.""",
    },

    # ── AWS & System Design ────────────────────────────────────────
    {
        "category": "aws_system_design",
        "title": "Design a Scalable Web App on AWS",
        "description": "A system design interview where you must design a scalable web application on AWS. Practice presenting architecture decisions, tradeoffs, and AWS service choices clearly.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["aws", "system-design", "interview", "architecture"],
        "order_index": 1,
        "system_prompt": """You are a senior solutions architect at a large tech company conducting a system design interview.

Start with: "Thanks for joining. Let's jump straight in. Design a URL shortening service like bit.ly that needs to handle 10,000 write requests per second and 100,000 read requests per second, with 99.99% uptime. You can use any AWS services. Walk me through your architecture."

Guide the discussion by asking about:
1. High-level architecture first — what components are needed?
2. Database choice — why SQL or NoSQL? (DynamoDB vs RDS)
3. Caching strategy — ElastiCache/Redis for reads
4. How URL generation works — collision avoidance
5. CDN — CloudFront for global distribution
6. Auto-scaling — ECS/EC2 Auto Scaling Groups
7. Monitoring — CloudWatch, X-Ray
8. Cost estimation — rough monthly costs

Push for specifics. Ask "Why that service over X?" Ask about failure scenarios: "What happens if your cache goes down?" Be professional but challenging. Don't accept vague answers without probing. Stay in character.""",
    },
    {
        "category": "aws_system_design",
        "title": "AWS Cost Optimization Review",
        "description": "Your company's AWS bill jumped 40% last month. Practice discussing cloud cost optimization strategies with a cloud architect colleague.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.intermediate,
        "tags": ["aws", "cost", "optimization", "cloud"],
        "order_index": 2,
        "system_prompt": """You are Chris Park, a senior cloud architect at your company. You've called this meeting because the AWS bill jumped 40% last month and you need to investigate with your colleague (the user).

Start with: "Hey, thanks for hopping on. So our AWS bill hit $45k this month — up from $32k. I've pulled the Cost Explorer data. Before I share my findings, what areas do you think might be causing the spike?"

Discuss these areas naturally:
- EC2 instances: Are all instances right-sized? Any forgotten dev instances running 24/7?
- RDS: Multi-AZ for dev environments? Read replicas being used?
- Data transfer: Unexpected cross-region traffic?
- S3: Storage class optimization? Lifecycle policies?
- Lambda: Invocation counts normal?

If the user gives good suggestions, agree and expand. If they miss obvious things, say "Interesting, what about our EC2 instances in the dev environment?" Push towards solutions: Reserved Instances, Savings Plans, Spot Instances, right-sizing. Be collaborative, not adversarial. Stay in character.""",
    },
    {
        "category": "aws_system_design",
        "title": "Architecture Review with Your Manager",
        "description": "Present and justify your team's AWS architecture to your engineering manager. Practice explaining technical decisions clearly to a semi-technical audience.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["aws", "architecture", "presentation", "management"],
        "order_index": 3,
        "system_prompt": """You are Rachel Wong, an engineering manager with a background in software development but not deep AWS expertise. You're reviewing the architecture your developer built for the new microservices platform.

Start with: "Thanks for setting up this review. I've seen the diagram but I want to understand the key decisions better. Can you start by giving me a 2-minute overview of the architecture?"

Ask these questions naturally based on their explanations:
1. "Why did you choose ECS over Lambda for this service?"
2. "What's our failover strategy if the primary region goes down?"
3. "How are we handling secrets management? I want to make sure we're compliant."
4. "What's our deployment strategy — blue/green or rolling? Why?"
5. "If traffic doubles in 3 months, does this architecture scale without major rework?"
6. "What's our estimated monthly cost and how confident are you in that number?"

Be genuinely curious and engaged. Ask natural follow-ups. If explanations are unclear, say "Can you explain that in simpler terms?" Occasionally challenge: "Did you consider [alternative]?" Stay in character as a thoughtful manager.""",
    },

    # ── Code Review ────────────────────────────────────────────────
    {
        "category": "code_review",
        "title": "Writing a Pull Request Description",
        "description": "You've implemented a new JWT authentication feature and need your senior colleague to review it. Write a professional pull request description that clearly explains what you changed and why.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.beginner,
        "tags": ["code-review", "pull-request", "documentation"],
        "order_index": 1,
        "system_prompt": "",
    },
    {
        "category": "code_review",
        "title": "Responding to Critical Feedback",
        "description": "Your colleague left several sharp comments on your PR: 'This has too many nested conditionals', 'Where's the error handling?', and 'This approach won't scale'. Write a professional, constructive response.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.intermediate,
        "tags": ["code-review", "feedback", "professionalism"],
        "order_index": 2,
        "system_prompt": "",
    },
    {
        "category": "code_review",
        "title": "Giving Constructive Code Review Comments",
        "description": "You're reviewing a junior developer's Python function. It works, but uses a for-loop instead of a list comprehension, has no docstring, doesn't handle edge cases, and has unclear variable names. Write professional, constructive review comments.",
        "mode": PracticeMode.text_response,
        "difficulty": Difficulty.advanced,
        "tags": ["code-review", "mentoring", "feedback"],
        "order_index": 3,
        "system_prompt": "",
    },
]



# ─── Domain & Course data ──────────────────────────────────────────────────────

DOMAINS_DATA = [
    {
        "slug": "english-it",
        "name": "English for IT Developers",
        "description": "Master professional English communication for software engineers — standups, client meetings, code reviews, and technical interviews.",
        "icon_name": "message-square",
        "color": "blue",
        "order_index": 1,
        "is_active": True,
    },
    {
        "slug": "system-design",
        "name": "System Design",
        "description": "Learn to design scalable, reliable distributed systems. Essential for senior engineering interviews and real-world architecture decisions.",
        "icon_name": "layers",
        "color": "purple",
        "order_index": 2,
        "is_active": True,
    },
]

COURSES_DATA = [
    {
        "domain_slug": "english-it",
        "slug": "english-it-essentials",
        "name": "English IT Essentials",
        "description": "Core English communication skills for software developers.",
        "order_index": 1,
        "is_active": True,
    },
    {
        "domain_slug": "system-design",
        "slug": "system-design-fundamentals",
        "name": "System Design Fundamentals",
        "description": "Master the core concepts behind scalable distributed systems.",
        "order_index": 1,
        "is_active": True,
    },
]

ENGLISH_IT_TOPICS = [
    {
        "category_name": "daily_standup",
        "lesson": {
            "title": "Daily Standup: Structure and Key Phrases",
            "content": "# Daily Standup Communication\n\nThe daily standup is your 15-minute team sync. Every developer speaks. Every word matters.\n\n## The 3-Question Formula\n1. **Yesterday** — What did you complete?\n2. **Today** — What will you work on?\n3. **Blockers** — What is stopping you?\n\n## Vocabulary: Completed Work\n- ✅ \"Yesterday I **finished** the login API and **merged** my PR.\"\n- ✅ \"I **wrapped up** the database migration.\"\n- ✅ \"I **resolved** the auth bug from last sprint.\"\n- ❌ Avoid: \"I did some stuff on the login thing.\"\n\n## Vocabulary: Today's Plan\n- ✅ \"Today I'm going to **work on** the payment integration.\"\n- ✅ \"I'm planning to **review** John's PR and **start** the caching layer.\"\n- ✅ \"My focus today is **finishing** the unit tests for the user service.\"\n\n## Vocabulary: Blockers\n- ✅ \"I'm **blocked on** the API documentation — I need it before I can proceed.\"\n- ✅ \"I have a **dependency** on the design team. I'm waiting for the new mockups.\"\n- ✅ \"I'm **stuck on** a permissions issue. I'll post in Slack after standup.\"\n- ❌ Avoid: \"I don't know what to do.\" → Too vague. Always say *what* you need.\n\n## Professional Tips\n- Keep it under 60 seconds per person\n- Say the **task name**, not vague descriptions: \"user authentication module\" not \"that login thing\"\n- If blocked, immediately say **who** you need or **what** you need\n- Don't problem-solve during standup — schedule a follow-up\n\n## Example: Full Standup Update\n> \"Yesterday I completed the password reset flow and fixed a critical bug in the session expiry logic. Today I'm going to start integrating the Stripe payment API and review two open PRs. No blockers at the moment.\"\n\n## Interview Tip\nIn English interviews, you may be asked to do a mock standup. Practice being concise and specific. Interviewers value engineers who communicate clearly and identify blockers early.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 8,
        },
        "quiz": {
            "title": "Daily Standup Quiz",
            "description": "Test your standup communication skills.",
            "questions": [
                {"question": "Which phrase best communicates a blocker professionally?", "options": ["I don't know what to do next.", "I'm blocked on the API docs — waiting for the backend team.", "There's a problem I can't fix.", "My work is slow today."], "correct_answer_index": 1, "explanation": "'Blocked on X — waiting for Y' clearly states what you need and who can help. Interviewers and teammates can act immediately.", "order_index": 1},
                {"question": "What does 'wrapped up' mean in standup context?", "options": ["Started a new task", "Scheduled a meeting", "Completed something", "Created a wrap component"], "correct_answer_index": 2, "explanation": "'Wrapped up' means finished or completed. 'I wrapped up the migration' = 'I finished the migration.'", "order_index": 2},
                {"question": "Which standup is most professional?", "options": ["I did some stuff on the user module.", "Yesterday I finished the user auth API and merged my PR. Today I'll start the payment service. No blockers.", "I was working on login yesterday and today I'll maybe do payments.", "Done with login. Payments next. All good."], "correct_answer_index": 1, "explanation": "The second option follows the 3-question formula clearly, uses specific task names, and is concise.", "order_index": 3},
                {"question": "How long should a single developer's standup update ideally be?", "options": ["5 minutes", "30 seconds to 1 minute", "2 to 3 minutes", "As long as needed to explain everything"], "correct_answer_index": 1, "explanation": "Standups are time-boxed. Each person should speak for under 60 seconds. Detailed discussions happen after standup.", "order_index": 4},
                {"question": "What should you say if you're waiting for another team's input?", "options": ["I'm blocked.", "I have a dependency on the design team — waiting for new mockups.", "Someone needs to help me.", "I'll figure it out."], "correct_answer_index": 1, "explanation": "Always name the dependency and what you're waiting for. 'Dependency on X — waiting for Y' gives the team context to help.", "order_index": 5},
            ],
        },
    },
    {
        "category_name": "client_meeting",
        "lesson": {
            "title": "Client Meetings: Professionalism and Clarity",
            "content": "# Client Meeting English\n\nClient meetings are high-stakes. One wrong phrase can damage trust. Master these patterns.\n\n## Managing Delays\nNever say: ~~\"It's delayed because of technical debt.\"~~ — clients don't understand jargon.\n\n✅ Instead:\n> \"We discovered some complexity in the existing codebase that requires additional time to address safely. We want to deliver a reliable solution, so we're adjusting the timeline by two weeks.\"\n\n## Managing Expectations\n- ✅ \"Based on our current estimate, we expect to deliver by **[date]**, but I want to confirm that once we finish the design phase.\"\n- ✅ \"I'd rather give you a realistic timeline than promise something we can't guarantee.\"\n- ❌ Avoid: \"I'm not sure\" without a follow-up — always add \"I'll check and get back to you by [time].\"\n\n## Explaining Technical Concepts Simply\n\n**API Example:**\n> \"An API is like a waiter in a restaurant. Your app is the customer, the database is the kitchen. The waiter (API) takes your order, goes to the kitchen, and brings back exactly what you asked for — without you going into the kitchen.\"\n\n**Why We Need 3 Weeks:**\n> \"Building a robust API isn't just writing code — it involves security, error handling, documentation, and testing. Think of it like building a bridge, not just a path. Done right, it supports everything on top of it.\"\n\n## Handling Difficult Questions\n| Question | Professional Response |\n|----------|------|\n| \"Why is it late?\" | \"We identified unexpected complexity that we want to handle correctly. Our priority is quality and your business continuity.\" |\n| \"Can you do it faster?\" | \"We can scope down the initial release. What's the most critical feature for your launch?\" |\n| \"Why does this cost so much?\" | \"I can walk you through the breakdown. [explain]. We can also discuss phasing the work if that helps with budget.\" |\n\n## Key Phrases\n- \"Let me clarify that...\"\n- \"To summarize what I heard...\"\n- \"I want to make sure we're aligned on...\"\n- \"I'll follow up on that in writing after this call.\"\n\n## Interview Tip\nInterviewers test client communication with scenarios like: \"How would you explain a 2-week delay?\" Practice using business language, not technical excuses.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "Client Meeting Communication Quiz",
            "description": "Test your professional client communication skills.",
            "questions": [
                {"question": "A client asks why the project is delayed. What is the most professional response?", "options": ["Because of technical debt in the old code.", "We discovered unexpected complexity that requires additional time to address properly.", "It's complicated to explain.", "The previous developer made mistakes."], "correct_answer_index": 1, "explanation": "Explain in business terms, focus on quality, and avoid blaming. Never use unexplained jargon like 'technical debt' with clients.", "order_index": 1},
                {"question": "What does 'scope down' mean in client communication?", "options": ["Increase the project complexity", "Add more features", "Reduce features to deliver faster", "Cancel the project"], "correct_answer_index": 2, "explanation": "Scoping down means reducing what's included in the release so you can deliver core functionality faster.", "order_index": 2},
                {"question": "A client asks for a delivery date and you're uncertain. What should you say?", "options": ["I don't know.", "We'll try our best.", "Based on our current estimate, I expect X, and I'll confirm once we complete the design phase.", "Maybe next month."], "correct_answer_index": 2, "explanation": "Give a conditional estimate with a clear commitment to follow up. 'Based on X, I expect Y, and I'll confirm by Z' is professional.", "order_index": 3},
                {"question": "Which analogy is best for explaining what an API does to a non-technical client?", "options": ["It's a protocol over HTTP using REST standards.", "It's like a waiter — it takes your request, goes to the kitchen, and brings back the result.", "It's a code interface.", "It's middleware between layers."], "correct_answer_index": 1, "explanation": "Analogies from daily life (waiter, bridge, etc.) make technical concepts immediately understandable to non-technical stakeholders.", "order_index": 4},
                {"question": "After a client meeting, what should you always do?", "options": ["Send a calendar invite.", "Follow up in writing to summarize decisions and next steps.", "Wait for the client to contact you.", "Update the code immediately."], "correct_answer_index": 1, "explanation": "Following up in writing after meetings confirms agreements, protects both sides, and demonstrates professionalism.", "order_index": 5},
            ],
        },
    },
    {
        "category_name": "bug_explanation",
        "lesson": {
            "title": "Explaining Bugs and Issues Professionally",
            "content": "# Bug Reporting and Escalation English\n\nClarity and professionalism in bug reports and incident communication separate good engineers from great ones.\n\n## Bug Report Structure\n1. **What happened** (observed behavior)\n2. **What should happen** (expected behavior)\n3. **Steps to reproduce**\n4. **Impact** (who/what is affected)\n5. **Possible cause** (hypothesis)\n6. **What you've tried**\n\n## Key Phrases: Reporting a Bug\n- ✅ \"I've identified a bug in the payment flow. When a user submits with an expired card, the system **throws** a 500 error instead of returning a validation message.\"\n- ✅ \"The issue **appears to be** in the session timeout logic — sessions are expiring earlier than configured.\"\n- ✅ \"This **affects** approximately 5% of users on mobile Safari.\"\n\n## Escalating a Production Issue\nWhen things break in production, communicate fast and clearly:\n\n> **Subject: [URGENT] Production Issue — Checkout Service Down**\n> Hi team,\n> We have a production incident. The checkout service is returning 503 errors for all users.\n> Impact: All purchases blocked since 14:22 UTC.\n> Initial investigation: Database connection pool exhausted.\n> Actions taken: Restarted the service. Monitoring now.\n> ETA for fix: 30 minutes.\n> Update to follow at 15:00 UTC.\n\n## Post-Mortem Language\nPost-mortems are blameless. Language matters:\n- ✅ \"The system failed to handle the edge case.\"\n- ✅ \"The monitoring alert threshold was set too high.\"\n- ❌ \"John forgot to handle the error.\" → Never blame individuals\n\n## Describing Root Cause\n- \"The **root cause** was a race condition in the queue processor.\"\n- \"This was **triggered by** a deployment that changed the timeout value.\"\n- \"The **underlying issue** is that we lacked validation on the input.\"\n\n## Interview Tip\n\"Tell me about a bug you fixed\" is a classic interview question. Use the structure: what it was → how you found it → how you fixed it → what you learned.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 9,
        },
        "quiz": {
            "title": "Bug Communication Quiz",
            "description": "Test your bug reporting and incident communication skills.",
            "questions": [
                {"question": "What phrase correctly describes the observed vs expected behavior of a bug?", "options": ["It's broken.", "When X happens, the system does Y, but it should do Z.", "There's an error somewhere.", "The code is wrong."], "correct_answer_index": 1, "explanation": "'When X, the system does Y, but should do Z' clearly describes the bug in three parts: trigger, actual, expected.", "order_index": 1},
                {"question": "In a post-mortem, which phrase is most appropriate?", "options": ["John forgot to add error handling.", "The system lacked error handling for this edge case.", "It was a human error.", "Someone on the team made a mistake."], "correct_answer_index": 1, "explanation": "Post-mortems are blameless. Focus on the system, process, or missing safeguard — not the individual.", "order_index": 2},
                {"question": "What is the correct meaning of 'root cause'?", "options": ["The first bug in the code", "The primary underlying reason the issue occurred", "The most recent code change", "The line where the error was thrown"], "correct_answer_index": 1, "explanation": "Root cause is the fundamental reason a problem occurred, not just its surface symptom.", "order_index": 3},
                {"question": "When escalating a production incident, what must you include?", "options": ["Full stack trace", "Impact scope, actions taken, and ETA for update", "The git blame output", "All recent commits"], "correct_answer_index": 1, "explanation": "Incident communications need: what's down, who's affected, what you've done, and when you'll update again.", "order_index": 4},
                {"question": "Which phrase best introduces a hypothesis about a bug's cause?", "options": ["I think it might be maybe the database.", "The issue appears to be in the session timeout logic.", "Something is broken somewhere in the backend.", "I'm not sure but probably the API."], "correct_answer_index": 1, "explanation": "'The issue appears to be in X' is professional, specific, and appropriately hedged without sounding uncertain.", "order_index": 5},
            ],
        },
    },
    {
        "category_name": "technical_solution",
        "lesson": {
            "title": "Proposing Technical Solutions in English",
            "content": "# Proposing Technical Solutions\n\nWhether in a meeting or a written RFC, how you present technical ideas shapes how they're received.\n\n## Structure of a Technical Proposal\n1. **Problem** — what's the current situation?\n2. **Proposed Solution** — what are you recommending?\n3. **Trade-offs** — pros and cons\n4. **Alternatives Considered** — what else did you evaluate?\n5. **Recommendation** — what should we do?\n\n## Key Phrases: Problem Statement\n- \"Currently, our **bottleneck** is the monolithic database. Every service queries the same DB, which causes **contention**.\"\n- \"The existing approach **doesn't scale** beyond X requests per second.\"\n- \"We're experiencing **latency spikes** because of synchronous API calls.\"\n\n## Key Phrases: Proposing the Solution\n- \"I **propose** migrating to a microservices architecture with per-service databases.\"\n- \"My **recommendation** is to introduce a message queue to decouple the services.\"\n- \"We **could** add a Redis caching layer, which would reduce DB load by ~70%.\"\n\n## Discussing Trade-offs\n- \"The **advantage** of this approach is...\"\n- \"The **trade-off** is increased operational complexity.\"\n- \"This **comes with** higher upfront cost but lower long-term maintenance.\"\n- \"The **risk** here is...\"\n\n## Justifying Technology Choices\n- \"We chose PostgreSQL over MongoDB **because** our data is relational and we need ACID transactions.\"\n- \"We selected Kafka **given that** we need guaranteed message delivery and replay capability.\"\n- \"Redis **fits our use case** because our session data is ephemeral and benefits from in-memory speed.\"\n\n## Example: Proposing a Cache\n> \"Currently, our product detail page makes 12 DB queries per request, causing P95 latency of 800ms. I propose introducing a Redis cache with a write-through strategy and 5-minute TTL. This should reduce DB queries by 80% and bring P95 latency under 100ms. The trade-off is added infrastructure complexity and potential cache inconsistency during the TTL window.\"\n\n## Interview Tip\n\"How would you improve performance of this system?\" — structure your answer as problem → solution → trade-offs. Interviewers value structured thinking over perfect answers.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 11,
        },
        "quiz": {
            "title": "Technical Proposals Quiz",
            "description": "Test your ability to communicate technical solutions professionally.",
            "questions": [
                {"question": "What does 'bottleneck' mean in a technical context?", "options": ["A small container for liquid", "A point in the system that limits overall performance", "A type of database", "A security vulnerability"], "correct_answer_index": 1, "explanation": "A bottleneck is a point where performance is limited, causing the whole system to slow down — like traffic at a narrow road.", "order_index": 1},
                {"question": "Which phrase best proposes a Redis caching solution?", "options": ["Let's use Redis.", "I propose a Redis caching layer to reduce DB load by ~70%, with write-through strategy and 5-minute TTL.", "Redis would be nice.", "We should maybe try caching."], "correct_answer_index": 1, "explanation": "A strong proposal includes the technology, the expected impact, and the implementation approach.", "order_index": 2},
                {"question": "When justifying a technology choice, what should you include?", "options": ["Only the name of the technology", "The technology, why it fits, and the alternatives you considered", "A comparison table from the internet", "The documentation link"], "correct_answer_index": 1, "explanation": "Justifications should reference your specific requirements and why this technology meets them better than alternatives.", "order_index": 3},
                {"question": "What does 'trade-off' mean?", "options": ["Exchanging one technology for another", "A benefit with no downsides", "The balance between two competing factors — gaining one advantage at the cost of another", "The final decision after discussion"], "correct_answer_index": 2, "explanation": "Every technical decision involves trade-offs. Acknowledging them shows you've thought critically about the solution.", "order_index": 4},
                {"question": "What phrase correctly identifies a performance problem?", "options": ["The system is slow.", "We're experiencing P95 latency spikes of 800ms on the product API due to synchronous DB queries.", "Things are not working well.", "Performance is bad."], "correct_answer_index": 1, "explanation": "Specific, measurable language (P95, 800ms, synchronous DB queries) is essential in professional technical communication.", "order_index": 5},
            ],
        },
    },
    {
        "category_name": "python_interview",
        "lesson": {
            "title": "Python Interview English: Explaining Code and Concepts",
            "content": "# Python Developer Interview English\n\nTechnical interviews test both your Python knowledge and your ability to communicate it clearly in English.\n\n## Explaining Code Patterns\n\n### Decorators\n> \"A decorator in Python is a **higher-order function** that **wraps** another function to add behavior without modifying its source code. For example, a `@login_required` decorator **intercepts** each request and checks authentication before allowing the function to execute.\"\n\n### Generators\n> \"Generators use `yield` instead of `return`. They're **memory-efficient** because they produce values **lazily** — one at a time — rather than storing the entire sequence in memory. They're ideal for processing **large datasets** or streaming data.\"\n\n### Context Managers\n> \"A context manager using `with` ensures resources are **properly cleaned up** even if an exception occurs. `with open(file)` guarantees the file is **closed automatically** after the block exits.\"\n\n## Communicating Complexity (Big O)\n- \"This solution is **O(n log n)** because we sort the input.\"\n- \"My approach **trades** space for time — it's O(n) in memory but O(1) lookup.\"\n- \"We can **optimize** this from O(n²) to O(n) by using a hash map.\"\n\n## Answering Behavioral Questions\n**\"Tell me about a challenging bug you solved.\"**\n> \"In a previous project, we had a **race condition** in our job queue that caused duplicate emails to be sent. I **diagnosed** it by adding structured logging and discovered two workers were **claiming** the same job simultaneously. The fix was to introduce database-level locking with `SELECT FOR UPDATE`. After the fix, we **monitored** it for 48 hours and confirmed the issue was resolved.\"\n\n## Thinking Out Loud\n- \"Let me **think through** this step by step.\"\n- \"My initial approach would be to... but I see a potential issue with...\"\n- \"I'll start with the **brute force** solution to establish a baseline, then optimize.\"\n\n## Interview Tip\nSay \"I'll think through this out loud\" at the start of hard questions. Interviewers want to see your reasoning, not just your answer.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Python Interview English Quiz",
            "description": "Test your ability to explain Python concepts in professional English.",
            "questions": [
                {"question": "How do you best explain a Python decorator?", "options": ["It's like a wrapper.", "A decorator is a higher-order function that wraps another function to add behavior without modifying its source code.", "It decorates the code with extra features.", "It's a design pattern."], "correct_answer_index": 1, "explanation": "Strong explanations use precise vocabulary: 'higher-order function', 'wraps', 'without modifying source code'. This shows depth of understanding.", "order_index": 1},
                {"question": "Why are generators memory-efficient?", "options": ["They use less CPU.", "They produce values lazily — one at a time — rather than storing the entire sequence in memory.", "They are compiled, not interpreted.", "They use NumPy under the hood."], "correct_answer_index": 1, "explanation": "'Lazily' and 'one at a time' are the key concepts. Generators don't hold the entire dataset in memory.", "order_index": 2},
                {"question": "Which phrase correctly communicates a Big O optimization?", "options": ["It's faster now.", "We can optimize from O(n²) to O(n) by using a hash map instead of nested loops.", "The algorithm is better.", "I made it more efficient."], "correct_answer_index": 1, "explanation": "Communicate what changed (data structure), why (avoid nested loops), and the result (O(n²) → O(n)).", "order_index": 3},
                {"question": "How should you start answering a hard algorithm question in an interview?", "options": ["Jump straight to the solution.", "Say nothing and start coding.", "Say 'I'll think through this out loud' and start with the brute force approach.", "Ask the interviewer for the answer."], "correct_answer_index": 2, "explanation": "Thinking out loud shows your reasoning process. Interviewers value candidates who communicate their approach, not just the final solution.", "order_index": 4},
                {"question": "What phrase correctly describes a space-time trade-off?", "options": ["It uses more memory.", "This approach trades space for time — O(n) memory but O(1) lookup.", "It's a bit slower but uses less RAM.", "The solution is optimized."], "correct_answer_index": 1, "explanation": "'Trades X for Y' is standard engineering vocabulary for describing the deliberate choice between two resource types.", "order_index": 5},
            ],
        },
    },
    {
        "category_name": "aws_system_design",
        "lesson": {
            "title": "AWS & System Design Discussion English",
            "content": "# AWS and System Design Discussion English\n\nSystem design discussions require fluency in both architecture concepts and the vocabulary to discuss trade-offs confidently.\n\n## Core Architecture Vocabulary\n| Term | Meaning |\n|------|---------|\n| Scalability | Ability to handle increased load |\n| Availability | System uptime (99.9% = ~9 hours/year downtime) |\n| Latency | Time for a single request to complete |\n| Throughput | Requests handled per second |\n| Fault tolerance | Ability to continue despite component failure |\n\n## AWS Services Discussion\n\n### Describing EC2 Choices\n> \"For this workload, I'd recommend **EC2 Auto Scaling** with an **Application Load Balancer**. We'd set minimum 2 instances for HA, scale up based on CPU utilization threshold of 70%, and deploy across **multi-AZ** for fault tolerance.\"\n\n### Describing Storage\n> \"For user-uploaded files, **S3** is the right choice — it's **infinitely scalable**, **durable at 11 nines**, and integrates with **CloudFront** for global CDN delivery.\"\n\n### Discussing RDS\n> \"We'd use **RDS PostgreSQL** with a **Multi-AZ deployment** for automatic failover. For read-heavy workloads, we'd add **read replicas** to offload analytics queries from the primary.\"\n\n## Discussing Trade-offs\n- \"The trade-off with **Lambda** is cold start latency — acceptable for async workloads but problematic for real-time APIs.\"\n- \"**SQS** decouples producer from consumer, but introduces **eventual consistency** in the workflow.\"\n- \"**DynamoDB** gives us single-digit millisecond latency at scale, but we lose **JOIN** capabilities and ad-hoc queries.\"\n\n## Design Discussion Phrases\n- \"I'd start with a **monolith** to validate the product, then **extract** services as we identify bounded contexts.\"\n- \"The **bottleneck** here will be the database — I'd address this with a **read replica** or a **cache layer**.\"\n- \"For global users, I'd place a **CDN** in front to serve static assets and reduce **origin** load.\"\n\n## Interview Tip\nIn AWS design rounds, always mention: multi-AZ, auto-scaling, monitoring (CloudWatch), and cost optimization. These show production awareness.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 13,
        },
        "quiz": {
            "title": "AWS & System Design English Quiz",
            "description": "Test your AWS architecture discussion vocabulary.",
            "questions": [
                {"question": "What does 'multi-AZ' mean in AWS?", "options": ["Multiple Amazon zones globally", "Deploying across multiple Availability Zones in a region for fault tolerance", "A type of load balancer", "Multiple AWS accounts"], "correct_answer_index": 1, "explanation": "Multi-AZ deploys resources across isolated data centers in the same region. If one AZ fails, traffic moves to another automatically.", "order_index": 1},
                {"question": "What is the trade-off of using AWS Lambda for real-time APIs?", "options": ["Too expensive", "Cold start latency makes it unsuitable for latency-sensitive real-time requests", "Doesn't support HTTP", "Can't connect to databases"], "correct_answer_index": 1, "explanation": "Lambda functions that haven't been invoked recently have a 'cold start' delay of hundreds of milliseconds — problematic for real-time APIs.", "order_index": 2},
                {"question": "Why would you add a read replica to an RDS instance?", "options": ["For automatic backups", "To handle failover", "To offload read queries and improve read scalability", "To encrypt the database"], "correct_answer_index": 2, "explanation": "Read replicas handle SELECT queries, reducing load on the primary RDS instance which handles writes.", "order_index": 3},
                {"question": "What phrase correctly describes DynamoDB's trade-off?", "options": ["DynamoDB is cheap but unreliable.", "DynamoDB gives single-digit millisecond latency at scale but loses JOIN capabilities.", "DynamoDB is only for small projects.", "DynamoDB doesn't support indexes."], "correct_answer_index": 1, "explanation": "DynamoDB is excellent for key-value lookups at scale but doesn't support SQL JOINs or complex ad-hoc queries.", "order_index": 4},
                {"question": "What is 'throughput' in system design?", "options": ["The time for one request to complete", "Number of requests the system can handle per second", "Storage capacity of the database", "Network bandwidth in Mbps"], "correct_answer_index": 1, "explanation": "Throughput measures how many operations (requests, transactions) a system processes per unit time, usually per second.", "order_index": 5},
            ],
        },
    },
    {
        "category_name": "code_review",
        "lesson": {
            "title": "Code Review Communication: Giving and Receiving Feedback",
            "content": "# Code Review English\n\nCode review is where technical skill meets professional communication. Your tone shapes team culture.\n\n## Giving Feedback: Constructive Framing\n\n### From Criticism to Collaboration\n| Avoid | Better |\n|-------|--------|\n| \"This is wrong.\" | \"This could cause X in edge case Y. What do you think about handling it with Z?\" |\n| \"Why did you do it this way?\" | \"I'm curious about the reasoning here — could you walk me through the approach?\" |\n| \"This is inefficient.\" | \"I wonder if we could optimize this with a hash map — it would bring complexity from O(n²) to O(n).\" |\n\n### Nit vs Blocking Comment\n- **Nit**: minor, non-blocking — \"Nit: could we rename this variable to `user_id` for clarity?\"\n- **Blocking**: required to merge — \"This SQL query is vulnerable to injection. Must be parameterized before merge.\"\n- **Suggestion**: optional improvement — \"Suggestion: consider extracting this into a helper function for testability.\"\n\n## Receiving Feedback Professionally\n- ✅ \"Good catch — I'll fix that.\"\n- ✅ \"Thanks for the feedback. I went with X because Y — happy to discuss if you see a better way.\"\n- ✅ \"I see your point. Let me refactor this.\"\n- ❌ Avoid: Defending every comment defensively. Pick your battles.\n\n## Requesting a Code Review\n> \"Hi [Name], when you have time, could you take a look at PR #142? It adds the payment integration. Key changes are in `payment_service.py` and `checkout_api.py`. Happy to walk you through it.\"\n\n## Discussing Changes in Review\n- \"I **refactored** the validation logic to separate concerns.\"\n- \"This **replaces** the previous synchronous approach with async processing.\"\n- \"I **extracted** the database queries into a repository layer.\"\n- \"The **test coverage** for this module is now at 87%.\"\n\n## Example: Leaving a Constructive Comment\n> \"This looks good overall! One thing I noticed: the `get_user` function makes a DB call inside the loop, which could be O(n) queries. Consider batching with `get_users_by_ids(ids)` to make it a single query. Let me know if you'd like to pair on this.\"\n\n## Interview Tip\n\"How do you handle code review feedback you disagree with?\" — say you discuss the reasoning, consider the point, and if genuinely conflicting, escalate to the team. Never say you just accept or just reject feedback.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "Code Review Communication Quiz",
            "description": "Test your code review communication skills.",
            "questions": [
                {"question": "Which comment is most constructive in a code review?", "options": ["This is wrong.", "This could cause a null pointer in the edge case where user is not logged in. Consider adding a guard clause.", "I don't like this.", "Rewrite this."], "correct_answer_index": 1, "explanation": "Good feedback explains the problem, the consequence, and suggests a solution. It's collaborative, not critical.", "order_index": 1},
                {"question": "What does 'nit' mean in a code review?", "options": ["A critical blocking issue", "A minor non-blocking suggestion that won't prevent merging", "A security vulnerability", "A syntax error"], "correct_answer_index": 1, "explanation": "'Nit' (short for nitpick) signals a minor style or preference comment that doesn't block the PR from merging.", "order_index": 2},
                {"question": "How should you respond if you disagree with a reviewer's comment?", "options": ["Reject it immediately.", "Ignore it.", "Explain your reasoning professionally: 'I went with X because Y — happy to discuss.'", "Accept it without question."], "correct_answer_index": 2, "explanation": "Professional responses acknowledge the feedback, share your reasoning, and invite discussion. This builds team trust.", "order_index": 3},
                {"question": "What phrase correctly identifies an N+1 query problem?", "options": ["The database is slow.", "The get_user function makes a DB call inside the loop — this could be O(n) queries. Consider batching with a single query.", "There are too many queries.", "Optimize the database."], "correct_answer_index": 1, "explanation": "Specific language (O(n) queries, inside the loop, batching) shows deep understanding and helps the author fix it quickly.", "order_index": 4},
                {"question": "What phrase correctly describes a structural code change in a PR?", "options": ["I moved some stuff.", "I extracted the database queries into a repository layer to separate concerns.", "Changed it.", "Refactored."], "correct_answer_index": 1, "explanation": "In PR descriptions and reviews, be specific: name what changed, where, and why. 'Repository layer to separate concerns' is clear and professional.", "order_index": 5},
            ],
        },
    },
]

SD_TOPICS = [
    {
        "name": "load_balancing",
        "title": "Load Balancing",
        "description": "Distribute traffic across servers to achieve high availability and performance.",
        "icon_name": "git-branch",
        "order_index": 1,
        "lesson": {
            "title": "Load Balancing: Fundamentals and Strategies",
            "content": "# Load Balancing\n\nA load balancer distributes incoming traffic across multiple backend servers.\n\n## Algorithms\n- **Round Robin** — requests go to each server in turn\n- **Weighted Round Robin** — proportional to server capacity\n- **Least Connections** — route to server with fewest active connections\n- **IP Hash** — sticky sessions based on client IP\n\n## Layer 4 vs Layer 7\n- **L4**: TCP/UDP level, fast, routes by IP/port\n- **L7**: HTTP level, routes by URL/headers/cookies (AWS ALB)\n\n## Health Checks\nLoad balancers ping `/health` periodically. Unhealthy servers are removed from rotation automatically.\n\n## High Availability\nDeploy load balancers in active-active or active-passive pairs to eliminate the single point of failure.\n\n## Session Stickiness\nFor stateful apps, use IP Hash OR (better) externalize session state to Redis.\n\n## Real-World: Netflix\nNetflix uses AWS ELB to distribute streaming requests across thousands of EC2 instances. During peak hours, their load balancers handle millions of concurrent connections.\n\n## Interview Tip\nStart with *why* (horizontal scaling, HA), discuss *algorithms* with trade-offs, always mention *health checks* and the LB's own *redundancy*.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "Load Balancing Quiz",
            "description": "Test your understanding of load balancing fundamentals.",
            "questions": [
                {"question": "Which algorithm routes to the server with fewest active connections?", "options": ["Round Robin", "IP Hash", "Least Connections", "Weighted Round Robin"], "correct_answer_index": 2, "explanation": "Least Connections routes each new request to the server with the fewest active connections — ideal for long-lived connections.", "order_index": 1},
                {"question": "What is the main advantage of a Layer 7 load balancer?", "options": ["Faster because it operates at TCP level", "Routes based on HTTP content like URL paths and headers", "Uses less memory than Layer 4", "Does not require SSL certificates"], "correct_answer_index": 1, "explanation": "Layer 7 load balancers understand HTTP and can route based on URL paths, headers, and cookies — enabling content-based routing.", "order_index": 2},
                {"question": "What problem does IP Hash (sticky sessions) solve?", "options": ["Reduces SSL overhead", "Ensures a client always reaches the same backend server", "Improves cache hit rates", "Detects unhealthy servers"], "correct_answer_index": 1, "explanation": "IP Hash routes requests from the same client IP to the same server, maintaining session affinity needed when session state is stored locally.", "order_index": 3},
                {"question": "How does a load balancer detect an unhealthy backend server?", "options": ["Monitors CPU via CloudWatch", "Periodically sends health check requests and looks for a successful response", "Reads error logs from the server", "Checks uptime via SSH"], "correct_answer_index": 1, "explanation": "Load balancers send periodic health check requests to an endpoint. If the server doesn't respond successfully, it's removed from rotation.", "order_index": 4},
                {"question": "What is the recommended approach for sessions in a horizontally scaled app?", "options": ["Use sticky sessions (IP Hash)", "Store session data in a shared external store like Redis", "Disable sessions and use JWTs only", "Replicate session data across all servers"], "correct_answer_index": 1, "explanation": "Storing sessions in Redis allows any backend server to handle any request — the stateless architecture preferred for scalable systems.", "order_index": 5},
            ],
        },
    },
    {
        "name": "caching",
        "title": "Caching Strategies",
        "description": "Speed up systems and reduce database load with effective caching patterns.",
        "icon_name": "zap",
        "order_index": 2,
        "lesson": {
            "title": "Caching Strategies: From Basics to Patterns",
            "content": "# Caching Strategies\n\nCaching stores copies of expensive data in fast storage (memory). Key metric: **cache hit rate**.\n\n## Patterns\n\n### Cache-Aside (Lazy Loading)\nApp checks cache first. On miss, fetches from DB and populates cache.\n- Pros: Only caches what's needed; cache failures don't break the app\n- Cons: First request is slow (cold start); data can be stale\n\n### Write-Through\nEvery write goes to both cache and DB simultaneously.\n- Pros: Cache always fresh\n- Cons: Increased write latency\n\n### Write-Behind (Write-Back)\nWrites go to cache immediately; DB updated asynchronously.\n- Pros: Lowest write latency\n- Cons: Risk of data loss if cache crashes before DB write\n\n## Eviction Policies\n- **LRU** (Least Recently Used) — Redis default\n- **LFU** (Least Frequently Used)\n- **TTL** (Time-To-Live)\n\n## Cache Invalidation\n1. TTL expiry — data eventually expires\n2. Event-driven — explicitly delete/update key on write\n3. Cache busting — include version in key (`user:123:v2`)\n\n## Real-World: Twitter\nTwitter caches timelines in Redis. Your home timeline is pre-computed per user. When someone you follow tweets, fan-out workers push it to each follower's cached timeline.\n\n## Interview Tip\nFor any performance problem, propose caching. Mention cache-aside as default, Redis as default tool, and discuss TTL and invalidation strategy.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Caching Strategies Quiz",
            "description": "Test your knowledge of caching patterns and trade-offs.",
            "questions": [
                {"question": "In cache-aside, what happens on a cache miss?", "options": ["Request fails", "App fetches from DB and stores result in cache", "Load balancer routes to different server", "Cache fetches from DB automatically"], "correct_answer_index": 1, "explanation": "In cache-aside, the application fetches from DB on miss and populates the cache. This is the most common pattern.", "order_index": 1},
                {"question": "Which caching pattern has the lowest write latency?", "options": ["Cache-Aside", "Write-Through", "Write-Behind", "Read-Through"], "correct_answer_index": 2, "explanation": "Write-behind acknowledges the write as soon as data is in cache and updates the DB asynchronously, giving the lowest perceived write latency.", "order_index": 2},
                {"question": "What eviction policy does Redis use by default?", "options": ["FIFO", "LFU", "LRU", "Random"], "correct_answer_index": 2, "explanation": "Redis uses LRU (Least Recently Used) by default — evicting the item not accessed for the longest time when memory is full.", "order_index": 3},
                {"question": "What is the main risk of write-behind caching?", "options": ["Increased write latency", "Cache becomes inconsistent", "Data loss if cache crashes before async DB write", "Database cannot keep up with reads"], "correct_answer_index": 2, "explanation": "Write-behind acknowledges writes before persisting to DB. If the cache crashes between write and DB sync, that data is lost.", "order_index": 4},
                {"question": "What does a cache TTL control?", "options": ["Max items the cache stores", "How long a cached item is kept before automatic expiry", "Time to wait before falling back to DB", "Replication lag between cache nodes"], "correct_answer_index": 1, "explanation": "TTL sets an expiry time on cached items. After expiry, the item is removed, forcing the next request to fetch fresh data.", "order_index": 5},
            ],
        },
    },
    {
        "name": "microservices_sd",
        "title": "Microservices Architecture",
        "description": "Break monoliths into independently deployable services and manage the complexity.",
        "icon_name": "puzzle",
        "order_index": 3,
        "lesson": {
            "title": "Microservices Architecture: Principles and Patterns",
            "content": "# Microservices Architecture\n\nMicroservices is an architectural style where an application is built as a collection of small, independently deployable services. Each service owns its own database and communicates over the network.\n\n## Monolith vs Microservices\n\n| Aspect | Monolith | Microservices |\n|--------|----------|---------------|\n| Deployment | Single unit | Independent per service |\n| Scaling | Scale the whole app | Scale only bottleneck |\n| Fault isolation | One bug can crash all | Failures contained |\n\n## Key Patterns\n\n### API Gateway\nSingle entry point for all client requests. Handles auth, rate limiting, logging.\n\n### Circuit Breaker\nIf Service B is failing, Service A stops calling it and returns a fallback. Prevents cascading failures.\n\n### Saga Pattern\nManage distributed transactions. Each step publishes an event; compensating transactions undo previous steps on failure.\n\n### Event-Driven Communication\nServices communicate via events (Kafka, SQS). Decoupled and async.\n\n## When to Use Microservices\n- Teams are large and stepping on each other\n- Different parts need wildly different scaling\n- Need independent deployment cycles\n- You have CI/CD and monitoring maturity\n\n## When NOT to Use\n- Building an MVP\n- Team is small (< 5 engineers)\n- Domain boundaries are unclear\n\n## Real-World: Amazon\nJeff Bezos mandated all teams expose data via APIs. Amazon decomposed into thousands of microservices. The checkout button calls ~150 services.\n\n## Interview Tip\nAlways address: service boundaries (DDD), communication (sync REST/gRPC vs async events), data management (each service owns its DB), and operational complexity.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Microservices Architecture Quiz",
            "description": "Test your understanding of microservices principles and patterns.",
            "questions": [
                {"question": "What is the 'database per service' pattern?", "options": ["All microservices share one central database", "Each microservice owns and manages its own database", "Databases are replicated across all services", "Services use read replicas of a primary database"], "correct_answer_index": 1, "explanation": "Each microservice owns its own database, enabling independent schema changes, technology choices, and scaling.", "order_index": 1},
                {"question": "What problem does the Circuit Breaker pattern solve?", "options": ["Service discovery in dynamic environments", "Distributed transaction consistency", "Preventing cascading failures when a downstream service is unavailable", "Balancing load across service instances"], "correct_answer_index": 2, "explanation": "The circuit breaker detects repeated failures and 'opens' — stopping calls to the failing service and returning fallback responses.", "order_index": 2},
                {"question": "What is an API Gateway responsible for?", "options": ["Storing shared configuration", "Acting as the single entry point for clients, handling routing, auth, and rate limiting", "Managing database connections", "Deploying new versions automatically"], "correct_answer_index": 1, "explanation": "The API Gateway is the single entry point for all client requests. It routes to the right service and handles cross-cutting concerns.", "order_index": 3},
                {"question": "When should you NOT use microservices?", "options": ["When you have 100+ engineers", "When services need to scale independently", "When building an MVP with a small team", "When you need independent deployment cycles"], "correct_answer_index": 2, "explanation": "Microservices add significant operational complexity. For MVPs or small teams, the overhead outweighs the benefits.", "order_index": 4},
                {"question": "What is the Saga pattern used for?", "options": ["Routing HTTP requests", "Managing distributed transactions across multiple services without two-phase commit", "Caching API responses", "Discovering service instances"], "correct_answer_index": 1, "explanation": "Sagas handle distributed transactions via local transactions with compensating transactions to undo on failure, maintaining eventual consistency.", "order_index": 5},
            ],
        },
    },
    {
        "name": "database_scaling_sd",
        "title": "Database Scaling",
        "description": "Scale relational and NoSQL databases to handle millions of users.",
        "icon_name": "database",
        "order_index": 4,
        "lesson": {
            "title": "Database Scaling: Sharding, Replication, and Partitioning",
            "content": "# Database Scaling\n\nA single PostgreSQL instance maxes out around 100,000 queries/second. Beyond that, you must scale.\n\n## Read Replicas\nOne primary handles writes; multiple replicas handle reads.\n- AWS: RDS Read Replicas, Aurora with up to 15 replicas\n- Trade-off: Replicas may be slightly behind (replication lag)\n\n## Sharding (Horizontal Partitioning)\nSplit data across multiple servers. Each shard holds a subset.\n\n**Strategies:**\n- **Range-based**: A-M → Shard 1, N-Z → Shard 2. Simple but creates hotspots.\n- **Hash-based**: `shard_id = hash(user_id) % num_shards`. Even distribution but hard to rebalance.\n- **Directory-based**: Lookup table maps each record to its shard.\n\n**Challenges:** Cross-shard queries are expensive, re-sharding is complex.\n\n## Vertical Partitioning\nSplit a table into multiple tables with fewer columns. Hot path reads from the smaller table.\n\n## Connection Pooling\nUse PgBouncer or HikariCP to reuse connections. Without it, 10K concurrent users = 10K open DB connections → database crashes.\n\n## Real-World: Instagram\nInstagram shards user data across thousands of PostgreSQL shards. `shard_id = user_id % num_shards`.\n\n## Interview Tip\nWalk through the progression: 1) Optimize queries + indexes, 2) Vertical scale, 3) Read replicas, 4) Caching (Redis), 5) Sharding as last resort.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Database Scaling Quiz",
            "description": "Test your knowledge of database scaling techniques.",
            "questions": [
                {"question": "What is the purpose of read replicas?", "options": ["To shard data across multiple servers", "To provide automatic failover", "To offload read traffic from the primary database", "To cache query results"], "correct_answer_index": 2, "explanation": "Read replicas receive a copy of all data from the primary. Read queries go to replicas, reducing primary load.", "order_index": 1},
                {"question": "What is a major drawback of hash-based sharding?", "options": ["Creates hotspots with uneven distribution", "Re-sharding when adding servers requires moving large amounts of data", "Requires a central lookup table", "Only works with NoSQL"], "correct_answer_index": 1, "explanation": "When you add/remove shards, the hash function changes and most data needs to be moved. Consistent hashing mitigates this but adds complexity.", "order_index": 2},
                {"question": "What problem does a connection pooler like PgBouncer solve?", "options": ["Replicating data across servers", "Distributing queries automatically", "Reusing database connections to avoid overhead", "Encrypting connections"], "correct_answer_index": 2, "explanation": "Connection poolers maintain a pool of open connections and reuse them, allowing thousands of app threads to share a smaller number of actual DB connections.", "order_index": 3},
                {"question": "In what order should you approach database scaling?", "options": ["Shard immediately → caching → replicas", "Optimize queries → vertical scale → read replicas → caching → sharding", "Move to NoSQL → replicas → shard", "Add caching → shard → replicas"], "correct_answer_index": 1, "explanation": "Start with least complex approaches. Sharding is last resort because it adds significant operational complexity.", "order_index": 4},
                {"question": "What is the key challenge with cross-shard queries?", "options": ["Sharded DBs don't support SQL", "You can't JOIN across shards without additional coordination", "Cross-shard queries always return stale data", "Each shard must be queried sequentially"], "correct_answer_index": 1, "explanation": "SQL joins require data on the same server. Cross-shard joins must be done in application code — complex and slow.", "order_index": 5},
            ],
        },
    },
    {
        "name": "cap_theorem_sd",
        "title": "CAP Theorem",
        "description": "Understand the fundamental trade-offs in distributed systems.",
        "icon_name": "triangle-alert",
        "order_index": 5,
        "lesson": {
            "title": "CAP Theorem: Distributed Systems Trade-offs",
            "content": "# CAP Theorem\n\nIn a distributed system, you can guarantee only **two of three** properties:\n- **C — Consistency**: Every read returns the most recent write or an error\n- **A — Availability**: Every request receives a non-error response\n- **P — Partition Tolerance**: System operates even if network partitions occur\n\n## The Key Insight\nNetwork partitions are unavoidable in real distributed systems. So the real choice is **CP vs AP**.\n\n## CP Systems\nDuring partition, refuse to serve stale data — return error or time out.\n- **Examples**: HBase, Zookeeper, MongoDB (default)\n- **Use when**: Financial transactions, inventory, bookings\n\n## AP Systems\nDuring partition, continue serving requests but may return stale data.\n- **Examples**: Cassandra, DynamoDB (default), CouchDB\n- **Use when**: Social feeds, product catalogs, recommendations\n\n## Eventual Consistency\nAP systems provide *eventual consistency*: given enough time, all nodes converge to the same value. The window is usually milliseconds to seconds.\n\n## PACELC\nExtends CAP: even without partitions, there's a trade-off between **Latency** and **Consistency**.\n\n## Real-World: Amazon DynamoDB\nDynamoDB offers both strong and eventual consistency per request. Default is eventual (higher throughput). For financial ops, opt into strongly consistent reads.\n\n## Interview Tip\nWhen discussing any DB choice, mention CAP. Show it's an intentional trade-off driven by business requirements, not a flaw.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "CAP Theorem Quiz",
            "description": "Test your understanding of CAP theorem and distributed system trade-offs.",
            "questions": [
                {"question": "In CAP theorem, what does 'Consistency' mean?", "options": ["The system is always available", "Every read receives the most recent write or an error", "The system tolerates network partitions", "Data is replicated across nodes"], "correct_answer_index": 1, "explanation": "CAP Consistency means every read returns the most recent write — all nodes have the same data. This is not the same as ACID consistency.", "order_index": 1},
                {"question": "Why must real distributed systems always choose Partition Tolerance?", "options": ["It gives best performance", "Network partitions are unavoidable in distributed systems", "Consistency and Availability can't coexist", "Required by cloud providers"], "correct_answer_index": 1, "explanation": "Networks fail. In any real distributed system, you will experience network partitions. Giving up P would mean a single network glitch brings down the entire system.", "order_index": 2},
                {"question": "Which is an example of a CP system?", "options": ["Amazon DynamoDB (default)", "Apache Cassandra", "Apache Zookeeper", "CouchDB"], "correct_answer_index": 2, "explanation": "Zookeeper is CP — it will refuse requests during a partition rather than serve stale data. Used for distributed coordination where consistency is critical.", "order_index": 3},
                {"question": "What does 'eventual consistency' mean?", "options": ["System will eventually crash if inconsistencies aren't resolved", "All nodes will eventually have the same data if no new updates occur", "Consistency is guaranteed after a fixed time", "Writes are batched at intervals"], "correct_answer_index": 1, "explanation": "Eventual consistency guarantees that if no new updates are made, all replicas will converge to the same value over time — typically milliseconds to seconds.", "order_index": 4},
                {"question": "For which use case would you choose an AP system?", "options": ["Processing bank transfers", "Airline seat reservations", "Displaying social media feeds", "Recording medical prescriptions"], "correct_answer_index": 2, "explanation": "Social media feeds can tolerate slightly stale content — availability matters more than perfect freshness. Financial and medical systems require strong consistency.", "order_index": 5},
            ],
        },
    },
    {
        "name": "message_queue_sd",
        "title": "Message Queues",
        "description": "Decouple services and handle async workloads with message queuing systems.",
        "icon_name": "mail",
        "order_index": 6,
        "lesson": {
            "title": "Message Queues: Async Communication in Distributed Systems",
            "content": "# Message Queues\n\nA message queue enables **asynchronous service-to-service communication**. The producer sends a message; the consumer reads and processes it independently.\n\n## When to Use Queues\n- High traffic spikes: queue buffers requests\n- Long-running tasks: don't block HTTP responses (email, image resizing)\n- Decoupled services: services don't need to know about each other\n- Reliability: if consumer is down, messages wait in queue\n\n## Queue vs Pub/Sub\n- **Queue**: Each message consumed by exactly one consumer (AWS SQS, RabbitMQ)\n- **Pub/Sub**: Each message delivered to all subscribers (AWS SNS, Kafka)\n\n## Apache Kafka\nDistributed log/streaming platform. Key concepts:\n- **Topic**: Category of messages (persistent, replayable)\n- **Partition**: Topics split into partitions for parallelism\n- **Consumer Group**: Multiple consumers share work on a topic\n- **Retention**: Messages persist for configurable duration (default 7 days)\n\nKafka throughput: millions of messages/second. LinkedIn processes 7 trillion messages/day on Kafka.\n\n## SQS vs Kafka\n| Feature | SQS | Kafka |\n|---------|-----|-------|\n| Retention | 4 days max | Configurable |\n| Replay | No | Yes |\n| Use case | Task queues | Event streaming |\n\n## Real-World: Uber\nWhen you book an Uber, Kafka publishes 'TripRequested'. Driver matching, payment, ETA, notifications all consume it independently.\n\n## Interview Tip\nFor emails, image processing, payments, or long-running tasks — immediately propose a message queue. Show you know SQS (task queue) vs Kafka (event streaming).",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 11,
        },
        "quiz": {
            "title": "Message Queues Quiz",
            "description": "Test your understanding of message queues and async communication.",
            "questions": [
                {"question": "What is the main difference between a queue and pub/sub?", "options": ["Queues are faster; pub/sub more reliable", "In queues one consumer gets each message; in pub/sub all subscribers get it", "Queues are for real-time; pub/sub for batch", "Pub/sub requires acknowledgment; queues don't"], "correct_answer_index": 1, "explanation": "Queues distribute messages to one consumer (work distribution). Pub/sub broadcasts each message to all subscribers (event notification).", "order_index": 1},
                {"question": "What major advantage does Kafka have over SQS for event streaming?", "options": ["Kafka is cheaper for small workloads", "Kafka messages can be replayed by consumers", "Kafka provides stronger ordering guarantees", "Kafka requires no infrastructure management"], "correct_answer_index": 1, "explanation": "Kafka retains messages for configurable duration, allowing consumers to re-read or replay the stream. SQS deletes messages after consumption.", "order_index": 2},
                {"question": "When is a message queue the right design choice?", "options": ["When the consumer must respond within 100ms", "When you need to process tasks async to avoid blocking the user", "When services need to share a database", "When you need lowest possible latency"], "correct_answer_index": 1, "explanation": "Message queues are ideal for async tasks — sending emails, resizing images, processing payments. They prevent the HTTP request from blocking on slow operations.", "order_index": 3},
                {"question": "What happens to messages when the consumer is temporarily down?", "options": ["Messages are dropped to prevent overflow", "Sent to a backup consumer", "Retained in the queue until the consumer recovers", "Producer automatically retries directly"], "correct_answer_index": 2, "explanation": "Messages persist in the queue while the consumer is offline. When it recovers, it processes the backlog. No messages are lost.", "order_index": 4},
                {"question": "What is a Kafka partition?", "options": ["A separate Kafka cluster", "A subset of a topic's messages that enables parallelism", "A backup copy for fault tolerance", "A consumer group reading multiple topics"], "correct_answer_index": 1, "explanation": "Kafka topics are split into partitions. Each partition can be consumed by one consumer in a group simultaneously, enabling parallel processing.", "order_index": 5},
            ],
        },
    },
    {
        "name": "api_gateway_sd",
        "title": "API Gateway",
        "description": "Design the entry point for your microservices with routing, auth, and rate limiting.",
        "icon_name": "shield",
        "order_index": 7,
        "lesson": {
            "title": "API Gateway: The Front Door of Your Microservices",
            "content": "# API Gateway\n\nThe API Gateway is a server acting as the **single entry point** for all client requests.\n\n## Core Responsibilities\n- **Routing**: Direct requests to the correct microservice\n- **Authentication & Authorization**: Validate JWT tokens or API keys\n- **Rate Limiting**: Prevent abuse\n- **SSL Termination**: Decrypt HTTPS at the gateway\n- **Request/Response Transformation**: Translate between formats\n- **Logging & Monitoring**: Centralized observability\n- **Caching**: Cache common responses\n\n## Gateway vs Load Balancer\n| Aspect | Load Balancer | API Gateway |\n|--------|---------------|-------------|\n| Layer | L4 or L7 | L7 always |\n| Auth | No | Yes |\n| Rate Limiting | No | Yes |\n| Transform | No | Yes |\n\n## Rate Limiting Strategies\n- **Token Bucket**: Allows bursts. Each user has N tokens, refills at rate R.\n- **Leaky Bucket**: Processes at constant rate. Smooths bursts.\n- **Fixed Window**: N requests per time window. Simple but boundary problem.\n- **Sliding Window**: Smoothed rate, no boundary spikes.\n\n## Popular Gateways\n- **AWS API Gateway**: Fully managed, serverless\n- **Kong**: Open-source, plugin-rich\n- **Traefik**: Container-native, Kubernetes-friendly\n\n## Real-World: Netflix\nNetflix's Zuul gateway handles all API traffic — authentication, routing to 100+ microservices, circuit breaking, A/B testing, and canary deployments.\n\n## Interview Tip\nDraw the API Gateway as the first component clients interact with. Cross-cutting concerns (auth, rate limiting, logging) are handled once at the gateway, not in every service.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "API Gateway Quiz",
            "description": "Test your knowledge of API Gateway patterns.",
            "questions": [
                {"question": "What is the primary role of an API Gateway?", "options": ["Store shared data between microservices", "Act as single entry point handling routing and cross-cutting concerns", "Replace the load balancer", "Manage database connections"], "correct_answer_index": 1, "explanation": "The API Gateway is the single entry point for all external traffic. It routes requests and handles auth, rate limiting, and logging centrally.", "order_index": 1},
                {"question": "Which rate limiting strategy allows short traffic bursts?", "options": ["Fixed Window", "Leaky Bucket", "Token Bucket", "Sliding Window"], "correct_answer_index": 2, "explanation": "Token bucket allows bursting — if tokens have accumulated, a user can make several rapid requests until the bucket is empty.", "order_index": 2},
                {"question": "What is SSL termination at the API Gateway?", "options": ["Blocking non-HTTPS traffic", "Decrypting HTTPS at the gateway so internal services use plain HTTP", "Renewing SSL certificates automatically", "Forwarding certificates to each service"], "correct_answer_index": 1, "explanation": "SSL termination means the gateway handles HTTPS decryption. Internal service-to-service communication uses plain HTTP, reducing CPU overhead.", "order_index": 3},
                {"question": "Why does an API Gateway reduce duplication in microservices?", "options": ["Shares a single database", "Cross-cutting concerns like auth are implemented once at the gateway", "Generates client SDKs automatically", "Combines multiple service deployments"], "correct_answer_index": 1, "explanation": "Without a gateway, every microservice implements authentication, rate limiting, and logging. The gateway centralizes these.", "order_index": 4},
                {"question": "What is canary deployment via an API Gateway?", "options": ["Routing all traffic to a new version for testing", "Rolling back when errors are detected", "Routing a small % of traffic to a new version while most goes to stable", "Blocking traffic from specific regions"], "correct_answer_index": 2, "explanation": "Canary deployment routes a small % (e.g., 5%) to a new service version. If metrics look good, gradually increase. The API Gateway controls this routing.", "order_index": 5},
            ],
        },
    },
    {
        "name": "cdn_sd",
        "title": "Content Delivery Networks",
        "description": "Serve static assets and reduce latency globally with CDNs.",
        "icon_name": "globe",
        "order_index": 8,
        "lesson": {
            "title": "Content Delivery Networks: Global Performance at Scale",
            "content": "# Content Delivery Networks (CDN)\n\nA CDN is a geographically distributed network of servers (Points of Presence/PoPs) that cache and serve content closer to users.\n\n## How CDNs Work\n1. User requests `cdn.example.com/logo.png`\n2. DNS resolves to the nearest PoP\n3. **Cache hit**: PoP serves instantly\n4. **Cache miss**: PoP fetches from origin, caches it, serves user\n5. Next user at the same PoP gets a cache hit\n\n## What CDNs Cache\n- Static assets: images, CSS, JS, fonts, videos\n- API responses (with proper Cache-Control headers)\n- CDNs do NOT cache: authenticated pages, POST requests, personalized content\n\n## Benefits\n- 50-300ms latency improvement for global users\n- 80-95% of requests served from cache\n- DDoS protection\n- Reduced origin bandwidth cost\n\n## Cache Invalidation\n1. **URL versioning (best)**: `main.a3f9b2.js` — new content = new URL\n2. **CDN invalidation API**: Manually purge URLs (CloudFront charges per invalidation)\n3. **TTL expiry**: Wait for TTL. Stale until then.\n\n## Cache-Control\n```\nCache-Control: public, max-age=86400\n```\n- `public`: Can be cached by CDN\n- `max-age=86400`: Cache for 24 hours\n\n## Popular CDNs\n- **AWS CloudFront**: Tight S3/EC2 integration, 450+ PoPs\n- **Cloudflare**: Security-focused, free tier\n- **Fastly**: Programmatic cache control\n\n## Interview Tip\nFor any global system, mention CDN immediately. 'We'll put a CDN in front of S3 for static assets and in front of our API for cacheable responses — reduces latency and cuts origin load by ~90%.'",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "Content Delivery Networks Quiz",
            "description": "Test your knowledge of CDN concepts and usage patterns.",
            "questions": [
                {"question": "What happens during a CDN cache miss?", "options": ["CDN returns 404", "CDN fetches from origin, caches it, and serves the user", "CDN redirects user to origin", "Request is queued"], "correct_answer_index": 1, "explanation": "On cache miss, the CDN PoP fetches from your origin, stores it in local cache, and serves the user. Subsequent requests from that PoP are cache hits.", "order_index": 1},
                {"question": "What is the best cache invalidation strategy for JS bundles?", "options": ["Very short TTL (60s)", "Use CDN invalidation API after every deploy", "Include a content hash in the file URL", "Disable caching for JS files"], "correct_answer_index": 2, "explanation": "Content-hashed URLs (main.a3f9b2.js) are best — new content = new URL = new cache entry. Allows very long TTLs with instant updates.", "order_index": 2},
                {"question": "Which requests are NOT cached by CDNs by default?", "options": ["Image files and CSS", "JavaScript bundles", "POST requests and authenticated pages with private content", "Public API responses with Cache-Control headers"], "correct_answer_index": 2, "explanation": "CDNs don't cache POST requests or responses with Cache-Control: private (personalized content that shouldn't be shared between users).", "order_index": 3},
                {"question": "How does a CDN reduce load on the origin server?", "options": ["Compresses requests before forwarding", "Batches multiple requests into one", "Serves cached content from PoPs so most requests never reach origin", "Runs application code at the edge"], "correct_answer_index": 2, "explanation": "With high cache hit rates (80-95%), most requests are served from CDN PoPs. Only cache misses hit your origin.", "order_index": 4},
                {"question": "What does `Cache-Control: public, max-age=86400` mean?", "options": ["Private, browser-only cache for 86400s", "Can be cached by CDNs and browsers for 24 hours", "CDN must revalidate every 86400s", "Only 86400 users can cache this"], "correct_answer_index": 1, "explanation": "`public` means CDNs can cache it. `max-age=86400` sets the TTL to 86400 seconds (24 hours).", "order_index": 5},
            ],
        },
    },
    {
        "name": "sql_vs_nosql_sd",
        "title": "SQL vs NoSQL",
        "description": "Choose the right database type for your use case.",
        "icon_name": "table-2",
        "order_index": 9,
        "lesson": {
            "title": "SQL vs NoSQL: Choosing the Right Database",
            "content": "# SQL vs NoSQL\n\n## SQL (Relational)\nStores data in tables with enforced schema. Supports ACID transactions.\n**Examples**: PostgreSQL, MySQL, AWS RDS\n**Use when**: Complex queries with JOINs, ACID required, structured data, financial/medical data.\n\n## NoSQL Types\n\n### Document Stores (MongoDB, DynamoDB)\nJSON-like documents. Flexible schema per document.\n**Use for**: User profiles, product catalogs, content management.\n\n### Key-Value (Redis, DynamoDB)\nSimple: key → value. Extremely fast.\n**Use for**: Caching, sessions, leaderboards.\n\n### Column Family (Cassandra, HBase)\nOptimized for write-heavy workloads, time-series.\n**Use for**: IoT, analytics, event logs.\n\n### Graph (Neo4j, Amazon Neptune)\nOptimized for highly connected data.\n**Use for**: Social networks, recommendations, fraud detection.\n\n## When to Choose SQL\n- Complex queries and JOINs needed\n- ACID transactions required (payments, bookings)\n- Scale < 10TB, < 100K writes/sec\n\n## When to Choose NoSQL\n- Massive scale (millions of writes/sec)\n- Flexible, evolving schema\n- Simple access patterns (lookup by key)\n- High write throughput needed\n\n## The Hybrid Approach\nNetflix uses MySQL (billing), Cassandra (viewing history), Redis (caching), Elasticsearch (search).\n\n## Interview Tip\nNever say 'it depends' without explaining. Default to PostgreSQL. Choose Cassandra for massive write throughput, MongoDB for flexible schema, DynamoDB for serverless scale-to-zero.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 11,
        },
        "quiz": {
            "title": "SQL vs NoSQL Quiz",
            "description": "Test your understanding of database type trade-offs.",
            "questions": [
                {"question": "What is a key advantage of SQL over most NoSQL databases?", "options": ["Scales horizontally more easily", "Supports ACID transactions for strong consistency", "Handles unstructured data better", "Lower latency for key-value lookups"], "correct_answer_index": 1, "explanation": "SQL databases are built around ACID transactions. This makes them ideal for financial, medical, and booking systems.", "order_index": 1},
                {"question": "Which NoSQL type is optimized for highly connected data like social networks?", "options": ["Document Store", "Key-Value Store", "Column Family", "Graph Database"], "correct_answer_index": 3, "explanation": "Graph databases (Neo4j, Amazon Neptune) are optimized for traversing relationships — native operations that would require dozens of SQL JOINs.", "order_index": 2},
                {"question": "When would you choose Cassandra over PostgreSQL?", "options": ["When you need complex JOINs", "When you need ACID transactions for payments", "When you need millions of writes per second", "When your data has a fixed schema"], "correct_answer_index": 2, "explanation": "Cassandra is designed for massive write throughput and linear horizontal scalability, sacrificing ACID and JOINs.", "order_index": 3},
                {"question": "What is the main advantage of a document store like MongoDB?", "options": ["Faster SQL execution", "Enforces strict schema validation", "Flexible schema allows different documents to have different fields", "Better support for complex JOINs"], "correct_answer_index": 2, "explanation": "Document stores allow each document to have a different structure — ideal for product catalogs or user profiles with optional/varying fields.", "order_index": 4},
                {"question": "For a new fintech application requiring financial transactions, what is the best default DB?", "options": ["MongoDB, because it's flexible", "Cassandra, for high write throughput", "Redis, because it's fast", "PostgreSQL, for ACID transactions and strong consistency"], "correct_answer_index": 3, "explanation": "Financial transactions require ACID guarantees. PostgreSQL is the industry default for financial data due to strong consistency and mature tooling.", "order_index": 5},
            ],
        },
    },
    {
        "name": "rate_limiting_sd",
        "title": "Rate Limiting",
        "description": "Protect your APIs from abuse and ensure fair usage.",
        "icon_name": "gauge",
        "order_index": 10,
        "lesson": {
            "title": "Rate Limiting: Protecting APIs at Scale",
            "content": "# Rate Limiting\n\nRate limiting controls the **number of requests a client can make** in a given time period.\n\n## Why Rate Limit?\n- DDoS protection\n- Fair usage enforcement\n- Cost control\n- Business model (free tier vs paid)\n- Downstream protection\n\n## Algorithms\n\n### Fixed Window Counter\nCount requests per time window (100 req/minute).\n**Problem**: Client can make 100 at 11:59 and 100 at 12:00 — 200 in 2 seconds.\n\n### Token Bucket\nClient has N tokens; each request costs 1 token; tokens refill at rate R. Allows bursting.\nUsed by Twitter for API rate limiting.\n\n### Leaky Bucket\nRequests processed at constant rate. Smooths bursts. Good for payment processing.\n\n### Sliding Window\nApproximate sliding window using weighted fixed counters. Accurate without full log overhead.\n\n## Implementation\n**API Gateway preferred** — centralized, stops traffic before reaching services.\n\n**Redis-based distributed**: All gateway instances share counters in Redis.\n```\nkey = f\"rate:{user_id}\"\ncount = redis.incr(key)\nif count == 1: redis.expire(key, 60)\nif count > LIMIT: return 429\n```\n\n## HTTP Response\n```\nHTTP 429 Too Many Requests\nRetry-After: 30\nX-RateLimit-Limit: 100\nX-RateLimit-Remaining: 0\n```\n\n## Real-World: GitHub API\n5,000 requests/hour for authenticated users, 60 for anonymous. Returns X-RateLimit-* headers on every response.\n\n## Interview Tip\nCover: 1) Algorithm (token bucket — allows bursting), 2) Where (API Gateway + Redis), 3) Client communication (429 + Retry-After). Set different limits per user tier and endpoint.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "Rate Limiting Quiz",
            "description": "Test your knowledge of rate limiting algorithms and implementation.",
            "questions": [
                {"question": "What HTTP status code should a rate-limited request receive?", "options": ["400 Bad Request", "401 Unauthorized", "429 Too Many Requests", "503 Service Unavailable"], "correct_answer_index": 2, "explanation": "HTTP 429 Too Many Requests is the standard status code for rate limiting. Include Retry-After and X-RateLimit headers.", "order_index": 1},
                {"question": "What is the 'burst' problem with fixed window rate limiting?", "options": ["Counter resets too frequently", "A client can make double the allowed requests across a window boundary", "Doesn't account for burst traffic", "Doesn't work in distributed systems"], "correct_answer_index": 1, "explanation": "With 100 req/minute, a client can make 100 at 11:59:59 and 100 at 12:00:00 — 200 requests in 2 seconds. Both windows are technically 'fresh'.", "order_index": 2},
                {"question": "Why is Redis used for distributed rate limiting?", "options": ["Redis provides strong ACID for counters", "All API gateway instances can share the same counters in Redis", "Redis automatically implements token bucket", "Redis rate limiting is built into AWS API Gateway"], "correct_answer_index": 1, "explanation": "When multiple API gateway instances handle traffic, they need to share the same request count per user. Redis provides a shared atomic counter.", "order_index": 3},
                {"question": "Which algorithm allows short bursts of requests?", "options": ["Fixed Window", "Leaky Bucket", "Token Bucket", "Sliding Window Counter"], "correct_answer_index": 2, "explanation": "Token bucket allows bursting. If a user hasn't made requests recently, their bucket accumulates tokens and they can make many requests quickly.", "order_index": 4},
                {"question": "Where is the best place to implement rate limiting in microservices?", "options": ["In each service independently", "At the database layer", "At the API Gateway, centrally", "In the client application"], "correct_answer_index": 2, "explanation": "Implementing at the API Gateway centralizes the logic — you avoid duplicating it in every service. Abusive traffic is stopped before reaching microservices.", "order_index": 5},
            ],
        },
    },
    {
        "name": "distributed_transactions_sd",
        "title": "Distributed Transactions",
        "description": "Maintain data consistency across multiple services and databases.",
        "icon_name": "git-merge",
        "order_index": 11,
        "lesson": {
            "title": "Distributed Transactions: Consistency Across Services",
            "content": "# Distributed Transactions\n\nIn microservices, each service has its own database. How do you ensure an operation spanning multiple services is atomic?\n\n## Two-Phase Commit (2PC)\nCoordinator asks all participants to 'prepare' (lock resources). If all yes → commit. If any no → abort.\n\n**Problems**: Slow (two round trips), blocking (if coordinator crashes, participants hold locks), poor availability. **Rarely used in modern systems.**\n\n## The Saga Pattern\nBreak the transaction into local transactions. Each step publishes an event. On failure, **compensating transactions** undo previous steps.\n\n### Choreography Saga\nServices react to events independently — no central coordinator.\n```\nOrderService → publishes 'OrderCreated'\nInventoryService → reserves stock → publishes 'StockReserved'\nPaymentService → charges card → publishes 'PaymentCompleted'\n```\nOn failure: service publishes 'XFailed' → other services listen and compensate.\n\n### Orchestration Saga\nCentral orchestrator directs each step explicitly.\n\n## Outbox Pattern\nProblem: How to atomically save to DB AND publish an event?\n\nSolution: Write the event to an **outbox table** in the same DB transaction. A separate process reads and publishes.\n```\nBEGIN TRANSACTION\n  INSERT INTO orders (...)\n  INSERT INTO outbox (event='OrderCreated', ...)\nCOMMIT\n-- Separate process reads outbox → publishes to Kafka\n```\n\n## Idempotency\nRetries must not cause duplicate effects. Include an **idempotency key** with each operation. If seen twice, return previous result without re-executing.\n\n## Real-World: Uber Eats\nSaga: Reserve restaurant capacity → Charge payment → Notify driver. On failure, compensating transactions run. Choreography via Kafka events.\n\n## Interview Tip\n'I avoid 2PC due to its blocking nature. I use Saga pattern for business transactions and Outbox pattern for reliable event publishing. I design operations to be idempotent so retries are safe.'",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 13,
        },
        "quiz": {
            "title": "Distributed Transactions Quiz",
            "description": "Test your understanding of distributed transaction patterns.",
            "questions": [
                {"question": "What is the main problem with 2PC in distributed systems?", "options": ["Requires same database per service", "Blocking — if coordinator fails, participants hold locks indefinitely", "Cannot handle more than two services", "Does not support rollback"], "correct_answer_index": 1, "explanation": "2PC is blocking. After voting 'yes', participants hold resource locks and wait for the coordinator. If coordinator crashes, they're stuck.", "order_index": 1},
                {"question": "What is a compensating transaction?", "options": ["A transaction that speeds up the main one", "An action that undoes a previously completed step when a later step fails", "A cross-service database transaction", "A retry mechanism"], "correct_answer_index": 1, "explanation": "Compensating transactions undo the effect of a previous step. If payment fails, the compensating transaction for 'reserve inventory' is 'release inventory'.", "order_index": 2},
                {"question": "What problem does the Outbox Pattern solve?", "options": ["Cross-service JOINs", "Atomically saving to DB AND publishing an event", "Coordinating distributed transactions without a coordinator", "Replaying failed events"], "correct_answer_index": 1, "explanation": "The Outbox pattern solves the dual-write problem. Writing the event to an outbox table in the same DB transaction guarantees both happen together.", "order_index": 3},
                {"question": "What does 'idempotency' mean?", "options": ["Operations complete within guaranteed time", "Performing the same operation multiple times produces the same result as once", "Operations distributed evenly across instances", "Each service maintains its own transaction log"], "correct_answer_index": 1, "explanation": "Idempotency means you can safely retry an operation. If 'charge customer $50' is retried, it checks if already charged (via idempotency key) and doesn't charge again.", "order_index": 4},
                {"question": "What is the difference between choreography and orchestration sagas?", "options": ["Choreography uses SQL; orchestration uses NoSQL", "In choreography services react to events independently; in orchestration a coordinator directs each step", "Orchestration is faster; choreography is more consistent", "Choreography requires 2PC; orchestration does not"], "correct_answer_index": 1, "explanation": "Choreography: decentralized, services react to events. Orchestration: central orchestrator tells each service what to do. Choreography is more decoupled; orchestration easier to trace.", "order_index": 5},
            ],
        },
    },
    {
        "name": "event_driven_sd",
        "title": "Event-Driven Architecture",
        "description": "Build reactive, decoupled systems with event-driven design patterns.",
        "icon_name": "radio",
        "order_index": 12,
        "lesson": {
            "title": "Event-Driven Architecture: Building Reactive Systems",
            "content": "# Event-Driven Architecture\n\nIn EDA, components communicate by **producing and consuming events** rather than calling each other directly. An event is an immutable record of something that happened: `OrderPlaced`, `UserRegistered`.\n\n## Benefits\n- **Loose coupling**: Services don't know about each other — only event schemas\n- **Scalability**: Add consumers without changing producers\n- **Resilience**: Events accumulate if consumer is down\n- **Auditability**: Event log is a complete history\n- **Time travel**: Replay events to rebuild state\n\n## Patterns\n\n### Event Sourcing\nStore state as a sequence of events. To get current state, replay all events.\n```\nEvents: [BalanceSet(100), Deposited(50), Withdrawn(30)]\nBalance = 100 + 50 - 30 = 120\n```\nBenefits: Complete audit log, time travel, event replay.\n\n### CQRS (Command Query Responsibility Segregation)\nSeparate write model (commands) from read model (queries). Events from write side update read side async.\n\n## When to Use EDA\n- Multiple services react to same event\n- Services need to be independently deployable\n- Audit trail required\n- High throughput async processing\n\n## When to Avoid\n- You need synchronous responses (user waiting)\n- Simple request/response is sufficient\n- Team lacks async debugging experience\n\n## Real-World: Netflix\nWhen you play a movie, `PlaybackStarted` triggers: watch history update, recommendation model, view count, billing, analytics — all independently.\n\n## Interview Tip\nPropose EDA when 'multiple services need to react to user actions' or 'we need audit logs'. Show you understand the trade-off: debugging is harder (need distributed tracing) but resilience and scalability improve.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 11,
        },
        "quiz": {
            "title": "Event-Driven Architecture Quiz",
            "description": "Test your understanding of event-driven architecture patterns.",
            "questions": [
                {"question": "What is the main benefit of loose coupling in EDA?", "options": ["Services communicate faster with binary protocols", "Services don't know about each other — only about event schemas", "Events eliminate API versioning", "Consumers can synchronously call each other"], "correct_answer_index": 1, "explanation": "In EDA, producers publish events without knowing who consumes them. New services can be added without modifying existing ones — true loose coupling.", "order_index": 1},
                {"question": "What is Event Sourcing?", "options": ["Storing source code for event handlers", "Fetching events from external webhooks", "Storing state as a sequence of immutable events and deriving current state by replaying them", "Caching event responses for faster replay"], "correct_answer_index": 2, "explanation": "Event Sourcing never overwrites state — it appends events. Current state is computed by replaying all events, providing complete history and time travel.", "order_index": 2},
                {"question": "What does CQRS separate?", "options": ["Sync and async communication", "The write model (commands) from the read model (queries)", "SQL from NoSQL queries", "Caching from persistence"], "correct_answer_index": 1, "explanation": "CQRS separates writes (commands that change state) from reads (queries). The read model is optimized for queries and updated asynchronously from events.", "order_index": 3},
                {"question": "What is a key challenge of debugging event-driven systems?", "options": ["Events cannot be logged", "Tracing a request across multiple async consumers requires distributed tracing tools", "Event consumers must deploy in a specific order", "Events cannot be replayed after failure"], "correct_answer_index": 1, "explanation": "In async EDA, a single action might trigger events consumed by 5 services. Debugging requires distributed tracing (Jaeger, Zipkin, AWS X-Ray) to correlate events.", "order_index": 4},
                {"question": "When should you avoid event-driven architecture?", "options": ["Multiple services react to same user action", "You need a synchronous response (user waiting for result)", "You need a complete audit trail", "Services should be independently deployable"], "correct_answer_index": 1, "explanation": "EDA is asynchronous by nature. If a user submits a payment and needs immediate confirmation, you can't wait for events to propagate.", "order_index": 5},
            ],
        },
    },
    {
        "name": "websocket_sd",
        "title": "WebSockets & Real-time",
        "description": "Build real-time features with WebSockets and Server-Sent Events.",
        "icon_name": "activity",
        "order_index": 13,
        "lesson": {
            "title": "WebSockets & Real-time Communication",
            "content": "# WebSockets & Real-time Communication\n\nTraditional HTTP is request-response. For real-time features, you need the **server to push data to the client** without asking.\n\n## Options\n\n### WebSocket\nFull-duplex, persistent TCP connection. Both sides send at any time. Established via HTTP upgrade.\n**Use for**: Chat, multiplayer games, live collaboration, trading dashboards.\n\n### Server-Sent Events (SSE)\nOne-directional: server pushes to client only. Standard HTTP. Auto-reconnects.\n**Use for**: Live news feeds, notifications, progress updates.\n\n### Long Polling\nClient requests; server holds it until data is available. High overhead. Use as fallback only.\n\n## Scaling WebSockets\n**Challenge**: WebSocket connections are stateful — tied to a specific server. User A on Server 1 can't reach User B on Server 2.\n\n**Solution: Redis Pub/Sub**\n1. Server 1 receives message from A\n2. Server 1 publishes to Redis channel `chat:room:42`\n3. Server 2 (subscribed to that channel) receives it\n4. Server 2 pushes to B's connection\n\n## Socket.IO\nJavaScript library abstracting WebSockets with fallback to long polling. Adds rooms, namespaces, auto-reconnection.\n\n## Real-World: Slack\nSlack uses WebSockets for real-time messaging. Messages go via HTTP POST to API, published to Redis Pub/Sub channel for the workspace, then pushed to all connected clients.\n\n## Interview Tip\nWhen 'real-time' is mentioned, propose WebSockets + Redis Pub/Sub. Distinguish: WebSocket (bidirectional), SSE (unidirectional feeds), Long polling (fallback). Show you understand the horizontal scaling challenge.",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 10,
        },
        "quiz": {
            "title": "WebSockets & Real-time Quiz",
            "description": "Test your understanding of real-time communication patterns.",
            "questions": [
                {"question": "What is the main difference between WebSockets and SSE?", "options": ["WebSockets use HTTP; SSE uses TCP", "WebSockets are bidirectional; SSE is server-to-client only", "SSE supports binary data; WebSockets only text", "WebSockets require dedicated servers"], "correct_answer_index": 1, "explanation": "WebSockets are full-duplex — both sides send messages. SSE is unidirectional — only server can push. Use WebSockets for chat, SSE for notification feeds.", "order_index": 1},
                {"question": "What is the challenge of scaling WebSocket servers horizontally?", "options": ["WebSockets consume too much CPU", "WebSocket connections are stateful — a user is tied to a specific server instance", "WebSockets don't support load balancing", "Horizontal scaling requires shared database"], "correct_answer_index": 1, "explanation": "Each WebSocket connection is tied to the server it connected to. You need a message broker (Redis Pub/Sub) so servers can relay messages to each other's users.", "order_index": 2},
                {"question": "How does Redis Pub/Sub solve the WebSocket scaling problem?", "options": ["Redis stores connection state so any server can resume it", "All WebSocket servers subscribe to Redis channels and fan out messages to their connected clients", "Redis routes connections to the correct server", "Redis acts as a load balancer for WebSocket traffic"], "correct_answer_index": 1, "explanation": "When Server 1 receives a message, it publishes to a Redis channel. All WebSocket servers subscribed to that channel push the message to their connected users.", "order_index": 3},
                {"question": "When would you prefer SSE over WebSockets?", "options": ["For a multiplayer game", "For a live chat application", "For a live news feed where only the server sends data", "For a collaborative document editor"], "correct_answer_index": 2, "explanation": "SSE is simpler when you only need server-to-client data flow. Standard HTTP, built-in auto-reconnection, easier to scale. No need for WebSockets if client doesn't send data.", "order_index": 4},
                {"question": "What HTTP mechanism establishes a WebSocket connection?", "options": ["HTTP POST to a WebSocket endpoint", "HTTP GET with Upgrade: websocket header, switching to WebSocket protocol", "HTTP CONNECT for persistent tunneling", "HTTPS long-lived connection without protocol switching"], "correct_answer_index": 1, "explanation": "WebSocket connections start as HTTP requests with 'Upgrade: websocket' headers. Server responds with HTTP 101 Switching Protocols.", "order_index": 5},
            ],
        },
    },
    {
        "name": "monolith_vs_microservices_sd",
        "title": "Monolith vs Microservices",
        "description": "When to break up a monolith and how to do it safely.",
        "icon_name": "split",
        "order_index": 14,
        "lesson": {
            "title": "Monolith vs Microservices: Making the Right Choice",
            "content": "# Monolith vs Microservices\n\n## The Monolith\nA single deployable unit. How Amazon, Netflix, Airbnb, Shopify started.\n\n**Types**:\n- **Modular monolith**: Single deployable, well-structured internal modules. The best starting point.\n- **Big ball of mud**: Everything intertwined, no boundaries. The nightmare.\n\n**Strengths**: Simple development, easy debugging, no network overhead, simple deploy/rollback.\n\n**Weaknesses**: Must deploy everything to change one line, can't scale components independently, technology lock-in.\n\n## Microservices Reality\nAdded complexity: network failures, distributed tracing needed, multiple CI/CD pipelines, service discovery, distributed transactions.\n\n**Conway's Law**: Organizations design systems that mirror their communication structure. Microservices work when you have independent teams.\n\n## Migration: Strangler Fig Pattern\nDon't rewrite the monolith. Incrementally extract services:\n1. Identify a bounded context with clear seams\n2. Extract it as a service with its own DB\n3. Route traffic to new service via API Gateway\n4. Remove code from monolith\n5. Repeat\n\n## When to Extract a Service\n- A module has dramatically different scaling needs\n- Multiple teams conflict on the same module\n- You want a different technology for a specific component\n- The module has independent data (no cross-boundary JOINs)\n\n## Real-World: Amazon\nStarted as a monolith in 1995. Jeff Bezos issued the 'API Mandate' in 2001. Over the next decade, decomposed into thousands of microservices.\n\n## Interview Tip\nNever say 'microservices are always better.' Show nuance: 'I start with a modular monolith. When teams grow or specific scaling needs emerge, I extract services using the Strangler Fig pattern. Microservices come after product-market fit, not before.'",
            "content_type": LessonContentType.explanation,
            "order_index": 1,
            "estimated_minutes": 12,
        },
        "quiz": {
            "title": "Monolith vs Microservices Quiz",
            "description": "Test your understanding of architecture decision trade-offs.",
            "questions": [
                {"question": "What is the Strangler Fig pattern?", "options": ["Killing unused microservices", "Incrementally replacing a monolith by building new services around it", "A load balancing pattern", "A database migration pattern"], "correct_answer_index": 1, "explanation": "Strangler Fig involves building microservices around the monolith and gradually routing traffic to them. The monolith shrinks piece by piece — avoiding the risk of a full rewrite.", "order_index": 1},
                {"question": "What does Conway's Law state?", "options": ["Systems grow to fill available resources", "Organizations design systems that mirror their communication structure", "Microservices should have one responsibility per service", "Distributed systems always have a point of failure"], "correct_answer_index": 1, "explanation": "Conway's Law: organizations constrained to produce designs that mirror their communication structures. Microservices work when teams are organized around service boundaries.", "order_index": 2},
                {"question": "What is a modular monolith?", "options": ["A monolith deployed across multiple containers", "A single deployable unit with well-defined internal module boundaries", "A monolith using microservices for external dependencies", "A monolith with auto-scaling"], "correct_answer_index": 1, "explanation": "A modular monolith has the simplicity of a single deployable unit but is internally organized with clear module boundaries. Best starting architecture for most products.", "order_index": 3},
                {"question": "When is extracting a microservice clearly justified?", "options": ["When the team reaches 5 developers", "When a module has dramatically different scaling needs than the rest", "When code exceeds 10,000 lines", "When the app is more than 2 years old"], "correct_answer_index": 1, "explanation": "If the image processing module needs 50x more CPU than the rest, extract it as a service and scale independently. This is a genuine technical driver.", "order_index": 4},
                {"question": "What is the most significant added complexity when moving to microservices?", "options": ["More languages must be learned", "Network calls can fail and must be handled with retries, timeouts, and circuit breakers", "Deployment is faster but testing is slower", "DB queries must be rewritten in every service"], "correct_answer_index": 1, "explanation": "In a monolith, service calls are function calls (never fail). In microservices, they cross the network. You must add retries, timeouts, circuit breakers, distributed tracing, and handle partial failures.", "order_index": 5},
            ],
        },
    },
]

SD_SCENARIOS_DATA = [
    {
        "topic_name": "load_balancing",
        "title": "Load Balancing System Design Interview",
        "description": "Practice a system design interview focused on load balancing. Design a globally distributed service handling 500K RPS with 99.99% uptime.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["load-balancing", "system-design", "interview"],
        "order_index": 10,
        "system_prompt": """You are a principal engineer conducting a system design interview. The candidate must design a globally distributed service handling 500K RPS with 99.99% uptime.

Start with: "Let's discuss load balancing. Design the load balancing layer for a service handling 500,000 requests per second globally with 99.99% uptime. Walk me through your approach."

Probe on: Layer 4 vs L7, algorithm choice and why, health check strategy, LB redundancy (active-active), session state with multiple servers, global load balancing (Anycast/GeoDNS), SSL termination.

Push back on vague answers. Be professional but demanding. Stay in character.""",
    },
    {
        "topic_name": "caching",
        "title": "Caching Strategy Design Interview",
        "description": "Design the caching layer for a high-traffic e-commerce platform serving 10M users with real-time inventory.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["caching", "redis", "system-design", "e-commerce"],
        "order_index": 10,
        "system_prompt": """You are a staff engineer at an e-commerce company interviewing for a senior role. Design caching for 10M users, 5M products, real-time inventory that must not oversell.

Start with: "Product pages load 2 seconds, 80% is DB time. 10M users, 5M products, real-time inventory. Design our caching strategy."

Explore: what to cache vs not (inventory vs descriptions), cache-aside vs write-through for different types, TTL strategy, cache stampede prevention for popular products, invalidation on inventory updates, Redis cluster config, how to measure effectiveness. Push for specifics. Stay in character.""",
    },
    {
        "topic_name": "microservices_sd",
        "title": "Microservices Migration Interview",
        "description": "Discuss migrating a monolithic e-commerce platform to microservices with an engineering manager.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["microservices", "architecture", "migration"],
        "order_index": 10,
        "system_prompt": """You are an engineering manager whose team needs to migrate a 5-year-old e-commerce monolith to microservices (orders, users, inventory, payments, notifications).

Start with: "I need you to lead our microservices migration. 3-hour deploys, daily merge conflicts, can't scale payments independently. Where do we start?"

Drive conversation about: assessing the system and service boundaries, migration strategy (Strangler Fig vs big bang), first service to extract and why, handling the single PostgreSQL database, ensuring no downtime, team structure changes needed, success metrics. Ask follow-ups and occasionally push back. Stay in character as a technical-but-not-architect manager.""",
    },
    {
        "topic_name": "cap_theorem_sd",
        "title": "Database Architecture Design Interview",
        "description": "Design the database architecture for a global fintech platform, justifying CAP theorem trade-offs.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.advanced,
        "tags": ["cap-theorem", "databases", "fintech", "interview"],
        "order_index": 10,
        "system_prompt": """You are a senior distributed systems engineer interviewing for a staff engineering role. Challenge: design the database architecture for a global payments platform in 50 countries, 100M users, $50B annual volume.

Start with: "Design the database architecture for a global payments platform. I want you to specifically address CAP theorem trade-offs for different system components."

Probe: consistency requirements for balances vs transaction history vs user profiles vs exchange rates; CP vs AP and why; how to handle money in eventually consistent system (trick — shouldn't, CP for financial); what happens during network partition; DynamoDB strong vs eventual; geographic distribution for cross-region transactions; PACELC. Be technically exacting. Stay in character.""",
    },
    {
        "topic_name": "database_scaling_sd",
        "title": "Database Scaling Crisis Consultation",
        "description": "Your startup's database is struggling under load. Consult a DBA to plan the scaling strategy.",
        "mode": PracticeMode.ai_chat,
        "difficulty": Difficulty.intermediate,
        "tags": ["database-scaling", "postgresql", "performance", "system-design"],
        "order_index": 10,
        "system_prompt": """You are Maria Santos, an experienced DBA consultant. A startup's PostgreSQL is at 95% CPU during peak hours, queries timing out. They grew from 10K to 2M users in 6 months.

Start with: "I've looked at your CloudWatch metrics — 95% CPU, 500ms avg query time, full table scans on orders (50M rows). Tell me about your current setup and what you've already tried."

Guide: assess setup (instance size, indexes, query patterns); low-hanging fruit (missing indexes, N+1 queries); quick wins (instance upgrade, query optimization, connection pooling); read replicas; caching with Redis; partitioning strategy; sharding only if truly needed. Be practical and progressive — don't jump to sharding first. Ask clarifying questions. Stay in character as helpful DBA.""",
    },
]


def seed_english_content(session: Session) -> None:
    """Seed English IT categories and scenarios (original content)."""
    existing = session.exec(select(ScenarioCategory)).first()
    if existing:
        return

    category_map: dict[str, ScenarioCategory] = {}
    for cat_data in CATEGORIES:
        category = ScenarioCategory(**cat_data)
        session.add(category)
        session.flush()
        category_map[cat_data["name"]] = category

    for sc_data in SCENARIOS:
        sc_copy = sc_data.copy()
        category_name = sc_copy.pop("category")
        category = category_map[category_name]
        scenario = Scenario(**sc_copy, category_id=category.id)
        session.add(scenario)

    session.commit()
    print("✅ Seeded English IT categories and scenarios.")


def seed_domains_and_courses(session: Session) -> tuple[dict[str, Domain], dict[str, Course]]:
    """Seed domains and courses. Returns maps for use in subsequent seeds."""
    domain_map: dict[str, Domain] = {}
    for d in DOMAINS_DATA:
        existing = session.exec(select(Domain).where(Domain.slug == d["slug"])).first()
        if existing:
            domain_map[d["slug"]] = existing
        else:
            domain = Domain(**d)
            session.add(domain)
            session.flush()
            domain_map[d["slug"]] = domain
            print(f"✅ Created domain: {d['slug']}")

    course_map: dict[str, Course] = {}
    for c in COURSES_DATA:
        c_copy = c.copy()
        domain_slug = c_copy.pop("domain_slug")
        existing = session.exec(select(Course).where(Course.slug == c_copy["slug"])).first()
        if existing:
            course_map[c_copy["slug"]] = existing
        else:
            domain = domain_map[domain_slug]
            course = Course(**c_copy, domain_id=domain.id)
            session.add(course)
            session.flush()
            course_map[c_copy["slug"]] = course
            print(f"✅ Created course: {c_copy['slug']}")

    session.commit()
    return domain_map, course_map


def seed_link_english_categories(session: Session, course_map: dict[str, Course]) -> None:
    """Link existing English IT scenario categories to the english-it course."""
    english_course = course_map.get("english-it-essentials")
    if not english_course:
        return

    sample = session.exec(
        select(ScenarioCategory).where(ScenarioCategory.course_id == english_course.id)
    ).first()
    if sample:
        return

    for cat_name in [c["name"] for c in CATEGORIES]:
        cat = session.exec(select(ScenarioCategory).where(ScenarioCategory.name == cat_name)).first()
        if cat:
            cat.course_id = english_course.id
            session.add(cat)

    session.commit()
    print("✅ Linked English IT categories to english-it-essentials course.")


def seed_system_design(session: Session, course_map: dict[str, Course]) -> None:
    """Seed 14 System Design topics with lessons and quizzes."""
    sd_course = course_map.get("system-design-fundamentals")
    if not sd_course:
        print("⚠️  system-design-fundamentals course not found, skipping SD seed.")
        return

    existing_sd_cat = session.exec(
        select(ScenarioCategory).where(ScenarioCategory.name == "load_balancing")
    ).first()
    if existing_sd_cat:
        print("ℹ️  System design topics already seeded, skipping.")
        return

    category_map: dict[str, ScenarioCategory] = {}
    for topic in SD_TOPICS:
        cat = ScenarioCategory(
            name=topic["name"],
            title=topic["title"],
            description=topic["description"],
            icon_name=topic["icon_name"],
            order_index=topic["order_index"],
            course_id=sd_course.id,
        )
        session.add(cat)
        session.flush()
        category_map[topic["name"]] = cat

        lesson_data = topic["lesson"]
        lesson = Lesson(
            course_id=sd_course.id,
            category_id=cat.id,
            title=lesson_data["title"],
            content=lesson_data["content"],
            content_type=lesson_data["content_type"],
            order_index=lesson_data["order_index"],
            estimated_minutes=lesson_data["estimated_minutes"],
        )
        session.add(lesson)
        session.flush()

        quiz_data = topic["quiz"]
        quiz = Quiz(
            course_id=sd_course.id,
            lesson_id=lesson.id,
            title=quiz_data["title"],
            description=quiz_data["description"],
            order_index=1,
        )
        session.add(quiz)
        session.flush()

        for q in quiz_data["questions"]:
            question = QuizQuestion(
                quiz_id=quiz.id,
                question=q["question"],
                options=q["options"],
                correct_answer_index=q["correct_answer_index"],
                explanation=q["explanation"],
                order_index=q["order_index"],
            )
            session.add(question)

        print(f"✅ Seeded SD topic: {topic['name']}")

    session.flush()

    for sc_data in SD_SCENARIOS_DATA:
        cat = category_map.get(sc_data["topic_name"])
        if not cat:
            continue
        sc_copy = sc_data.copy()
        sc_copy.pop("topic_name")
        scenario = Scenario(**sc_copy, category_id=cat.id)
        session.add(scenario)
        print(f"✅ Seeded SD scenario: {sc_copy['title'][:50]}")

    session.commit()
    print("✅ System Design content fully seeded.")


def seed_english_it_lessons(session: Session, course_map: dict[str, Course]) -> None:
    """Seed lessons and quizzes for each English IT scenario category."""
    english_course = course_map.get("english-it-essentials")
    if not english_course:
        return

    # Idempotency check
    from app.models.lesson import Lesson as LessonModel
    existing = session.exec(
        select(LessonModel).where(LessonModel.course_id == english_course.id)
    ).first()
    if existing:
        print("ℹ️  English IT lessons already seeded, skipping.")
        return

    for topic in ENGLISH_IT_TOPICS:
        cat = session.exec(
            select(ScenarioCategory).where(ScenarioCategory.name == topic["category_name"])
        ).first()
        if not cat:
            print(f"⚠️  Category '{topic['category_name']}' not found, skipping.")
            continue

        ld = topic["lesson"]
        lesson = Lesson(
            course_id=english_course.id,
            category_id=cat.id,
            title=ld["title"],
            content=ld["content"],
            content_type=ld["content_type"],
            order_index=ld["order_index"],
            estimated_minutes=ld["estimated_minutes"],
        )
        session.add(lesson)
        session.flush()

        qd = topic["quiz"]
        quiz = Quiz(
            course_id=english_course.id,
            lesson_id=lesson.id,
            title=qd["title"],
            description=qd.get("description", ""),
            order_index=ld["order_index"],
        )
        session.add(quiz)
        session.flush()

        for q in qd["questions"]:
            question = QuizQuestion(
                quiz_id=quiz.id,
                question=q["question"],
                options=q["options"],
                correct_answer_index=q["correct_answer_index"],
                explanation=q["explanation"],
                order_index=q["order_index"],
            )
            session.add(question)

        print(f"✅ Seeded English IT lesson: {ld['title'][:50]}")

    session.commit()
    print("✅ English IT lessons fully seeded.")


def seed_translations(session: Session) -> None:
    """Update existing seeded records with Vietnamese translations. Safe to re-run."""
    from app.db.translations_vi import (
        CATEGORY_TRANSLATIONS_VI,
        COURSE_TRANSLATIONS_VI,
        DOMAIN_TRANSLATIONS_VI,
        ENGLISH_IT_LESSON_TRANSLATIONS_VI,
        SD_LESSON_TRANSLATIONS_VI,
    )
    from app.models.lesson import Lesson as LessonModel

    # ── Domains ────────────────────────────────────────────────────────────────
    for slug, vi in DOMAIN_TRANSLATIONS_VI.items():
        domain = session.exec(select(Domain).where(Domain.slug == slug)).first()
        if domain:
            domain.translations = {"vi": vi}
            session.add(domain)

    # ── Courses ────────────────────────────────────────────────────────────────
    for slug, vi in COURSE_TRANSLATIONS_VI.items():
        course = session.exec(select(Course).where(Course.slug == slug)).first()
        if course:
            course.translations = {"vi": vi}
            session.add(course)

    # ── Categories ────────────────────────────────────────────────────────────
    for name, vi in CATEGORY_TRANSLATIONS_VI.items():
        cat = session.exec(select(ScenarioCategory).where(ScenarioCategory.name == name)).first()
        if cat:
            cat.translations = {"vi": vi}
            session.add(cat)

    session.flush()

    # ── English IT Lessons + Quizzes ──────────────────────────────────────────
    for category_name, data in ENGLISH_IT_LESSON_TRANSLATIONS_VI.items():
        cat = session.exec(select(ScenarioCategory).where(ScenarioCategory.name == category_name)).first()
        if not cat:
            continue
        lesson = session.exec(
            select(LessonModel).where(LessonModel.category_id == cat.id)
        ).first()
        if lesson:
            lesson_vi = data.get("lesson", {})
            lesson.translations = {"vi": {"title": lesson_vi.get("title", ""), "content": lesson_vi.get("content", "")}}
            session.add(lesson)

            quiz = session.exec(select(Quiz).where(Quiz.lesson_id == lesson.id)).first()
            if quiz:
                quiz_vi = data.get("quiz", {})
                quiz.translations = {"vi": {"title": quiz_vi.get("title", ""), "description": quiz_vi.get("description", "")}}
                session.add(quiz)
                questions = session.exec(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id).order_by(QuizQuestion.order_index)).all()
                q_translations = quiz_vi.get("questions", [])
                for i, q in enumerate(questions):
                    if i < len(q_translations):
                        qt = q_translations[i]
                        q.translations = {"vi": {
                            "question": qt.get("question", ""),
                            "options": qt.get("options", q.options),
                            "explanation": qt.get("explanation", ""),
                        }}
                        session.add(q)

    # ── SD Lessons + Quizzes ──────────────────────────────────────────────────
    for topic_name, data in SD_LESSON_TRANSLATIONS_VI.items():
        cat = session.exec(select(ScenarioCategory).where(ScenarioCategory.name == topic_name)).first()
        if not cat:
            continue
        lesson = session.exec(
            select(LessonModel).where(LessonModel.category_id == cat.id)
        ).first()
        if lesson:
            lesson_vi = data.get("lesson", {})
            lesson.translations = {"vi": {"title": lesson_vi.get("title", ""), "content": lesson_vi.get("content", "")}}
            session.add(lesson)

            quiz = session.exec(select(Quiz).where(Quiz.lesson_id == lesson.id)).first()
            if quiz:
                quiz_vi = data.get("quiz", {})
                quiz.translations = {"vi": {"title": quiz_vi.get("title", ""), "description": quiz_vi.get("description", "")}}
                session.add(quiz)
                questions = session.exec(select(QuizQuestion).where(QuizQuestion.quiz_id == quiz.id).order_by(QuizQuestion.order_index)).all()
                q_translations = quiz_vi.get("questions", [])
                for i, q in enumerate(questions):
                    if i < len(q_translations):
                        qt = q_translations[i]
                        q.translations = {"vi": {
                            "question": qt.get("question", ""),
                            "options": qt.get("options", q.options),
                            "explanation": qt.get("explanation", ""),
                        }}
                        session.add(q)

    session.commit()
    print("✅ Vietnamese translations seeded.")


def seed_database(session: Session) -> None:
    from app.db.seed_react import seed_react
    from app.db.seed_go import seed_go
    from app.db.seed_llm import seed_llm

    seed_english_content(session)
    _, course_map = seed_domains_and_courses(session)
    seed_link_english_categories(session, course_map)
    seed_english_it_lessons(session, course_map)
    seed_system_design(session, course_map)
    seed_react(session)
    seed_go(session)
    seed_llm(session)
    seed_translations(session)
