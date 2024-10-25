-- Creates an index on the names table.
CREATE INDEX idx_name_first ON names (SUBSTRING(name, 1, 1));
