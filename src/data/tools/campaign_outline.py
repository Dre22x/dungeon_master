"""
Campaign Outline Generation Tool

This module provides tools for generating and saving campaign story outlines
to the Firestore database. The outline includes the main quest, plot acts,
key NPCs, and monsters for a cohesive campaign narrative.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from firestore import db_utils
from google.cloud import firestore
import random

def generate_campaign_outline(campaign_id: str, outline_data: dict) -> str:
    """
    Saves a campaign outline to the Firestore database.
    
    Args:
        campaign_id: str - The ID of the campaign
        outline_data: dict - The campaign outline data with the following structure:
            {
                "title": str,
                "theme": str,
                "summary": str,
                "main_quest": str,
                "plot_acts": dict,
                "key_npcs": list,
                "key_monsters": list
            }
    
    Returns:
        str - Success or error message
    """
    try:
        # Get the database client
        db = db_utils.get_db_client()
        if not db:
            return "Error: Database client is not available."
        
        # Save the outline to the campaign document
        campaign_ref = db.collection('campaigns').document(campaign_id)
        
        # Check if campaign exists
        campaign_doc = campaign_ref.get()
        if not campaign_doc.exists:
            return f"Error: Campaign '{campaign_id}' not found."
        
        # Update the campaign with the outline data
        campaign_ref.update({
            'campaign_outline': outline_data,
            'outline_created': firestore.SERVER_TIMESTAMP
        })
        
        print(f"[CampaignOutline] Campaign outline saved for campaign '{campaign_id}'")
        return f"Campaign outline saved successfully for campaign '{campaign_id}'"
        
    except Exception as e:
        return f"Error saving campaign outline: {e}"

def load_campaign_outline(campaign_id: str) -> dict:
    """
    Loads a campaign outline from the Firestore database.
    
    Args:
        campaign_id: str - The ID of the campaign
    
    Returns:
        dict - The campaign outline data or error message
    """
    try:
        # Get the database client
        db = db_utils.get_db_client()
        if not db:
            return {"error": "Database client is not available."}
        
        # Load the campaign document
        campaign_ref = db.collection('campaigns').document(campaign_id)
        campaign_doc = campaign_ref.get()
        
        if not campaign_doc.exists:
            return {"error": f"Campaign '{campaign_id}' not found."}
        
        campaign_data = campaign_doc.to_dict()
        outline_data = campaign_data.get('campaign_outline')
        
        if not outline_data:
            return {"error": f"No campaign outline found for campaign '{campaign_id}'"}
        
        print(f"[CampaignOutline] Campaign outline loaded for campaign '{campaign_id}'")
        return outline_data
        
    except Exception as e:
        return {"error": f"Error loading campaign outline: {e}"}

def generate_random_campaign_outline(campaign_id: str, theme: str = "classic fantasy") -> str:
    """
    Generates a random campaign outline based on a theme and saves it to the database.
    
    Args:
        campaign_id: str - The ID of the campaign
        theme: str - The theme for the campaign (e.g., "classic fantasy", "horror", "political intrigue")
    
    Returns:
        str - Success or error message
    """
    try:
        # Generate outline based on theme
        outline_data = _create_outline_from_theme(theme)
        
        # Save the outline
        return generate_campaign_outline(campaign_id, outline_data)
        
    except Exception as e:
        return f"Error generating campaign outline: {e}"

def _create_outline_from_theme(theme: str) -> dict:
    """
    Creates a campaign outline based on the given theme.
    
    Args:
        theme: str - The theme for the campaign
    
    Returns:
        dict - The generated campaign outline
    """
    # Define outline templates for different themes
    templates = {
        "classic fantasy": {
            "titles": [
                "The Saga of the Sunstone",
                "The Lost Crown of Eldoria",
                "The Dragon's Hoard",
                "The Curse of the Ancient Keep",
                "The Prophecy of the Crystal Staff"
            ],
            "artifact_types": [
                "sacred stone", "ancient crown", "dragon's treasure", "cursed relic", "prophetic staff"
            ],
            "villain_types": [
                "goblin warchief", "dark sorcerer", "corrupted knight", "ancient dragon", "evil necromancer"
            ],
            "location_types": [
                "village", "forest", "mountain fortress", "ancient ruins", "underground lair"
            ]
        },
        "horror": {
            "titles": [
                "The Haunting of Blackwood Manor",
                "The Curse of the Shadowborn",
                "The Last Light of Ravenspire",
                "The Whispering Catacombs",
                "The Blood Moon Prophecy"
            ],
            "artifact_types": [
                "cursed artifact", "ancient tome", "shadow crystal", "blood relic", "dark mirror"
            ],
            "villain_types": [
                "undead lord", "shadow demon", "mad cultist", "ancient horror", "corrupted priest"
            ],
            "location_types": [
                "haunted mansion", "dark forest", "ancient crypt", "abandoned temple", "shadow realm"
            ]
        },
        "political intrigue": {
            "titles": [
                "The Crown of Betrayal",
                "The Merchant's Conspiracy",
                "The Noble's Game",
                "The Throne of Shadows",
                "The Court of Lies"
            ],
            "artifact_types": [
                "royal crown", "merchant's ledger", "noble's seal", "throne", "court document"
            ],
            "villain_types": [
                "corrupt noble", "scheming merchant", "power-hungry advisor", "treacherous knight", "manipulative courtier"
            ],
            "location_types": [
                "royal court", "merchant district", "noble estate", "city streets", "secret meeting place"
            ]
        }
    }
    
    # Get template for the theme, default to classic fantasy
    template = templates.get(theme.lower(), templates["classic fantasy"])
    
    # Generate random elements
    title = random.choice(template["titles"])
    artifact = random.choice(template["artifact_types"])
    villain = random.choice(template["villain_types"])
    location = random.choice(template["location_types"])
    
    # Create the outline structure
    outline = {
        "title": title,
        "theme": theme,
        "summary": f"The {artifact} has been stolen by the {villain}. The players must recover it before it's too late.",
        "main_quest": f"Recover the {artifact} from the {villain}.",
        "plot_acts": {
            "act_1": {
                "title": "The Call to Adventure",
                "summary": f"The players learn of the {artifact}'s theft and are tasked with the quest.",
                "key_location": f"The {location}",
                "primary_conflict": f"Convincing the quest giver of their worth and understanding the threat."
            },
            "act_2": {
                "title": "The Journey",
                "summary": f"The players must travel through dangerous territory to find the {villain}'s lair.",
                "key_location": f"The path to the {location}",
                "primary_conflict": f"Surviving the journey and gathering information about the {villain}."
            },
            "act_3": {
                "title": "The Confrontation",
                "summary": f"The players must face the {villain} and recover the {artifact}.",
                "key_location": f"The {villain}'s lair",
                "primary_conflict": f"Final battle against the {villain} and their minions."
            }
        },
        "key_npcs": [
            {
                "name": "Quest Giver",
                "location": f"The {location}",
                "role": f"Provides the quest to recover the {artifact}."
            },
            {
                "name": "Guide",
                "location": "Along the journey",
                "role": "Provides aid and information about the quest."
            }
        ],
        "key_monsters": [
            {
                "name": f"{villain.title()}",
                "location": f"The {villain}'s lair",
                "role": "Main antagonist who stole the artifact."
            },
            {
                "name": f"{villain.title()}'s Minions",
                "location": f"The {villain}'s lair",
                "role": "Supporting enemies that protect the villain."
            }
        ]
    }
    
    return outline 