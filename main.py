from google.adk.sessions import InMemorySessionService
from agents.agent import root_agent
from google.genai import types # For creating message Content/Parts
from google.adk.runners import Runner
import asyncio
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyAMEgPT8FjJ2ToGvTsn2o0GoodN_wV4Qy8"

# MODEL_NAME = "gemini-2.0-flash"
MODEL_NAME = "gemini-2.0-flash-lite"

APP_NAME = "dungeon_master"
USER_ID = "user_1"
SESSION_ID = "session_01"

async def main():
    # When running directly, we must manually set up the runner and memory.
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
      agent=root_agent,
      app_name=APP_NAME,
      session_service=session_service
    )


    query = input("\n[Root Agent]> ")
    await call_agent_async(query, runner, USER_ID, SESSION_ID)
    
async def call_agent_async(query, runner, user_id, session_id):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    runner.run(user_id=user_id, session_id=session_id, new_message=content)

    final_response_text = "Agent did not produce a final response." # Default

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
      if event.is_final_response():
        if event.content and event.content.parts:
          # Assuming text response in the first part
          final_response_text = event.content.parts[0].text
        elif event.actions and event.actions.escalate: # Handle potential errors/escalations
          final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
        # Add more checks here if needed (e.g., specific error codes)
        break # Stop processing events once the final response is found

    print(f"\n[Root Agent] Final Response: {final_response_text}")



if __name__ == "__main__":
  print("AI DM Application running in direct execution mode (python main.py).")
  asyncio.run(main())
