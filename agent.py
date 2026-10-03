import re

from ml_model import MLModel
from tools import search_products, analyse_products


class AIAgent:
    """
    Lightweight agent for the hackathon MVP.

    The agent:
    1. Understands the user's request using an ML classifier.
    2. Creates a plan.
    3. Calls tools.
    4. Analyses the returned data.
    5. Generates a structured response.
    """

    def __init__(self):
        self.model = MLModel()

    def process(self, query: str):
        intent_result = self.model.predict(query)
        intent = intent_result["prediction"]
        confidence = intent_result["confidence"]

        steps = [
            {
                "title": "Understand Request",
                "detail": f"Detected intent: {intent} (ML confidence: {confidence:.0%})."
            },
            {
                "title": "Create Plan",
                "detail": "Select the relevant tool, retrieve information, analyse it, then generate a useful answer."
            }
        ]

        tools = []
        if intent == "laptop_recommendation":
            steps.append({
                "title": "Search Product Knowledge Base",
                "detail": "Retrieved laptop candidates matching the user's budget, intended use and feature preferences."
            })
            products = search_products(query)
            tools.append("Product Knowledge Base")

            focus = self._infer_focus(query)
            products = self._rank_for_focus(products, focus)
            analysed = analyse_products(products)
            tools.append("ML/Data Analysis")

            steps.append({
                "title": "Analyse & Compare",
                "detail": f"Compared CPU, RAM, storage, display, battery and price using a {focus} preference profile."
            })

            answer = self._format_laptop_answer(analysed, focus, query)

        else:
            steps.append({
                "title": "Generate Response",
                "detail": "No specialised tool was required, so the agent returned a general response."
            })
            answer = (
                "I can help with laptop recommendations, coding setup choices and AI/ML explanations. "
                "Try: **What is the best laptop for a computer science student under £800?**"
            )

        steps.append({
            "title": "Generate Response",
            "detail": "Compiled the analysed results into a concise response with pros, cons and prices."
        })
        steps.append({
            "title": "Provide Final Answer",
            "detail": "Returned the result to the user."
        })

        return {
            "answer": answer,
            "steps": steps,
            "tools": tools,
            "intent": intent,
            "confidence": confidence,
        }

    def _infer_focus(self, query: str):
        text = query.lower()
        if any(word in text for word in ["battery", "portable", "travel", "lightweight", "long battery"]):
            return "battery"
        if any(word in text for word in ["performance", "gaming", "heavy", "video editing", "developer", "coding", "programming"]):
            return "performance"
        if any(word in text for word in ["student", "budget", "cheap", "value", "affordable"]):
            return "value"
        return "balanced"

    def _rank_for_focus(self, products, focus: str):
        def sort_key(product):
            cpu = product["cpu"].lower()
            ram = product["ram"]
            display = product["display"].lower()
            battery = product["battery"].lower()

            score = 0
            if "16gb" in ram:
                score += 4
            elif "8gb" in ram:
                score += 2
            if "i7" in cpu or "ryzen 7" in cpu or "m3" in cpu:
                score += 4
            elif "i5" in cpu or "ryzen 5" in cpu:
                score += 3
            if "2.8k" in display or "oled" in display:
                score += 2
            if "15 hours" in battery or "18 hours" in battery or "up to 12" in battery:
                score += 3
            if focus == "battery":
                score += 4 if "up to 12" in battery or "up to 15" in battery or "up to 18" in battery else 0
            elif focus == "performance":
                score += 3 if "i7" in cpu or "ryzen 7" in cpu else 0
            elif focus == "value":
                score += 2 if product["price"] < 700 else 0
            return score

        return sorted(products, key=sort_key, reverse=True)

    def _format_laptop_answer(self, products, focus: str, query: str):
        budget_match = re.search(r"£\s?(\d+)|(?:under|budget|up to|less than)\s?(\d+)", query, flags=re.I)
        budget = int((budget_match.group(1) or budget_match.group(2))) if budget_match else 800

        lines = [
            "### 💻 Smart laptop recommendations",
            "",
            f"I matched your request to a {focus}-focused shortlist and prioritised laptops within the £{budget} range.",
            ""
        ]

        for i, p in enumerate(products[:3], 1):
            lines.append(f"**{i}. {p['name']} — £{p['price']}**")
            lines.append(
                f"- {p['cpu']} · {p['ram']} RAM · {p['storage']} · {p['display']}"
            )
            lines.append(f"- Battery: {p['battery']}")
            lines.append(f"- **Best for:** {p['pros']}")
            lines.append(f"- **Trade-off:** {p['cons']}")
            lines.append("")

        if focus == "battery":
            summary = "The shortlist leans toward portability and long runtime, ideal for study days, commuting and light travel."
        elif focus == "performance":
            summary = "The shortlist prioritises CPU power and memory for coding, data work and heavier multitasking."
        elif focus == "value":
            summary = "The shortlist prioritises the best price-to-performance ratio for students and everyday productivity."
        else:
            summary = "The shortlist balanced price, performance and portability for a typical Computer Science user."

        lines.append(f"**Overall:** {summary}")
        return "\n".join(lines)
