import streamlit as st
import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
import os
from typing import List
from PIL import Image

# Project imports
from core.container import Container, create_finance_agent
from core.settings import settings
from finance.models.enums import TransactionCategory
from finance.ledger import Ledger
from finance.services.advisor import AdvisorService

# Load environment
load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="Wealth OS | Quant Terminal",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Quant Terminal Aesthetic) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
    
    :root {
        --terminal-bg: #0f172a;
        --accent-emerald: #10b981;
        --accent-blue: #3b82f6;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #020617;
        color: var(--text-main);
    }
    
    .stApp {
        background-color: #020617;
    }

    /* Metric Cards - Quant Style */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.5);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem !important;
        color: var(--accent-emerald) !important;
    }

    /* Sidebar - Deep Console */
    div[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }

    /* Custom Quant Cards */
    .quant-card {
        background: #0f172a;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1e293b;
        margin-bottom: 16px;
    }
    
    .status-badge {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    /* Professional Data Table */
    .stDataFrame {
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Terminal Ready. Wealth OS initialized. **Private Wealth Strategist** online. How shall we allocate capital today?"}
    ]

if "currency_symbol" not in st.session_state:
    st.session_state.currency_symbol = "$"

if "deps" not in st.session_state:
    try:
        st.session_state.deps = Container.get_finance_dependencies()
    except Exception as e:
        st.error(f"Critical System Error: {e}")
        st.session_state.deps = None

def get_ledger_data():
    if not st.session_state.deps:
        return None
    try:
        expenses = st.session_state.deps.expense_repo.list_all()
        income = st.session_state.deps.income_repo.list_all()
        return Ledger(transactions=expenses + income)
    except:
        return None

# --- BRANDING & SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 30px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #10b981; font-family: \"JetBrains Mono\", monospace; letter-spacing: -1px; margin-bottom: 0;'>WEALTH OS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.7rem; color: #94a3b8; letter-spacing: 2px; text-transform: uppercase;'>Terminal Interface v2.5</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    nav = st.radio(
        "MODULE SELECT", 
        ["📊 QUANT TERMINAL", "🗨️ ADVISOR CONSOLE", "🛡️ SYSTEM SECURITY", "🧪 DATA LAB"], 
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    if st.button("🔴 RESET SESSION", width='stretch'):
        st.session_state.messages = []
        st.rerun()

    with st.expander("👤 ARCHITECT PROFILE"):
        st.caption("**Lead Architect:** Gaurav Gurjar")
        st.caption("**Uplink:** ggurjar333@gmail.com")
        st.caption("**Status:** Institutional Agent")

# --- GLOBAL HEADER UTILITY ---
def render_terminal_header(title, subtitle):
    head_col1, head_col2 = st.columns([4, 1])
    with head_col1:
        st.title(title)
        st.markdown(subtitle)
    with head_col2:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.session_state.currency_symbol = st.selectbox(
            "CURRENCY", 
            ["$", "₹", "€", "£", "¥", "₩", "₿"], 
            index=["$", "₹", "€", "£", "¥", "₩", "₿"].index(st.session_state.currency_symbol),
            label_visibility="collapsed"
        )
    st.divider()

# --- QUANT TERMINAL VIEW ---
if nav == "📊 QUANT TERMINAL":
    render_terminal_header("📊 Wealth Analytics Terminal", "High-fidelity financial reporting and capital flow diagnostics.")
    
    ledger = get_ledger_data()
    
    if ledger:
        # TOP PERFORMANCE KPI ROW
        currency = st.session_state.currency_symbol
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("NET LIQUIDITY", f"{currency}{ledger.net_cashflow:,.2f}", f"+{currency}{ledger.net_cashflow:,.2f}")
        col2.metric("MONTHLY BURN", f"{currency}{ledger.average_burn_rate:,.2f}", f"Avg Outflow")
        
        runway = ledger.financial_runway
        runway_str = f"{runway:.1f} Mo" if runway != float('inf') else "∞"
        col3.metric("FINANCIAL RUNWAY", runway_str, "Safety Buffer")
        
        savings_rate = (ledger.net_cashflow / (ledger.inflow or 1)) * 100
        col4.metric("SAVINGS RATIO", f"{savings_rate:.1f}%", f"{'Stable' if savings_rate > 20 else 'Critical'}")

        st.divider()

        # QUANT VISUALIZATIONS
        tab_flow, tab_stats = st.tabs(["📉 CAPITAL FLOW", "📈 STATISTICAL AUDIT"])
        
        with tab_flow:
            st.subheader("Historical Capital Area Chart")
            df = pd.DataFrame([{
                "Date": t.date,
                "Amount": t.amount,
                "Type": t.type.value.title()
            } for t in ledger.transactions])
            
            if not df.empty:
                df_sorted = df.sort_values("Date")
                fig_flow = px.area(df_sorted, x="Date", y="Amount", color="Type",
                                  color_discrete_map={"Income": "#10b981", "Expense": "#ef4444"},
                                  template="plotly_dark")
                fig_flow.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_family="JetBrains Mono",
                )
                st.plotly_chart(fig_flow, width='stretch')
            else:
                st.info("No transaction telemetry available.")

        with tab_stats:
            col_s1, col_s2 = st.columns(2)
            
            with col_s1:
                st.subheader("Consumption Breakdown")
                expenses = [t for t in ledger.transactions if t.type.value == 'expense']
                if expenses:
                    df_exp = pd.DataFrame([{
                        "Category": e.category.value if e.category else "Misc",
                        "Amount": e.amount
                    } for e in expenses])
                    fig_pie = px.sunburst(df_exp, path=['Category'], values='Amount',
                                        color_discrete_sequence=px.colors.qualitative.Prism,
                                        template="plotly_dark")
                    st.plotly_chart(fig_pie, width='stretch')

            with col_s2:
                st.subheader("Advisor Audit")
                advisor = AdvisorService()
                report = advisor.analyze_spending(expenses)
                for rec in report.recommendations:
                    st.markdown(f"""
                        <div class="quant-card">
                            <span class="status-badge">Recommendation</span><br/><br/>
                            {rec}
                        </div>
                    """, unsafe_allow_html=True)

        # LEDGER TRANSACTION LOG
        st.subheader("Institutional Transaction Log")
        df_log = pd.DataFrame([{
            "TS": t.date.strftime("%Y-%m-%d %H:%M"),
            "ENTRY": t.description,
            "CLASSIFICATION": t.category.value.upper() if t.category else "N/A",
            "VALUATION": f"{st.session_state.currency_symbol}{t.amount:,.2f}",
            "STATUS": "SETTLED"
        } for t in sorted(ledger.transactions, key=lambda x: x.date, reverse=True)])
        st.dataframe(df_log, width='stretch', hide_index=True)

    else:
        st.warning("Database Uplink Null. Deploy configuration in 'System Security'.")

