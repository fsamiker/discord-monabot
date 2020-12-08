class Skill:

    def __init__(self, sk_json):
        self.name = sk_json.get('Name')
        if self.name is None:
            raise KeyError
        self.description = sk_json.get('Description', 'N/A').replace('\n', ' ')
        self.type = sk_json.get('Type', 'Unknown')
        self.scaling = sk_json.get('Scaling', [])
        self.levelling = sk_json.get('Leveling', [])

    def get_icon(self):
        return f'assets/genshin/icons/i_{self.name.replace(":", "-")}.png'