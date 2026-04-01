# py-maskopy

Quickstart:

```bash
docker compose -f config/docker-compose.yml up -d
python3 -m pip install -r config/requirements.txt
python3 scripts/reset_data.py
python3 scripts/mask_data.py
docker compose -f config/docker-compose.yml down
```

Full documentation: `docs/README.md`
