# py-maskopy

Quickstart:

```bash
python3 -m venv .venv
source .venv/bin/activate
docker compose -f config/docker-compose.yml up -d
docker exec -it maskopy-oracle sqlplus maskopy/maskopypwd@//localhost:1521/FREEPDB1
python3 -m pip install -e .
docker compose -f config/docker-compose.yml down
```

Full documentation: `docs/README.md`
