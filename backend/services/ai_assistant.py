import os
from datetime import datetime, timedelta
from anthropic import Anthropic
from sqlalchemy.orm import Session
from backend.models import DonationItem, OutboundRecord

def generate_weekly_summary(db: Session) -> dict:
    """Generate AI-powered weekly summary using Claude."""
    
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        # Fallback if no API key
        return {
            "summary": "This week, our Women's Center supported the community through donations and distributions. For detailed analytics, please check the reports section.",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "ai_powered": False,
            "model": None
        }
    
    # Calculate date range (last 7 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    # Query intake and outbound for last 7 days
    intakes = db.query(DonationItem).filter(
        DonationItem.intake_time >= start_date
    ).all()
    
    outbounds = db.query(OutboundRecord).filter(
        OutboundRecord.outbound_time >= start_date
    ).all()
    
    # Aggregate by category
    category_stats = {}
    categories = ["hygiene", "clothing", "food", "household", "other"]
    
    for cat in categories:
        intake_total = sum(i.quantity for i in intakes if i.category == cat)
        outbound_total = sum(o.quantity for o in outbounds if o.category == cat)
        net = intake_total - outbound_total
        
        category_stats[cat] = {
            "intake": intake_total,
            "outbound": outbound_total,
            "net": net
        }
    
    # Build prompt for Claude
    stats_text = "\n".join([
        f"- {cat.title()}: {stats['intake']} items received, {stats['outbound']} distributed (net: {stats['net']:+d})"
        for cat, stats in category_stats.items()
    ])
    
    prompt = f"""You are writing a warm, inspiring 2-3 paragraph summary for donors and volunteers at a Women's Center donation program.

Here are this week's donation statistics:

{stats_text}

Write a heartfelt summary that:
1. Thanks donors and volunteers
2. Highlights the impact (mention specific numbers)
3. Notes any categories running low (negative net)
4. Ends on an uplifting note about community support

Keep it warm, genuine, and under 200 words. Don't use corporate jargon."""
    
    try:
        # Call Claude API
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        summary_text = message.content[0].text
        
        return {
            "summary": summary_text,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "ai_powered": True,
            "model": "claude-3-5-sonnet-20241022"
        }
        
    except Exception as e:
        # Fallback on error
        return {
            "summary": f"This week, our Women's Center received donations and supported community members. Error generating detailed summary: {str(e)}",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "ai_powered": False,
            "model": None,
            "error": str(e)
        }
