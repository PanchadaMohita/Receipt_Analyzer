KEYWORDS = {
    "Food":          ["coffee", "tea", "rice", "bread", "juice", "milk", "snack", "zomato", "swiggy"],
    "Groceries":     ["shampoo", "soap", "oil", "sugar", "salt", "atta", "ghee", "butter"],
    "Electronics":   ["iphone", "samsung", "laptop", "phone", "mobile", "tablet", "tv"],
    "Health":        ["medical", "pharmacy", "medicine", "tablet", "clinic", "vitamin"],
    "Transport":     ["uber", "ola", "petrol", "diesel", "bus", "metro", "cab"],
    "Shopping":      ["amazon", "flipkart", "myntra", "shirt", "jeans", "shoe"],
    "Personal Care": ["himalaya", "dove", "face wash", "lotion", "cream", "deodorant"],
}

def _get_category(name):
    n = name.lower()
    return next((cat for cat, kws in KEYWORDS.items() if any(k in n for k in kws)), "Others")

def categorize(items):
    for item in items:
        item["category"] = _get_category(item.get("name", ""))
    return items

