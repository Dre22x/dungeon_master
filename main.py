import uuid
from google.adk.sessions import InMemorySessionService
from root_agent.agent import root_agent
from google.adk.runners import Runner
import asyncio
from utils import call_agent_async

from dotenv import load_dotenv
load_dotenv()

async def main_async():
  APP_NAME = "dungeon_master"
  USER_ID = "user_1"
  SESSION_ID = str(uuid.uuid4())
  print(f"Session ID: {SESSION_ID}")

  session_service = InMemorySessionService()
  initial_state = {
      "campaign_id": SESSION_ID,
      "game_state": "new_campaign",
      "last_scene": "",
      "last_action": "",
      "campaign_outline": "",
      "characters": [],
      "npcs": [],
      "combat_participants": dict(),
      "combat_details": dict(),
      "dialogue_participants": [],
      "location": "",
      "current_act": "",
  }

  session = await session_service.create_session(
      app_name=APP_NAME,
      user_id=USER_ID,
      session_id=SESSION_ID,
      state=initial_state
  )

  print(f"Session created: {SESSION_ID}")

  runner = Runner(
      agent=root_agent,
      app_name=APP_NAME,
      session_service=session_service
  )

  while True:
    user_input = input("\n[Player]> ")
    await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()