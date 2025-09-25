#!/bin/bash
# ========= CONFIG ==========
BASE_URL="https://wublessing.pythonanywhere.com/api/"
USERNAME="blessing1"
PASSWORD="cynthia95"
# ===========================

echo "🔑 Logging in to get JWT token..."
TOKEN=$(curl -s -X POST $BASE_URL/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" | jq -r '.access')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "❌ Failed to retrieve token. Check your credentials."
  exit 1
fi

echo "✅ Got Access Token!"

# -----------------------
echo -e "\n📋 Listing all polls..."
curl -s -X GET $BASE_URL/api/polls/ -H "Authorization: Bearer $TOKEN" | jq

# -----------------------
echo -e "\n➕ Creating a new poll..."
NEW_POLL=$(curl -s -X POST $BASE_URL/api/polls/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"question":"What is your favorite programming language?","created_by":1}' | jq)

echo "$NEW_POLL"
POLL_ID=$(echo $NEW_POLL | jq -r '.id')

# -----------------------
echo -e "\n📖 Retrieving poll ID $POLL_ID..."
curl -s -X GET $BASE_URL/api/polls/$POLL_ID/ -H "Authorization: Bearer $TOKEN" | jq

# -----------------------
echo -e "\n✏️ Updating poll ID $POLL_ID..."
curl -s -X PUT $BASE_URL/api/polls/$POLL_ID/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"question":"Updated question: Which backend framework do you prefer?","created_by":1}' | jq

# -----------------------
echo -e "\n🗑️ Deleting poll ID $POLL_ID..."
curl -s -X DELETE $BASE_URL/api/polls/$POLL_ID/ -H "Authorization: Bearer $TOKEN"

echo -e "\n✅ Done testing API!"
