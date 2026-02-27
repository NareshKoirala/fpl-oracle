The Final Project Architecture: "The FPL Oracle"
1. The Multi-Pipeline Producer (Data Ingestors)

Instead of one big scraper, you have Source-Specific Workers:

    Worker A (FPL API): Fetches the "Official" data (points, prices, ownership percentage).

    Worker B (FotMob/Understat): Fetches the "Advanced" stats (xG, xA, clean sheet odds).

    Worker C (Social/News): Scrapes reliable FPL journalists and injury news.

    Action: All these workers "Push" their raw JSON packets into the Redis Raw-Data Queue.

2. The Specialized Analysts (Probability Workers)

Redis feeds the raw data to your 5 specialized workers. Each one calculates a specific coefficient:

    Worker 1 (The Physio): Calculates an Injury Probability (0.0 - 1.0). It looks at the "yellow flag" status and cross-references it with recent news.

    Worker 2 (The Manager): Calculates a Minutes Probability. It checks if a player just played 90 minutes in the Champions League and might be rotated (benched) in the EPL.

    Worker 3 (The Tactical Analyst): Calculates Match Strength. It uses MATH 120 (Linear Algebra) principles to weigh the player's team form against the opponent's defensive weaknesses.

    Worker 4 (The Form Expert): Uses STAT 151 (Statistics) logic to calculate a "weighted mean" of the player's last 5 games, giving more importance to the most recent match.

3. The Aggregator (The Statistical Machine Learner)

This is the "Brain" that answers the user:

    Logic: It takes all coefficients (Injury % × Minutes % × Match Strength × Form) to create an Expected Points (xP) value for every player.

    The Answer: When a user asks "Should I captain Saka?", this worker compares Saka’s xP against Haaland’s and Salah’s for that specific Gameweek.

Why this is the perfect "Portfolio Piece" for U of A:

    Concurrency (CMPT 340): You are demonstrating that you know how to manage multiple data streams simultaneously using Redis and Docker. 

    Statistical Logic (STAT 151): You aren't just "guessing" if Saka is good; you are using statistical probability to back it up. 

    Scalability: If the project gets popular and 1,000 people ask questions at once, you just spin up more "Aggregator" Docker containers.
