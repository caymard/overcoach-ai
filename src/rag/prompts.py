"""Prompt templates for RAG queries."""

TEAM_COMPOSITION_PROMPT = """You are an expert Overwatch coach. Based on the provided context, suggest an optimal team composition.

**CONTEXT:**
- Map: {map_name}
- Enemy Team: {enemy_team}
- Current Team: {current_team}
- Difficulties: {difficulties}

**KNOWLEDGE BASE:**
Heroes Information:
{heroes_context}

Map Information:
{maps_context}

**INSTRUCTIONS:**
Provide a detailed, structured response with:

1. RECOMMENDED TEAM (5 heroes):
   Format each as: "Hero Name (Role): Brief reasoning"
   - 1-2 Tank(s)
   - 2-3 Damage
   - 1-2 Support(s)

2. COUNTER STRATEGY:
   Explain how this team counters the enemy composition

3. TEAM SYNERGIES:
   Describe 2-3 key ability combinations or playstyles

4. ALTERNATIVES:
   Suggest 2-3 substitute heroes if primary picks are taken

Be specific, actionable, and focus on current Overwatch meta.
"""


HERO_COUNTER_PROMPT = """Based on the Overwatch heroes database, identify effective counters to {hero_name}.

Provide:
1. **Hard Counters** (3 heroes): Heroes with strong advantages and why
2. **Soft Counters** (2 heroes): Heroes with moderate advantages
3. **Key Strategies**: Specific tactics to counter this hero

Be concise and focus on practical in-game advice.
"""


MAP_STRATEGY_PROMPT = """Provide strategic information for: {map_name}

Include:
1. **Map Type**: (Control/Escort/Hybrid/Push)
2. **Key Positions**: Critical high grounds, choke points, cover
3. **Recommended Heroes**: Best hero types for this map
4. **Strategy Tips**: Attack and defense approaches

{additional_context}

Keep response focused and actionable.
"""
