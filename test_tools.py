#!/usr/bin/env python3
"""
Comprehensive test suite for all tools modules
Tests all functions defined in the tools folder
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import json
import requests

# Add the current directory to the path so we can import the tools modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all the tools modules
from tools import tools
from tools import character_data
from tools import classes
from tools import races
from tools import spells
from tools import subclasses
from tools import monsters
from tools import equipment
from tools import weapons
from tools import magic_items
from tools import traits
from tools import subraces
from tools import rules
from tools import game_mechanics
from tools import misc_tools


class TestTools(unittest.TestCase):
    """Test cases for the core tools module"""
    
    @patch('tools.tools.requests.get')
    def test_fetch_index_success(self, mock_get):
        """Test successful index fetching"""
        tools._fetch_index.cache_clear()
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": [{"name": "test", "url": "/test"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = tools._fetch_index("test-category")
        self.assertEqual(result, {"results": [{"name": "test", "url": "/test"}]})
    
    @patch('tools.tools.requests.get')
    def test_fetch_index_failure(self, mock_get):
        """Test index fetching failure"""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        result = tools._fetch_index("test-category")
        self.assertEqual(result, [])
    
    def test_search_index_exact_match(self):
        """Test exact match in search index"""
        index = {"results": [{"name": "Test Item", "url": "/test"}]}
        result = tools._search_index("Test Item", index)
        self.assertEqual(result, {"name": "Test Item", "url": "/test"})
    
    def test_search_index_partial_match(self):
        """Test partial match in search index"""
        index = {"results": [{"name": "Test Item", "url": "/test"}]}
        result = tools._search_index("Test", index)
        self.assertEqual(result, {"name": "Test Item", "url": "/test"})
    
    def test_search_index_no_match(self):
        """Test no match in search index"""
        index = {"results": [{"name": "Test Item", "url": "/test"}]}
        result = tools._search_index("Nonexistent", index)
        self.assertIsNone(result)
    
    @patch('tools.tools.requests.get')
    def test_fetch_data_by_url_success(self, mock_get):
        """Test successful data fetching by URL"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "test", "details": "test details"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = tools._fetch_data_by_url("/test")
        self.assertEqual(result, {"name": "test", "details": "test details"})
    
    @patch('tools.tools.requests.get')
    def test_fetch_data_by_url_failure(self, mock_get):
        """Test data fetching failure by URL"""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        result = tools._fetch_data_by_url("/test")
        self.assertIsNone(result)
    
    def test_fetch_data_by_url_empty(self):
        """Test data fetching with empty URL"""
        result = tools._fetch_data_by_url("")
        self.assertIsNone(result)
    
    @patch('tools.tools._fetch_index')
    @patch('tools.tools._search_index')
    @patch('tools.tools._fetch_data_by_url')
    def test_get_item_details_success(self, mock_fetch_data, mock_search, mock_fetch_index):
        """Test successful item details retrieval"""
        mock_fetch_index.return_value = {"results": []}
        mock_search.return_value = {"url": "/test"}
        mock_fetch_data.return_value = {"name": "test", "details": "test details"}
        
        result = tools._get_item_details("test-category", "test-item")
        self.assertEqual(result, {"name": "test", "details": "test details"})
    
    @patch('tools.tools._fetch_index')
    def test_get_item_details_index_failure(self, mock_fetch_index):
        """Test item details retrieval with index failure"""
        mock_fetch_index.return_value = []
        
        result = tools._get_item_details("test-category", "test-item")
        self.assertIn("error", result)
    
    @patch('tools.tools._fetch_index')
    @patch('tools.tools._search_index')
    def test_get_item_details_item_not_found(self, mock_search, mock_fetch_index):
        """Test item details retrieval when item not found"""
        mock_fetch_index.return_value = {"results": []}
        mock_search.return_value = None
        
        result = tools._get_item_details("test-category", "test-item")
        self.assertIn("error", result)
    
    @patch('tools.tools._fetch_index')
    @patch('tools.tools._search_index')
    @patch('tools.tools._fetch_data_by_url')
    def test_get_equipment_details(self, mock_fetch_data, mock_search_index, mock_fetch_index):
        """Test equipment details retrieval"""
        mock_fetch_index.return_value = [{"equipment": [{"name": "Sword", "url": "/sword"}]}]
        mock_search_index.return_value = {"name": "Sword", "url": "/sword"}
        mock_fetch_data.return_value = {"name": "Sword", "details": "A sharp blade"}
        
        result = tools.get_equipment_details("Sword")
        self.assertEqual(result, {"name": "Sword", "details": "A sharp blade"})
    
    @patch('tools.tools._fetch_index')
    def test_get_starting_equipment(self, mock_fetch_index):
        """Test starting equipment retrieval"""
        mock_fetch_index.return_value = {"results": []}
        
        result = tools.get_starting_equipment("Fighter")
        self.assertIn("error", result)
    
    @patch('tools.tools._fetch_index')
    def test_get_all_equipments(self, mock_fetch_index):
        """Test getting all equipment"""
        mock_fetch_index.return_value = [{"name": "Weapon", "equipment": []}]
        
        result = tools.get_all_equipments()
        self.assertEqual(result, [{"name": "Weapon", "equipment": []}])


