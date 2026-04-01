"""
BePelican — Generador de Data para Web App
Ejecutar: python3 update_data.py
Genera el archivo data.json que la Web App usa para mostrar datos
"""

import requests
import json
import os
from datetime import datetime

# Get token from environment variable (GitHub Actions) or fallback to hardcoded value
# For production on GitHub: set META_TOKEN in GitHub Secrets
# For local testing: replace the string below with your token
TOKEN = os.getenv("META_TOKEN", "EAFZAnIUQUoCMBREAl5ZBnJo7PhBHHzNYQZCdCtx0LuGEcDI7I1y13u6x20CQ8AJWQe2EXZAy5VBOUfFqvcgtQsjYxmQR9ABhfQNcUZCujr6ZBvPst0sRByBMsYd0UWVycZBF769D8EKCzArHuwTJqXqohScA6Vzj3mZAZCQDZBqiQtsYhTwKW9RpayJC54LA07UPlJggZDZD")

ACCOUNTS = {
    "act_31667825": "BePelican | Chepe",
    "act_558128806445249": "Be Pelican"
}

def get_campaigns(account_id):
    url = f"https://graph.facebook.com/v19.0/{account_id}/campaigns"
    params = {
        "fields": "name,status,objective,daily_budget,insights.date_preset(last_30d){spend,impressions,clicks,ctr,cpc,reach,frequency,actions}",
        "access_token": TOKEN
    }
    r = requests.get(url, params=params)
    data = r.json()
    if "error" in data:
        print(f"  ❌ Error: {data['error']['message']}")
        return []
    return data.get("data", [])

def get_action(actions, keyword):
    for a in actions:
        if keyword in a.get("action_type", ""):
            return int(a.get("value", 0))
    return 0

def fetch_all_data():
    campaigns = []
    totals = {"spend": 0, "reach": 0, "msgs": 0, "impressions": 0, "clicks": 0, "ctr_avg": 0}

    for account_id, account_name in ACCOUNTS.items():
        for c in get_campaigns(account_id):
            ins_list = c.get("insights", {}).get("data", [])
            ins = ins_list[0] if ins_list else {}
            actions = ins.get("actions", [])

            spend       = float(ins.get("spend", 0))
            impressions = int(ins.get("impressions", 0))
            clicks      = int(ins.get("clicks", 0))
            ctr         = float(ins.get("ctr", 0))
            cpc         = float(ins.get("cpc", 0))
            reach       = int(ins.get("reach", 0))
            frequency   = float(ins.get("frequency", 0))
            msgs        = get_action(actions, "messaging_connection")
            engagements = get_action(actions, "post_engagement")
            link_clicks = get_action(actions, "link_click")

            # Contabilizar activas
            if c["status"] == "ACTIVE":
                totals["spend"]       += spend
                totals["reach"]       += reach
                totals["msgs"]        += msgs
                totals["impressions"] += impressions
                totals["clicks"]      += clicks

            campaigns.append({
                "account": account_name,
                "name": c["name"],
                "status": c["status"],
                "objective": c.get("objective", ""),
                "daily_budget": int(c.get("daily_budget", 0)),
                "spend": spend,
                "impressions": impressions,
                "clicks": clicks,
                "ctr": ctr,
                "cpc": cpc,
                "reach": reach,
                "frequency": frequency,
                "msgs": msgs,
                "engagements": engagements,
                "link_clicks": link_clicks,
            })

    # Calcular CTR promedio
    if totals["impressions"] > 0:
        totals["ctr_avg"] = (totals["clicks"] / totals["impressions"]) * 100

    return {
        "timestamp": datetime.now().isoformat(),
        "campaigns": campaigns,
        "totals": totals
    }

if __name__ == "__main__":
    print("🦤 BePelican — Actualizando datos...")
    try:
        data = fetch_all_data()

        # Guardar en la carpeta del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, "data.json")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Datos actualizados → {output_file}")
        print(f"   Campañas: {len(data['campaigns'])}")
        print(f"   Gasto: ${int(data['totals']['spend']):,} COP")
        print(f"   Alcance: {data['totals']['reach']:,} personas")

    except Exception as e:
        print(f"❌ Error: {e}")
