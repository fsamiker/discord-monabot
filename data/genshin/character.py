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
            output.append(sk_db.get(name))
        return output

    def get_ascension_resource(self, starting_lvl=1, end_lvl=90):
        asc_list = sorted(self.ascension, key=lambda i:int(i['Required Level']))

        return self.get_material_list(asc_list, 'Required Level', 'Materials', starting_lvl, end_lvl)

    def get_talent_resource(self, sk_db, starting_lvl=1, end_lvl=10):
        talents = self.get_skills(sk_db)

        material_lst = []
        for t in talents:
            material_lst += t.levelling

        material_lst = sorted(material_lst, key=lambda i:int(i['Level']))
        return self.get_material_list(material_lst, 'Level', 'Material', starting_lvl, end_lvl)

    @staticmethod
    def get_material_list(material_lst, lvl_key, mat_key, starting_lvl, end_lvl):
        filtered_list = [m for m in material_lst if int(m[lvl_key]) >= starting_lvl and int(m[lvl_key]) <= end_lvl]
        print(filtered_list)
        materials_needed = [a[mat_key] for a in filtered_list]
        mora_needed  = sum([int(a['Mora'].replace(',', '')) for a in filtered_list])
        lvl_range = []
        if len(filtered_list) >= 1:
            lvl_range.append(filtered_list[0][lvl_key])
        if len(filtered_list) >=2:
            lvl_range.append(filtered_list[-1][lvl_key])

        consolidated_materials = {}
        for m in materials_needed:
            for item in m:
                if item[0] is None:
                    continue
                if item[0] in consolidated_materials.keys():
                    consolidated_materials[item[0]] += int(item[1])
                else:
                    consolidated_materials[item[0]] = int(item[1])
        
        return {
            'Materials': consolidated_materials,
            'Mora': mora_needed,
            'Range': lvl_range
        }