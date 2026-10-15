"""Initial schema migration

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-10-10 21:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Bảng users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), server_default="CUSTOMER", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_phone_number"), "users", ["phone_number"], unique=True)

    # 2. Bảng catalog_items
    op.create_table(
        "catalog_items",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("stock_quantity", sa.Integer(), server_default="100", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # 3. Bảng orders
    op.create_table(
        "orders",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("user_id", sa.String(length=50), server_default="guest_user", nullable=False),
        sa.Column("item_id", sa.String(length=50), nullable=False),
        sa.Column("scheduled_time", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="CONFIRMED", nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("notes", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orders_scheduled_time"), "orders", ["scheduled_time"], unique=False)

def downgrade() -> None:
    op.drop_index(op.f("ix_orders_scheduled_time"), table_name="orders")
    op.drop_table("orders")
    op.drop_table("catalog_items")
    op.drop_index(op.f("ix_users_phone_number"), table_name="users")
    op.drop_table("users")
