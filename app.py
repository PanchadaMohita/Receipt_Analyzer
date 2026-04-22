import streamlit as st, json, os
from ocr import extract_text
from llm_parser import parse
from categorize import categorize

os.makedirs("input", exist_ok=True)

st.set_page_config(page_title="Receipt Analyzer", page_icon="🧾")
st.title("🧾 Receipt Analyzer")

file = st.file_uploader("Upload receipt", type=["jpg", "jpeg", "png"])

if file:
    path = "input/receipt.jpg"
    with open(path, "wb") as f:
        f.write(file.getvalue())

    col1, col2 = st.columns([1, 2])
    col1.image(file, width=300)

    with col2:
        with st.spinner("Processing..."):
            result = parse(extract_text(path))
            if "items" in result:
                result["items"] = categorize(result["items"])

        if "error" in result:
            st.error(f"⚠️ {result['error']}")
        else:
            st.subheader("📊 Spending Summary")
            totals = {}
            for item in result.get("items", []):
                cat = item.get("category", "Others")
                try:
                    totals[cat] = totals.get(cat, 0) + float(str(item.get("price", 0)).replace(",", ""))
                except ValueError:
                    pass

            cols = st.columns(min(len(totals), 3))
            for i, (cat, amt) in enumerate(sorted(totals.items(), key=lambda x: -x[1])):
                cols[i % 3].metric(cat, f"₹{amt:,.2f}")

            st.divider()
            st.metric("🧾 Total", f"₹{float(str(result.get('total','0')).replace(',','')):,.2f}")
            st.subheader("🛒 Items")
            st.table(result.get("items", []))

            st.subheader("📊 Expense Distribution")
            
        import pandas as pd
        import matplotlib.pyplot as plt
        plt.switch_backend('Agg')


        items = result.get("items", [])

        if items:
          df = pd.DataFrame(items)

    
          df["price"] = df["price"].apply(lambda x: float(str(x).replace(",", "")) if str(x).replace(",", "").replace(".", "").isdigit() else 0)

          category_sum = df.groupby("category")["price"].sum()

          fig, ax = plt.subplots()
          category_sum.plot.pie(autopct='%1.1f%%', ax=ax)
          ax.set_ylabel("")  

          st.pyplot(fig)

        st.subheader("⬇️ Download Data")

        import json

        json_data = json.dumps(result, indent=4)

        st.download_button(
          label="Download JSON",
          data=json_data,
          file_name="receipt_data.json",
          mime="application/json"
)

