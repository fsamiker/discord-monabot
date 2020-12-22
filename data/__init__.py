from sqlalchemy.orm import registry

mapper_reg = registry()
Base = mapper_reg.generate_base()