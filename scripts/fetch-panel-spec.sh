#!/usr/bin/env bash
# Fetches the OpenAPI spec of a Remnawave panel version into tests/spec/.
# Runs that version on a throwaway database in Docker and reads the spec from
# its backend-tools Swagger, signing the access cookie with the APP_SECRET it
# was started with. Everything is removed afterwards.
#
# usage: scripts/fetch-panel-spec.sh 3.4.8
set -euo pipefail

VERSION=$1
OUT="$(cd "$(dirname "$0")/.." && pwd)/tests/spec/remnawave-$VERSION.json"
PORT=${PORT:-3999}
WORK=$(mktemp -d)
SECRET=$(openssl rand -hex 32)

curl -fsSL "https://raw.githubusercontent.com/remnawave/backend/refs/tags/$VERSION/.env.sample" -o "$WORK/.env"
sed -i.bak \
  -e "s|^APP_SECRET=.*|APP_SECRET=$SECRET|" \
  -e "s|^METRICS_PASS=.*|METRICS_PASS=$(openssl rand -hex 16)|" \
  -e "s|^WEBHOOK_SECRET_HEADER=.*|WEBHOOK_SECRET_HEADER=$(openssl rand -hex 32)|" \
  -e "s|^FRONT_END_DOMAIN=.*|FRONT_END_DOMAIN=localhost|" \
  -e "s|^SUB_PUBLIC_DOMAIN=.*|SUB_PUBLIC_DOMAIN=localhost/api/sub|" \
  -e "s|^PANEL_DOMAIN=.*|PANEL_DOMAIN=localhost|" \
  "$WORK/.env"

cat > "$WORK/compose.yml" <<YAML
name: remnapy-spec
services:
  db:
    image: postgres:18.4
    environment: {POSTGRES_USER: postgres, POSTGRES_PASSWORD: postgres, POSTGRES_DB: postgres}
    healthcheck: {test: ['CMD-SHELL', 'pg_isready -U postgres'], interval: 2s, retries: 30}
  valkey:
    image: valkey/valkey:9-alpine
    command: valkey-server --save "" --appendonly no --unixsocket /var/run/valkey/valkey.sock --unixsocketperm 777
    volumes: [sock:/var/run/valkey]
  remnawave:
    image: remnawave/backend:$VERSION
    env_file: .env
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/postgres
    ports: ['127.0.0.1:$PORT:3000']
    volumes: [sock:/var/run/valkey]
    depends_on: {db: {condition: service_healthy}, valkey: {condition: service_started}}
volumes:
  sock: {}
YAML

cleanup() {
  docker compose -f "$WORK/compose.yml" down -v >/dev/null 2>&1 || true
  docker image rm "remnawave/backend:$VERSION" >/dev/null 2>&1 || true
  rm -rf "$WORK"
}
trap cleanup EXIT

docker compose -f "$WORK/compose.yml" up -d --quiet-pull >/dev/null 2>&1

TOKEN=$(python3 - "$SECRET" <<'PY'
import base64, hashlib, hmac, json, sys, time

def part(data):
    return base64.urlsafe_b64encode(json.dumps(data, separators=(",", ":")).encode()).rstrip(b"=")

head = part({"alg": "HS256", "typ": "JWT"})
body = part({"scope": "access", "iss": "Remnawave", "exp": int(time.time()) + 3600})
sign = base64.urlsafe_b64encode(
    hmac.new(sys.argv[1].encode(), head + b"." + body, hashlib.sha256).digest()
).rstrip(b"=")
print((head + b"." + body + b"." + sign).decode())
PY
)

for _ in $(seq 1 90); do
  if curl -fs -o "$WORK/spec.json" \
      -H "Cookie: rw-tools=$TOKEN" \
      -H "x-forwarded-proto: https" -H "x-forwarded-for: 127.0.0.1" \
      "http://127.0.0.1:$PORT/api/backend-tools/swagger-json"; then
    python3 -c 'import json, sys; json.dump(json.load(open(sys.argv[1])), open(sys.argv[2], "w"), indent=2, ensure_ascii=False)' \
      "$WORK/spec.json" "$OUT"
    echo "saved $OUT"
    exit 0
  fi
  sleep 2
done

echo "panel $VERSION did not serve its spec" >&2
docker compose -f "$WORK/compose.yml" logs --tail 30 remnawave >&2
exit 1
