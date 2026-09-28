(* ============================================================ *)
(*  CS357 — Natural Deduction in Coq                             *)
(*  Companion .v file for lecture notes                          *)
(* ============================================================ *)

(* ---------------------------------------------------------- *)
(*  Section 1: Implication (→)                                 *)
(* ---------------------------------------------------------- *)

(* Lemma 6 from lecture: A → (A → B) → (B → C) → C *)
Lemma lemma6 : forall (A B C : Prop),
  A -> (A -> B) -> (B -> C) -> C.
Proof.
  intros A B C HA HAB HBC.
  apply HBC.
  apply HAB.
  exact HA.
Qed.

(* Transitivity of implication *)
Lemma impl_trans : forall (A B C : Prop),
  (A -> B) -> (B -> C) -> A -> C.
Proof.
  intros A B C HAB HBC HA.
  apply HBC.
  apply HAB.
  exact HA.
Qed.

(* Self-implication: A → A (identity) *)
Lemma impl_id : forall (A : Prop),
  A -> A.
Proof.
  intros A HA.
  exact HA.
Qed.

(* Contraposition: (A → B) → (¬B → ¬A) *)
Lemma contraposition : forall (A B : Prop),
  (A -> B) -> (~B -> ~A).
Proof.
  intros A B HAB HNB HA.
  apply HNB.
  apply HAB.
  exact HA.
Qed.

(* ---------------------------------------------------------- *)
(*  Section 2: Conjunction (∧)                                 *)
(* ---------------------------------------------------------- *)

(* Commutativity of AND *)
Lemma and_comm : forall (A B : Prop),
  A /\ B -> B /\ A.
Proof.
  intros A B H.
  destruct H as [HA HB].
  split.
  - exact HB.
  - exact HA.
Qed.

(* Associativity of AND *)
Lemma and_assoc : forall (A B C : Prop),
  (A /\ B) /\ C -> A /\ (B /\ C).
Proof.
  intros A B C H.
  destruct H as [HAB HC].
  destruct HAB as [HA HB].
  split.
  - exact HA.
  - split.
    + exact HB.
    + exact HC.
Qed.

(* A → (B → A ∧ B) — introduction *)
Lemma and_intro : forall (A B : Prop),
  A -> B -> A /\ B.
Proof.
  intros A B HA HB.
  split.
  - exact HA.
  - exact HB.
Qed.

(* ---------------------------------------------------------- *)
(*  Section 3: Disjunction (∨)                                 *)
(* ---------------------------------------------------------- *)

(* Left introduction: A → A ∨ B *)
Lemma or_intro_l : forall (A B : Prop),
  A -> A \/ B.
Proof.
  intros A B HA.
  left.
  exact HA.
Qed.

(* Right introduction: B → A ∨ B *)
Lemma or_intro_r : forall (A B : Prop),
  B -> A \/ B.
Proof.
  intros A B HB.
  right.
  exact HB.
Qed.

(* Commutativity of OR *)
Lemma or_comm : forall (A B : Prop),
  A \/ B -> B \/ A.
Proof.
  intros A B H.
  destruct H as [HA | HB].
  - right. exact HA.
  - left.  exact HB.
Qed.

(* ---------------------------------------------------------- *)
(*  Section 4: Negation (¬) and False (⊥)                      *)
(* ---------------------------------------------------------- *)

(* ¬A is defined as A → False *)
(* From A and ¬A, we get False *)
Lemma neg_elim : forall (A : Prop),
  A -> ~A -> False.
Proof.
  intros A HA HNA.
  apply HNA.
  exact HA.
Qed.

(* Ex falso quodlibet: from False, anything follows *)
Lemma ex_falso : forall (A : Prop),
  False -> A.
Proof.
  intros A HF.
  contradiction.
Qed.

(* Double negation introduction: A → ¬¬A *)
Lemma dne_intro : forall (A : Prop),
  A -> ~ ~ A.
Proof.
  intros A HA HNA.
  apply HNA.
  exact HA.
Qed.

(* ---------------------------------------------------------- *)
(*  Section 5: Classical Logic (requires axiom)                *)
(* ---------------------------------------------------------- *)

Require Import Classical.

(* Law of Excluded Middle *)
Lemma excluded_middle : forall (A : Prop),
  A \/ ~A.
Proof.
  intro A.
  apply classic.
Qed.

(* Peirce's Law: ((A → B) → A) → A *)
(* Holds in classical logic, not intuitionistic *)
Lemma peirce : forall (A B : Prop),
  ((A -> B) -> A) -> A.
Proof.
  intros A B H.
  apply H.
  intro HA.
  destruct (classic A) as [HA' | HNA].
  - exact HA'.
  - contradiction.
Qed.

(* ---------------------------------------------------------- *)
(*  Section 6: Bonus — Proving equality                        *)
(* ---------------------------------------------------------- *)

(* Leibniz equality: if x = y, then P x → P y *)
Lemma eq_subst : forall (A : Type) (P : A -> Prop) (x y : A),
  x = y -> P x -> P y.
Proof.
  intros A P x y Heq HPx.
  rewrite Heq.
  exact HPx.
Qed.