class TestCharacterData(unittest.TestCase):
    """Test cases for character_data module"""
    
    @patch('tools.character_data._get_item_details')
    def test_get_ability_score_details(self, mock_get_item):
        """Test ability score details retrieval"""
        mock_get_item.return_value = {"name": "Strength", "full_name": "STR"}
        result = character_data.get_ability_score_details("Strength")
        self.assertEqual(result, {"name": "Strength", "full_name": "STR"})
    
    @patch('tools.character_data._get_item_details')
    def test_get_alignment_details(self, mock_get_item):
        """Test alignment details retrieval"""
        mock_get_item.return_value = {"name": "Lawful Good", "description": "Good alignment"}
        result = character_data.get_alignment_details("Lawful Good")
        self.assertEqual(result, {"name": "Lawful Good", "description": "Good alignment"})
    
    @patch('tools.character_data._get_item_details')
    def test_get_background_details(self, mock_get_item):
        """Test background details retrieval"""
        mock_get_item.return_value = {"name": "Acolyte", "skill_proficiencies": ["Religion"]}
        result = character_data.get_background_details("Acolyte")
        self.assertEqual(result, {"name": "Acolyte", "skill_proficiencies": ["Religion"]})
    
    @patch('tools.character_data._get_item_details')
    def test_get_skill_details(self, mock_get_item):
        """Test skill details retrieval"""
        mock_get_item.return_value = {"name": "Athletics", "ability_score": "Strength"}
        result = character_data.get_skill_details("Athletics")
        self.assertEqual(result, {"name": "Athletics", "ability_score": "Strength"})
    
    @patch('tools.character_data._get_item_details')
    def test_get_proficiency_details(self, mock_get_item):
        """Test proficiency details retrieval"""
        mock_get_item.return_value = {"name": "Longswords", "type": "Weapon"}
        result = character_data.get_proficiency_details("Longswords")
        self.assertEqual(result, {"name": "Longswords", "type": "Weapon"})
    
    @patch('tools.character_data._get_item_details')
    def test_get_language_details(self, mock_get_item):
        """Test language details retrieval"""
        mock_get_item.return_value = {"name": "Common", "type": "Standard"}
        result = character_data.get_language_details("Common")
        self.assertEqual(result, {"name": "Common", "type": "Standard"})
    
    @patch('tools.character_data._fetch_index')
    def test_get_all_backgrounds(self, mock_fetch_index):
        """Test getting all backgrounds"""
        mock_fetch_index.return_value = {"results": [{"name": "Acolyte"}]}
        result = character_data.get_all_backgrounds()
        self.assertEqual(result, {"results": [{"name": "Acolyte"}]})
    
    @patch('tools.character_data._fetch_index')
    def test_get_all_languages(self, mock_fetch_index):
        """Test getting all languages"""
        mock_fetch_index.return_value = {"results": [{"name": "Common"}]}
        result = character_data.get_all_languages()
        self.assertEqual(result, {"results": [{"name": "Common"}]})
    
    @patch('tools.character_data._fetch_index')
    def test_get_all_proficiencies(self, mock_fetch_index):
        """Test getting all proficiencies"""
        mock_fetch_index.return_value = {"results": [{"name": "Longswords"}]}
        result = character_data.get_all_proficiencies()
        self.assertEqual(result, {"results": [{"name": "Longswords"}]})
    
    @patch('tools.character_data._fetch_index')
    def test_get_all_skills(self, mock_fetch_index):
        """Test getting all skills"""
        mock_fetch_index.return_value = {"results": [{"name": "Athletics"}]}
        result = character_data.get_all_skills()
        self.assertEqual(result, {"results": [{"name": "Athletics"}]})
    
    @patch('tools.character_data._fetch_index')
    def test_get_all_ability_scores(self, mock_fetch_index):
        """Test getting all ability scores"""
        mock_fetch_index.return_value = {"results": [{"name": "Strength"}]}
        result = character_data.get_all_ability_scores()
        self.assertEqual(result, {"results": [{"name": "Strength"}]})
    
    @patch('tools.character_data._fetch_index')
    def test_get_all_alignments(self, mock_fetch_index):
        """Test getting all alignments"""
        mock_fetch_index.return_value = {"results": [{"name": "Lawful Good"}]}
        result = character_data.get_all_alignments()
        self.assertEqual(result, {"results": [{"name": "Lawful Good"}]})
    
    @patch('builtins.print')
    def test_finalize_character(self, mock_print):
        """Test character finalization"""
        ability_scores = {"Strength": 16, "Dexterity": 14, "Constitution": 12}
        skills = ["Athletics", "Intimidation"]
        proficiencies = ["Longswords", "Heavy Armor"]
        equipment = ["Longsword", "Chain Mail"]
        
        result = character_data.finalize_character(
            "Test Character", "Human", "Fighter", 1, "Soldier", "Lawful Good",
            ability_scores, skills, proficiencies, equipment
        )
        
        self.assertIn("Character sheet for Test Character has been successfully generated", result)
        mock_print.assert_called()


