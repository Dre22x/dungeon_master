import uuid
from google.adk.sessions import InMemorySessionService
from agents.agent import root_agent
from google.adk.runners import Runner
import asyncio
from core.utils import call_agent_async
from data.tools.misc_tools import load_campaign, save_campaign, create_campaign
from dotenv import load_dotenv
load_dotenv()

async def main_async():
  APP_NAME = "dungeon_master"
  USER_ID = "user_1"

  answer = input("Do you want to start a new campaign? (y/n)")
  if answer.lower() != "y":
    campaign_id = input("Enter campaign ID: ")

    # load initial state from db
    try:
      initial_state = load_campaign(campaign_id)
    except:
      print("Campaign not found")
      return
  else:
    campaign_id = str(uuid.uuid4())
    print(f"Starting new campaign with ID: {campaign_id}")
    initial_state = create_campaign(campaign_id)

  SESSION_ID = campaign_id

  session_service = InMemorySessionService()

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