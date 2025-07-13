import streamlit as st
import calendar
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from db import init_db

def resource_management():
    st.title("🖥 Resource Management - Desktop Sharing (Service Tags)")

    conn = init_db()

    
    devices = conn.execute("SELECT service_tag, employee_id FROM devices WHERE is_shared = 'Yes' LIMIT 5").fetchall()
    if len(devices) < 5:
        st.warning("⚠ Need at least 5 shared devices marked with 'is_shared = Yes'")
        return

    owners = [owner for _, owner in devices]

    
    all_users = conn.execute("SELECT DISTINCT employee_id FROM devices").fetchall()
    all_users = [u[0] for u in all_users]
    sharers = [u for u in all_users if u not in owners][:5]

    if len(sharers) < 5:
        st.warning("⚠ Not enough eligible sharing users found.")
        return

    
    year, month = 2025, 7
    days_in_july = pd.date_range(f"{year}-07-01", f"{year}-07-31")
    np.random.seed(42)

    share_plan = {}  
    for i in range(5):
        service_tag, owner = devices[i]
        sharer = sharers[i]
        days = sorted(np.random.choice(days_in_july, size=18, replace=False))
        share_plan[service_tag] = {
            "owner": owner,
            "sharer": sharer,
            "days": days
        }

    
    fig, ax = plt.subplots(figsize=(14, 7))
    cal = calendar.Calendar()
    weeks = cal.monthdayscalendar(year, month)
    colors = ['red', 'green', 'blue', 'orange', 'black']
    tag_colors = dict(zip(list(share_plan.keys()), colors))

    for week_idx, week in enumerate(weeks):
        for day_idx, day in enumerate(week):
            if day == 0:
                continue

            rect = plt.Rectangle((day_idx, -week_idx), 1, 1, edgecolor='gray', facecolor='white')
            ax.add_patch(rect)
            ax.text(day_idx + 0.5, -week_idx + 0.8, str(day), ha='center', va='center', fontsize=10, weight='bold')

            y_offset = -week_idx + 0.1
            for tag, info in share_plan.items():
                if pd.Timestamp(f"{year}-{month:02d}-{day:02d}") in info["days"]:
                    ax.plot([day_idx + 0.2, day_idx + 0.8], [y_offset]*2, color=tag_colors[tag], lw=4)
                    y_offset += 0.2

    ax.set_xlim(0, 7)
    ax.set_ylim(-len(weeks), 1)
    ax.axis('off')
    plt.title("📅 July 2025 - Desktop Sharing Calendar", fontsize=14, weight='bold')

    
    legend_items = [
        mpatches.Patch(color=tag_colors[tag],
                       label=f"Service Tag: {tag} (Owner: {share_plan[tag]['owner']}, Shared with: {share_plan[tag]['sharer']})")
        for tag in share_plan
    ]
    ax.legend(handles=legend_items, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=1, fontsize=9)
    st.pyplot(fig)

    
    st.subheader("📋 Sharing Summary")
    for tag, info in share_plan.items():
        st.markdown(f"🔁 *Service Tag {tag}* (owned by {info['owner']}) is shared with *{info['sharer']}* for 18 days.")