class TestClasses(unittest.TestCase):
    """Test cases for classes module"""
    
    @patch('tools.classes._get_item_details')
    def test_get_class_details(self, mock_get_item):
        """Test class details retrieval"""
        mock_get_item.return_value = {"name": "Fighter", "hit_die": 10}
        result = classes.get_class_details("Fighter")
        self.assertEqual(result, {"name": "Fighter", "hit_die": 10})
    
    @patch('tools.classes._get_item_details')
    def test_get_spellcasting_info(self, mock_get_item):
        """Test spellcasting info retrieval"""
        mock_get_item.return_value = {"spellcasting_ability": "Intelligence"}
        result = classes.get_spellcasting_info("Wizard")
        self.assertEqual(result, {"spellcasting_ability": "Intelligence"})
    
    @patch('tools.classes._get_item_details')
    def test_get_multiclassing_info(self, mock_get_item):
        """Test multiclassing info retrieval"""
        mock_get_item.return_value = {"prerequisites": []}
        result = classes.get_multiclassing_info("Fighter")
        self.assertEqual(result, {"prerequisites": []})
    
    @patch('tools.classes._fetch_index')
    def test_get_subclasses_available_for_class(self, mock_fetch_index):
        """Test getting subclasses for a class"""
        mock_fetch_index.return_value = {"results": [{"name": "Champion"}]}
        result = classes.get_subclasses_available_for_class("Fighter")
        self.assertEqual(result, [{"name": "Champion"}])
    
    @patch('tools.classes._fetch_index')
    def test_get_spells_available_for_class(self, mock_fetch_index):
        """Test getting spells for a class"""
        mock_fetch_index.return_value = {"results": [{"name": "Fireball"}]}
        result = classes.get_spells_available_for_class("Wizard")
        self.assertEqual(result, [{"name": "Fireball"}])
    
    @patch('tools.classes._fetch_index')
    def test_get_features_available_for_class(self, mock_fetch_index):
        """Test getting features for a class"""
        mock_fetch_index.return_value = {"results": [{"name": "Second Wind"}]}
        result = classes.get_features_available_for_class("Fighter")
        self.assertEqual(result, [{"name": "Second Wind"}])
    
    @patch('tools.classes._fetch_index')
    def test_get_proficiencies_available_for_class(self, mock_fetch_index):
        """Test getting proficiencies for a class"""
        mock_fetch_index.return_value = {"results": [{"name": "All Armor"}]}
        result = classes.get_proficiencies_available_for_class("Fighter")
        self.assertEqual(result, [{"name": "All Armor"}])
    
    @patch('tools.classes._fetch_index')
    def test_get_all_level_resources_for_class(self, mock_fetch_index):
        """Test getting all level resources for a class"""
        mock_fetch_index.return_value = [{"level": 1, "features": []}]
        result = classes.get_all_level_resources_for_class("Fighter")
        self.assertEqual(result, [{"level": 1, "features": []}])
    
    @patch('tools.classes._fetch_index')
    def test_get_level_resources_for_class_at_level(self, mock_fetch_index):
        """Test getting level resources for a class at specific level"""
        mock_fetch_index.return_value = {"level": 1, "features": []}
        result = classes.get_level_resources_for_class_at_level("Fighter", "1")
        self.assertEqual(result, {"level": 1, "features": []})
    
    @patch('tools.classes._fetch_index')
    def test_get_features_for_class_at_level(self, mock_fetch_index):
        """Test getting features for a class at specific level"""
        mock_fetch_index.return_value = {"results": [{"name": "Second Wind"}]}
        result = classes.get_features_for_class_at_level("Fighter", "1")
        self.assertEqual(result, [{"name": "Second Wind"}])
    
    @patch('tools.classes._fetch_index')
    def test_get_spells_for_class_at_level(self, mock_fetch_index):
        """Test getting spells for a class at specific level"""
        mock_fetch_index.return_value = {"results": [{"name": "Magic Missile"}]}
        result = classes.get_spells_for_class_at_level("Wizard", "1")
        self.assertEqual(result, [{"name": "Magic Missile"}])
    
    @patch('tools.classes._fetch_index')
    def test_get_all_classes(self, mock_fetch_index):
        """Test getting all classes"""
        mock_fetch_index.return_value = {"results": [{"name": "Fighter"}]}
        result = classes.get_all_classes()
        self.assertEqual(result, {"results": [{"name": "Fighter"}]})
    
    @patch('builtins.print')
    def test_display_class_info(self, mock_print):
        """Test class info display"""
        class_data = {
            "name": "Fighter",
            "hit_die": 10,
            "proficiencies": [{"name": "All Armor"}],
            "saving_throws": [{"name": "Strength"}]
        }
        classes.display_class_info(class_data)
        mock_print.assert_called()


