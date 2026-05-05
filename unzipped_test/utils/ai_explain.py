import os

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def ai_explain(profile, anomalies, trust_score, api_key=None):
    """Generate AI-powered data quality explanation using OpenAI GPT.

    Sends a structured prompt with dataset metrics to GPT-4.1-mini
    and returns a business-friendly analysis.

    Args:
        profile: The data profile dictionary from profiler.profile_data().
        anomalies: The anomaly counts dictionary from anomaly.detect_anomalies().
        trust_score: The overall trust score (0-100).
        api_key: Optional OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        str: AI-generated explanation, or a fallback message if unavailable.
    """
    if not OPENAI_AVAILABLE:
        return "⚠️ OpenAI package not installed. Run: pip install openai"

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        return "⚠️ No OpenAI API key provided. Set OPENAI_API_KEY or enter it in the sidebar."

    client = OpenAI(api_key=key)

    prompt = f"""
    Analyze this dataset quality:

    Trust Score: {trust_score}
    Missing Values: {profile['missing']}
    Duplicates: {profile['duplicates']}
    Anomalies: {anomalies}

    Explain:
    - Is this dataset reliable?
    - What are the biggest risks?
    - What should the user do next?

    Keep it short, business-friendly.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI analysis failed: {str(e)}"