# --- ADVISOR CONSOLE VIEW ---
elif nav == "🗨️ ADVISOR CONSOLE":
    render_terminal_header("🗨️ Private Wealth Strategist", "Direct neural link to specialized wealth management agents.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f"<div style='font-family: \"JetBrains Mono\", monospace;'>{message['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Input transaction or query strategist..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"`>>> {prompt}`")

        with st.chat_message("assistant"):
            model = settings.get_model()
            placeholder = st.empty()
            placeholder.markdown("🔍 *AUDITING LEDGER...*")
            
            async def exec_strat():
                agent = create_finance_agent()
                res = await agent.run(prompt, model=model, deps=st.session_state.deps)
                return res.output

            try:
                out = asyncio.run(exec_strat())
                placeholder.markdown(out)
                st.session_state.messages.append({"role": "assistant", "content": out})
            except Exception as e:
                st.error(f"STRATEGY ERROR: {e}")

# --- SYSTEM SECURITY VIEW ---
elif nav == "🛡️ SYSTEM SECURITY":
    render_terminal_header("🛡️ Institutional Security Protocol", "Cryptographic key management and database connection routing.")
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Data Storage (Supabase)")
            sb_url = st.text_input("VAULT URL", value=os.getenv("SUPABASE_URL", ""))
            sb_key = st.text_input("VAULT ROLE KEY", value=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""), type="password")
        
        with c2:
            st.subheader("Inference Engine")
            prov = st.selectbox("LLM PROVIDER", ["ollama", "openai", "gemini"], 
                               index=["ollama", "openai", "gemini"].index(settings.MODEL_PROVIDER))
            oll_url = st.text_input("UPLINK ADDR", value=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"))

        if st.button("🔒 AUTHORIZE & SYNC SYSTEMS", type="primary", width='stretch'):
            os.environ["SUPABASE_URL"] = sb_url
            os.environ["SUPABASE_SERVICE_ROLE_KEY"] = sb_key
            os.environ["OLLAMA_BASE_URL"] = oll_url
            
            Container.reset_dependencies()
            try:
                st.session_state.deps = Container.get_finance_dependencies()
                st.success("AUTHENTICATION SUCCESSFUL. TELEMETRY INITIALIZED.")
                st.balloons()
            except Exception as e:
                st.error(f"AUTH FAULT: {e}")


# --- DATA LAB VIEW ---
elif nav == "🧪 DATA LAB":
    render_terminal_header("🧪 Wealth OS Data Laboratory", "Sandbox environment for ledger experimentation and stress testing.")
    
    st.info("The Data Lab allows you to perform destructive operations or populate synthetic telemetry for system validation.")
    
    dm_col1, dm_col2 = st.columns(2)
    
    with dm_col1:
        st.markdown("""
            <div style='background: rgba(239, 68, 68, 0.1); padding: 25px; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.2);'>
                <h3 style='color: #ef4444; margin-top: 0;'>⚠️ PURGE ALL VAULTS</h3>
                <p style='font-size: 0.9rem; color: #94a3b8;'>Wipe all transaction telemetry from the connected Supabase instance. This <strong>cannot</strong> be undone.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("☣️ INITIALIZE TOTAL WIPE", width='stretch', type="secondary"):
            if "wipe_confirm" not in st.session_state:
                st.session_state.wipe_confirm = True
                st.warning("CONFIRMATION REQUIRED: Press the button again to verify total data destruction.")
            else:
                try:
                    with st.spinner("EXECUTING DATA PURGE..."):
                        if st.session_state.deps:
                            st.session_state.deps.expense_repo.clear()
                            st.session_state.deps.income_repo.clear()
                        else:
                            st.error("Uplink missing. Cannot execute wipe.")
                    st.success("VAULTS EMPTIED. SYSTEM RESET TO ZERO STATE.")
                    del st.session_state.wipe_confirm
                    st.rerun()
                except Exception as e:
                    st.error(f"WIPE FAILED: {e}")

    with dm_col2:
        st.markdown("""
            <div style='background: rgba(16, 185, 129, 0.1); padding: 25px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.2);'>
                <h3 style='color: #10b981; margin-top: 0;'>🌱 SYNTHETIC SEEDING</h3>
                <p style='font-size: 0.9rem; color: #94a3b8;'>Generate 90 days of high-fidelity financial telemetry (Salary, Rent, Lifestyle) for demonstration.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧪 GENERATE SYNTHETIC TELEMETRY", width='stretch'):
            from finance.utils.seeder import DataSeeder
            try:
                with st.spinner("SYNTHESIZING FLOWS..."):
                    if st.session_state.deps:
                        DataSeeder.seed_dummy_data(st.session_state.deps)
                        st.success("SYNTHETIC DATA LOADED. RE-AUDITING...")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Uplink missing. Cannot seed data.")
            except Exception as e:
                st.error(f"SEEDING FAILED: {e}")

st.markdown("---")
st.caption("© 2025 Wealth OS Terminal | Email: ggurjar333@gmail.com")
