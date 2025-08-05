# I. Introduction

The program called “FamBot” is a conversational chatbot that utilizes a simple natural
language processor designed to extract family relationship facts from plain English sentences and
store them in a PROLOG knowledge base. At its core, the script uses regular expressions to
identify predefined patterns in sentences like "John and Mary are siblings" or "Peter is the father
of Anne."
It is a system for acquiring and managing family relationship knowledge from natural
language input. It aims to achieve this by first interpreting user-provided sentences about family
ties, then translating these into a structured, machine-readable format compatible with a Prolog
knowledge base. A key aspect of its intelligence lies in its ability to not only store new facts but
also to perform crucial checks: it prevents the addition of redundant information by identifying
duplicate facts, and more importantly, it attempts to validate the logical consistency of new
relationships against its existing knowledge, providing immediate feedback to the user on
whether the fact was learned, already known, or deemed logically impossible. By maintaining a
dynamic "family pool" of recognized individuals, the system can enhance its validation
capabilities and lay the groundwork for more complex reasoning about familial structures.

# II. Knowledge Base

In this section, the prolog inferences that were encoded in the knowledge base are
individually enumerated and described using the knowledge base.

**1. Sibling rule**
is_sibling_of(X, Y) ↔
sibling(X, Y) ∨ sibling(Y, X) ∨
∃P (parent(P, X) ∧ parent(P, Y)) ∨
∃P (mother(P, X) ∧ mother(P, Y)) ∨
∃P (father(P, X) ∧ father(P, Y)) ∨
∃P (parent(P, Y) ∧ child(X, P)) ∨
∃M (mother(M, Y) ∧ daughter(X, M)) ∨
∃F (father(F, Y) ∧ son(X, F)) ∨
∃P ((child(X, P) ∨ son(X, P) ∨ daughter(X, P)) ∧


(child(Y, P) ∨ son(Y, P) ∨ daughter(Y, P) ∨
parent(P, Y) ∨ mother(P, Y) ∨ father(P, Y))) ∨
∃P ((parent(P, X) ∨ mother(P, X) ∨ father(P, X)) ∧
(child(Y, P) ∨ son(Y, P) ∨ daughter(Y, P) ∨
parent(P, Y) ∨ mother(P, Y) ∨ father(P, Y))) ∨
brother(X, Y) ∨ brother(Y, X) ∨
sister(X, Y) ∨ sister(Y, X)
This rule checks whether X and Y can be inferred to be sibling. This is done by checking
if they have a relationship with a shared parent, and they are either sister, or brother of
one another.

**2. Sibling Title Assignability rule**
is_sibling_title_assignable(S, X) ↔ is_sibling_of(S, X)
This checks if a sibling role can be assigned between S and X. This makes use of the a
defined rule ‘is_sibling_of’ to check if they are actually siblings.
**3. Sister and Brother Title Assignability rule**
is_sister_title_assignable(S, X) ↔
is_sibling_of(S, X) ∧
¬sister(S, X) ∧ ¬brother(S, X) ∧
¬has_male_title(S)
is_brother_title_assignable(S, X) ↔
is_sibling_of(S, X) ∧
¬sister(S, X) ∧ ¬brother(S, X) ∧
¬has_female_title(S)
This check whether a person can be assigned to be a sister or brother of X by checking if
they are siblings, and they don’t have the title yet, and if their gender will match the title
that will be assigned to them
**4. Parent rule**


```
is_parent_of(P, C) ↔
child(C, P) ∨ son(C, P) ∨ daughter(C, P) ∨
∃X ((parent(P, X) ∨ mother(P, X) ∨ father(P, X)) ∧
(sibling(X, C) ∨ sister(X, C) ∨ brother(X, C))) ∨
∃X ((child(X, P) ∨ son(X, P) ∨ daughter(X, P)) ∧
(sibling(X, C) ∨ sister(X, C) ∨ brother(X, C))) ∨
parent(P, C) ∨ father(P, C) ∨ mother(P, C)
This rule examines whether two person parent and child relationship by directly
examining whether the child is an offspring of the parent, and examines whether a person
is a sibling of the child which mean they share the same parents.
```
**5. Parent Title Assignability rule**
is_parent_title_assignable(P, C) ↔ is_parent_of(P, C)
This rules examins whether a parent title can be derived by making use of the
is_parent_of’
**6. Mother and Father Title Assignability**
is_mother_title_assignable(P, C) ↔
is_parent_of(P, C) ∧
¬mother(P, C) ∧
¬has_male_title(P)
is_father_title_assignable(P, C) ↔
is_parent_of(P, C) ∧
¬father(P, C) ∧
¬has_female_title(P)
These rules check if they can be assigned the mother or father role of the child. This is
done by examining if P is the parent of the child, and they haven’t been assigned the mother or
father title, and lastly if they have no conflicting gender.
**7. Grandparent Inference**
is_grandparent_of(G, X) ↔


