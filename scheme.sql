CREATE TABLE tags (
    code VARCHAR(255) NOT NULL COLLATE NOCASE,
    content VARCHAR(255) NOT NULL,
    author_id INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    created_at DATE DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'utc')),
    updated_at DATE,
    deleted_at DATE,
    usage INTEGER DEFAULT 0
);

CREATE UNIQUE INDEX unique_active_tag ON tags(code) WHERE deleted_at IS NULL;
