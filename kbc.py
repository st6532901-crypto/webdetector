def kbc():
    print(" Welcome to Kaun Banega Crorepati, Deviyon aur Sajjanon! ")
    name = input("Aap apna name bataiye: ")
    print(f"\nCongratulations {name}, aapka swagat hai KBC mein!")
    print("Isse pehle ki game shuru kare, kuch niyamon se avagat ho jaein:")
    print("1. Aapke paas 3 lifelines hain: 50-50, Phone a Friend, Ask the Audience")
    print("2. Prashno ka sahi uttar dene par hi aap agle round mein ja sakte hain")
    print("3. Aap kisi bhi samay game chhod sakte hain aur apni jeeti hui rakam le ja sakte hain\n")

questions = [
    {
        "question": "Which of these cities is the capital of India?",
        "options": {"A": "Delhi", "B": "Chandigarh", "C": "Mumbai", "D": "Chennai"},
        "correct_answer": "A",
        "prize_money": 1000
    },
    {
        "question": "Who is known as the 'Missile Man of India'?",
        "options": {"A": "Homi J. Bhabha", "B": "Vikram Sarabhai", "C": "A.P.J. Abdul Kalam", "D": "C.V. Raman"},
        "correct_answer": "C",
        "prize_money": 2000
    },
    {
        "question": "The currency of Japan is:",
        "options": {"A": "Yuan", "B": "Won", "C": "Yen", "D": "Ringgit"},
        "correct_answer": "C",
        "prize_money": 5000
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": {"A": "Earth", "B": "Mars", "C": "Jupiter", "D": "Saturn"},
        "correct_answer": "B",
        "prize_money": 10000
    },
    {
        "question": "Which country is called Bhikharistan of the world?",
        "options": {"A": "Pakistan", "B": "Pakxtan", "C": "Pakistan", "D": "Pakistan"},
        "correct_answer": "A",
        "prize_money": "1 kg Atta"
    },
    {
        "question": "What Riya likes most in her life?",
        "options": {"A": "Abhishek", "B": "Abhishek", "C": "Abhishek", "D": "Abhishek"},
        "correct_answer": "A",
        "prize_money": "1 life partner, who loves her unconditionally and makes her all wishes come true"
    }
]

kbc()

total_prize = 0

for i, q in enumerate(questions, start=1):
    print(f"\n Question {i} (Prize: {q['prize_money']})")
    print(q['question'])
    for key, value in q["options"].items():
        print(f"{key}. {value}")
    
    answer = input("Enter your answer (A/B/C/D) or type 'quit' to exit: ")

    if answer.lower() == 'quit':
        print(f"\nYou quit the game! You are leaving with ₹{total_prize}.")
        break
    elif answer.upper() == q["correct_answer"]:
        print("Bohot bohot badhai ho! Ye correct answer hai!")
        # Add the prize if it's numeric
        if isinstance(q["prize_money"], int):
            total_prize += q["prize_money"]
            print(f"Aapne jeete ₹{q['prize_money']}! Ab tak kul rakam: ₹{total_prize}.")
        else:
            print(f"Aapne jeeta: {q['prize_money']}")
        print("Chaliye agle prashn ki taraf badhte hain...")
    else:
        print("Hame afsos hai, lekin ye galat uttar hai! Game over.")
        print(f"Aap ghar le ja rahe hain ₹{total_prize}.")
        break

print("\n Dhanyawaad KBC khelne ke liye!")
