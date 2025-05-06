from alembic import op
import sqlalchemy as sa

revision = 'V12'
down_revision = 'V11'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE users
        ALTER
        COLUMN role_id TYPE VARCHAR
        USING CASE role_id
            WHEN 1 THEN 'teacher'
            WHEN 2 THEN 'student'
            WHEN 3 THEN 'admin'
            ELSE role_id::text
        END
        """
    )
    op.add_column('lessons', sa.Column('creator_id', sa.String()))
    op.add_column('attendance_sessions', sa.Column('creator_id', sa.String()))
    op.alter_column("users", "role_id", new_column_name="role")
    op.drop_table('roles')


def downgrade():
    op.execute(
        """
        ALTER TABLE users
        ALTER
        COLUMN role_id TYPE INTEGER
        USING CASE role_id
            WHEN 'teacher' THEN 1
            WHEN 'student' THEN 2
            WHEN 'admin' THEN 3
            ELSE role_id::integer
        END
        """
    )

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False)
    )
    op.alter_column("users", "role", new_column_name="role_id")
    op.drop_column('lessons', 'creator_id')
    op.drop_column('attendance_sessions', 'creator_id')
