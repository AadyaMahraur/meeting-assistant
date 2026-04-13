Model: gemini-3-flash-preview

How the prompt works?
The prompt mentions all the required headings(short summary, long summary, action items etc) with descriptions and specifications. It explicitly define rules regarding AI hallucination, ambiguity, and corner cases. It also provides the output format (json object). Finally, it provides the meeting content.




What the output looks like?
Json object
Short Summary: Structure of purpose, key decisions made, outcome is present
Detailed Summary: Lists all talking points from the meeting for short, bulleted sample.
Correctly identified all decisions
Correctly identified all explicit actions, actions as result of blockers
Correctly identified blockers and their types



What problems you noticed?
Key decisions made:
Shorter: mentions areas but not the actual decision made
Long, raw: identifies only explicit instructions as decisions

Got confused by who raised a blocker and who was supposed to work on it
Criteria for priority of action items is not very clear
Misclassifies as "open questions" type of blocker none are available
Tries to find 5-6 points from each topic, instead of identifying all.




What you plan to adjust?
Check if every topic point can fit into either decision, action, or blocker. Check for overlap, define categories. Same with blocker types.
Prompt such that all relevant details are identified. 
