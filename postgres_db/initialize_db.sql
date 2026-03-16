-- =========================
-- Request table
-- =========================
CREATE TABLE IF NOT EXISTS request (
    id SERIAL PRIMARY KEY,
    request_timestamp TIMESTAMP NOT NULL,
    recordcount INTEGER
);

-- =========================
-- Observation table
-- =========================
CREATE TABLE IF NOT EXISTS observation (
    id SERIAL PRIMARY KEY,
    source_id TEXT NOT NULL,
    request_id INTEGER NOT NULL,
    observation_type TEXT,
    location_code TEXT,
    observation_time TIMESTAMP,
    observation_value DOUBLE PRECISION,

    CONSTRAINT fk_request
        FOREIGN KEY (request_id)
        REFERENCES request(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_observation 
        UNIQUE (source_id, observation_type)

);

-- =========================
-- Optional helpful indexes
-- =========================
CREATE INDEX IF NOT EXISTS idx_observation_request_id
ON observation(request_id);

CREATE INDEX IF NOT EXISTS idx_observation_time
ON observation(observation_time);

CREATE INDEX IF NOT EXISTS idx_observation_location
ON observation(location_code);