from sqlalchemy.orm import ColumnProperty, Composite, Relationship


Property = ColumnProperty | Relationship | Composite
