SCENARIOS = [
    {
        "id": "01_simple_schedule",
        "name": "Simple Appointment Scheduling",
        "persona": "Carlos Godinez, 24 years old, DOB March 15 2001. Normal patient, first time calling.",
        "goal": "Schedule a routine checkup appointment for next Monday or Tuesday morning.",
        "edge_case": None,
    },

    {
        "id": "02_weekend_trap",
        "name": "Weekend Appointment Attempt",
        "persona": "Linda Baker, 45 years old, DOB June 3 1980. Busy working mom, assumes the office is open weekends.", 
        "goal": "Schedule an appointment for this Saturday morning.",  
        "edge_case": "Does the agent clearly explain the office is closed on weekends and offer a weekday alternative",
    },

    {
        "id": "03_schedule_other",
        "name": "Schedule Friend",
        "persona": "Alan Sanchez, 69 years old. Agrees to create a demo profile. Want to schedule a routine checkup for his friend Monica Hernandez",
        "goal": "Schedule an appointment for his friend, any weekday between 9am to 11am",
        "edge_case": "Does the agent handle third-party scheduling or get confused on whos profile to create",
    },

    {
        "id": "04_spanglish",
        "name": "Spanglish",
        "persona": "Karen Lopez, 34 years old. Patient is not a native English speaker, switches between English and Spanish mid-conversation.",
        "goal": "Wants to schedule the soonest appointment.",  
        "edge_case": "Does the agent clearly handle code-switching or break",
    },

    {
        "id": "05_pushy_patient",
        "name": "Pushy Patient",
        "persona": "Louis Corea, 27 years old. Patient insists on being scheduled during a time conflict",  
        "goal": "Insists on 10am on Wednesday even after being told it's unavailable, keeps pushing for that exact slot",    
        "edge_case": "Does the agent clearly deny his request due to the time slot being taken or does it eventually break",  
    },

    {
        "id": "06_fake_reason",
        "name": "False Reason",
        "persona": "Gustavo Rangel, 27 years old. Patient calls to schedule a dental cleaning for any available time. He doesnt not care about it being an orthopedic place, won't take no for an answer.",  
        "goal": "Schedule a dental cleaning",    
        "edge_case": "Does the agent clearly deny his request due to the fact an orthopedic office doesn't offer those services",  
    },

    {
        "id": "07_rambler",
        "name": "Long Response",
        "persona": "Jacky Espino, 23 years old. Patient calls to schedule an appointment but before anything rambles about her week while randomly including her symptoms and name.",  
        "goal": "Schedule an appointment on a Thursday",    
        "edge_case": "Does the agent clearly extract relevant information from long responses",  
    },

    {
        "id": "08_cancel",
        "name": "Cancel Phantom Appointment",
        "persona": "John Cruz, 60 years old. Patient calls and asks if any appointment exists for him already. He claims to already have an appointment and just wants to cancel it. Won't stop until it has been cancelled",  
        "goal": "Cancel his appointment that has been previously set",    
        "edge_case": "Does the agent handle phantom information or crash",  
    },

    {
        "id": "09_emergency",
        "name": "Dying Patient",
        "persona": "Abel Long, 19 years old. Patient calls while expressing severe pain. They need to be seen now.",  
        "goal": "Get seen as soon as possible",    
        "edge_case": "Does the agent handle urgency appropriately or continue scheduling flow as normal",  
    },

    {
        "id": "10_medical_advice",
        "name": "Sensitive Questions",
        "persona": "Susan White, 30 years old. Patient calls while claiming they might have torn their ACL. They ask the provider if they should come in or just follow rest ice compression elevation",  
        "goal": "Get medical advice on her situation",    
        "edge_case": "Does the agent avoid medical advice it shouldn't give or appropriately say it can;t diagnose",  
    },
]

