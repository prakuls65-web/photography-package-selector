
import streamlit as st
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Frame & Focus Studio", page_icon="📷", layout="wide")

# Original pricing structure
SERVICE_RATES = {"Wedding": 25000, "Portrait": 5000, "Event": 12000, "Fashion": 15000}
PACKAGE_MULTIPLIERS = {"Essential": 1, "Signature": 1.5, "Luxury": 2}
ADDONS = {"Extra editing": 2000, "Printed album": 3500, "Extra photographer": 5000}
PHOTOS = ["editorial_street.png", "hands_detail.png", "heritage_story.png",
          "intimate_wedding.png", "red_door_couple.png", "studio_mark.png",
          "wedding_ceremony.png"]

# Studio styling
st.markdown("""
<style>
.stApp{background:#111;color:#f5f0e8}
h1,h2,h3{color:#e8c99b}
div.stButton>button{background:#b99468;color:#111;border-radius:8px}
[data-testid="stMetric"]{background:#242424;padding:14px;border-radius:10px}
</style>
""", unsafe_allow_html=True)

if Path("studio_mark.png").exists():
    st.image("studio_mark.png", width=110)

st.title("FRAME & FOCUS STUDIO")
st.caption("Photography that preserves the feeling, not just the moment.")
st.divider()

# Portfolio gallery uses images already in the repository
st.subheader("Selected Stories")
cols = st.columns(3)
for col, photo in zip(cols, PHOTOS[:3]):
    if Path(photo).exists():
        col.image(photo, use_container_width=True)

st.divider()
st.subheader("Build Your Photography Package")
left, right = st.columns(2)

with left:
    customer = st.text_input("Your name")
    service = st.selectbox("Photography service", list(SERVICE_RATES))
    package = st.selectbox("Package", list(PACKAGE_MULTIPLIERS))
    hours = st.slider("Coverage hours", 1, 12, 4)

with right:
    shoot_date = st.date_input("Preferred date", min_value=date.today())
    budget = st.number_input("Your budget (₹)", min_value=0, value=30000, step=1000)
    addons = st.multiselect("Optional extras", list(ADDONS))

# Calculate the price using the selected service, package and hours
base_rate = SERVICE_RATES[service]
package_rate = base_rate * PACKAGE_MULTIPLIERS[package]
coverage_cost = package_rate * hours / 4
addon_cost = sum(ADDONS[item] for item in addons)
subtotal = coverage_cost + addon_cost

# Automatically calculate discount based on selected package
if package == "Luxury":
    discount_percent = 10
elif package == "Signature":
    discount_percent = 5
else:
    discount_percent = 0

discount_rate = discount_percent / 100
discount = subtotal * discount_rate
total = max(0, subtotal - discount)
# Recommend changes when the selected package exceeds the customer's budget
if budget <= 0:
    budget_suggestion = "Enter a budget above ₹0 to receive a recommendation."
elif budget < SERVICE_RATES[service]:
    budget_suggestion = "Your budget is below the base rate for this service. Try another service."
elif budget >= total:
    budget_suggestion = "Your current configuration fits within your stated budget."
elif budget >= base_rate * PACKAGE_MULTIPLIERS["Essential"]:
    budget_suggestion = "Try the Essential collection, reduce coverage hours, or remove optional add-ons."
else:
    budget_suggestion = "Consider adjusting the service type or discussing a custom brief."

# Display an itemised estimate
st.divider()
st.subheader("Your Estimate")
a, b, c = st.columns(3)
a.metric("Subtotal", f"₹{subtotal:,.0f}")
b.metric(f"Discount ({discount_percent}%)", f"−₹{discount:,.0f}")
c.metric("Estimated total", f"₹{total:,.0f}")

with st.container(border=True):
    st.markdown("### Price breakdown")
    st.write(f"Photography service: **{service}**")
    st.write(f"Package: **{package} ({PACKAGE_MULTIPLIERS[package]}×)**")
    st.write(f"Coverage: **{hours} hours**")
    st.write(f"Photography and coverage: ₹{coverage_cost:,.0f}")
    st.write(f"Optional extras: ₹{addon_cost:,.0f}")
    st.write(f"Discount: −₹{discount:,.0f}")
    st.markdown(f"### Final estimate: ₹{total:,.0f}")

st.info(budget_suggestion)

# Validate the customer's details before generating a quotation
if st.button("Generate quotation", use_container_width=True):
    if not customer.strip():
        st.error("Please enter your name.")
    elif shoot_date < date.today():
        st.error("Please select a valid date.")
    else:
        quote = f"""FRAME & FOCUS STUDIO
PHOTOGRAPHY QUOTATION

Client: {customer}
Service: {service}
Package: {package}
Coverage: {hours} hours
Preferred date: {shoot_date}
Extras: {', '.join(addons) if addons else 'None'}

Photography and coverage: ₹{coverage_cost:,.2f}
Optional extras: ₹{addon_cost:,.2f}
Subtotal: ₹{subtotal:,.2f}
Discount ({discount_percent}%): ₹{discount:,.2f}
FINAL ESTIMATE: ₹{total:,.2f}

Budget recommendation: {budget_suggestion}
Subject to final confirmation.
"""
        st.success("Your quotation is ready.")
        st.download_button("Download quotation", quote,
                           file_name="photography_quotation.txt", mime="text/plain")

# Display the remaining existing portfolio photographs
st.divider()
st.subheader("More Moments")
gallery = st.columns(4)
for col, photo in zip(gallery, PHOTOS[3:]):
    if Path(photo).exists():
        col.image(photo, use_container_width=True)

st.caption("© Frame & Focus Studio | Every frame tells a story.")
