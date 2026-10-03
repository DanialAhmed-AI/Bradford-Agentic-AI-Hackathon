import re

PRODUCTS = [
    {
        "name": "Acer Aspire 5 (A515-58)",
        "price": 549,
        "cpu": "Intel Core i5-1235U",
        "ram": "8GB",
        "storage": "512GB SSD",
        "display": "15.6-inch Full HD",
        "battery": "Up to 10 hours",
        "pros": "Great value and solid coding performance",
        "cons": "8GB RAM can feel tight for heavy multitasking",
    },
    {
        "name": "Lenovo IdeaPad Slim 3",
        "price": 599,
        "cpu": "AMD Ryzen 5 7520U",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "14-inch Full HD",
        "battery": "Up to 12 hours",
        "pros": "Lightweight, comfortable keyboard, and 16GB RAM",
        "cons": "Basic build quality and average speakers",
    },
    {
        "name": "ASUS Vivobook 15",
        "price": 649,
        "cpu": "Intel Core i5-13420H",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "15.6-inch Full HD",
        "battery": "Up to 11 hours",
        "pros": "Strong CPU and excellent value for software work",
        "cons": "Slightly heavier than ultrabooks",
    },
    {
        "name": "HP 15",
        "price": 699,
        "cpu": "AMD Ryzen 5",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "15.6-inch Full HD",
        "battery": "Up to 9 hours",
        "pros": "Solid everyday performance and student-friendly price",
        "cons": "Display brightness is only average",
    },
    {
        "name": "Dell Inspiron 15 3530",
        "price": 749,
        "cpu": "Intel Core i7-1355U",
        "ram": "16GB",
        "storage": "1TB SSD",
        "display": "15.6-inch FHD",
        "battery": "Up to 10 hours",
        "pros": "Large storage, strong productivity performance",
        "cons": "Heavier and less premium design",
    },
    {
        "name": "Microsoft Surface Laptop Go 3",
        "price": 799,
        "cpu": "Intel Core i5",
        "ram": "8GB",
        "storage": "256GB SSD",
        "display": "12.4-inch PixelSense",
        "battery": "Up to 15 hours",
        "pros": "Excellent battery life and premium build",
        "cons": "Low storage and a smaller screen",
    },
    {
        "name": "Lenovo Yoga 7i",
        "price": 849,
        "cpu": "Intel Core i5-1335U",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "14-inch 2.8K",
        "battery": "Up to 12 hours",
        "pros": "Premium display, versatile design, and strong multitasking",
        "cons": "More expensive than traditional budget laptops",
    },
    {
        "name": "HP Pavilion 14",
        "price": 899,
        "cpu": "Intel Core i7",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "14-inch FHD",
        "battery": "Up to 11 hours",
        "pros": "Strong all-round performance and quality keyboard",
        "cons": "Not the lightest or cheapest choice",
    },
    {
        "name": "Acer Swift Go 14",
        "price": 899,
        "cpu": "Intel Core i7-1260P",
        "ram": "16GB",
        "storage": "1TB SSD",
        "display": "14-inch 2.8K",
        "battery": "Up to 12 hours",
        "pros": "Excellent screen, portability, and fast performance",
        "cons": "Higher price and limited port selection",
    },
    {
        "name": "Dell XPS 13",
        "price": 999,
        "cpu": "Intel Core i7",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "13.4-inch FHD+",
        "battery": "Up to 12 hours",
        "pros": "Premium design and excellent portability",
        "cons": "Expensive and smaller keyboard trackpad area",
    },
    {
        "name": "ASUS Zenbook 14",
        "price": 1049,
        "cpu": "AMD Ryzen 7 7840U",
        "ram": "16GB",
        "storage": "1TB SSD",
        "display": "14-inch OLED",
        "battery": "Up to 13 hours",
        "pros": "Excellent balance of power, battery life, and portability",
        "cons": "Premium price point",
    },
    {
        "name": "MacBook Air 13-inch",
        "price": 1099,
        "cpu": "Apple M3",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "13.6-inch Retina",
        "battery": "Up to 18 hours",
        "pros": "Excellent battery, silent operation, premium build",
        "cons": "Higher cost and less Windows-focused software compatibility",
    },
]


def search_products(query: str):
    """Demo product search tool using a local knowledge base."""
    budget_match = re.search(r"£\s?(\d+)", query)
    if budget_match:
        budget = int(budget_match.group(1))
    else:
        budget_match = re.search(r"under\s?(\d+)|(?:up\s+to|<=|less\s+than)\s?(\d+)", query, flags=re.I)
        budget = int((budget_match.group(1) or budget_match.group(2))) if budget_match else 800

    max_budget = max(500, budget)
    return [p for p in PRODUCTS if p["price"] <= max_budget]


def analyse_products(products):
    """Score and rank the product list by value, RAM, CPU and storage."""

    def score(p):
        ram_score = 2 if "16GB" in p["ram"] else 1 if "8GB" in p["ram"] else 0
        cpu_score = 3 if any(token in p["cpu"].lower() for token in ["i7", "ryzen 7", "m3"]) else 2 if any(token in p["cpu"].lower() for token in ["i5", "ryzen 5"]) else 1
        storage_score = 2 if "1TB" in p["storage"] else 1 if "512GB" in p["storage"] else 0
        value_score = max(0, 1000 - p["price"]) / 100
        return ram_score + cpu_score + storage_score + value_score

    return sorted(products, key=score, reverse=True)