class TestRaces(unittest.TestCase):
    """Test cases for races module"""
    
    @patch('tools.races._get_item_details')
    def test_get_race_details(self, mock_get_item):
        """Test race details retrieval"""
        mock_get_item.return_value = {"name": "Human", "size": "Medium"}
        result = races.get_race_details("Human")
        self.assertEqual(result, {"name": "Human", "size": "Medium"})
    
    @patch('tools.races._fetch_index')
    def test_get_subraces_available_for_race(self, mock_fetch_index):
        """Test getting subraces for a race"""
        mock_fetch_index.return_value = {"results": [{"name": "High Elf"}]}
        result = races.get_subraces_available_for_race("Elf")
        self.assertEqual(result, [{"name": "High Elf"}])
    
    @patch('tools.races._fetch_index')
    def test_get_proficiencies_available_for_race(self, mock_fetch_index):
        """Test getting proficiencies for a race"""
        mock_fetch_index.return_value = {"results": [{"name": "Longswords"}]}
        result = races.get_proficiencies_available_for_race("Elf")
        self.assertEqual(result, [{"name": "Longswords"}])
    
    @patch('tools.races._fetch_index')
    def test_get_traits_available_for_race(self, mock_fetch_index):
        """Test getting traits for a race"""
        mock_fetch_index.return_value = {"results": [{"name": "Darkvision"}]}
        result = races.get_traits_available_for_race("Elf")
        self.assertEqual(result, [{"name": "Darkvision"}])
    
    @patch('tools.races._fetch_index')
    def test_get_all_races(self, mock_fetch_index):
        """Test getting all races"""
        mock_fetch_index.return_value = {"results": [{"name": "Human"}]}
        result = races.get_all_races()
        self.assertEqual(result, [{"name": "Human"}])
    
    @patch('builtins.print')
    def test_display_race_info(self, mock_print):
        """Test race info display"""
        race_data = {
            "name": "Human",
            "size": "Medium",
            "speed": 30,
            "ability_bonuses": [{"ability_score": {"name": "Strength"}, "bonus": 1}]
        }
        races.display_race_info(race_data)
        mock_print.assert_called()


