CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE sensordatatable (
    data_id uuid DEFAULT uuid_generate_v4 (),
    sensorresult JSONB NOT NULL
);