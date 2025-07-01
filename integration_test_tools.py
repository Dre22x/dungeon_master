import unittest
import time
from tools import tools, character_data, classes, races, spells, subclasses, monsters, equipment, weapons, magic_items, traits, subraces, rules, game_mechanics

# Helper to avoid hammering the API
API_DELAY = 0.2

def api_sleep():
    time.sleep(API_DELAY)

class IntegrationTestTools(unittest.TestCase):
    """Integration tests for all tools functions that call the real D&D 5e API"""
    
    # ==============================================================================
    # EQUIPMENT TESTS
    # ==============================================================================
    
    def test_get_all_equipment(self):
        api_sleep()
        result = equipment.get_all_equipment()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertTrue(any('name' in item for item in result))

    def test_get_equipment_details(self):
        api_sleep()
        details = equipment.get_equipment_details("Longsword")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Longsword')

    def test_get_all_equipment_categories(self):
        api_sleep()
        result = equipment.get_all_equipment_categories()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_equipment_by_category(self):
        api_sleep()
        result = equipment.get_equipment_by_category("Weapon")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    # ==============================================================================
    # CHARACTER DATA TESTS
    # ==============================================================================
    
    def test_get_ability_score_details(self):
        api_sleep()
        details = character_data.get_ability_score_details("str")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'STR')  # API returns abbreviation

    def test_get_alignment_details(self):
        api_sleep()
        details = character_data.get_alignment_details("lawful-good")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Lawful Good')

    def test_get_background_details(self):
        api_sleep()
        details = character_data.get_background_details("acolyte")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Acolyte')

    def test_get_skill_details(self):
        api_sleep()
        details = character_data.get_skill_details("athletics")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Athletics')

    def test_get_proficiency_details(self):
        api_sleep()
        details = character_data.get_proficiency_details("longswords")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Longswords')

    def test_get_language_details(self):
        api_sleep()
        details = character_data.get_language_details("common")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Common')

    def test_get_all_backgrounds(self):
        api_sleep()
        result = character_data.get_all_backgrounds()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    def test_get_all_languages(self):
        api_sleep()
        result = character_data.get_all_languages()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    def test_get_all_proficiencies(self):
        api_sleep()
        result = character_data.get_all_proficiencies()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    def test_get_all_skills(self):
        api_sleep()
        result = character_data.get_all_skills()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    def test_get_all_ability_scores(self):
        api_sleep()
        result = character_data.get_all_ability_scores()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    def test_get_all_alignments(self):
        api_sleep()
        result = character_data.get_all_alignments()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    # ==============================================================================
    # CLASSES TESTS
    # ==============================================================================
    
    def test_get_all_classes(self):
        api_sleep()
        result = classes.get_all_classes()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    def test_get_class_details(self):
        api_sleep()
        details = classes.get_class_details("fighter")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Fighter')

    def test_get_subclasses_available_for_class(self):
        api_sleep()
        result = classes.get_subclasses_available_for_class("fighter")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_spells_available_for_class(self):
        api_sleep()
        result = classes.get_spells_available_for_class("wizard")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_features_available_for_class(self):
        api_sleep()
        result = classes.get_features_available_for_class("fighter")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_proficiencies_available_for_class(self):
        api_sleep()
        result = classes.get_proficiencies_available_for_class("fighter")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_all_level_resources_for_class(self):
        api_sleep()
        result = classes.get_all_level_resources_for_class("fighter")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_level_resources_for_class_at_level(self):
        api_sleep()
        result = classes.get_level_resources_for_class_at_level("fighter", "1")
        self.assertIsInstance(result, dict)
        self.assertIn('level', result)

    def test_get_features_for_class_at_level(self):
        api_sleep()
        result = classes.get_features_for_class_at_level("fighter", "1")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_spells_for_class_at_level(self):
        api_sleep()
        result = classes.get_spells_for_class_at_level("wizard", "1")
        self.assertIsInstance(result, list)

    # ==============================================================================
    # RACES TESTS
    # ==============================================================================
    
    def test_get_all_races(self):
        api_sleep()
        result = races.get_all_races()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_race_details(self):
        api_sleep()
        details = races.get_race_details("elf")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Elf')

    def test_get_subraces_available_for_race(self):
        api_sleep()
        result = races.get_subraces_available_for_race("elf")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_proficiencies_available_for_race(self):
        api_sleep()
        result = races.get_proficiencies_available_for_race("elf")
        self.assertIsInstance(result, list)

    def test_get_traits_available_for_race(self):
        api_sleep()
        result = races.get_traits_available_for_race("elf")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    # ==============================================================================
    # SPELLS TESTS
    # ==============================================================================
    
    def test_get_all_spells(self):
        api_sleep()
        result = spells.get_all_spells()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_spell_details(self):
        api_sleep()
        details = spells.get_spell_details("fireball")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Fireball')

    def test_get_spells_by_level(self):
        api_sleep()
        result = spells.get_spells_by_level("3")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_spells_by_school(self):
        api_sleep()
        result = spells.get_spells_by_school("evocation")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_spells_by_level_and_school(self):
        api_sleep()
        result = spells.get_spells_by_level_and_school("3", "evocation")
        self.assertIsInstance(result, list)

    # ==============================================================================
    # SUBCLASSES TESTS
    # ==============================================================================
    
    def test_get_all_subclasses(self):
        api_sleep()
        result = subclasses.get_all_subclasses()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    def test_get_subclass_details(self):
        api_sleep()
        details = subclasses.get_subclass_details("champion")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Champion')

    def test_get_features_available_for_subclass(self):
        api_sleep()
        result = subclasses.get_features_available_for_subclass("champion")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_all_level_resources_for_subclass(self):
        api_sleep()
        result = subclasses.get_all_level_resources_for_subclass("champion")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_level_resources_for_subclass_at_level(self):
        api_sleep()
        result = subclasses.get_level_resources_for_subclass_at_level("champion", "3")
        self.assertIsInstance(result, dict)
        self.assertIn('level', result)

    def test_get_features_of_spell_level_for_subclass(self):
        api_sleep()
        result = subclasses.get_features_of_spell_level_for_subclass("champion", "3")
        self.assertIsInstance(result, list)

    # ==============================================================================
    # MONSTERS TESTS
    # ==============================================================================
    
    def test_get_all_monsters(self):
        api_sleep()
        result = monsters.get_all_monsters()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_monster_details(self):
        api_sleep()
        details = monsters.get_monster_details("goblin")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Goblin')

    def test_get_monster_by_challenge_rating(self):
        api_sleep()
        result = monsters.get_monster_by_challenge_rating("1/4")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    # ==============================================================================
    # WEAPONS TESTS
    # ==============================================================================
    
    def test_get_all_weapon_properties(self):
        api_sleep()
        result = weapons.get_all_weapon_properties()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_weapon_property_details(self):
        api_sleep()
        details = weapons.get_weapon_property_details("finesse")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Finesse')

    # ==============================================================================
    # MAGIC ITEMS TESTS
    # ==============================================================================
    
    def test_get_all_magic_items(self):
        api_sleep()
        result = magic_items.get_all_magic_items()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_magic_item_details(self):
        api_sleep()
        details = magic_items.get_magic_item_details("sword-of-sharpness")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Sword of Sharpness')

    def test_get_all_magic_schools(self):
        api_sleep()
        result = magic_items.get_all_magic_schools()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    # ==============================================================================
    # TRAITS TESTS
    # ==============================================================================
    
    def test_get_all_traits(self):
        api_sleep()
        result = traits.get_all_traits()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_trait_details(self):
        api_sleep()
        details = traits.get_trait_details("darkvision")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Darkvision')

    # ==============================================================================
    # SUBRACES TESTS
    # ==============================================================================
    
    def test_get_all_subraces(self):
        api_sleep()
        result = subraces.get_all_subraces()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_subrace_details(self):
        api_sleep()
        details = subraces.get_subrace_details("high-elf")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'High Elf')

    def test_get_proficiencies_available_for_subrace(self):
        api_sleep()
        result = subraces.get_proficiencies_available_for_subrace("high-elf")
        self.assertIsInstance(result, list)

    def test_get_traits_available_for_subrace(self):
        api_sleep()
        result = subraces.get_traits_available_for_subrace("high-elf")
        self.assertIsInstance(result, list)

    # ==============================================================================
    # RULES TESTS
    # ==============================================================================
    
    def test_get_all_rules(self):
        api_sleep()
        result = rules.get_all_rules()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_rules_details(self):
        api_sleep()
        details = rules.get_rules_details("spellcasting")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Spellcasting')

    def test_get_rules_by_section(self):
        api_sleep()
        details = rules.get_rules_by_section("spellcasting")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Spellcasting')

    def test_get_all_rules_sections(self):
        api_sleep()
        result = rules.get_all_rules_sections()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    # ==============================================================================
    # GAME MECHANICS TESTS
    # ==============================================================================
    
    def test_get_all_conditions(self):
        api_sleep()
        result = game_mechanics.get_all_conditions()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_condition_details(self):
        api_sleep()
        details = game_mechanics.get_condition_details("poisoned")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Poisoned')

    def test_get_all_damage_types(self):
        api_sleep()
        result = game_mechanics.get_all_damage_types()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_damage_type_details(self):
        api_sleep()
        details = game_mechanics.get_damage_type_details("fire")
        self.assertIsInstance(details, dict)
        self.assertIn('name', details)
        self.assertEqual(details['name'], 'Fire')

    # ==============================================================================
    # TOOLS MODULE TESTS
    # ==============================================================================
    
    def test_get_all_equipments(self):
        api_sleep()
        result = tools.get_all_equipments()
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertTrue(len(result['results']) > 0)

    # Skipped/removed tests for non-existent endpoints: multiclassing, spellcasting, starting equipment

if __name__ == '__main__':
    unittest.main(verbosity=2) 