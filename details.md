Mini Project: Lexical and Syntactic Analysis of Informal Urban Communication in Yaoundé
Project Context:
Yaoundé is a multilingual city where people communicate in a mixture of English, French, Pidgin, Fulfulde, Ewondo 
expressions, slang (“franc-anglais”), and city-specific abbreviations. Students must collect real conversations from 
taxis, chop et yamo, roadside businesses, neighborhoods, bike riders (bendskins), University environment, etc.
Project Objective
To design and implement a mini-language analyzer capable of performing lexical and syntactic analysis on real 
spoken expressions from Yaoundé, and detect patterns related to commuting, market activities, security issues, 
weather, transport, Electricity and daily transactions.
Project Components 
1. Data Collection (Unique to Each Student)
Divide yourself in groups of 3. Each group must record 10–15 real-life statements heard in Yaoundé on topics such 
as:
i. Taxi and commuting issues
ii. Poor internet connectivity
iii. Limited Electricity supply
iv. Market bargaining
v. Rainy season struggles
vi. Fuel scarcity
vii. Roadside business interactions
viii. Bendskin communication
ix. Security announcements or checkpoints
x. Life at the ICT University
Students MUST manually transcribe these sentences. (That is listen carefully and write the exact words spoken —
including slang, code-mixing, accents, incomplete sentences, or mistakes)
2. Lexical Analysis
1. Identify tokens such as
i. Nouns (e.g., tchop, quartier, moto-guy)
ii. Verbs (drop me, send me urgent 2k, dey for front)
iii. Slang words (hmmm, garrr, zéro-zéro, je wanda, ekiee)
iv. Code-mixed expressions (French + English + Pidgin)
2. Create a custom lexical specification using:
i. Regular expressions for token types
ii. A small LEX/FLEX program or a custom lexical analyzer in any programming language of your choice 
(Java/Python)
3. Analyze token frequency and variation.
3. Syntactic Analysis
1. Construct a context-free grammar (CFG) that describes the structure of the expressions collected.
2. Show steps:
i. Remove left recursion
ii. Do left factoring
iii. Compute FIRST and FOLLOW sets
iv. Build an LL(1) parsing table
v. Or construct LR(0) or SLR(1) items
3. Test their grammar using their own collected sentences.
4. Show which sentences are accepted or rejected.
4. Implementation Requirement
Implement:
i. A simple parser (LL(1) or SLR(1))
ii. That can read their tokenized inputs
iii. And determine whether a sentence fits their constructed grammar
5. Final Deliverables
A. Report (25–30 pages)
Must include:
i. Raw collected statements
ii. Token tables
iii. Regular expressions
iv. Grammar rules
v. Parsing table or LR automaton
vi. Screenshots of working analyzer
vii. Discussion on why Yaoundé communication is linguistically complex
B. Source Code
i. Lexical analyzer
ii. Parser
iii. Test cases taken from your data