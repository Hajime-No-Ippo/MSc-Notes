(* ==== q1.v ==== *)
Parameter A: Prop.
Lemma q1 : A -> A.
Proof.
  intros.
  exact H.
Qed.


(* ==== q2.v ==== *)
Parameter A B: Prop.
Lemma q2: A->(B->A).
Proof.
  intro.
  intros.
  exact H.
Qed.




(* ==== q3.v ==== *)
Parameter A B C: Prop.
Lemma q3: (A->B->C)->B->A->C.
Proof.
  intro.
  intro.
  intro.
  apply H.
  - apply H1.
  - apply H0.
Qed.



(* ==== q4.v ==== *)
Parameter A B : Prop.
Lemma q4: (A->A->B)->A->B.
Proof.
  intros.
  apply H.
  - apply H0.
  - apply H0.
Qed.


(* ==== q5.v ==== *)
Parameter A B: Prop.

Lemma q5: (A->B)->A->A->B.
Proof.
  intros.
  apply H.
  apply H0.
Qed.



(* ==== q6.v ==== *)
Parameter A B C D: Prop.

Lemma q6: (A->B)->(A->C)->(B->C->D)->A->D.
Proof.
  intros.
  apply H1.
  - apply H. apply H2.
  - apply H0. apply H2.
Qed.
    



(* ==== q7.v ==== *)
Parameter A B: Prop.
Lemma q7: ((((A->B)->A)->A)->B)->B.
Proof.
  intros.
  apply H.
  intros.
  apply H0.
  intros.
  apply H.
  intro.
  apply H1.
Qed.



