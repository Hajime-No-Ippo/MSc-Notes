(* ==== q1.v ==== *)
Parameter A B C: Prop.

Lemma q1: ((A /\ B) /\ C) -> (A /\ (B /\ C)).
Proof.
  intros H.
  destruct H as [[H0 H1] H2].
  split.
  - exact H0.
  - split.
    + exact H1.
    + exact H2.
Qed.


(* ==== q2.v ==== *)
Lemma q2: ((A /\ B) -> C) -> (A -> (B -> C)).
Proof.
  intros H HA HB.
  apply H.
  split.
  - exact HA.
  - exact HB.
Qed.


(* ==== q3.v ==== *)
Lemma q3: ((A \/ B) \/ C) -> (A \/ (B \/ C)).
Proof.
  intros H.
  destruct H as [H0 | H2].
  - destruct H0 as [HA | HB].
    + left. exact HA.
    + right. left. exact HB.
  - right. right. exact H2.
Qed.


(* ==== q4.v ==== *)
Lemma q4: ((A \/ B) -> C) -> (A -> (B -> C)).
Proof.
  intros H HA HB.
  apply H.
  left. exact HA.
Qed.


(* ==== q5.v ==== *)
Lemma q5: (~A \/ B) -> (A -> B).
Proof.
  intros H HA.
  destruct H as [H0 | H1].
  - exfalso. apply H0. exact HA.
  - exact H1.
Qed.


(* ==== q6.v ==== *)
Lemma q6: (A -> B) -> (~B -> ~A).
Proof.
  intros H HB.
  red. intro HA.
  apply HB. apply H. exact HA.
Qed.


(* ==== q7.v ==== *)
Lemma q7: ~(A /\ ~A).
Proof.
  red. intros H.
  destruct H as [H0 H1].
  apply H1. exact H0.
Qed.


(* ==== q8.v ... q11.v ==== *)
(* LEM is assumed explicitly: Rocq's logic is constructive, so the
   law of the excluded middle is NOT available for free. *)
Parameter E F: Prop.
Hypothesis LEM: forall P: Prop, P \/ ~P.

Lemma q8: ~(E \/ F) -> (~E /\ ~F).
Proof.
  intros H.
  split.
  - intro HE. apply H. left. exact HE.
  - intro HF. apply H. right. exact HF.
Qed.

Lemma q9: (~E /\ ~F) -> ~(E \/ F).
Proof.
  intros H.
  destruct H as [HE HF].
  intros H0.
  destruct H0 as [HE0 | HF0].
  - apply HE. exact HE0.
  - apply HF. exact HF0.
Qed.

Lemma q10: (~E \/ ~F) -> ~(E /\ F).
Proof.
  intros H.
  destruct H as [HE | HF].
  - intros H0. destruct H0 as [HE0 HF0]. apply HE. exact HE0.
  - intros H0. destruct H0 as [HE0 HF0]. apply HF. exact HF0.
Qed.

Lemma q11: ~(E /\ F) -> (~E \/ ~F).
Proof.
  intros H.
  destruct (LEM E) as [HE | HE].
  - right. intro HF. apply H. split. exact HE. exact HF.
  - left. exact HE.
Qed.
