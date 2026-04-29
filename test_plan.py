from rag_engine import generate_rag_plan

print("🧘 Asking the Ayurvedic Master for a plan...")
try:
    # Test with sample data
    plan = generate_rag_plan(age=25, weight=70, goal="Loss", dosha="Kapha")
    
    print("\n✅ SUCCESS! Here is a piece of your plan:")
    print(f"Core Focus: {plan['ayurvedicInsight']['coreFocus']}")
    print(f"Breakfast: {plan['dailyPlan']['breakfast']['name']}")
except Exception as e:
    print(f"❌ FAILED: {e}")