discount = subtotal * discount_rate
total = max(0, subtotal - discount)

# Suggest a collection based on the budget, without silently changing the customer's selection.
if budget <= 0:
    budget_suggestion = "Enter a budget above ₹0 to receive a recommendation."
elif budget < SERVICE_RATES[service]:
    budget_suggestion = "Your budget is below the base rate for this service. Try a shorter session or another service."
elif budget >= total:
    budget_suggestion = "Your current configuration fits within your stated budget."
elif budget >= base_rate * PACKAGE_MULTIPLIERS["Essential"]:
    budget_suggestion = "Try the Essential collection, reduce the coverage hours, or remove optional add-ons."
else:
    budget_suggestion = "Consider adjusting the service type or discussing a custom brief."

with summary:
    st.markdown("<div class='eyebrow'>YOUR ESTIMATE</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="price-card">
          <div style="color:#d9cdbb;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase">Estimated total</div>
          <div class="price-number">{money(total)}</div>
          <div style="color:#e2d9ca;font-size:.9rem">{service}</div>
          <hr style="border-color:#51483b">
          <div style="color:#f3eadc;font-size:.9rem">Collection: <b>{package}</b></div>
          <div style="color:#d9cdbb;font-size:.9rem">Coverage: {hours} hour(s)</div>
          <div style="color:#d9cdbb;font-size:.9rem">Shoot date: {preferred_date.strftime('%d %b %Y')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown("#### Budget check")
    st.info(budget_suggestion)
    if budget > 0:
        difference = budget - total
        if difference >= 0:
            st.success(f"You are approximately {money(difference)} under budget.")
        else:
            st.warning(f"This estimate is approximately {money(abs(difference))} over budget.")
    st.markdown("#### What's included?")
    st.markdown(
        f"""
        - {service}
        - {package} collection
        - {hours} hour(s) of coverage
        - {editing_style} editing
        - {delivery}
        - {"Second photographer" if add_second else "One photographer"}
        """
    )

st.write("")
with st.expander("View detailed price breakdown"):
    price_rows = [
        ("Base photography rate", base_rate),
        (f"Additional hours ({extra_hours})", extra_hour_cost),
        ("Collection upgrade", package_upgrade),
        ("Shoot scale", scale_cost),
        ("Image delivery", delivery_cost),
        ("Travel", travel_cost),
        ("Second photographer", second_cost),
        ("Priority delivery", rush_cost),
        ("Additional retouching", retouch_cost),
        ("Subtotal", subtotal),
        (discount_label, -discount),
        ("Estimated total", total),
    ]
    for label, amount in price_rows:
        st.write(f"**{label}:** {money(amount)}")

# Create a downloadable plain-text quotation using the user's selections.
quote_lines = [
    "FRAME & FOCUS — PHOTOGRAPHY ESTIMATE",
    "=" * 42,
    f"Customer: {customer_name.strip() or 'Not provided'}",
    f"Email: {customer_email.strip() or 'Not provided'}",
    f"Preferred date: {preferred_date.strftime('%d %B %Y')}",
    "",
    f"Service: {service}",
    f"Collection: {package}",
    f"Coverage: {hours} hour(s)",
    f"Shoot scale: {shoot_size}",
    f"Editing: {editing_style}",
    f"Delivery: {delivery}",
    "",
]
quote_lines.extend([f"{label}: {money(amount)}" for label, amount in price_rows])
quote_lines += [
    "",
    "This is an educational-project estimate, not a confirmed booking.",
    "All prices are sample prices and may be changed by the studio.",
]
quote_text = "\n".join(quote_lines)

download_col, note_col = st.columns([1, 2])
with download_col:
    st.download_button(
        "Download your quotation (.txt)",
        data=quote_text,
        file_name="frame_and_focus_quote.txt",
        mime="text/plain",
        use_container_width=True,
    )
with note_col:
    st.caption("The quotation includes the selected package, date, itemised charges, discount, and estimated total.")

st.divider()
st.markdown(
    """
    <div style="text-align:center;padding:1rem 0 0.5rem">
      <div class="eyebrow">FRAME & FOCUS STUDIO</div>
      <p class="small-muted">Sample academic project · Prices are illustrative · No payment or booking is processed</p>
    </div>
    """,
    unsafe_allow_html=True,
)
