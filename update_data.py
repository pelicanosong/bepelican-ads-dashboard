import requests
import json
import os
from datetime import datetime

TOKEN = os.environ.get("META_ACCESS_TOKEN")
ACCOUNTS = ["act_3166782", "act_5581288064452"]
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Períodos disponibles: (nombre_archivo, date_preset, etiqueta)
PERIODS = [
    ("data_today.json",       "today",              "Hoy"),
    ("data_week.json",        "this_week_mon_today", "Esta semana"),
    ("data_month.json",       "this_month",         "Este mes"),
    ("data_last_month.json",  "last_month",         "Mes anterior"),
    ("data_3months.json",     "last_90d",           "Últimos 3 meses"),
]

# data.json sigue existiendo como alias de "este mes" (retrocompatibilidad)
DEFAULT_PERIOD_FILE = "data_month.json"


def get_account_name(account_id):
    url = f"{BASE_URL}/{account_id}"
    params = {"access_token": TOKEN, "fields": "name"}
    r = requests.get(url, params=params)
    data = r.json()
    if "name" in data:
        return data["name"]
    return account_id


def get_campaigns(account_id, date_preset):
    url = f"{BASE_URL}/{account_id}/campaigns"
    params = {
        "access_token": TOKEN,
        "fields": (
            "name,status,objective,daily_budget,"
            "insights{"
            "spend,impressions,clicks,ctr,cpc,reach,frequency,"
            "actions,engagement_rate_ranking"
            "}"
        ),
        "date_preset": date_preset,
        "limit": 100
    }
    r = requests.get(url, params=params)
    result = r.json()
    if "error" in result:
        print(f"  ⚠️  Error en {account_id}: {result['error'].get('message', result['error'])}")
        return []
    return result.get("data", [])


def extract_msgs(actions):
    if not actions:
        return 0
    for a in actions:
        if a.get("action_type") in [
            "onsite_conversion.messaging_conversation_started_7d",
            "onsite_conversion.messaging_first_reply"
        ]:
            return int(float(a.get("value", 0)))
    return 0


def extract_engagements(actions):
    if not actions:
        return 0
    engagement_types = {
        "post_engagement", "page_engagement",
        "post_reaction", "post", "comment", "like", "video_view"
    }
    total = 0
    for a in actions:
        if a.get("action_type") in engagement_types:
            total += int(float(a.get("value", 0)))
    return total


def fetch_period_data(date_preset, label):
    print(f"\n📅 Obteniendo datos para: {label} ({date_preset})")
    campaigns_out = []
    totals = {
        "spend": 0.0,
        "reach": 0,
        "msgs": 0,
        "impressions": 0,
        "clicks": 0,
        "ctr_vals": [],
        "freq_vals": [],
        "active_freq_sum": 0.0,
        "active_impressions": 0,
        "active_reach": 0,
    }

    for acct in ACCOUNTS:
        acct_name = get_account_name(acct)
        campaigns = get_campaigns(acct, date_preset)
        print(f"  🏷️  {acct_name}: {len(campaigns)} campañas")

        for c in campaigns:
            ins_data = c.get("insights", {})
            ins = ins_data.get("data", [{}])[0] if ins_data else {}

            spend        = float(ins.get("spend", 0))
            reach        = int(ins.get("reach", 0))
            impressions  = int(ins.get("impressions", 0))
            clicks       = int(ins.get("clicks", 0))
            ctr          = float(ins.get("ctr", 0))
            cpc_raw      = ins.get("cpc", None)
            cpc          = float(cpc_raw) if cpc_raw else (spend / clicks if clicks > 0 else 0.0)
            frequency    = float(ins.get("frequency", 0))
            actions      = ins.get("actions", [])
            msgs         = extract_msgs(actions)
            engagements  = extract_engagements(actions)

            # Budget diario (puede ser 0 si usa presupuesto de conjunto de anuncios)
            daily_budget_raw = c.get("daily_budget", "0")
            try:
                daily_budget = int(daily_budget_raw) // 100  # en COP (la API retorna centavos)
            except (ValueError, TypeError):
                daily_budget = 0

            campaign_entry = {
                "id":           c.get("id"),
                "account":      acct_name,
                "name":         c.get("name"),
                "status":       c.get("status", "UNKNOWN"),
                "objective":    c.get("objective", ""),
                "daily_budget": daily_budget,
                "spend":        spend,
                "impressions":  impressions,
                "clicks":       clicks,
                "link_clicks":  clicks,   # aproximación si no hay breakdown
                "ctr":          ctr,
                "cpc":          cpc,
                "reach":        reach,
                "frequency":    frequency,
                "msgs":         msgs,
                "engagements":  engagements,
            }
            campaigns_out.append(campaign_entry)

            # Acumular totales
            totals["spend"]       += spend
            totals["reach"]       += reach
            totals["msgs"]        += msgs
            totals["impressions"] += impressions
            totals["clicks"]      += clicks
            if ctr > 0:
                totals["ctr_vals"].append(ctr)
            if frequency > 0:
                totals["freq_vals"].append(frequency)

            # Para frecuencia ponderada de campañas activas
            if c.get("status") == "ACTIVE" and reach > 0:
                totals["active_freq_sum"]    += frequency * reach
                totals["active_impressions"] += impressions
                totals["active_reach"]       += reach

    # Métricas globales calculadas correctamente
    ti = totals["impressions"]
    tc = totals["clicks"]
    ts = totals["spend"]
    tr = totals["active_reach"]

    ctr_weighted  = (tc / ti * 100) if ti > 0 else 0.0
    cpm_global    = (ts / ti * 1000) if ti > 0 else 0.0
    freq_weighted = (totals["active_freq_sum"] / tr) if tr > 0 else 0.0

    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "period":    {"preset": date_preset, "label": label},
        "campaigns": campaigns_out,
        "totals": {
            "spend":       ts,
            "reach":       totals["reach"],
            "msgs":        totals["msgs"],
            "impressions": ti,
            "clicks":      tc,
            "ctr_avg":     ctr_weighted,   # ✅ CTR ponderado real
            "cpm":         cpm_global,     # ✅ CPM global correcto
            "frequency":   freq_weighted,  # ✅ Frecuencia ponderada
        }
    }

    active_count  = sum(1 for c in campaigns_out if c["status"] == "ACTIVE")
    paused_count  = len(campaigns_out) - active_count
    print(f"  ✅ {active_count} activas, {paused_count} pausadas — Gasto total: ${ts:,.0f} COP")
    return output


# ──────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────
if not TOKEN:
    print("❌ META_ACCESS_TOKEN no está configurado.")
    exit(1)

print("🚀 Iniciando actualización de datos BePelican Meta Ads...")

for filename, preset, label in PERIODS:
    try:
        data = fetch_period_data(preset, label)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  💾 Guardado: {filename}")
    except Exception as e:
        print(f"  ❌ Error en período '{label}': {e}")

# Mantener data.json como alias de "este mes" para retrocompatibilidad
import shutil
try:
    shutil.copy(DEFAULT_PERIOD_FILE, "data.json")
    print(f"\n🔁 data.json actualizado como alias de {DEFAULT_PERIOD_FILE}")
except FileNotFoundError:
    print(f"\n⚠️  No se pudo copiar {DEFAULT_PERIOD_FILE} a data.json")

print("\n✅ Actualización completada.")
