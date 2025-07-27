import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

# Add the parent directory to the path so we can import the tools modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.character_data import finalize_character

class TestCharacterFinalization(unittest.TestCase):
    """Test the finalize_character function with various character combinations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.maxDiff = None  # Show full diff for failed tests
    
    def capture_print_output(self, func, *args, **kwargs):
        """Helper to capture printed output"""
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            result = func(*args, **kwargs)
        return result, captured_output.getvalue()
    
    def test_basic_fighter_character(self):
        """Test a basic fighter character"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Thorin Ironfist",
            race="Dwarf",
            char_class="Fighter",
            level=1,
            background="Soldier",
            alignment="Lawful Good",
            ability_scores={"Strength": 16, "Dexterity": 14, "Constitution": 15, "Intelligence": 10, "Wisdom": 12, "Charisma": 8},
            skills=["Athletics", "Intimidation", "Perception", "Survival"],
            proficiencies=["All armor", "Shields", "Simple weapons", "Martial weapons"],
            equipment=["Longsword", "Shield", "Chain mail", "Crossbow, light", "20 bolts", "Explorer's pack"]
        )
        
        # Check return value
        self.assertIn("Thorin Ironfist", result)
        self.assertIn("successfully generated", result)
        
        # Check output contains all expected sections
        self.assertIn("CHARACTER SHEET", output)
        self.assertIn("Name: Thorin Ironfist", output)
        self.assertIn("Race: Dwarf", output)
        self.assertIn("Class: Fighter (Level 1)", output)
        self.assertIn("Background: Soldier", output)
        self.assertIn("Alignment: Lawful Good", output)
        self.assertIn("ABILITY SCORES", output)
        self.assertIn("STR: 16", output)
        self.assertIn("DEX: 14", output)
        self.assertIn("CON: 15", output)
        self.assertIn("INT: 10", output)
        self.assertIn("WIS: 12", output)
        self.assertIn("CHA: 8", output)
        self.assertIn("SKILLS & PROFICIENCIES", output)
        self.assertIn("Athletics", output)
        self.assertIn("Intimidation", output)
        self.assertIn("All armor", output)
        self.assertIn("EQUIPMENT", output)
        self.assertIn("Longsword", output)
        self.assertIn("Chain mail", output)
    
    def test_wizard_character(self):
        """Test a wizard character with different ability score format"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Elara Moonwhisper",
            race="High Elf",
            char_class="Wizard",
            level=3,
            background="Sage",
            alignment="Neutral Good",
            ability_scores={"STR": 8, "DEX": 14, "CON": 12, "INT": 18, "WIS": 10, "CHA": 16},
            skills=["Arcana", "History", "Insight", "Investigation"],
            proficiencies=["Daggers", "Quarterstaffs", "Light crossbows"],
            equipment=["Spellbook", "Arcane focus", "Scholar's pack", "Spell scrolls"]
        )
        
        self.assertIn("Elara Moonwhisper", result)
        self.assertIn("Class: Wizard (Level 3)", output)
        self.assertIn("STR: 8", output)
        self.assertIn("INT: 18", output)
        self.assertIn("Arcana", output)
        self.assertIn("Spellbook", output)
    
    def test_rogue_character(self):
        """Test a rogue character with many skills"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Shadow",
            race="Tiefling",
            char_class="Rogue",
            level=5,
            background="Criminal",
            alignment="Chaotic Neutral",
            ability_scores={"Strength": 10, "Dexterity": 18, "Constitution": 14, "Intelligence": 12, "Wisdom": 8, "Charisma": 16},
            skills=["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Sleight of Hand", "Stealth"],
            proficiencies=["Light armor", "Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
            equipment=["Rapier", "Shortbow", "20 arrows", "Leather armor", "Thieves' tools", "Backpack"]
        )
        
        self.assertIn("Shadow", result)
        self.assertIn("Class: Rogue (Level 5)", output)
        self.assertIn("DEX: 18", output)
        self.assertIn("Acrobatics", output)
        self.assertIn("Stealth", output)
        self.assertIn("Rapier", output)
    
    def test_cleric_character(self):
        """Test a cleric character with religious background"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Brother Marcus",
            race="Human",
            char_class="Cleric",
            level=2,
            background="Acolyte",
            alignment="Lawful Good",
            ability_scores={"Strength": 14, "Dexterity": 10, "Constitution": 16, "Intelligence": 12, "Wisdom": 18, "Charisma": 14},
            skills=["Insight", "Medicine", "Persuasion", "Religion"],
            proficiencies=["Light armor", "Medium armor", "Shields", "Simple weapons"],
            equipment=["Mace", "Shield", "Scale mail", "Holy symbol", "Priest's pack"]
        )
        
        self.assertIn("Brother Marcus", result)
        self.assertIn("Class: Cleric (Level 2)", output)
        self.assertIn("WIS: 18", output)
        self.assertIn("Religion", output)
        self.assertIn("Holy symbol", output)
    
    def test_barbarian_character(self):
        """Test a barbarian character with minimal skills"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Grommash",
            race="Half-Orc",
            char_class="Barbarian",
            level=1,
            background="Outlander",
            alignment="Chaotic Good",
            ability_scores={"Strength": 18, "Dexterity": 14, "Constitution": 16, "Intelligence": 8, "Wisdom": 12, "Charisma": 10},
            skills=["Athletics", "Survival"],
            proficiencies=["Light armor", "Medium armor", "Shields", "Simple weapons", "Martial weapons"],
            equipment=["Greataxe", "Javelin", "Explorer's pack"]
        )
        
        self.assertIn("Grommash", result)
        self.assertIn("Class: Barbarian (Level 1)", output)
        self.assertIn("STR: 18", output)
        self.assertIn("Greataxe", output)
    
    def test_paladin_character(self):
        """Test a paladin character with many proficiencies"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Sir Gareth",
            race="Human",
            char_class="Paladin",
            level=4,
            background="Noble",
            alignment="Lawful Good",
            ability_scores={"Strength": 16, "Dexterity": 10, "Constitution": 14, "Intelligence": 12, "Wisdom": 8, "Charisma": 18},
            skills=["Athletics", "Insight", "Intimidation", "Persuasion"],
            proficiencies=["All armor", "Shields", "Simple weapons", "Martial weapons"],
            equipment=["Longsword", "Shield", "Chain mail", "Holy symbol", "Priest's pack", "Signet ring"]
        )
        
        self.assertIn("Sir Gareth", result)
        self.assertIn("Class: Paladin (Level 4)", output)
        self.assertIn("CHA: 18", output)
        self.assertIn("All armor", output)
        self.assertIn("Signet ring", output)
    
    def test_druid_character(self):
        """Test a druid character with nature focus"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Willow",
            race="Wood Elf",
            char_class="Druid",
            level=2,
            background="Hermit",
            alignment="Neutral Good",
            ability_scores={"Strength": 10, "Dexterity": 16, "Constitution": 14, "Intelligence": 12, "Wisdom": 18, "Charisma": 8},
            skills=["Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Survival"],
            proficiencies=["Light armor", "Medium armor", "Shields", "Clubs", "Daggers", "Darts", "Javelins", "Maces", "Quarterstaffs", "Scimitars", "Sickles", "Slings", "Spears"],
            equipment=["Scimitar", "Shield", "Leather armor", "Druidic focus", "Explorer's pack"]
        )
        
        self.assertIn("Willow", result)
        self.assertIn("Class: Druid (Level 2)", output)
        self.assertIn("WIS: 18", output)
        self.assertIn("Animal Handling", output)
        self.assertIn("Druidic focus", output)
    
    def test_sorcerer_character(self):
        """Test a sorcerer character with innate magic"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Zara",
            race="Dragonborn",
            char_class="Sorcerer",
            level=3,
            background="Entertainer",
            alignment="Chaotic Good",
            ability_scores={"Strength": 12, "Dexterity": 14, "Constitution": 16, "Intelligence": 10, "Wisdom": 8, "Charisma": 18},
            skills=["Acrobatics", "Deception", "Insight", "Performance", "Persuasion"],
            proficiencies=["Daggers", "Quarterstaffs", "Light crossbows"],
            equipment=["Dagger", "Arcane focus", "Entertainer's pack", "Costume"]
        )
        
        self.assertIn("Zara", result)
        self.assertIn("Class: Sorcerer (Level 3)", output)
        self.assertIn("CHA: 18", output)
        self.assertIn("Performance", output)
        self.assertIn("Costume", output)
    
    def test_warlock_character(self):
        """Test a warlock character with pact magic"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Mordecai",
            race="Tiefling",
            char_class="Warlock",
            level=2,
            background="Criminal",
            alignment="Neutral Evil",
            ability_scores={"Strength": 8, "Dexterity": 14, "Constitution": 12, "Intelligence": 16, "Wisdom": 10, "Charisma": 18},
            skills=["Arcana", "Deception", "Intimidation", "Investigation"],
            proficiencies=["Light armor", "Simple weapons"],
            equipment=["Pact weapon", "Arcane focus", "Burglar's pack"]
        )
        
        self.assertIn("Mordecai", result)
        self.assertIn("Class: Warlock (Level 2)", output)
        self.assertIn("CHA: 18", output)
        self.assertIn("Pact weapon", output)
    
    def test_monk_character(self):
        """Test a monk character with martial arts"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Li Wei",
            race="Human",
            char_class="Monk",
            level=1,
            background="Hermit",
            alignment="Lawful Neutral",
            ability_scores={"Strength": 12, "Dexterity": 18, "Constitution": 14, "Intelligence": 10, "Wisdom": 16, "Charisma": 8},
            skills=["Acrobatics", "Athletics", "Insight", "Religion", "Stealth"],
            proficiencies=["Simple weapons", "Shortswords"],
            equipment=["Shortsword", "Explorer's pack", "10 darts"]
        )
        
        self.assertIn("Li Wei", result)
        self.assertIn("Class: Monk (Level 1)", output)
        self.assertIn("DEX: 18", output)
        self.assertIn("10 darts", output)
    
    def test_ranger_character(self):
        """Test a ranger character with wilderness skills"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Aria",
            race="Wood Elf",
            char_class="Ranger",
            level=2,
            background="Outlander",
            alignment="Neutral Good",
            ability_scores={"Strength": 14, "Dexterity": 18, "Constitution": 14, "Intelligence": 12, "Wisdom": 16, "Charisma": 10},
            skills=["Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"],
            proficiencies=["Light armor", "Medium armor", "Shields", "Simple weapons", "Martial weapons"],
            equipment=["Longbow", "20 arrows", "Scale mail", "Explorer's pack"]
        )
        
        self.assertIn("Aria", result)
        self.assertIn("Class: Ranger (Level 2)", output)
        self.assertIn("DEX: 18", output)
        self.assertIn("20 arrows", output)
    
    def test_bard_character(self):
        """Test a bard character with performance skills"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Lysandra",
            race="Half-Elf",
            char_class="Bard",
            level=3,
            background="Entertainer",
            alignment="Chaotic Good",
            ability_scores={"Strength": 10, "Dexterity": 16, "Constitution": 14, "Intelligence": 12, "Wisdom": 8, "Charisma": 18},
            skills=["Acrobatics", "Deception", "Insight", "Intimidation", "Performance", "Persuasion"],
            proficiencies=["Light armor", "Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
            equipment=["Rapier", "Lute", "Entertainer's pack", "Costume"]
        )
        
        self.assertIn("Lysandra", result)
        self.assertIn("Class: Bard (Level 3)", output)
        self.assertIn("CHA: 18", output)
        self.assertIn("Lute", output)
    
    def test_edge_case_empty_lists(self):
        """Test with empty skills and proficiencies lists"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Minimal",
            race="Human",
            char_class="Fighter",
            level=1,
            background="Soldier",
            alignment="Neutral",
            ability_scores={"Strength": 15, "Dexterity": 14, "Constitution": 13, "Intelligence": 12, "Wisdom": 10, "Charisma": 8},
            skills=[],
            proficiencies=[],
            equipment=[]
        )
        
        self.assertIn("Minimal", result)
        self.assertIn("SKILLS & PROFICIENCIES", output)
        self.assertIn("EQUIPMENT", output)
        # Should handle empty lists gracefully
    
    def test_edge_case_single_items(self):
        """Test with single items in lists"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Simple",
            race="Elf",
            char_class="Wizard",
            level=1,
            background="Sage",
            alignment="Lawful Good",
            ability_scores={"Strength": 8, "Dexterity": 14, "Constitution": 12, "Intelligence": 16, "Wisdom": 10, "Charisma": 12},
            skills=["Arcana"],
            proficiencies=["Daggers"],
            equipment=["Spellbook"]
        )
        
        self.assertIn("Simple", result)
        self.assertIn("Arcana", output)
        self.assertIn("Daggers", output)
        self.assertIn("Spellbook", output)
    
    def test_edge_case_long_names(self):
        """Test with very long character names"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Very Long Character Name That Might Break Formatting",
            race="Dragonborn",
            char_class="Paladin",
            level=1,
            background="Noble",
            alignment="Lawful Good",
            ability_scores={"Strength": 16, "Dexterity": 10, "Constitution": 14, "Intelligence": 12, "Wisdom": 8, "Charisma": 18},
            skills=["Athletics", "Insight"],
            proficiencies=["All armor", "Shields"],
            equipment=["Longsword", "Shield"]
        )
        
        self.assertIn("Very Long Character Name That Might Break Formatting", result)
        self.assertIn("Name: Very Long Character Name That Might Break Formatting", output)
    
    def test_edge_case_high_level(self):
        """Test with high level character"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Epic Hero",
            race="Human",
            char_class="Fighter",
            level=20,
            background="Hero",
            alignment="Chaotic Good",
            ability_scores={"Strength": 20, "Dexterity": 18, "Constitution": 20, "Intelligence": 16, "Wisdom": 14, "Charisma": 12},
            skills=["Athletics", "Intimidation", "Perception", "Survival"],
            proficiencies=["All armor", "Shields", "Simple weapons", "Martial weapons"],
            equipment=["Legendary Sword", "Dragon Scale Armor", "Ring of Protection"]
        )
        
        self.assertIn("Epic Hero", result)
        self.assertIn("Class: Fighter (Level 20)", output)
        self.assertIn("STR: 20", output)
        self.assertIn("Legendary Sword", output)
    
    def test_edge_case_special_characters(self):
        """Test with special characters in names and equipment"""
        result, output = self.capture_print_output(
            finalize_character,
            name="K'thrall the Destroyer",
            race="Tiefling",
            char_class="Warlock",
            level=1,
            background="Criminal",
            alignment="Chaotic Evil",
            ability_scores={"Strength": 12, "Dexterity": 14, "Constitution": 13, "Intelligence": 16, "Wisdom": 10, "Charisma": 18},
            skills=["Deception", "Intimidation"],
            proficiencies=["Light armor", "Simple weapons"],
            equipment=["Dagger of Venom", "Potion of Healing", "Scroll of Fireball"]
        )
        
        self.assertIn("K'thrall the Destroyer", result)
        self.assertIn("Name: K'thrall the Destroyer", output)
        self.assertIn("Dagger of Venom", output)
        self.assertIn("Scroll of Fireball", output)
    
    def test_edge_case_mixed_case_ability_scores(self):
        """Test with mixed case ability score keys"""
        result, output = self.capture_print_output(
            finalize_character,
            name="Mixed Case",
            race="Human",
            char_class="Fighter",
            level=1,
            background="Soldier",
            alignment="Neutral",
            ability_scores={"STR": 15, "Dexterity": 14, "CON": 13, "Intelligence": 12, "WIS": 10, "Charisma": 8},
            skills=["Athletics"],
            proficiencies=["All armor"],
            equipment=["Longsword"]
        )
        
        self.assertIn("Mixed Case", result)
        self.assertIn("STR: 15", output)
        self.assertIn("DEX: 14", output)
        self.assertIn("CON: 13", output)
        self.assertIn("INT: 12", output)
        self.assertIn("WIS: 10", output)
        self.assertIn("CHA: 8", output)

if __name__ == '__main__':
    unittest.main(verbosity=2) 