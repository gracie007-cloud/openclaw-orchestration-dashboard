"""init (squashed)

Revision ID: 1d844b04ee06
Revises:
Create Date: 2026-02-06

This is a squashed init migration representing the current schema at revision
`1d844b04ee06`.

Note: older Alembic revision files were consolidated into this single revision.
Databases already stamped/applied at `1d844b04ee06` will remain compatible.
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = "1d844b04ee06"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "gateways",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("token", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("main_session_key", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("workspace_root", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "skyll_enabled",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "boards",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("slug", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("gateway_id", sa.Uuid(), nullable=True),
        sa.Column(
            "board_type",
            sa.String(),
            server_default="goal",
            nullable=False,
        ),
        sa.Column("objective", sa.Text(), nullable=True),
        sa.Column("success_metrics", sa.JSON(), nullable=True),
        sa.Column("target_date", sa.DateTime(), nullable=True),
        sa.Column(
            "goal_confirmed",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("goal_source", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["gateway_id"], ["gateways.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_boards_slug", "boards", ["slug"], unique=False)
    op.create_index("ix_boards_gateway_id", "boards", ["gateway_id"], unique=False)
    op.create_index("ix_boards_board_type", "boards", ["board_type"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("clerk_user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("preferred_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("pronouns", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("timezone", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("notes", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("context", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("is_super_admin", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_clerk_user_id", "users", ["clerk_user_id"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "agents",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("board_id", sa.Uuid(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("openclaw_session_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("agent_token_hash", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("heartbeat_config", sa.JSON(), nullable=True),
        sa.Column("identity_profile", sa.JSON(), nullable=True),
        sa.Column("identity_template", sa.Text(), nullable=True),
        sa.Column("soul_template", sa.Text(), nullable=True),
        sa.Column("provision_requested_at", sa.DateTime(), nullable=True),
        sa.Column(
            "provision_confirm_token_hash",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=True,
        ),
        sa.Column("provision_action", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("delete_requested_at", sa.DateTime(), nullable=True),
        sa.Column(
            "delete_confirm_token_hash",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=True,
        ),
        sa.Column("last_seen_at", sa.DateTime(), nullable=True),
        sa.Column(
            "is_board_lead",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agents_board_id", "agents", ["board_id"], unique=False)
    op.create_index("ix_agents_name", "agents", ["name"], unique=False)
    op.create_index("ix_agents_status", "agents", ["status"], unique=False)
    op.create_index(
        "ix_agents_openclaw_session_id", "agents", ["openclaw_session_id"], unique=False
    )
    op.create_index("ix_agents_agent_token_hash", "agents", ["agent_token_hash"], unique=False)
    op.create_index(
        "ix_agents_provision_confirm_token_hash",
        "agents",
        ["provision_confirm_token_hash"],
        unique=False,
    )
    op.create_index("ix_agents_provision_action", "agents", ["provision_action"], unique=False)
    op.create_index(
        "ix_agents_delete_confirm_token_hash",
        "agents",
        ["delete_confirm_token_hash"],
        unique=False,
    )
    op.create_index("ix_agents_is_board_lead", "agents", ["is_board_lead"], unique=False)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("board_id", sa.Uuid(), nullable=True),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("priority", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("due_at", sa.DateTime(), nullable=True),
        sa.Column("in_progress_at", sa.DateTime(), nullable=True),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("assigned_agent_id", sa.Uuid(), nullable=True),
        sa.Column(
            "auto_created",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("auto_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["assigned_agent_id"], ["agents.id"]),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tasks_board_id", "tasks", ["board_id"], unique=False)
    op.create_index("ix_tasks_status", "tasks", ["status"], unique=False)
    op.create_index("ix_tasks_priority", "tasks", ["priority"], unique=False)
    op.create_index("ix_tasks_due_at", "tasks", ["due_at"], unique=False)
    op.create_index("ix_tasks_assigned_agent_id", "tasks", ["assigned_agent_id"], unique=False)
    op.create_index("ix_tasks_created_by_user_id", "tasks", ["created_by_user_id"], unique=False)

    op.create_table(
        "activity_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("message", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("agent_id", sa.Uuid(), nullable=True),
        sa.Column("task_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_activity_events_event_type", "activity_events", ["event_type"], unique=False)
    op.create_index("ix_activity_events_agent_id", "activity_events", ["agent_id"], unique=False)
    op.create_index("ix_activity_events_task_id", "activity_events", ["task_id"], unique=False)

    op.create_table(
        "board_memory",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("board_id", sa.Uuid(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column(
            "is_chat",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("source", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_board_memory_board_id", "board_memory", ["board_id"], unique=False)
    op.create_index("ix_board_memory_is_chat", "board_memory", ["is_chat"], unique=False)
    op.create_index(
        "ix_board_memory_board_id_is_chat_created_at",
        "board_memory",
        ["board_id", "is_chat", "created_at"],
        unique=False,
    )

    op.create_table(
        "approvals",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("board_id", sa.Uuid(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=True),
        sa.Column("agent_id", sa.Uuid(), nullable=True),
        sa.Column("action_type", sa.String(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Integer(), nullable=False),
        sa.Column("rubric_scores", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_approvals_board_id", "approvals", ["board_id"], unique=False)
    op.create_index("ix_approvals_agent_id", "approvals", ["agent_id"], unique=False)
    op.create_index("ix_approvals_task_id", "approvals", ["task_id"], unique=False)
    op.create_index("ix_approvals_status", "approvals", ["status"], unique=False)

    op.create_table(
        "board_onboarding_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("board_id", sa.Uuid(), nullable=False),
        sa.Column("session_key", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.String(),
            server_default="active",
            nullable=False,
        ),
        sa.Column("messages", sa.JSON(), nullable=True),
        sa.Column("draft_goal", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_board_onboarding_sessions_board_id",
        "board_onboarding_sessions",
        ["board_id"],
        unique=False,
    )
    op.create_index(
        "ix_board_onboarding_sessions_status",
        "board_onboarding_sessions",
        ["status"],
        unique=False,
    )

    op.create_table(
        "task_fingerprints",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("board_id", sa.Uuid(), nullable=False),
        sa.Column("fingerprint_hash", sa.String(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_task_fingerprints_board_hash",
        "task_fingerprints",
        ["board_id", "fingerprint_hash"],
        unique=True,
    )
    op.create_index(
        "ix_task_fingerprints_board_id",
        "task_fingerprints",
        ["board_id"],
        unique=False,
    )
    op.create_index(
        "ix_task_fingerprints_fingerprint_hash",
        "task_fingerprints",
        ["fingerprint_hash"],
        unique=False,
    )
    op.create_index(
        "ix_task_fingerprints_task_id",
        "task_fingerprints",
        ["task_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_task_fingerprints_task_id", table_name="task_fingerprints")
    op.drop_index(
        "ix_task_fingerprints_fingerprint_hash",
        table_name="task_fingerprints",
    )
    op.drop_index("ix_task_fingerprints_board_id", table_name="task_fingerprints")
    op.drop_index("ix_task_fingerprints_board_hash", table_name="task_fingerprints")
    op.drop_table("task_fingerprints")

    op.drop_index(
        "ix_board_onboarding_sessions_status",
        table_name="board_onboarding_sessions",
    )
    op.drop_index(
        "ix_board_onboarding_sessions_board_id",
        table_name="board_onboarding_sessions",
    )
    op.drop_table("board_onboarding_sessions")

    op.drop_index("ix_approvals_status", table_name="approvals")
    op.drop_index("ix_approvals_task_id", table_name="approvals")
    op.drop_index("ix_approvals_agent_id", table_name="approvals")
    op.drop_index("ix_approvals_board_id", table_name="approvals")
    op.drop_table("approvals")

    op.drop_index(
        "ix_board_memory_board_id_is_chat_created_at",
        table_name="board_memory",
    )
    op.drop_index("ix_board_memory_is_chat", table_name="board_memory")
    op.drop_index("ix_board_memory_board_id", table_name="board_memory")
    op.drop_table("board_memory")

    op.drop_index("ix_activity_events_task_id", table_name="activity_events")
    op.drop_index("ix_activity_events_agent_id", table_name="activity_events")
    op.drop_index("ix_activity_events_event_type", table_name="activity_events")
    op.drop_table("activity_events")

    op.drop_index("ix_tasks_created_by_user_id", table_name="tasks")
    op.drop_index("ix_tasks_assigned_agent_id", table_name="tasks")
    op.drop_index("ix_tasks_due_at", table_name="tasks")
    op.drop_index("ix_tasks_priority", table_name="tasks")
    op.drop_index("ix_tasks_status", table_name="tasks")
    op.drop_index("ix_tasks_board_id", table_name="tasks")
    op.drop_table("tasks")

    op.drop_index("ix_agents_is_board_lead", table_name="agents")
    op.drop_index("ix_agents_delete_confirm_token_hash", table_name="agents")
    op.drop_index("ix_agents_provision_action", table_name="agents")
    op.drop_index("ix_agents_provision_confirm_token_hash", table_name="agents")
    op.drop_index("ix_agents_agent_token_hash", table_name="agents")
    op.drop_index("ix_agents_openclaw_session_id", table_name="agents")
    op.drop_index("ix_agents_status", table_name="agents")
    op.drop_index("ix_agents_name", table_name="agents")
    op.drop_index("ix_agents_board_id", table_name="agents")
    op.drop_table("agents")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_clerk_user_id", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_boards_board_type", table_name="boards")
    op.drop_index("ix_boards_gateway_id", table_name="boards")
    op.drop_index("ix_boards_slug", table_name="boards")
    op.drop_table("boards")

    op.drop_table("gateways")

