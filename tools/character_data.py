from tools import _get_item_details, _fetch_index

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

def get_all_backgrounds() -> list:
  """Tool to get all backgrounds."""
  return _fetch_index("backgrounds")

def get_all_languages() -> list:
  """Tool to get all languages."""
  return _fetch_index("languages")

def get_all_proficiencies() -> list:
  """Tool to get all proficiencies."""
  return _fetch_index("proficiencies")

def get_all_skills() -> list:
  """Tool to get all skills."""
  return _fetch_index("skills")

def get_all_ability_scores() -> list:
  """Tool to get all ability scores."""
  return _fetch_index("ability-scores")

def get_all_alignments() -> list:
  """Tool to get all alignments."""
  return _fetch_index("alignments")



