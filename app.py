import streamlit as st

# Configure the browser tab and page layout.
st.set_page_config(page_title="Photography Package Selector", page_icon="📷", layout="centered")

# Keep all prices in Indian rupees (₹); these are sample prices for this student project.
SERVICE_RATES = {
    "Portrait Photography": 3000,
    "Wedding Photography": 12000,
    "Pre-wedding Photography": 8000,
    "Event Photography": 7000,
    "Product Photography": 4500,
}

PACKAGE_MULTIPLIERS = {
    "Basic": 1.00,
    "Standard": 1.35,
    "Premium": 1.75,
}

st.title("Photography Package Selector")
st.write("Build a photography package and get an estimated price before booking.")
st.caption("Sample pricing for demonstration. Final quotes may vary by photographer and location.")

# Collect the customer's choices using Streamlit input widgets.
service = st.selectbox("1. Photography type", list(SERVICE_RATES.keys()))
package = st.selectbox("2. Package level", list(PACKAGE_MULTIPLIERS.keys()))
hours = st.number_input("3. Booking duration (hours)", min_value=1, max_value=12, value=2, step=1)
event_size = st.selectbox("4. Event / shoot size", ["Small", "Medium", "Large"])
travel_km = st.number_input("5. Travel distance (km)", min_value=0, max_value=500, value=0, step=5)
advanced_editing = st.checkbox("Advanced photo editing (+₹1,500)")
printed_album = st.checkbox("Printed photo album (+₹2,000)")
extra_photographer = st.checkbox("Add a second photographer (+₹2,500)")

# Define size-based charges with a clear mapping.
if event_size == "Small":
    size_charge = 0
elif event_size == "Medium":
    size_charge = 1500
else:
    size_charge = 3000

# Calculate extra-hour charges after the first two hours included in the base rate.
included_hours = 2
extra_hours = max(0, int(hours) - included_hours)
hourly_rate = SERVICE_RATES[service] * 0.20
extra_hour_charge = extra_hours * hourly_rate

# Apply the selected package multiplier to the photography service and duration charges.
base_cost = SERVICE_RATES[service] + extra_hour_charge
package_cost = base_cost * (PACKAGE_MULTIPLIERS[package] - 1)

# Travel is free for the first 20 km; additional distance is charged per kilometre.
chargeable_km = max(0, int(travel_km) - 20)
travel_charge = chargeable_km * 15

# Add optional service charges only when the customer selects them.
editing_charge = 1500 if advanced_editing else 0
album_charge = 2000 if printed_album else 0
second_photographer_charge = 2500 if extra_photographer else 0

# Use a button so the customer can request the final estimate after making selections.
if st.button("Calculate package price", type="primary"):
    try:
        # Validate numeric inputs before displaying the estimate.
        if hours < 1 or hours > 12 or travel_km < 0 or travel_km > 500:
            st.error("Please enter values within the allowed ranges.")
        else:
            subtotal = (
                base_cost
                + package_cost
                + size_charge
                + travel_charge
                + editing_charge
                + album_charge
                + second_photographer_charge
            )

            # Apply a 10% discount to Premium packages with bookings of at least 6 hours.
            if package == "Premium" and hours >= 6:
                discount = subtotal * 0.10
                discount_message = "Premium long-booking discount (10%)"
            elif package == "Standard" and hours >= 8:
                discount = subtotal * 0.05
                discount_message = "Standard long-booking discount (5%)"
            else:
                discount = 0
                discount_message = "No long-booking discount"

            # Calculate the final estimated price after discounts.
            total = max(0, subtotal - discount)

            st.subheader("Your estimated package")
            st.write(f"**Photography service:** {service}")
            st.write(f"**Selected package:** {package}")
            st.write(f"**Duration:** {int(hours)} hour(s)")
            st.divider()

            # Present an itemised breakdown so customers can understand the total.
            st.write(f"Base photography rate: ₹{SERVICE_RATES[service]:,.2f}")
            st.write(f"Additional hours: ₹{extra_hour_charge:,.2f}")
            st.write(f"Package upgrade: ₹{package_cost:,.2f}")
            st.write(f"Event / shoot size: ₹{size_charge:,.2f}")
            st.write(f"Travel charge: ₹{travel_charge:,.2f}")
            st.write(f"Advanced editing: ₹{editing_charge:,.2f}")
            st.write(f"Printed album: ₹{album_charge:,.2f}")
            st.write(f"Second photographer: ₹{second_photographer_charge:,.2f}")
            st.write(f"Subtotal: ₹{subtotal:,.2f}")
            st.write(f"{discount_message}: -₹{discount:,.2f}")
            st.success(f"Estimated total: ₹{total:,.2f}")
            st.caption("This is an estimate, not a confirmed booking or final commercial quote.")

    except (TypeError, ValueError, KeyError) as error:
        # Show a helpful message rather than letting unexpected input errors crash the app.
        st.error(f"Unable to calculate the estimate. Check your selections and try again. ({error})")

# Explain the sample pricing rules in the app for transparency.
with st.expander("View pricing rules"):
    st.write("- The base rate includes up to 2 hours of photography.")
    st.write("- Each additional hour costs 20% of the selected service's base rate.")
    st.write("- Basic, Standard, and Premium packages use multipliers of 1.00, 1.35, and 1.75.")
    st.write("- Medium and Large shoots add ₹1,500 and ₹3,000 respectively.")
    st.write("- Travel is free for the first 20 km, then ₹15 per additional kilometre.")
    st.write("- Premium bookings of 6+ hours receive 10% off; Standard bookings of 8+ hours receive 5% off.")
