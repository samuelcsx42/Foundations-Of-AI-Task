/*
 * CCS 2226 Foundations of AI - 2026
 * Task Three – Prolog: Family Tree
 * Contains: grandparents, parents, children, grandchildren, cousins, uncles, aunts
 *
 * How to run:
 *   1. Install SWI-Prolog  →  https://www.swi-prolog.org/download/stable
 *   2. Open terminal and run:   swipl family_tree.pl
 *   3. Query examples are listed at the bottom of this file.
 */

% ═══════════════════════════════════════════════════════════
% SECTION 1 – Base Facts (the family tree)
% ═══════════════════════════════════════════════════════════

% parent(Parent, Child)
parent(george,  henry).
parent(george,  diana).
parent(mary,    henry).
parent(mary,    diana).

parent(henry,   alice).
parent(henry,   bob).
parent(susan,   alice).
parent(susan,   bob).

parent(diana,   carol).
parent(diana,   david).
parent(tom,     carol).
parent(tom,     david).

% ─── Bob has a child with Eve ───
parent(bob,     emma).
parent(eve,     emma).

% ─── Carol has a child with Frank ───
parent(carol,   james).
parent(frank,   james).

% gender facts
male(george).
male(henry).
male(tom).
male(bob).
male(david).
male(frank).
male(james).

female(mary).
female(diana).
female(susan).
female(alice).
female(eve).
female(emma).
female(carol).


% ═══════════════════════════════════════════════════════════
% SECTION 2 – Derived Rules
% ═══════════════════════════════════════════════════════════

% ── Father / Mother ──
father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M).

% ── Grandparent ──
grandparent(GP, GC) :-
    parent(GP, P),
    parent(P,  GC).

grandfather(GF, GC) :- grandparent(GF, GC), male(GF).
grandmother(GM, GC) :- grandparent(GM, GC), female(GM).

% ── Grandchild ──
grandchild(GC, GP) :- grandparent(GP, GC).

% ── Sibling (same parent, different person) ──
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% ── Brother / Sister ──
brother(B, X) :- sibling(B, X), male(B).
sister(S, X)  :- sibling(S, X), female(S).

% ── Uncle / Aunt ──
uncle(U, X)  :- brother(U, P), parent(P, X).
uncle(U, X)  :- sibling(U, P), parent(P, X), male(U).   % covers half-siblings

aunt(A, X)   :- sister(A, P),  parent(P, X).
aunt(A, X)   :- sibling(A, P), parent(P, X), female(A).

% ── Cousin ──
cousin(X, Y) :-
    parent(PX, X),
    parent(PY, Y),
    sibling(PX, PY).

% ── Descendant (recursive) ──
descendant(D, A) :- parent(A, D).
descendant(D, A) :- parent(A, X), descendant(D, X).

% ── Ancestor (recursive) ──
ancestor(A, D) :- descendant(D, A).


% ═══════════════════════════════════════════════════════════
% SECTION 3 – Convenience predicates for "list all"
% ═══════════════════════════════════════════════════════════

% List all members of the family
all_members(Ms) :-
    findall(X, (male(X) ; female(X)), All),
    sort(All, Ms).

% Print all grandchildren of a person
show_grandchildren(GP) :-
    findall(GC, grandchild(GC, GP), GCs),
    format("Grandchildren of ~w: ~w~n", [GP, GCs]).

% Print all cousins of a person
show_cousins(X) :-
    findall(C, (cousin(C, X), C \= X), Cs),
    sort(Cs, Sorted),
    format("Cousins of ~w: ~w~n", [X, Sorted]).


% ═══════════════════════════════════════════════════════════
% SECTION 4 – Auto-run demo on load
% ═══════════════════════════════════════════════════════════

:- initialization(demo, main).

demo :-
    nl,
    writeln("╔══════════════════════════════════════════════════╗"),
    writeln("║  CCS 2226 Foundations of AI – Family Tree Demo  ║"),
    writeln("╚══════════════════════════════════════════════════╝"),
    nl,

    writeln("── Grandparents of alice ──"),
    forall(grandparent(GP, alice),
           format("  ~w is a grandparent of alice~n", [GP])),
    nl,

    writeln("── Parents of bob ──"),
    forall(parent(P, bob),
           format("  ~w is a parent of bob~n", [P])),
    nl,

    writeln("── Children of henry ──"),
    forall(parent(henry, C),
           format("  ~w is a child of henry~n", [C])),
    nl,

    show_grandchildren(george),
    nl,

    show_cousins(alice),
    nl,

    writeln("── Uncles of alice ──"),
    forall(uncle(U, alice),
           format("  ~w is an uncle of alice~n", [U])),
    nl,

    writeln("── Aunts of bob ──"),
    forall(aunt(A, bob),
           format("  ~w is an aunt of bob~n", [A])),
    nl,

    writeln("── All descendants of george ──"),
    findall(D, descendant(D, george), Desc),
    sort(Desc, SortedDesc),
    format("  ~w~n", [SortedDesc]),
    nl,

    writeln("── Interactive query mode ──"),
    writeln("  Try:  grandparent(george, X)."),
    writeln("        cousin(alice, X)."),
    writeln("        uncle(U, emma)."),
    writeln("        aunt(A, james)."),
    nl.

/*
 * ═══════════════════════════════════════════════════════════
 * FAMILY TREE DIAGRAM
 * ═══════════════════════════════════════════════════════════
 *
 *  George + Mary               (Grandparents – Generation 1)
 *     |         |
 *   Henry     Diana             (Parents – Generation 2)
 *     +Susan    +Tom
 *    /  \       / \
 *  Alice Bob  Carol David       (Children – Generation 3)
 *         +Eve  +Frank
 *          |     |
 *        Emma  James            (Grandchildren – Generation 4)
 *
 * Relationships:
 *   - Alice & Bob are siblings (cousins to Carol & David)
 *   - Carol & David are siblings (cousins to Alice & Bob)
 *   - Henry is uncle to Carol & David; Diana is aunt to Alice & Bob
 *   - George & Mary are grandparents to Alice, Bob, Carol, David
 *   - George & Mary are great-grandparents to Emma & James
 * ═══════════════════════════════════════════════════════════
 */
