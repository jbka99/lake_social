from alembic import op
import sqlalchemy as sa


revision = "d339a62ffea9"
down_revision = "bcc0fb809f19"
branch_labels = None
depends_on = None


def _has_column(bind, table_name: str, column_name: str) -> bool:
    """Portable-ish check for Postgres/SQLite."""
    dialect = bind.dialect.name
    if dialect == "postgresql":
        sql = sa.text(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = :t AND column_name = :c
            """
        )
        return bind.execute(sql, {"t": table_name, "c": column_name}).first() is not None

    # sqlite fallback
    if dialect == "sqlite":
        rows = bind.execute(sa.text(f"PRAGMA table_info({table_name})")).fetchall()
        return any(r[1] == column_name for r in rows)

    # generic fallback: try to select
    try:
        bind.execute(sa.text(f"SELECT {column_name} FROM {table_name} LIMIT 1"))
        return True
    except Exception:
        return False


def upgrade():
    bind = op.get_bind()

    # post.comment_count
    if not _has_column(bind, "post", "comment_count"):
        op.add_column(
            "post",
            sa.Column("comment_count", sa.Integer(), nullable=False, server_default="0"),
        )

    # post.score
    if not _has_column(bind, "post", "score"):
        op.add_column(
            "post",
            sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
        )

    # comment.score
    if not _has_column(bind, "comment", "score"):
        op.add_column(
            "comment",
            sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
        )

    # (опционально) убрать дефолт после заполнения.
    # На Postgres безопаснее НЕ трогать это, чтобы не ловить нюансы alter_column.
    # Если очень хочешь убрать — сделаем отдельной миграцией и с existing_type.


def downgrade():
    bind = op.get_bind()

    # drop in reverse order; check existence to avoid crashes
    if _has_column(bind, "comment", "score"):
        op.drop_column("comment", "score")

    if _has_column(bind, "post", "score"):
        op.drop_column("post", "score")

    if _has_column(bind, "post", "comment_count"):
        op.drop_column("post", "comment_count")
