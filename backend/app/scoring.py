def calc(a):
    q=sum(a[k]["score"]*w for k,w in {"problem_clarity":.2,"innovation":.2,"impact":.2,"solution_quality":.15,"user_value":.15,"ethics":.1}.items())
    f=sum(a[k]["score"]*w for k,w in {"technical_feasibility":.25,"mvp_feasibility":.25,"time_feasibility":.2,"team_skill_match":.2}.items())+(100-a["dependency_risk"]["score"])*.1
    p=70 if a.get("pitch",{}).get("one_line_pitch") else 0
    r=q*.4+f*.4+p*.2
    return {"idea_quality_score":round(q,2),"build_feasibility_score":round(f,2),"hackathon_readiness_score":round(r,2)}
