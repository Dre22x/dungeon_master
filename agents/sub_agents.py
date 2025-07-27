
from google.adk.agents import LlmAgent
from tools.character_data import *
from tools.classes import *
from tools.equipment import *
from tools.game_mechanics import *
from tools.magic_items import *
from tools.monsters import *
from tools.rules import *
from tools.races import *
from tools.subclasses import *
from tools.spells import *
from tools.subraces import *
from tools.traits import *
from tools.weapons import *
from tools.misc_tools import roll_dice, store_npc_in_memory, get_npc_from_memory, clear_npc_memory, list_npcs_in_memory, send_response_to_root_agent, route_action_to_root_agent
from tools.tools import get_starting_equipment
from tools.campaign_outline import generate_campaign_outline, load_campaign_outline
from firestore.db_utils import *
from agents.config_loader import get_model_for_agent
import os
import sys

def load_instructions(filename: str) -> str:
    """
    Load instructions from a text file in the instructions directory.
    """
    instructions_path = os.path.join(os.path.dirname(__file__), 'instructions', filename)
    try:
        with open(instructions_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: Instructions file {filename} not found at {instructions_path}")
        print("Please ensure the instructions file exists in the agents/instructions/ directory.")
        sys.exit(1)

# --- Create Sub Agents ---
narrative_agent = LlmAgent(
  name="narrative_agent",
  model=get_model_for_agent("narrative_agent"),
  description="You are the world's greatest storyteller, a master of prose and atmosphere. Your purpose is to paint a vivid picture of the world for the players, engaging all their senses. You are to be creative, evocative, and compelling. ",
  instruction=load_instructions("narrative_agent.txt"),
  tools=[send_response_to_root_agent, get_game_state, change_game_state, load_campaign, save_campaign, save_npc_to_campaign,
         get_all_monsters, get_monster_details,
         get_all_races, get_race_details,
         get_all_magic_items, get_magic_item_details,
         get_all_spells, get_spell_details,
         load_campaign_outline,
         # Combat result tools for agent handoff
         get_combat_result,
         clear_combat_result]
)

npc_agent = LlmAgent(
  name="npc_agent",
  model=get_model_for_agent("npc_agent"),
  description="You are a master method actor. Your sole purpose is to embody and roleplay as any Non-Player Character (NPC) in the game world. ",
  instruction=load_instructions("npc_agent.txt"),
    tools=[send_response_to_root_agent, load_npc_from_campaign, save_npc_to_campaign, 
           store_npc_in_memory, get_npc_from_memory, clear_npc_memory, list_npcs_in_memory]
)

rules_lawyer_agent = LlmAgent(
  name="rules_lawyer_agent",
  model=get_model_for_agent("rules_lawyer_agent"),
  description="You are an impartial and highly precise 'Rules Lawyer' for a Dungeons and Dragons 5th Edition game. Your job is to be the ultimate authority on game mechanics. You are logical, factual, and concise. You do not have a personality and you never roleplay. ",
  instruction=load_instructions("rules_lawyer_agent.txt"),
    tools=[send_response_to_root_agent, get_spell_details, 
           get_all_spells, 
           get_race_details, 
           get_all_races, 
           get_class_details, 
           get_all_classes,
           get_background_details,
           get_all_backgrounds,
           get_equipment_details,
           get_all_equipment,
           get_all_equipment_categories,
           get_equipment_by_category,
           get_ability_score_details,
           get_all_ability_scores,
           get_alignment_details,
           get_all_alignments,
           get_skill_details, 
           get_all_skills,
           get_language_details,
           get_all_languages,
           get_all_proficiencies,
           get_proficiency_details,
           get_subclass_details,
           get_all_subclasses,
           get_subrace_details,
           get_all_subraces,
           get_trait_details,
           get_all_traits,
           get_weapon_property_details,
           get_all_weapon_properties,
           get_condition_details,
           get_all_conditions,
           get_damage_type_details,
           get_all_damage_types,
           get_magic_item_details,
           get_all_magic_items,
           get_all_magic_schools,
           get_rules_details,
           get_rules_by_section,
           get_all_rules_sections,
           get_all_rules,
           get_all_monsters,
           get_monster_details,
           get_monster_by_challenge_rating,
           get_all_spells,
           get_spell_details,
           get_spells_by_level_and_school,
           get_spells_by_school,
           roll_dice,
           load_character_from_campaign,
           list_characters_in_campaign,
           get_character_items,
           get_character_spells,
           # Combat mechanics tools
           start_combat,
           get_combat_state,
           update_combat_participant_hp,
           end_combat,
           get_next_turn,
           advance_turn,
           calculate_hp,
           # Combat result tools for agent handoff
           create_combat_result,
           get_combat_result,
           clear_combat_result,
           # NPC combat classification tools
           classify_npc_for_combat,
           get_monster_for_npc_classification,
           resolve_npc_to_monster
          ]
)

player_interface_agent = LlmAgent(
  name="player_interface_agent",
  model=get_model_for_agent("player_interface_agent"),
  description="You are the Player Interface Agent - the central hub for all player interactions in the Dungeons & Dragons game. You are the ONLY agent that directly communicates with the player. All other agents communicate through you. ",
  instruction=load_instructions("player_interface_agent.txt"),
    tools=[route_action_to_root_agent, change_game_state, get_game_state, load_npc_from_campaign, load_campaign]
)


character_creation_agent = LlmAgent(
  name="character_creation_agent",
  model=get_model_for_agent("character_creation_agent"),
  description="You are a friendly and knowledgeable Character Creation Assistant for Dungeons & Dragons 5th Edition. Your goal is to help a new player create their very first character. You are patient, encouraging, and an expert at explaining complex game concepts in a simple and engaging way. ",
  instruction=load_instructions("character_creation_agent.txt"),
    tools=[send_response_to_root_agent, get_spell_details, 
           get_all_spells, 
           get_race_details, 
           get_all_races, 
           get_class_details, 
           get_all_classes,
           get_background_details,
           get_all_backgrounds,
           get_equipment_details,
           get_all_equipment,
           get_all_equipment_categories,
           get_equipment_by_category,
           get_starting_equipment,
           get_ability_score_details,
           get_all_ability_scores,
           get_alignment_details,
           get_all_alignments,
           get_skill_details, 
           get_all_skills,
           get_language_details,
           get_all_languages,
           get_all_proficiencies,
           get_proficiency_details,
           get_subclass_details,
           get_all_subclasses,
           get_subrace_details,
           get_all_subraces,
           get_trait_details,
           get_all_traits,
           get_weapon_property_details,
           get_all_weapon_properties,
           get_condition_details,
           get_all_conditions,
           get_damage_type_details,
           get_all_damage_types,
           get_magic_item_details,
           get_all_magic_items,
           get_all_magic_schools,
           finalize_character,
           create_character_data,
           save_character_to_campaign,
          ]
)

campaign_creation_agent = LlmAgent(
  name="campaign_creation_agent",
  model=get_model_for_agent("campaign_creation_agent"),
  description="You are a master storyteller and campaign architect, specializing in creating compelling campaign outlines for Dungeons & Dragons adventures. Your sole purpose is to generate unique, engaging story structures that will guide the narrative flow of new campaigns. ",
  instruction=load_instructions("campaign_creation_agent.txt"),
    tools=[send_response_to_root_agent, generate_campaign_outline, 
           get_all_monsters, get_monster_details,
           get_all_races, get_race_details,
           get_all_classes, get_class_details,
           get_all_spells, get_spell_details,
           get_all_magic_items, get_magic_item_details,
           get_all_backgrounds, get_background_details]
)
