# this program constructs user metadata that gets appended to user request to API

from datetime import date,datetime
from openai import OpenAI
import time
from textwrap import dedent


#hardcoded key for testing
client = OpenAI(api_key="")
# !! REMEMBER TO REMOVE !!

sysPrompt="""Extract the following fields from the user's input:

        - task_name [required]: A clear and concise title for the task. Preserve only specific details (e.g., meeting person/place, subject, action, time)
        - task_time [optional]: only return in 12hr format (like "4:32 PM"). Use user's current time if input mentions relative terms (like "in 2 hours", "this evening"). Else return null
        - task_description [optional]: Paraphrase extra details if provided, return null if none.
        - due_date [required]: Parse any mentioned absolute date, if relative ("tomorrow", "next Friday"), use the appended user metadata (current day and date) to resolve into DD Mon YYYY (like "17 Jul 2023", "27 Feb 2024", "11 Jan 2025")
        - priority [optional]: default to 4(low) if not mentioned; events like exams, assignment submissions, university coursework are HIGH PRIORITY (1 or 2 depending on user wording). Must be an integer >= 1 and <= 4
        - color [optional]: default to #FDB927 unless user has mentioned 'EXAM/UNIVERSITY' related terms [return RED] (ALWAYS RETURN AS HEX)
        
        Respond with valid JSON containing ONLY THESE FIELDS"""

# construct user metadata that is passed to api
def initializeUserTzData():
    todaysDate = str(date.today())
    timeRn = datetime.now()
    strTime = timeRn.strftime(" %I:%M %p ")
    strDay = timeRn.strftime(" %A ")

    metadata = { "todaysDate (yyyy/mm/dd): ":todaysDate,
              "current time: ":strTime,
              "current day: ":strDay }
    
    return str(metadata)



def warmupCall():
    warmup_startTime=time.time()
    emptyResponse = client.responses.create(
        model="gpt-4.1-nano-2025-04-14",
        instructions="warmup call for cold-start latency, respond with 'warmed up' ",
        input="  "
    )
    print('api WARMUP RESPONSE: ',emptyResponse.output_text)
    warmup_endTime=time.time()
    warmupClock = warmup_endTime - warmup_startTime
    print('api WARMUP time: ',warmupClock)



# pass to api
def postRequest(userInput) -> str:  
    # userInput is dict
    stringInput = str(userInput["task_description"])     
    start_time=time.time()
    userTzData=initializeUserTzData()
    response = client.responses.create(

            model="gpt-4.1-nano-2025-04-14",

            instructions=dedent(sysPrompt),

            input= stringInput + "[USER TIMEZONE METADATA] \n" + userTzData
            
    )

    end_time=time.time()
    internalClock = end_time-start_time
    print('api response time: ',internalClock)
    print('api RESPONSE JSON: ',response.output_text)

    return response.output_text