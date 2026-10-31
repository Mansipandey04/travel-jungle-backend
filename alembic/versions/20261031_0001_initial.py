"""initial schema

Revision ID: 20261031_0001
Revises:
Create Date: 2026-10-31

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261031_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

JSONType = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "destinations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("region", sa.String(length=120), nullable=False),
        sa.Column("state", sa.String(length=120), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("hero_image_url", sa.String(length=500), nullable=True),
        sa.Column("editorial", JSONType, nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_demo", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_destinations_slug", "destinations", ["slug"], unique=True)

    op.create_table(
        "trips",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("destination_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=True),
        sa.Column("itinerary", JSONType, nullable=True),
        sa.Column("inclusions", JSONType, nullable=True),
        sa.Column("hero_image_url", sa.String(length=500), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_demo", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["destination_id"], ["destinations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_trips_slug", "trips", ["slug"], unique=True)
    op.create_index("ix_trips_destination_id", "trips", ["destination_id"])

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("destination_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=True),
        sa.Column("ends_on", sa.Date(), nullable=True),
        sa.Column("location_label", sa.String(length=200), nullable=True),
        sa.Column("hero_image_url", sa.String(length=500), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_demo", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["destination_id"], ["destinations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_events_slug", "events", ["slug"], unique=True)
    op.create_index("ix_events_destination_id", "events", ["destination_id"])

    op.create_table(
        "hidden_india_stories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("destination_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("tagline", sa.String(length=300), nullable=False),
        sa.Column("layer_discover", JSONType, nullable=False),
        sa.Column("layer_experience", JSONType, nullable=False),
        sa.Column("layer_explore", JSONType, nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_demo", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["destination_id"], ["destinations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("destination_id"),
    )
    op.create_index("ix_hidden_india_stories_slug", "hidden_india_stories", ["slug"], unique=True)

    op.create_table(
        "travel_stories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("destination_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("body_md", sa.Text(), nullable=False),
        sa.Column("author_display", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("is_demo", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["destination_id"], ["destinations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_travel_stories_slug", "travel_stories", ["slug"], unique=True)
    op.create_index("ix_travel_stories_destination_id", "travel_stories", ["destination_id"])
    op.create_index("ix_travel_stories_status", "travel_stories", ["status"])

    op.create_table(
        "story_images",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("travel_story_id", sa.Integer(), nullable=True),
        sa.Column("hidden_india_story_id", sa.Integer(), nullable=True),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("alt", sa.String(length=300), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("credit", sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(["travel_story_id"], ["travel_stories.id"]),
        sa.ForeignKeyConstraint(["hidden_india_story_id"], ["hidden_india_stories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_story_images_travel_story_id", "story_images", ["travel_story_id"])
    op.create_index("ix_story_images_hidden_india_story_id", "story_images", ["hidden_india_story_id"])

    op.create_table(
        "enquiries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("subject", sa.String(length=200), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("contact_messages")
    op.drop_table("enquiries")
    op.drop_index("ix_story_images_hidden_india_story_id", table_name="story_images")
    op.drop_index("ix_story_images_travel_story_id", table_name="story_images")
    op.drop_table("story_images")
    op.drop_index("ix_travel_stories_status", table_name="travel_stories")
    op.drop_index("ix_travel_stories_destination_id", table_name="travel_stories")
    op.drop_index("ix_travel_stories_slug", table_name="travel_stories")
    op.drop_table("travel_stories")
    op.drop_index("ix_hidden_india_stories_slug", table_name="hidden_india_stories")
    op.drop_table("hidden_india_stories")
    op.drop_index("ix_events_destination_id", table_name="events")
    op.drop_index("ix_events_slug", table_name="events")
    op.drop_table("events")
    op.drop_index("ix_trips_destination_id", table_name="trips")
    op.drop_index("ix_trips_slug", table_name="trips")
    op.drop_table("trips")
    op.drop_index("ix_destinations_slug", table_name="destinations")
    op.drop_table("destinations")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