∃C ((child(C, G) ∨ son(C, G) ∨ daughter(C, G)) ∧
(parent(C, X) ∨ father(C, X) ∨ mother(C, X) ∨
child(X, C) ∨ son(X, C) ∨ daughter(X, C) ∨
aunt(C, X) ∨ uncle(C, X))) ∨
∃C ((parent(G, C) ∨ mother(G, C) ∨ father(G, C))
This rule examines whether G is the grandparent of X by inspecting if the parent of X is a
child of the grandparent G. Furthermore, it checks whether the X has an uncle or aunt that is a
child of grandparent G.

**8. Grandmother and Grandfather Title Assignability**
is_grandmother_title_assignable(G, X) ↔
is_grandparent_of(G, X) ∧
¬grandmother(G, X) ∧
¬has_male_title(G)
is_grandfather_title_assignable(G, X) ↔
is_grandparent_of(G, X) ∧
¬grandfather(G, X) ∧
¬has_female_title(G)
These rules check whether grandparent G can be assigned the grandmother or
grandmother role of X. This is done by examining, if they don’t have conflicting gender, the
grandmother or grandfather title haven’t been assigned to grandparent G yet, and examines if
grandparent G is an actual child grandchild of X by making use use of the ‘is_grandparent_of’
rule
**9. Child Rule**
is_child_of(C, P) ↔
child(C, P) ∨ daughter(C, P) ∨ son(C, P) ∨
∃X ((child(X, P) ∨ son(X, P) ∨ daughter(X, P)) ∧
(sibling(X, C) ∨ sister(X, C) ∨ brother(X, C))) ∨
parent(P, C) ∨ father(P, C) ∨ mother(P, C) ∨
∃X ((parent(P, X) ∨ mother(P, X) ∨ father(P, X)) ∧
(sibling(X, C) ∨ sister(X, C) ∨ brother(X, C)))


```
This examines whether C is the child of P by checking if that child is the has the role son,
daughter, or child of P. Furthermore. It also check whether P is the parent of the child by
examining if P has the titles of parent, father, mother of C. Lastly it also examines
whether the sibling of C is also the parent P, which means that they share the same parent.
```
**10. Child Title Assignability**
is_child_title_assignable(C, P) ↔ is_child_of(C, P)
**11.. Daughter and Son Title Assignability**
is_daughter_title_assignable(C, P) ↔
is_child_of(C, P) ∧
¬daughter(C, P) ∧
¬has_male_title(C)
is_son_title_assignable(C, P) ↔
is_child_of(C, P) ∧
¬son(C, P) ∧
¬has_female_title(C)
These rules check whether the title of son or daughter can be assigned to the child of P.
This examines whether C is an offspring of C and they do not have the corresponding son or
daughter title already, and check whether proper gender is assigned to their corresponding title.
**12. Aunt and Uncle Title Assignability**
is_aunt_title_assignable(A, X) ↔
(sister(A, Y) ∨ is_sibling_of(A, Y)) ∧
(is_child_of(X, Y) ∨ is_parent_of(Y, X)) ∧
¬aunt(A, X) ∧ ¬uncle(A, X) ∧ ¬has_male_title(A)
is_uncle_title_assignable(U, X) ↔
(brother(U, Y) ∨ is_sibling_of(U, Y)) ∧ (is_child_of(X, Y) ∨
is_parent_of(Y, X)) ∧


```
¬uncle(U, X) ∧ ¬aunt(U, X) ∧ ¬has_female_title(U)
These rules examine whether a person is an uncle or an aunt of X. This is done by
checking if their sibling is the child of X, and if examine if they have the proper gender
role assigned to them
```
**13. Gender Inference from Title**
has_male_title(X) ↔
∃Y (brother(X, Y) ∨ father(X, Y) ∨ son(X, Y) ∨ grandfather(X,
Y) ∨ uncle(X, Y))
has_female_title(X) ↔
∃Y (sister(X, Y) ∨ mother(X, Y) ∨ daughter(X, Y) ∨
grandmother(X, Y) ∨ aunt(X, Y))
These rules check whether X is a male or a female by either checking if they have
the role that is assigned to their male or female gender.

# III. Chatbot Implementation

```
The chatbot is implemented as a rule-based AI by utilizing Python for user interaction,
parsing of user prompt, and preprocessing prompt. The Prolog is used for logical inference and is
integrated with Python by using the Pyswip library. The chatbot interprets user prompts from a
set of predefined statement prompts and question prompts which interact with the knowledge
base through a query or an assertion. The chatbot implementation is divided across four Python
files which are chatbot.py, regex.py , prolog.py , and relationships.py in which each of these
python files performs a specific task in preprocessing, and handling the knowledgebase of the
prolog file.
Initially, the program will ask the user to input a prompt. The chatbot will make use of
the regex stored in the regex.py to determine the type of the prompt which is either a statement
or question, and to extract the names from the prompt and the relationship to assign between the
```

people from the prompt. If the prompt is a statement, the chatbot performs some investigation
whether the fact exists in the knowledge base indicating that the query is a just a will store only a
duplicate in the knowledge base. Then if the prompt is not a duplicate in the knowledge base, the
chatbot will validate the logic of the relationship before appending the relationship to the
knowledge base. For example, the logic checks whether a person can be a father of another
person.
In handling question-based prompts, the chatbot creates queries that are obtained from
relationships.py which are able to get yes or no answers, or the descendants or ancestors of a
person. Lastly, the chatbot maintains information about which people are already in the
knowledge base through a variable named ‘family_pool’ which is a set of strings that contains
the names of the people who were stored in the knowledge base. This process ensures that there
are no conflicting entries, and is consistent. Pyswip is mainly responsible for examining the
reasoning of the relationship between people through making use of Prolog queries, while
Python is responsible for parsing the user input, management of the names who are in the
knowledge base, and providing proper output to the user.
**Implementation Components**
● chatbot.py
○ Handles the prompt of the user, and manages the flow of the program.
○ It examines whether the statement is a statement or a question.
○ It is responsible for validating the user input and appending data to the knowledge
base.
● regex.py
○ Makes use of regex patterns to examine whether the prompt is valid
○ Responsible for extracting the names and relationship from the user prompt
● prolog.py
○ Responsible for creating the valid prolog fact given the names and relationship
between the people.
○ Contains helper function to append the fact into the knowledge base.
● relationship.py


```
○ Contains constants that are predefined prolog rules, gender specific roles, and
valid regex filters.
```
# IV. Results

```
The chatbot was tested and evaluated on a set of relationship based test cases
which also involve valid and invalid scenarios. The chatbot showed great performance in
handling direct relationships like siblings, and parent-child, and even grandparent-child
relationships. In addition the chatbot was able to handle more complex relationships like
aunt, and uncle relationships through several logics.
However despite a strong performance in matching the relationship between
people, its weakness lies in the rule-based system that was created. The rules that were
created may still incorrectly identify that the relationship is valid despite it being a
conflicting relationship. Furthermore, the chatbot may not allow for more complex
relationships
```
# V. Limitations and Challenges

```
The chatbot handles the user input, and provides output based on a set of
predefined rules and pattern matching, which make the chatbot require the user to follow
the exact structure of the sentence. This means that with slight variation with
capitalization or incorrect spelling, and phrasing will make the chatbot less friendly for
users compared to LLMs which has more flexibility to understand the user sentence
despite slight variations, and incorrect spelling and grammar.
Furthermore, the ability of the chatbot to get the relationship between two people
is manually predefined. It is a rule-based system that stores information on the knowledge
base according to the logic that was created by the user. LLMs are trained on a very large
amount of data on the internet which means that the AI model can adapt to the increasing
complexity of the relationship. A rule-based system requires constant updating to account
```

```
for growing complexities of the relationship between people, and can be prone to human
error.
```
# VI. Conclusion

```
The processing of implementing the rule based AI chatbot combines both Python and
Prolog for handling user input and providing output to user, and handling the relationship of user
through a predefined set of rules. This is done by dividing the tasks among Python files. The
python preprocessing of user input involve prompt sentence pattern recognition with the use of
regex, and handling of dynamic knowledge base using Pyswip to call Prolog. The system was
also able to handle complex family relationship, and makes use of the family_pool set to account
for existing entities for the prompt, and to ensure that there are no contradictory relationship that
was inserted to the knowledge base.
We have realized the strength of the rule-based AI in providing explained and controlled
behaviour of the chatbot given that rules were strictly defined. However we have also realzied
that the rule-based system has it’s challenges and limitations where it lacks the flexibility to
parse user input given that there are mispelled word, or missing characters. The chatbot’s
performance is heavily dependent on the predefined rules which may fail on some cases while
the complexity of the family tree increases.
```
