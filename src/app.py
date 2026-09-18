import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -----------------------------
# Load models
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

runs_model = joblib.load(
    MODELS_DIR / "crickopt_final_runs_model.pkl"
)

wicket_model = joblib.load(
    MODELS_DIR / "crickopt_final_wicket_model.pkl"
)

final_features = [
    "innings",
    "over_number",
    "current_score",
    "wickets_lost",
    "runs_last_6",
    "runs_last_12",
    "wickets_last_12",
    "striker_balls",
    "batter_past_avg",
    "bowler_past_runs_per_ball",
    "bowler_past_wicket_rate",
    "matchup_past_runs_per_ball",
    "matchup_past_wicket_rate"
]


# -----------------------------
# Tactical score
# -----------------------------

def calculate_tactical_score(predicted_runs, wicket_probability):

    run_component = 1 - min(predicted_runs / 6, 1)
    wicket_component = wicket_probability

    return (
        0.70 * run_component +
        0.30 * wicket_component
    )


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("🏏 CrickOpt")
st.subheader("AI-Based Cricket Tactical Decision Optimization")

st.write(
    "Enter the current match situation to estimate "
    "next-ball runs and wicket probability."
)

st.divider()

innings = st.number_input(
    "Innings",
    min_value=1,
    max_value=2,
    value=2
)

over_number = st.number_input(
    "Over Number",
    min_value=0,
    max_value=49,
    value=20
)

current_score = st.number_input(
    "Current Score",
    min_value=0,
    value=120
)

wickets_lost = st.number_input(
    "Wickets Lost",
    min_value=0,
    max_value=10,
    value=3
)

runs_last_6 = st.number_input(
    "Runs in Last 6 Balls",
    min_value=0,
    value=5
)

runs_last_12 = st.number_input(
    "Runs in Last 12 Balls",
    min_value=0,
    value=12
)

wickets_last_12 = st.number_input(
    "Wickets in Last 12 Balls",
    min_value=0,
    max_value=10,
    value=0
)

striker_balls = st.number_input(
    "Striker Balls Faced",
    min_value=0,
    value=25
)

batter_past_avg = st.number_input(
    "Batter Past Average Runs/Ball",
    min_value=0.0,
    value=0.80
)

bowler_past_runs_per_ball = st.number_input(
    "Bowler Past Runs/Ball",
    min_value=0.0,
    value=0.75
)

bowler_past_wicket_rate = st.number_input(
    "Bowler Past Wicket Rate",
    min_value=0.0,
    value=0.03
)

matchup_past_runs_per_ball = st.number_input(
    "Batter-Bowler Past Runs/Ball",
    min_value=0.0,
    value=0.70
)

matchup_past_wicket_rate = st.number_input(
    "Batter-Bowler Past Wicket Rate",
    min_value=0.0,
    value=0.03
)


# -----------------------------
# Prediction
# -----------------------------
st.divider()
st.subheader("🎯 Bowler Tactical Comparison")

st.write(
    "Enter the historical performance of up to three candidate bowlers."
)

bowler_names = []

col1, col2, col3 = st.columns(3)

with col1:
    bowler1 = st.text_input("Bowler 1", "Bowler A")
    bowler1_runs = st.number_input(
        "Bowler 1 Runs/Ball",
        min_value=0.0,
        value=0.75,
        key="b1r"
    )
    bowler1_wicket = st.number_input(
        "Bowler 1 Wicket Rate",
        min_value=0.0,
        value=0.03,
        key="b1w"
    )

with col2:
    bowler2 = st.text_input("Bowler 2", "Bowler B")
    bowler2_runs = st.number_input(
        "Bowler 2 Runs/Ball",
        min_value=0.0,
        value=0.85,
        key="b2r"
    )
    bowler2_wicket = st.number_input(
        "Bowler 2 Wicket Rate",
        min_value=0.0,
        value=0.025,
        key="b2w"
    )

with col3:
    bowler3 = st.text_input("Bowler 3", "Bowler C")
    bowler3_runs = st.number_input(
        "Bowler 3 Runs/Ball",
        min_value=0.0,
        value=0.70,
        key="b3r"
    )
    bowler3_wicket = st.number_input(
        "Bowler 3 Wicket Rate",
        min_value=0.0,
        value=0.04,
        key="b3w"
    )