class TestSpells(unittest.TestCase):
    """Test cases for spells module"""
    
    @patch('tools.spells._get_item_details')
    def test_get_spell_details(self, mock_get_item):
        """Test spell details retrieval"""
        mock_get_item.return_value = {"name": "Fireball", "level": 3}
        result = spells.get_spell_details("Fireball")
        self.assertEqual(result, {"name": "Fireball", "level": 3})
    
    @patch('tools.spells._fetch_index')
    def test_get_spells_by_level(self, mock_fetch_index):
        """Test getting spells by level"""
        mock_fetch_index.return_value = {"results": [{"name": "Fireball"}]}
        result = spells.get_spells_by_level("3")
        self.assertEqual(result, [{"name": "Fireball"}])
    
    @patch('tools.spells._fetch_index')
    def test_get_spells_by_school(self, mock_fetch_index):
        """Test getting spells by school"""
        mock_fetch_index.return_value = {"results": [{"name": "Fireball"}]}
        result = spells.get_spells_by_school("Evocation")
        self.assertEqual(result, [{"name": "Fireball"}])
    
    @patch('tools.spells._fetch_index')
    def test_get_spells_by_level_and_school(self, mock_fetch_index):
        """Test getting spells by level and school"""
        mock_fetch_index.return_value = {"results": [{"name": "Fireball"}]}
        result = spells.get_spells_by_level_and_school("3", "Evocation")
        self.assertEqual(result, [{"name": "Fireball"}])
    
    @patch('tools.spells._fetch_index')
    def test_get_all_spells(self, mock_fetch_index):
        """Test getting all spells"""
        mock_fetch_index.return_value = {"results": [{"name": "Fireball"}]}
        result = spells.get_all_spells()
        self.assertEqual(result, [{"name": "Fireball"}])
    
    @patch('builtins.print')
    def test_display_spell_info(self, mock_print):
        """Test spell info display"""
        spell_data = {
            "name": "Fireball",
            "level_text": "3rd-level",
            "school": {"name": "Evocation"},
            "casting_time": "1 action",
            "range": "150 feet",
            "components": ["V", "S", "M"],
            "duration": "Instantaneous",
            "desc": ["A bright streak flashes from your pointing finger..."]
        }
        spells.display_spell_info(spell_data)
        mock_print.assert_called()


class TestSubclasses(unittest.TestCase):
    """Test cases for subclasses module"""
    
    @patch('tools.subclasses._get_item_details')
    def test_get_subclass_details(self, mock_get_item):
        """Test subclass details retrieval"""
        mock_get_item.return_value = {"name": "Champion", "class": "Fighter"}
        result = subclasses.get_subclass_details("Champion")
        self.assertEqual(result, {"name": "Champion", "class": "Fighter"})
    
    @patch('tools.subclasses._fetch_index')
    def test_get_features_available_for_subclass(self, mock_fetch_index):
        """Test getting features for a subclass"""
        mock_fetch_index.return_value = {"results": [{"name": "Improved Critical"}]}
        result = subclasses.get_features_available_for_subclass("Champion")
        self.assertEqual(result, [{"name": "Improved Critical"}])
    
    @patch('tools.subclasses._fetch_index')
    def test_get_all_level_resources_for_subclass(self, mock_fetch_index):
        """Test getting all level resources for a subclass"""
        mock_fetch_index.return_value = [{"level": 3, "features": []}]
        result = subclasses.get_all_level_resources_for_subclass("Champion")
        self.assertEqual(result, [{"level": 3, "features": []}])
    
    @patch('tools.subclasses._fetch_index')
    def test_get_level_resources_for_subclass_at_level(self, mock_fetch_index):
        """Test getting level resources for a subclass at specific level"""
        mock_fetch_index.return_value = {"level": 3, "features": []}
        result = subclasses.get_level_resources_for_subclass_at_level("Champion", "3")
        self.assertEqual(result, {"level": 3, "features": []})
    
    @patch('tools.subclasses._fetch_index')
    def test_get_features_of_spell_level_for_subclass(self, mock_fetch_index):
        """Test getting features for a subclass at specific level"""
        mock_fetch_index.return_value = {"results": [{"name": "Improved Critical"}]}
        result = subclasses.get_features_of_spell_level_for_subclass("Champion", "3")
        self.assertEqual(result, [{"name": "Improved Critical"}])
    
    @patch('tools.subclasses._fetch_index')
    def test_get_all_subclasses(self, mock_fetch_index):
        """Test getting all subclasses"""
        mock_fetch_index.return_value = {"results": [{"name": "Champion"}]}
        result = subclasses.get_all_subclasses()
        self.assertEqual(result, {"results": [{"name": "Champion"}]})
    
    @patch('builtins.print')
    def test_display_class_info(self, mock_print):
        """Test subclass info display"""
        subclass_data = {
            "name": "Champion",
            "hit_die": 10,
            "proficiencies": [{"name": "All Armor"}],
            "saving_throws": [{"name": "Strength"}]
        }
        subclasses.display_class_info(subclass_data)
        mock_print.assert_called()


