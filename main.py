from google.adk.agents import LlmAgent
from tools.monster_tool import MonsterTool


def main():
    monster_tool = MonsterTool()
    agent = LlmAgent(
        name="Monster Hunter",
        tools=[monster_tool],
        verbose=True
    )
    agent.run("What is the size of a goblin?")



if __name__ == "__main__":
    main()