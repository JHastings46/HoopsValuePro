import streamlit as st
import pandas as pd

st.set_page_config(page_title="2026 NBA Free-Agent Value Board", layout="wide")

with st.sidebar:
    st.markdown("### Built by Joel Hastings")
    st.markdown("[GitHub](https://github.com/JHastings46)")
    st.markdown("[LinkedIn](https://linkedin.com/in/joel-hastings-976bb855)")
    st.markdown("[Tableau Public](https://public.tableau.com/app/profile/joel.hastings)")

@st.cache_data
def load_board():
    return pd.read_csv("2026_free_agent_value_board_full.csv")

df = load_board()

st.title("2026 NBA Free-Agent Value Board")
st.markdown("A two-model system predicting free-agent market cost and future production, built to identify contracts the market may be over- or under-valuing.")
st.caption("Model 1 predicts market cost (AAV % of cap). Model 2 predicts future production (VORP). Cap Efficiency = predicted future VORP per 1% of actual cap spent.")

col1, col2, col3 = st.columns(3)
with col1:
    evaluation_filter = st.multiselect(
        "Contract Evaluation",
        options=df["Contract Evaluation"].unique(),
        default=list(df["Contract Evaluation"].unique())
    )
with col2:
    tier_filter = st.multiselect(
        "Future Production Tier",
        options=df["Future Production Tier"].unique(),
        default=list(df["Future Production Tier"].unique())
    )
with col3:
    sort_by = st.selectbox(
        "Sort by",
        options=["Absolute Difference", "Cap Efficiency Rank", "Future Production Rank"],
        index=0
    )

filtered = df[
    df["Contract Evaluation"].isin(evaluation_filter) &
    df["Future Production Tier"].isin(tier_filter)
].sort_values(sort_by, ascending=(sort_by != "Absolute Difference"))

st.dataframe(filtered, use_container_width=True, hide_index=True)

with st.expander("Model limitations and notes"):
    notes_df = df[df["Notes"] != ""][["Player", "Notes"]]
    if len(notes_df) > 0:
        st.dataframe(notes_df, use_container_width=True, hide_index=True)
    st.caption("Model 1 test R² ≈ 0.43. Model 2 trained on a smaller sample with age range 19–39; predictions outside that range are extrapolations. Read alongside context, not as a sole recommendation.")
