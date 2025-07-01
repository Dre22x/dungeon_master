from tools import _get_item_details, _fetch_index
import textwrap
# --- Character Data Tools ---

def get_ability_score_details(score_name: str) -> dict:
    """Tool to get details about an ability score (e.g., Strength)."""
    return _get_item_details("ability-scores", score_name)

def get_alignment_details(alignment_name: str) -> dict:
    """Tool to get details about an alignment (e.g., Lawful Good)."""
    return _get_item_details("alignments", alignment_name)

def get_background_details(background_name: str) -> dict:
    """Tool to get details about a background (e.g., Acolyte)."""
    return _get_item_details("backgrounds", background_name)

def get_skill_details(skill_name: str) -> dict:
    """Tool to get details about a specific skill (e.g., Athletics)."""
    return _get_item_details("skills", skill_name)

def get_proficiency_details(proficiency_name: str) -> dict:
    """Tool to get details about a proficiency (e.g., 'all armor', 'longswords')."""
    return _get_item_details("proficiencies", proficiency_name)

def get_language_details(language_name: str) -> dict:
    """Tool to get details about a specific language."""
    return _get_item_details("languages", language_name)

# --- Character Data get_all tools ---

def get_all_backgrounds() -> list[dict]:
  """Tool to get all backgrounds."""
  return _fetch_index("backgrounds")

def get_all_languages() -> list[dict]:
  """Tool to get all languages."""
  return _fetch_index("languages")

def get_all_proficiencies() -> list[dict]:
  """Tool to get all proficiencies."""
  return _fetch_index("proficiencies")

def get_all_skills() -> list[dict]:
  """Tool to get all skills."""
  return _fetch_index("skills")

def get_all_ability_scores() -> list[dict]:
  """Tool to get all ability scores."""
  return _fetch_index("ability-scores")

def get_all_alignments() -> list[dict]:
  """Tool to get all alignments."""
  return _fetch_index("alignments")




# --- Character Creation Tools ---
def finalize_character(
    name: str, 
    race: str, 
    char_class: str, 
    level: int,
    background: str,
    alignment: str,
    ability_scores: dict, 
    skills: list[str], 
    proficiencies: list[str],
    equipment: list[str],
    ) -> str:
    """
    Formats and prints a complete character sheet summary to the console. 
    This is the final step of character creation.
    """
    sheet = []
    # Helper for adding lines
    def add_line(text="", indent=0):
        sheet.append(" " * indent + text)

    # --- Header ---
    add_line("="*60)
    add_line(f" CHARACTER SHEET ".center(60, "="))
    add_line("="*60)
    add_line()
    
    # --- Basic Info ---
    add_line(f"Name: {name}")
    add_line(f"Race: {race}")
    add_line(f"Class: {char_class} (Level {level})")
    add_line(f"Background: {background}")
    add_line(f"Alignment: {alignment}")
    add_line()
    add_line("-" * 60)

    # --- Ability Scores ---
    add_line("ABILITY SCORES".center(60))
    add_line()
    scores_text = []
    for score, value in ability_scores.items():
        scores_text.append(f"{score[:3].upper()}: {str(value).ljust(2)}")
    add_line(" | ".join(scores_text).center(60))
    add_line()
    add_line("-" * 60)

    # --- Skills & Proficiencies ---
    add_line("SKILLS & PROFICIENCIES".center(60))
    add_line()
    add_line("Skills:", 2)
    add_line(textwrap.fill(", ".join(sorted(skills)), width=55, initial_indent=' '*4, subsequent_indent=' '*4))
    add_line()
    add_line("Other Proficiencies:", 2)
    add_line(textwrap.fill(", ".join(sorted(proficiencies)), width=55, initial_indent=' '*4, subsequent_indent=' '*4))
    add_line()
    add_line("-" * 60)

    # --- Equipment ---
    add_line("EQUIPMENT".center(60))
    add_line()
    for item in equipment:
        add_line(f"- {item}", 4)
    add_line()

    # --- Footer ---
    add_line("="*60)

    # Print to console
    final_sheet = "\n".join(sheet)
    print(final_sheet)
    
    # Return a confirmation message
    return f"Character sheet for {name} has been successfully generated and printed."