class TestMonsters(unittest.TestCase):
    """Test cases for monsters module"""
    
    @patch('tools.monsters._get_item_details')
    def test_get_monster_details(self, mock_get_item):
        """Test monster details retrieval"""
        mock_get_item.return_value = {"name": "Goblin", "size": "Small"}
        result = monsters.get_monster_details("Goblin")
        self.assertEqual(result, {"name": "Goblin", "size": "Small"})
    
    @patch('tools.monsters._fetch_index')
    def test_get_monster_by_challenge_rating(self, mock_fetch_index):
        """Test getting monsters by challenge rating"""
        mock_fetch_index.return_value = {"results": [{"name": "Goblin"}]}
        result = monsters.get_monster_by_challenge_rating("1/4")
        self.assertEqual(result, [{"name": "Goblin"}])
    
    @patch('tools.monsters._fetch_index')
    def test_get_all_monsters(self, mock_fetch_index):
        """Test getting all monsters"""
        mock_fetch_index.return_value = {"results": [{"name": "Goblin"}]}
        result = monsters.get_all_monsters()
        self.assertEqual(result, [{"name": "Goblin"}])
    
    @patch('builtins.print')
    def test_display_monster_info(self, mock_print):
        """Test monster info display"""
        monster_data = {
            "name": "Goblin",
            "size": "Small",
            "type": "Humanoid",
            "alignment": "Neutral Evil",
            "armor_class": 15,
            "hit_points": 7,
            "hit_dice": "2d6",
            "speed": {"walk": "30 ft"},
            "strength": 8,
            "dexterity": 14,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 8,
            "charisma": 8,
            "actions": [{"name": "Scimitar", "desc": "Melee Weapon Attack"}]
        }
        monsters.display_monster_info(monster_data)
        mock_print.assert_called()


class TestEquipment(unittest.TestCase):
    """Test cases for equipment module"""
    
    @patch('tools.equipment._fetch_index')
    @patch('tools.equipment._search_index')
    @patch('tools.equipment._fetch_data_by_url')
    def test_get_equipment_details(self, mock_fetch_data, mock_search_index, mock_fetch_index):
        """Test equipment details retrieval"""
        mock_fetch_index.return_value = [{"equipment": [{"name": "Longsword", "url": "/longsword"}]}]
        mock_search_index.return_value = {"name": "Longsword", "url": "/longsword"}
        mock_fetch_data.return_value = {"name": "Longsword", "details": "A long blade"}
        result = equipment.get_equipment_details("Longsword")
        self.assertEqual(result, {"name": "Longsword", "details": "A long blade"})
    
    @patch('tools.equipment._fetch_index')
    def test_get_all_equipment(self, mock_fetch_index):
        """Test getting all equipment"""
        mock_fetch_index.return_value = {"results": [{"name": "Longsword"}]}
        result = equipment.get_all_equipment()
        self.assertEqual(result, [{"name": "Longsword"}])
    
    @patch('tools.equipment._fetch_index')
    def test_get_all_equipment_categories(self, mock_fetch_index):
        """Test getting all equipment categories"""
        mock_fetch_index.return_value = {"results": [{"name": "Weapon"}]}
        result = equipment.get_all_equipment_categories()
        self.assertEqual(result, [{"name": "Weapon"}])
    
    @patch('tools.equipment._fetch_index')
    def test_get_equipment_by_category(self, mock_fetch_index):
        """Test getting equipment by category"""
        mock_fetch_index.return_value = {"results": [{"name": "Longsword"}]}
        result = equipment.get_equipment_by_category("Weapon")
        self.assertEqual(result, [{"name": "Longsword"}])


class TestWeapons(unittest.TestCase):
    """Test cases for weapons module"""
    
    @patch('tools.weapons._get_item_details')
    def test_get_weapon_property_details(self, mock_get_item):
        """Test weapon property details retrieval"""
        mock_get_item.return_value = {"name": "Finesse", "description": "Use DEX for attack and damage"}
        result = weapons.get_weapon_property_details("Finesse")
        self.assertEqual(result, {"name": "Finesse", "description": "Use DEX for attack and damage"})
    
    @patch('tools.weapons._fetch_index')
    def test_get_all_weapon_properties(self, mock_fetch_index):
        """Test getting all weapon properties"""
        mock_fetch_index.return_value = {"results": [{"name": "Finesse"}]}
        result = weapons.get_all_weapon_properties()
        self.assertEqual(result, [{"name": "Finesse"}])