if st.button("🔍 Analyze Match Situation"):

    input_data = pd.DataFrame([{
        "innings": innings,
        "over_number": over_number,
        "current_score": current_score,
        "wickets_lost": wickets_lost,
        "runs_last_6": runs_last_6,
        "runs_last_12": runs_last_12,
        "wickets_last_12": wickets_last_12,
        "striker_balls": striker_balls,
        "batter_past_avg": batter_past_avg,
        "bowler_past_runs_per_ball": bowler_past_runs_per_ball,
        "bowler_past_wicket_rate": bowler_past_wicket_rate,
        "matchup_past_runs_per_ball": matchup_past_runs_per_ball,
        "matchup_past_wicket_rate": matchup_past_wicket_rate
    }])

    predicted_runs = runs_model.predict(
        input_data[final_features]
    )[0]

    wicket_probability = wicket_model.predict_proba(
        input_data[final_features]
    )[0][1]

    tactical_score = calculate_tactical_score(
        predicted_runs,
        wicket_probability
    )

    st.divider()

    st.subheader("🏏 CrickOpt Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Predicted Runs",
        f"{predicted_runs:.2f}"
    )

    col2.metric(
        "Wicket Probability",
        f"{wicket_probability:.2%}"
    )

    col3.metric(
        "Tactical Score",
        f"{tactical_score:.3f}"
    )

    st.success(
        "Analysis generated successfully."
    )
        # -----------------------------
    # Bowler Comparison
    # -----------------------------

    bowler_data = [
        (bowler1, bowler1_runs, bowler1_wicket),
        (bowler2, bowler2_runs, bowler2_wicket),
        (bowler3, bowler3_runs, bowler3_wicket)
    ]

    bowler_results = []

    for name, runs_rate, wicket_rate in bowler_data:

        bowler_input = input_data.copy()

        bowler_input["bowler_past_runs_per_ball"] = runs_rate
        bowler_input["bowler_past_wicket_rate"] = wicket_rate

        # Keep current matchup information
        bowler_input["matchup_past_runs_per_ball"] = runs_rate
        bowler_input["matchup_past_wicket_rate"] = wicket_rate

        predicted = runs_model.predict(
            bowler_input[final_features]
        )[0]

        wicket_prob = wicket_model.predict_proba(
            bowler_input[final_features]
        )[0][1]

        score = calculate_tactical_score(
            predicted,
            wicket_prob
        )

        bowler_results.append({
            "Bowler": name,
            "Predicted Runs": predicted,
            "Wicket Probability": wicket_prob,
            "Tactical Score": score
        })

    comparison_df = pd.DataFrame(bowler_results)

    comparison_df = comparison_df.sort_values(
            "Tactical Score",
            ascending=False
        ).reset_index(drop=True)

    st.divider()

    st.subheader("🏏 Bowler Comparison")
        
    st.dataframe(
        comparison_df,
        width="stretch"
    )

    st.subheader("📊 Tactical Score Comparison")

    chart_data = comparison_df.set_index("Bowler")[
        ["Tactical Score"]
    ]

    st.bar_chart(
        chart_data,
        width="stretch"
    )

    st.subheader("💡 CrickOpt Decision Explanation")

    recommended = comparison_df.iloc[0]

    st.write(
        f"**{recommended['Bowler']}** has the highest tactical score "
        f"among the entered candidates."
    )

    st.write(
        f"Expected next-ball runs: "
        f"**{recommended['Predicted Runs']:.2f}**"
    )

    st.write(
        f"Estimated wicket probability: "
        f"**{recommended['Wicket Probability']:.2%}**"
    )

    st.info(
        "CrickOpt combines predicted scoring risk and wicket probability "
        "to provide a tactical decision-support signal."
    )

    st.success(
        f"🎯 CrickOpt Tactical Option: {recommended['Bowler']}"
    )
    st.info(
            "The tactical score is a prototype decision-support metric "
            "and should not be interpreted as a guaranteed match outcome."
        )