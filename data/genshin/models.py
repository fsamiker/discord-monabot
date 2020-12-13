from sqlalchemy.util.langhelpers import hybridproperty
from data.db import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class TalentMaterial(Base):
    __tablename__ = 'talentmaterial'
    talent_id = Column(Integer, ForeignKey('talentlevels.id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), primary_key=True)
    count = Column(Integer)
    material = relationship("Material")

    def __repr__(self):
        return f'<{self.material.name} x{self.count}>'

class CharacterMaterial(Base):
    __tablename__ = 'charactermaterial'
    character_id = Column(Integer, ForeignKey('characterlevels.id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), primary_key=True)
    count = Column(Integer)
    material = relationship("Material")

    def __repr__(self):
        return f'<{self.material.name} x{self.count}>'

class Character(Base):

    __tablename__= 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sex = Column(String)
    region = Column(String)
    birthday = Column(String)
    affiliation = Column(String, default='Unknown')
    special_dish = relationship("Food", uselist=False, back_populates="specialty_of")
    obtain_str = Column(String, default='Unknown')
    talents = relationship("Talent", back_populates="character")
    constellations = relationship("Constellation", back_populates="character")
    levels = relationship("CharacterLevel", back_populates="character")
    element = Column(String)
    rarity = Column(Integer)
    weapon_type = Column(String)
    icon_url = Column(String)
    portrait_url = Column(String)
    profile_url = Column (String)

    def __repr__(self):
        return f'<Character: {self.name}>'

class CharacterLevel(Base):
    __tablename__ = 'characterlevels'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="levels")
    level = Column(Integer)
    materials = relationship("CharacterMaterial")
    cost = Column(Integer)
    base_stat_str = Column(String)

    @hybridproperty
    def base_stats(self):
        return

    def __repr__(self):
        return f'<{self.character.name} character stats lvl {self.level}>'

class Talent(Base):
    __tablename__= 'talents'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="talents")
    levels = relationship("TalentLevel", back_populates="talent")
    name = Column(String)
    description = Column(String, default='Unknown')
    typing = Column(String, default='Unknown')
    icon_url = Column(String)

    def __repr__(self):
        return f'<Talent: {self.name} ({self.character.name})>'

class TalentLevel(Base):
    __tablename__ = 'talentlevels'
    id = Column(Integer, primary_key=True)
    talent_id = Column(Integer, ForeignKey('talents.id'))
    talent = relationship("Talent", back_populates="levels")
    level = Column(Integer)
    cost = Column(Integer)
    base_stat_str = Column(String)
    materials = relationship("TalentMaterial")

    @hybridproperty
    def base_stats(self):
        return

    def __repr__(self):
        return f'<{self.character.name} talent stats Lvl {self.level}>'

class Material(Base):
    __tablename__= 'materials'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    typing = Column(String, default='Unknown')
    rarity = Column(Integer)
    description = Column(String, default='Unknown')
    obtain_str = Column(String, default='Unknown')
    icon_url = Column(String)

    def __repr__(self):
        return f'<Material: {self.name}>'

    @hybridproperty
    def how_to_obtain(self):
        return self.obtain_str.split('//')

class Constellation(Base):
    __tablename__= 'constellations'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="constellations")
    name = Column(String)
    effect = Column(String)
    level = Column(Integer)

    def __repr__(self):
        return f'<{self.character.name} constellation C{self.level}: {self.name}>'

class Food(Base):
    __tablename__= 'foods'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    icon_url = Column(String)
    rarity = Column(Integer)
    typing = Column(String)
    description = Column(String)
    effect = Column(String)
    character_id = Column(Integer, ForeignKey('characters.id'))
    specialty_of = relationship("Character", uselist=False, back_populates="special_dish")
