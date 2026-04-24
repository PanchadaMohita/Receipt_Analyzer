import streamlit as st
import json, os
import pandas as pd
import matplotlib.pyplot as plt

from ocr import extract_text
from llm_parser import parse
from categorize import categorize

os.makedirs("input", exist_ok=True)

st.set_page_config(page_title="Receipt Analyzer", page_icon="🧾")
st.title(" Receipt Analyzer")

file = st.file_uploader("Upload receipt", type=["jpg", "jpeg", "png"])

if file:
    path = "input/receipt.jpg"

    with open(path, "wb") as f:
        f.write(file.getvalue())

    col1, col2 = st.columns([1, 2])
    col1.image(file, width=300)

    with col2:
        with st.spinner("Processing..."):

            # OCR
            text = extract_text(path)
            st.text_area(" OCR Output", text, height=200)
            st.text(text)

            # LLM Parsing
            result = parse(text)
            st.write(" Parsed Result:", result)

            if "items" in result:
                result["items"] = categorize(result["items"])

    # ERROR HANDLING
    if "error" in result:
        st.error(f" {result['error']}")

    else:
        items = result.get("items", [])

        
        # Spending Summary
        
        st.subheader(" Spending Summary")

        totals = {}

        for item in items:
            name = item.get("name", "").lower()
            price_str = str(item.get("price", "0")).replace(",", "").strip()

            try:
                price = float(price_str)
            except:
                price = 0.0

            #  FIX unrealistic OCR values
            if price > 5000:
                if not any(word in name for word in ["phone", "iphone", "tv", "laptop"]):
                    if price >= 1000:
                        price = price / 100   # 7000 → 70
                    elif price >= 100:
                        price = price / 10

            cat = item.get("category", "Others") or "Others"
            totals[cat] = totals.get(cat, 0) + price

        if totals:
            num_cols = min(len(totals), 3)
            cols = st.columns(num_cols)

            for i, (cat, amt) in enumerate(sorted(totals.items(), key=lambda x: -x[1])):
                cols[i % num_cols].metric(cat, f"₹{amt:,.2f}")
        else:
            st.warning(" No categories found")

        
        # Total
    
        st.divider()

        total_value = result.get("total", "")

        try:
            total_value = float(str(total_value).replace(",", "").strip())
        except:
            total_value = sum(totals.values())

        st.metric("🧾 Total", f"₹{total_value:,.2f}")

        
        # Items Table
        
        st.subheader("🛒 Items")
        st.table(items if items else [])

        
        # Pie Chart
        
        st.subheader(" Expense Distribution")

        if totals:
            df = pd.DataFrame(list(totals.items()), columns=["category", "amount"])

            fig, ax = plt.subplots()
            df.set_index("category")["amount"].plot.pie(autopct='%1.1f%%', ax=ax)
            ax.set_ylabel("")

            st.pyplot(fig)
        else:
            st.warning(" No data for chart")

        
        #  Download JSON
        # 
        st.subheader(" Download Data")

        json_data = json.dumps(result, indent=4)

        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="receipt_data.json",
            mime="application/json"
        )
