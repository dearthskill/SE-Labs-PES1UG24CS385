"""Sightings log for a wildlife sanctuary, stored in an SQLite database."""
import hashlib
import sqlite3


def create_schema(conn):
    """Create the sightings table on the given connection."""
    conn.execute(
        "CREATE TABLE sightings ("
        "id INTEGER PRIMARY KEY, species TEXT, zone TEXT, count INTEGER)"
    )


def log_sighting(conn, species, zone, count, extras=None):
    """Record a sighting and add its count to the per-species totals."""
    if extras is None:
        extras = {}
    conn.execute(
        "INSERT INTO sightings (species, zone, count) VALUES (?, ?, ?)",
        (species, zone, count),
    )
    extras[species] = extras.get(species, 0) + count
    return extras


def observer_id(observer):
    """Return a short anonymised ID for an observer's name."""
    return hashlib.sha256(observer.encode()).hexdigest()[:6]


def zone_summary(conn, zone):
    """Return the total number of animals seen in a zone (0 if none)."""
    row = conn.execute(
        "SELECT SUM(count) FROM sightings WHERE zone = ?", (zone,)
    ).fetchone()
    return row[0] if row[0] is not None else 0


def rarest(conn):
    """Return the species with the lowest total count, or None if empty."""
    rows = conn.execute(
        "SELECT species, SUM(count) FROM sightings GROUP BY species"
    ).fetchall()
    if not rows:
        return None
    rarest_row = min(rows, key=lambda r: r[1])
    return rarest_row[0]


def main():
    """Run a short demonstration of the sightings log."""
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    totals = log_sighting(conn, "Leopard", "North", 1)
    log_sighting(conn, "Chital", "North", 24, totals)
    log_sighting(conn, "Hornbill", "East", 3, totals)
    if len(totals) != 3:
        raise RuntimeError("expected totals for 3 species")
    print(observer_id("Arun"), zone_summary(conn, "North"), rarest(conn))
    conn.close()


if __name__ == "__main__":
    main()
