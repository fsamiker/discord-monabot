from data.genshin.skill import Skill


class Character:

    def __init__(self, ch_json):
        self.name = ch_json.get('Name')
        if self.name is None:
            raise KeyError

        self.sex = ch_json.get('Sex', 'Unknown')
        self.birthday = ch_json.get('Birthday', 'Unknown')
        self.region = ch_json.get('Region', 'Unknown')
        self.affiliation = ch_json.get('Affiliation', 'Unknown')
        self.special_dish = ch_json.get('Special Dish', 'Unknown')
        self.obtain = ch_json.get('How to Obtain', 'Unknown')
        self.skills = ch_json.get('skills', [])
        self.element = ch_json.get('Element', 'Unknown')
        self.rarity = int(ch_json.get('Rarity', 0)) or 0
        self.weapon = ch_json.get('Weapon', 'Unknown')
        self.base_stats = ch_json.get('base_stats', [])
        self.talent_materials = ch_json.get('talent_materials', [])
        self.constellation = ch_json.get('constellation', [])
        self.ascension = ch_json.get('ascension', [])


    def get_basic_info(self):
        return [self.weapon, self.region, self.birthday, self.affiliation, self.special_dish]

    def get_icon(self):
        return f'assets/genshin/characters/i_{self.name}.png'

    def get_portrait(self):
        return f'assets/genshin/characters/p_{self.name}.png'
    
    def get_element_icon(self):
        return f'assets/genshin/icons/i_{self.element}.png'

    def get_skills(self, sk_db):
        output = []
        for s in self.skills:
            name = s.replace(':', '-')
            output.append(Skill(sk_db.get(name)))
        return output