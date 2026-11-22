-- Mỗi người một key
CREATE TABLE IF NOT EXISTS keys (
  code        TEXT PRIMARY KEY,           -- NK-XXXX-XXXX-XXXX
  name        TEXT NOT NULL,              -- tên người được cấp
  note        TEXT NOT NULL DEFAULT '',
  max_devices INTEGER NOT NULL DEFAULT 1, -- số máy được dùng cùng lúc
  expires_at  INTEGER,                    -- hết hạn (ms), NULL = vĩnh viễn
  revoked     INTEGER NOT NULL DEFAULT 0, -- 1 = đã khoá
  created_at  INTEGER NOT NULL
);
-- Các máy đã kích hoạt bằng key
CREATE TABLE IF NOT EXISTS devices (
  code      TEXT NOT NULL,
  device    TEXT NOT NULL,
  label     TEXT NOT NULL DEFAULT '',
  first_at  INTEGER NOT NULL,
  last_at   INTEGER NOT NULL,
  PRIMARY KEY (code, device)
);
-- Đếm số lần nhập sai theo IP (chống dò key)
CREATE TABLE IF NOT EXISTS fails (
  ip      TEXT PRIMARY KEY,
  n       INTEGER NOT NULL,
  since   INTEGER NOT NULL
);
