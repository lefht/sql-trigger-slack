CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

-- Create notification trigger function
CREATE OR REPLACE FUNCTION notify_user_changes()
RETURNS TRIGGER AS $$
DECLARE
    notification json;
BEGIN
    notification := json_build_object(
        'operation', TG_OP,
        'record', json_build_object(
            'id', NEW.id,
            'name', NEW.name,
            'email', NEW.email
        )
    );
    PERFORM pg_notify('my_channel', notification::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS user_changes_trigger ON users;
CREATE TRIGGER user_changes_trigger
    AFTER INSERT OR UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION notify_user_changes();