class TestMagicItems(unittest.TestCase):
    """Test cases for magic_items module"""
    
    @patch('tools.magic_items._get_item_details')
    def test_get_magic_item_details(self, mock_get_item):
        """Test magic item details retrieval"""
        mock_get_item.return_value = {"name": "Sword of Sharpness", "rarity": "Very Rare"}
        result = magic_items.get_magic_item_details("Sword of Sharpness")
        self.assertEqual(result, {"name": "Sword of Sharpness", "rarity": "Very Rare"})
    
    @patch('tools.magic_items._fetch_index')
    def test_get_all_magic_items(self, mock_fetch_index):
        """Test getting all magic items"""
        mock_fetch_index.return_value = {"results": [{"name": "Sword of Sharpness"}]}
        result = magic_items.get_all_magic_items()
        self.assertEqual(result, [{"name": "Sword of Sharpness"}])
    
    @patch('tools.magic_items._fetch_index')
    def test_get_all_magic_schools(self, mock_fetch_index):
        """Test getting all magic schools"""
        mock_fetch_index.return_value = {"results": [{"name": "Evocation"}]}
        result = magic_items.get_all_magic_schools()
        self.assertEqual(result, [{"name": "Evocation"}])


class TestTraits(unittest.TestCase):
    """Test cases for traits module"""
    
    @patch('tools.traits._get_item_details')
    def test_get_trait_details(self, mock_get_item):
        """Test trait details retrieval"""
        mock_get_item.return_value = {"name": "Darkvision", "description": "See in darkness"}
        result = traits.get_trait_details("Darkvision")
        self.assertEqual(result, {"name": "Darkvision", "description": "See in darkness"})
    
    @patch('tools.traits._fetch_index')
    def test_get_all_traits(self, mock_fetch_index):
        """Test getting all traits"""
        mock_fetch_index.return_value = {"results": [{"name": "Darkvision"}]}
        result = traits.get_all_traits()
        self.assertEqual(result, [{"name": "Darkvision"}])


class TestSubraces(unittest.TestCase):
    """Test cases for subraces module"""
    
    @patch('tools.subraces._get_item_details')
    def test_get_subrace_details(self, mock_get_item):
        """Test subrace details retrieval"""
        mock_get_item.return_value = {"name": "High Elf", "race": "Elf"}
        result = subraces.get_subrace_details("High Elf")
        self.assertEqual(result, {"name": "High Elf", "race": "Elf"})
    
    @patch('tools.subraces._fetch_index')
    def test_get_proficiencies_available_for_subrace(self, mock_fetch_index):
        """Test getting proficiencies for a subrace"""
        mock_fetch_index.return_value = {"results": [{"name": "Longswords"}]}
        result = subraces.get_proficiencies_available_for_subrace("High Elf")
        self.assertEqual(result, [{"name": "Longswords"}])
    
    @patch('tools.subraces._fetch_index')
    def test_get_traits_available_for_subrace(self, mock_fetch_index):
        """Test getting traits for a subrace"""
        mock_fetch_index.return_value = {"results": [{"name": "Elf Weapon Training"}]}
        result = subraces.get_traits_available_for_subrace("High Elf")
        self.assertEqual(result, [{"name": "Elf Weapon Training"}])
    
    @patch('tools.subraces._fetch_index')
    def test_get_all_subraces(self, mock_fetch_index):
        """Test getting all subraces"""
        mock_fetch_index.return_value = {"results": [{"name": "High Elf"}]}
        result = subraces.get_all_subraces()
        self.assertEqual(result, [{"name": "High Elf"}])


