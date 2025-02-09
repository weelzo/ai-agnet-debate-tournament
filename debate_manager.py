from debate_agents.proponent import proponent
from debate_agents.opponent import opponent
from debate_agents.moderator import moderator
from debate_agents.judge import judge

def run_debate(topic):
    context = []
    debate_rounds = []
    num_rounds = 10

    print(f"🎤 Debate Topic: {topic}")
    debate_rounds.append({"role": "Topic", "text": topic, "round": 0, "type": "topic"})
    
    # Opening Statements
    proponent_statement = proponent.respond(f"Present your opening argument for: {topic}")
    print(f"🟢 Proponent: {proponent_statement}")
    context.append({"role": "Proponent", "text": proponent_statement})
    debate_rounds.append({"role": "Proponent", "text": proponent_statement, "round": 0, "type": "opening"})

    opponent_statement = opponent.respond(f"Present your opening argument against: {topic}", context)
    print(f"🔴 Opponent: {opponent_statement}")
    context.append({"role": "Opponent", "text": opponent_statement})
    debate_rounds.append({"role": "Opponent", "text": opponent_statement, "round": 0, "type": "opening"})

    # Multiple rounds of debate
    for round_num in range(1, num_rounds + 1):
        print(f"\n📍 Round {round_num}")
        
        # Moderator guides the discussion
        moderator_guidance = moderator.respond(
            f"Round {round_num}: Analyze the current state of the debate and pose a specific question or point that needs to be addressed by both sides.",
            context
        )
        print(f"⚖️ Moderator: {moderator_guidance}")
        context.append({"role": "Moderator", "text": moderator_guidance})
        debate_rounds.append({"role": "Moderator", "text": moderator_guidance, "round": round_num, "type": "guidance"})

        # Proponent's turn
        proponent_response = proponent.respond(
            f"Round {round_num}: Address the moderator's point and strengthen your position: {moderator_guidance}",
            context
        )
        print(f"🟢 Proponent: {proponent_response}")
        context.append({"role": "Proponent", "text": proponent_response})
        debate_rounds.append({"role": "Proponent", "text": proponent_response, "round": round_num, "type": "response"})

        # Opponent's turn
        opponent_response = opponent.respond(
            f"Round {round_num}: Address both the moderator's point and the proponent's latest argument: {proponent_response}",
            context
        )
        print(f"🔴 Opponent: {opponent_response}")
        context.append({"role": "Opponent", "text": opponent_response})
        debate_rounds.append({"role": "Opponent", "text": opponent_response, "round": round_num, "type": "response"})

    # Final Judgment
    print("\n🏁 Final Judgment")
    judge_decision = judge.respond(
        "After reviewing all arguments presented in this extensive debate, provide a comprehensive evaluation and declare a winner with detailed reasoning.",
        context
    )
    print(f"👨‍⚖️ Judge: {judge_decision}")
    debate_rounds.append({"role": "Judge", "text": judge_decision, "round": num_rounds + 1, "type": "decision"})

    return {
        "topic": topic,
        "rounds": debate_rounds
    }