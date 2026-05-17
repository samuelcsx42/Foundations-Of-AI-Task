% ============================================================
%  PROLOG FAMILY TREE — family_tree.pl
%  Task Three (b) & (c)
%
%  HOW TO RUN:
%    1. Install SWI-Prolog: https://www.swi-prolog.org/download/stable
%    2. Open terminal and run: swipl family_tree.pl
%    3. Query at the ?- prompt (examples at the bottom of this file)
% ============================================================


% ============================================================
%  SECTION 1 — FACTS: parent/2
%  parent(Parent, Child).
%
%  Family structure:
%
%  Generation 1 (Grandparents):
%    George + Mary  |  Robert + Helen
%
%  Generation 2 (Parents / Uncles / Aunts):
%    Tom (son of George & Mary)
%    Susan (daughter of George & Mary)
%    David (son of Robert & Helen)
%
%  Generation 3 (Children / Grandchildren / Cousins):
%    Alice, Bob  (children of Tom)
%    Carol       (child of Susan)
%    Dan         (child of David)
% ============================================================

% --- Grandparents → Parents ---
parent(george, tom).
parent(george, susan).
parent(mary,   tom).
parent(mary,   susan).

parent(robert, david).
parent(helen,  david).

% --- Parents → Children ---
parent(tom,   alice).
parent(tom,   bob).
parent(susan, carol).
parent(david, dan).


% ============================================================
%  SECTION 2 — GENDER FACTS
%  male/1 and female/1 used to derive gender-specific relations
% ============================================================

male(george).
male(robert).
male(tom).
male(david).
male(bob).
male(dan).

female(mary).
female(helen).
female(susan).
female(alice).
female(carol).


% ============================================================
%  SECTION 3 — DERIVED RULES
% ============================================================

% --- father/2: father(F, C) — F is the father of C ---
father(F, C) :-
    parent(F, C),
    male(F).

% --- mother/2: mother(M, C) — M is the mother of C ---
mother(M, C) :-
    parent(M, C),
    female(M).

% --- grandparent/2: grandparent(GP, GC) ---
grandparent(GP, GC) :-
    parent(GP, P),
    parent(P, GC).

% --- grandfather/2 ---
grandfather(GF, GC) :-
    grandparent(GF, GC),
    male(GF).

% --- grandmother/2 ---
grandmother(GM, GC) :-
    grandparent(GM, GC),
    female(GM).

% --- sibling/2: share at least one common parent ---
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% --- brother/2 ---
brother(B, X) :-
    sibling(B, X),
    male(B).

% --- sister/2 ---
sister(S, X) :-
    sibling(S, X),
    female(S).

% --- uncle/2: uncle(U, X) — U is uncle of X ---
uncle(U, X) :-
    parent(P, X),
    brother(U, P).

% --- aunt/2: aunt(A, X) — A is aunt of X ---
aunt(A, X) :-
    parent(P, X),
    sister(A, P).

% --- cousin/2: share a grandparent but not a parent ---
cousin(X, Y) :-
    grandparent(GP, X),
    grandparent(GP, Y),
    \+ parent(P, X), \+ parent(P, Y),   % different parents
    X \= Y.

% Cleaner cousin rule using sibling parents
cousin(X, Y) :-
    parent(PX, X),
    parent(PY, Y),
    sibling(PX, PY),
    X \= Y.

% --- ancestor/2: recursive — ancestor(A, D) ---
ancestor(A, D) :-
    parent(A, D).
ancestor(A, D) :-
    parent(A, M),
    ancestor(M, D).

% --- descendant/2 ---
descendant(D, A) :-
    ancestor(A, D).


% ============================================================
%  SECTION 4 — SAMPLE QUERIES
%  Copy-paste any of these at the ?- prompt after loading
% ============================================================

%  Who are Tom's children?
%    ?- parent(tom, X).
%
%  Who are Alice's grandparents?
%    ?- grandparent(X, alice).
%
%  Is George Alice's grandfather?
%    ?- grandfather(george, alice).
%
%  Who are Tom's siblings?
%    ?- sibling(X, tom).
%
%  Who is Susan's brother?
%    ?- brother(X, susan).
%
%  Who are Alice's uncles?
%    ?- uncle(X, alice).
%
%  Who are Alice's aunts?
%    ?- aunt(X, alice).
%
%  Who are Alice and Dan's cousins?
%    ?- cousin(alice, dan).
%
%  List ALL cousins pairs:
%    ?- cousin(X, Y).
%
%  Who are all descendants of George?
%    ?- descendant(X, george).
%
%  Is Bob an ancestor of George? (should fail)
%    ?- ancestor(bob, george).