class TestRules(unittest.TestCase):
    """Test cases for rules module"""
    
    @patch('tools.rules._get_item_details')
    def test_get_rules_details(self, mock_get_item):
        """Test rules details retrieval"""
        mock_get_item.return_value = {"name": "Spellcasting", "description": "How to cast spells"}
        result = rules.get_rules_details("Spellcasting")
        self.assertEqual(result, {"name": "Spellcasting", "description": "How to cast spells"})
    
    @patch('tools.rules._get_item_details')
    def test_get_rules_by_section(self, mock_get_item):
        """Test rules by section retrieval"""
        mock_get_item.return_value = {"name": "Spellcasting", "description": "How to cast spells"}
        result = rules.get_rules_by_section("Spellcasting")
        self.assertEqual(result, {"name": "Spellcasting", "description": "How to cast spells"})
    
    @patch('tools.rules._fetch_index')
    def test_get_all_rules(self, mock_fetch_index):
        """Test getting all rules"""
        mock_fetch_index.return_value = {"results": [{"name": "Spellcasting"}]}
        result = rules.get_all_rules()
        self.assertEqual(result, [{"name": "Spellcasting"}])
    
    @patch('tools.rules._fetch_index')
    def test_get_all_rules_sections(self, mock_fetch_index):
        """Test getting all rules sections"""
        mock_fetch_index.return_value = {"results": [{"name": "Spellcasting"}]}
        result = rules.get_all_rules_sections()
        self.assertEqual(result, [{"name": "Spellcasting"}])


class TestGameMechanics(unittest.TestCase):
    """Test cases for game_mechanics module"""
    
    @patch('tools.game_mechanics._get_item_details')
    def test_get_condition_details(self, mock_get_item):
        """Test condition details retrieval"""
        mock_get_item.return_value = {"name": "Poisoned", "description": "Disadvantage on attacks"}
        result = game_mechanics.get_condition_details("Poisoned")
        self.assertEqual(result, {"name": "Poisoned", "description": "Disadvantage on attacks"})
    
    @patch('tools.game_mechanics._get_item_details')
    def test_get_damage_type_details(self, mock_get_item):
        """Test damage type details retrieval"""
        mock_get_item.return_value = {"name": "Fire", "description": "Fire damage"}
        result = game_mechanics.get_damage_type_details("Fire")
        self.assertEqual(result, {"name": "Fire", "description": "Fire damage"})
    
    @patch('tools.game_mechanics._fetch_index')
    def test_get_all_conditions(self, mock_fetch_index):
        """Test getting all conditions"""
        mock_fetch_index.return_value = {"results": [{"name": "Poisoned"}]}
        result = game_mechanics.get_all_conditions()
        self.assertEqual(result, [{"name": "Poisoned"}])
    
    @patch('tools.game_mechanics._fetch_index')
    def test_get_all_damage_types(self, mock_fetch_index):
        """Test getting all damage types"""
        mock_fetch_index.return_value = {"results": [{"name": "Fire"}]}
        result = game_mechanics.get_all_damage_types()
        self.assertEqual(result, [{"name": "Fire"}])


class TestMiscTools(unittest.TestCase):
    """Test cases for misc_tools module"""
    
    def test_roll_dice_d20(self):
        """Test rolling d20 dice"""
        result = misc_tools.roll_dice("d20", 3)
        self.assertEqual(len(result), 3)
        for roll in result:
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 20)
    
    def test_roll_dice_d12(self):
        """Test rolling d12 dice"""
        result = misc_tools.roll_dice("d12", 2)
        self.assertEqual(len(result), 2)
        for roll in result:
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 12)
    
    def test_roll_dice_d10(self):
        """Test rolling d10 dice"""
        result = misc_tools.roll_dice("d10", 2)
        self.assertEqual(len(result), 2)
        for roll in result:
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 10)
    
    def test_roll_dice_d8(self):
        """Test rolling d8 dice"""
        result = misc_tools.roll_dice("d8", 2)
        self.assertEqual(len(result), 2)
        for roll in result:
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 8)
    
    def test_roll_dice_d6(self):
        """Test rolling d6 dice"""
        result = misc_tools.roll_dice("d6", 2)
        self.assertEqual(len(result), 2)
        for roll in result:
            self.assertGreaterEqual(roll, 1)
            self.assertLessEqual(roll, 6)
    
    def test_roll_dice_invalid(self):
        """Test rolling invalid dice type"""
        result = misc_tools.roll_dice("d100", 1)
        self.assertEqual(result, [])


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestTools,
        TestCharacterData,
        TestClasses,
        TestRaces,
        TestSpells,
        TestSubclasses,
        TestMonsters,
        TestEquipment,
        TestWeapons,
        TestMagicItems,
        TestTraits,
        TestSubraces,
        TestRules,
        TestGameMechanics,
        TestMiscTools
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Exit with appropriate code
    sys.exit(len(result.failures) + len(result.errors)) 