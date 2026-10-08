import streamlit as st
import pandas as pd

st.title("AI Cost-Effectiveness Dashboard")

st.write("AI-Assisted Diagnosis vs Standard Diagnosis")

# -----------------------------
# Scenario Selection
# -----------------------------

st.subheader("Scenario Selection")

col1, col2 = st.columns(2)

with col1:
    prevalence = st.selectbox(
        "Prevalence",
        [20, 50, 80]
    )

with col2:
    ai_accuracy = st.selectbox(
        "AI Accuracy",
        [75, 80, 85, 90, 95, 98]
    )

# -----------------------------
# Fixed Study Parameters
# -----------------------------

number_of_patients = 1000
standard_accuracy = 70

# -----------------------------
# Automatic Calculations
# -----------------------------

standard_correct = round(
    number_of_patients * standard_accuracy / 100
)

ai_correct = round(
    number_of_patients * ai_accuracy / 100
)

incremental_correct = ai_correct - standard_correct

# -----------------------------
# Results
# -----------------------------

st.subheader("Diagnostic Results")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Standard Correct Diagnoses",
    standard_correct
)

col2.metric(
    "AI Correct Diagnoses",
    ai_correct
)

col3.metric(
    "Incremental Correct Diagnoses",
    incremental_correct
)

# -----------------------------
# Study Information
# -----------------------------

st.subheader("Study Information")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Number of Patients",
    number_of_patients
)

col2.metric(
    "Standard Accuracy",
    f"{standard_accuracy}%"
)

col3.metric(
    "AI Accuracy",
    f"{ai_accuracy}%"
)

# -----------------------------
# Current Scenario
# -----------------------------

st.subheader("Current Scenario")

st.write(
    f"Prevalence: *{prevalence}%*"
)

st.write(
    f"AI Accuracy: *{ai_accuracy}%*"
)
# -----------------------------
# Cost Calculations
# -----------------------------

standard_costs = {
    20: 89270,
    50: 134820,
    80: 176310
}

ai_costs = {
    20: {
        75: 79290,
        80: 69600,
        85: 59910,
        90: 50220,
        95: 41980,
        98: 36340
    },
    50: {
        75: 119040,
        80: 104710,
        85: 90960,
        90: 78080,
        95: 64440,
        98: 56370
    },
    80: {
        75: 157920,
        80: 140110,
        85: 122300,
        90: 105360,
        95: 86390,
        98: 74950

    }
}

standard_cost = standard_costs[prevalence]

ai_cost = ai_costs[prevalence].get(ai_accuracy)

if ai_cost is not None:
    cost_difference = ai_cost - standard_cost

    if incremental_correct > 0:
        cost_savings_per_additional = (
            (standard_cost - ai_cost) / incremental_correct
        )
    else:
        cost_savings_per_additional = 0
# -----------------------------
# Cost Results
# -----------------------------

st.subheader("Cost Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Standard Cost",
    f"€{standard_cost:,.0f}"
)

col2.metric(
    "AI Cost",
    f"€{ai_cost:,.0f}"
)

col3.metric(
    "Cost Difference",
    f"€{cost_difference:,.0f}"
)

col4.metric(
    "Cost Savings per Additional Correct Diagnosis",
    f"€{cost_savings_per_additional:,.2f}"
)
# -----------------------------
# Total Cost Chart
# -----------------------------

st.subheader("Impact of AI Diagnostic Accuracy on Total Cost")

cost_data = {
    20: {
        "AI Accuracy": [75, 80, 85, 90, 95, 98],
        "Standard Cost": [89270, 89270, 89270, 89270, 89270, 89270],
        "AI Cost": [79290, 69600, 59910, 50220, 41980, 36340]
    },

    50: {
        "AI Accuracy": [75, 80, 85, 90, 95, 98],
        "Standard Cost": [134820, 134820, 134820, 134820, 134820, 134820],
        "AI Cost": [119040, 104710, 90960, 78080, 64040, 56370]
    },

    80: {
        "AI Accuracy": [75, 80, 85, 90, 95, 98],
        "Standard Cost": [176310, 176310, 176310, 176310, 176310, 176310],
        "AI Cost": [157920, 140110, 122300, 105360, 86390, 74950]
    }
}

chart_data = pd.DataFrame(cost_data[prevalence])

st.line_chart(
    chart_data,
    x="AI Accuracy",
    y=["Standard Cost", "AI Cost"]
)
# -----------------------------
# Incremental Correct Diagnoses Chart
# -----------------------------

st.subheader("AI Accuracy (%) vs Incremental Correct Diagnoses")

incremental_data = pd.DataFrame({
    "AI Accuracy": [75, 80, 85, 90, 95, 98],
    "Incremental Correct Diagnoses": [50, 100, 150, 200, 250, 280]
})

st.vega_lite_chart(
    incremental_data,
    {
        "mark": {
            "type": "line",
            "point": True,
            "interpolate": "basis"
        },
        "encoding": {
            "x": {
                "field": "AI Accuracy",
                "type": "quantitative",
                "scale": {
                    "domain": [75, 98]
                },
                "title": "AI Accuracy (%)"
            },
            "y": {
                "field": "Incremental Correct Diagnoses",
                "type": "quantitative",
                "title": "Incremental Correct Diagnoses"
            }
        }
    },
    use_container_width=True
)
# -----------------------------
# Cost Difference Chart
# -----------------------------

st.subheader(
    f"Cost Difference vs AI Accuracy — Prevalence: {prevalence}%"
)

cost_difference_data = {
    20: {
        "AI Accuracy": [75, 80, 85, 90, 95, 98],
        "Cost Difference": [-9980, -19670, -29360, -39050, -47290, -52930]
    },

    50: {
        "AI Accuracy": [75, 80, 85, 90, 95, 98],
        "Cost Difference": [-15780, -30110, -43860, -56740, -70780, -78450]
    },

    80: {
        "AI Accuracy": [75, 80, 85, 90, 95, 98],
        "Cost Difference": [-18390, -36200, -54010, -70950, -89920, -101360]
    }
}

cost_difference_chart = pd.DataFrame(
    cost_difference_data[prevalence]
)

st.line_chart(
    cost_difference_chart.set_index("AI Accuracy")
)