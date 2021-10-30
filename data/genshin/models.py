from data import Base
from sqlalchemy.util.langhelpers import hybridproperty
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey, Table
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

class WeaponMaterial(Base):
    __tablename__ = 'weaponmaterial'
    talent_id = Column(Integer, ForeignKey('weaponlevels.id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), primary_key=True)
    count = Column(Integer)
    material = relationship("Material")

    def __repr__(self):
        return f'<{self.material.name} x{self.count}>'

materialenemy_association = Table('enemymaterial', Base.metadata,
    Column('material_id', Integer, ForeignKey('materials.id')),
    Column('enemy_id', Integer, ForeignKey('enemies.id'))
)

materialdomain_association = Table('domainmaterial', Base.metadata,
    Column('material_id', Integer, ForeignKey('materials.id')),
    Column('domainlevel_id', Integer, ForeignKey('domainlevels.id'))
)
artifactdomain_association =Table('domainartifact', Base.metadata,
    Column('artifact_id', Integer, ForeignKey('artifacts.id')),
    Column('domainlevel_id', Integer, ForeignKey('domainlevels.id'))
)

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
    dropped_by = relationship(
        "Enemy",
        secondary=materialenemy_association,
        back_populates="material_drops")
    domains = relationship(
        "DomainLevel",
        secondary=materialdomain_association,
        back_populates="material_drops")

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

    def __repr__(self):
        return f'<Food: {self.name}>'

class Weapon(Base):
    __tablename__= 'weapons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    icon_url = Column(String)
    rarity = Column(Integer)
    typing = Column(String)
    series = Column(String)
    levels = relationship("WeaponLevel", back_populates="weapon")
    description = Column(String)
    effect = Column(String)
    secondary_stat = Column(String)

    def __repr__(self):
        return f'<Weapon ({self.typing}): {self.name}>'

class WeaponLevel(Base):
    __tablename__= 'weaponlevels'
    id = Column(Integer, primary_key=True)
    weapon_id = Column(Integer, ForeignKey('weapons.id'))
    weapon = relationship("Weapon", back_populates="levels")
    level = Column(Integer)
    cost = Column(Integer)
    base_atk = Column(Integer)
    base_secondary = Column(String)
    materials = relationship("WeaponMaterial")

    def __repr__(self):
        return f'<{self.weapon.name} stats Lvl {self.level}>'

class Enemy(Base):
    __tablename__= 'enemies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    icon_url = Column(String)
    material_drops = relationship(
        "Material",
        secondary=materialenemy_association,
        back_populates="dropped_by")
    variants = Column(String)
    typing = Column(String)

    def __repr__(self):
        return f'<Enemy ({self.typing}): {self.name}>'

    def get_variants(self):
        return self.variants.split(',')

class Artifact(Base):
    __tablename__= 'artifacts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    icon_url = Column(String)
    min_rarity = Column(Integer)
    max_rarity = Column(Integer)
    bonus_one = Column(String)
    bonus_two = Column(String)
    bonus_three = Column(String)
    bonus_four = Column(String)
    bonus_five = Column(String)
    domains = relationship(
        "DomainLevel",
        secondary=artifactdomain_association,
        back_populates="artifact_drops")

    def __repr__(self):
        return f'<Artifact Set: {self.name}>'

class Domain(Base):
    __tablename__= 'domains'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    icon_url = Column(String)
    location = Column(String)
    description = Column(String)
    recommended_elements = Column(String)
    typing = Column(String)
    levels = relationship("DomainLevel", back_populates="domain")

    def __repr__(self):
        return f'<Domain: {self.name}>'

    def get_rec_elements(self):
        if self.recommended_elements:
            return self.recommended_elements.split(',')
        return

class DomainLevel(Base):
    __tablename__= 'domainlevels'
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer, ForeignKey('domains.id'))
    domain = relationship("Domain", back_populates="levels")
    day = Column(String)
    requirement = Column(Integer)
    ar_exp = Column(Integer)
    friendship_exp = Column(Integer)
    mora = Column(Integer)
    leyline = Column(String)
    level = Column(Integer)
    material_drops = relationship(
        "Material",
        secondary=materialdomain_association,
        back_populates="domains")
    artifact_drops = relationship(
        "Artifact",
        secondary=artifactdomain_association,
        back_populates="domains")
    enemies = Column(String)
    objective = Column(String)

    def __repr__(self):
        return f'<Domain Level: {self.domain.name}>'

    def get_enemies(self):
        return self.enemies.split('\n')
