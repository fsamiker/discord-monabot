class Material:

    def __init__(self, mat_json):
        self.name = mat_json.get('Name')
        if self.name is None:
            raise KeyError
        self.type = mat_json.get('Type', 'Unknown')
        self.rarity = int((mat_json.get('Rarity', 0) or 0))
        self.description = mat_json.get('Description')
        self.obtain = mat_json.get('How to Obtain')

    def get_icon(self):
        return f'assets/genshin/icons/i_{self.name}.png'