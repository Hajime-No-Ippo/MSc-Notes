---
tags: [cs320, lab, computer-networks, transport-layer, tcp, wireshark, lecture-notes]
module: CS320
topic: "Lab 5 — TCP: Wireshark Lab"
date: 2026-11-05
next: "[[]]"
prev: "[[2026-10-26 - TCP]]"
---

# Lab 5 — TCP: Wireshark Lab

> [!info] CS320 Lab 5 (Wireshark TCP) — 2026-11-05
> Analysing a trace of a 150 KB file (Lewis Carroll's *Alice's Adventures in Wonderland*) uploaded to `gaia.cs.umass.edu` via **HTTP POST**.
> Trace: `tcp-ethereal-trace-1` from <http://gaia.cs.umass.edu/wireshark-labs/wireshark-traces.zip>
> Lab sheet: `CS320_Lab5.pdf` (Kurose & Ross, *Computer Networking: A Top-Down Approach*, 6th ed. — Wireshark TCP lab)

In this lab we investigate TCP's behaviour in detail — sequence and acknowledgement numbers for reliable transfer, congestion control (slow start + congestion avoidance), and receiver-advertised flow control — by reading the trace of the Alice-in-Wonderland upload.

**Connection at a glance**

| | Client | Server |
|---|---|---|
| IP address | `192.168.1.102` | `128.119.245.12` (= `gaia.cs.umass.edu`) |
| TCP port | `1161` | `80` |
| ISN | `232129012` | `883061785` |
| Bytes sent | 164 090 B (122 data segments) | — |

---

## Part 1 — A First Look at the Trace

### q1 — Client IP address and port

The client (source) transferring the file is **`192.168.1.102`** on TCP port **`1161`**.

### q2 — Server IP address and port

`gaia.cs.umass.edu` is **`128.119.245.12`**, sending and receiving TCP segments for this connection on port **`80`** (HTTP).

---

## Part 2 — The Three-Way Handshake

### q3 — Sequence number of the SYN

The SYN that initiates the connection carries **sequence number `232129012`** — the client's *initial sequence number* (ISN). The segment is identified as a SYN by the **SYN flag** bit being set (Wireshark shows Flags `[S]`, control-bits value `0x002`).

### q4 — Sequence number and acknowledgement of the SYNACK

The SYNACK sent by `gaia.cs.umass.edu` in reply has:

| Field | Value | Meaning |
|---|---|---|
| Sequence number | `883061785` | the server's own ISN |
| Acknowledgement | `232129013` | client's ISN **+ 1** |

The server determined the acknowledgement value as **"the next sequence number I expect from you"** — i.e. the client's SYN occupied one sequence number, so the server acknowledges it by saying it next expects `client_isn + 1`. The segment is identified as a SYNACK because **both the SYN and ACK flags** are set (Wireshark shows `[S.]`).

### q5 — Sequence number of the HTTP POST segment

Filtering for `http` reveals the **POST** request; its first TCP segment has **relative sequence number `1`** (absolute `232129013`). Clicking **"Reassembled TCP Segments"** patches all the TCP segments that make up the full HTTP message together into one frame, showing:

```
POST /ethereal-labs/lab3-1-reply.htm HTTP/1.1
```

followed by the request headers and the body of *Alice in Wonderland* (you may need to scroll down to see the whole frame).

---

## Part 3 — RTT Estimation

### q6(a) — RTT of the initial SYN

Time from the SYN (14:44:20.570) to the SYNACK (14:44:20.594):

$$
\text{RTT}_\text{SYN} = 0.023172\ \text{s} \approx 23.2\ \text{ms}
$$

### q6(b) — Next 10 valid RTTs

RTT is the time between a data packet and the ACK sent *in response to* that packet. Because ACKs are cumulative, a delayed ACK may acknowledge several packets — only the time from the **last** packet in the series (the one that actually triggered the ACK) to the ACK is a valid RTT.

| # | SampleRTT (ms) |
|---|---|
| 1 | 27.46 |
| 2 | 35.56 |
| 3 | 70.06 |
| 4 | 114.43 |
| 5 | 139.89 |
| 6 | 189.65 |
| 7 | 180.62 |
| 8 | 51.40 |
| 9 | 94.35 |
| 10 | 141.92 |

### q6(c) — EstimatedRTT

$$
\text{EstimatedRTT} = (1-\alpha)\cdot\text{EstimatedRTT} + \alpha\cdot\text{SampleRTT}, \quad \alpha = 0.125
$$

The first `EstimatedRTT` is set equal to the SYN's measured RTT (23.17 ms); each subsequent one folds in the next SampleRTT:

| Sample | SampleRTT (ms) | EstimatedRTT (ms) |
|---|---|---|
| 0 (SYN) | 23.17 | 23.17 |
| 1 | 27.46 | 23.71 |
| 2 | 35.56 | 25.19 |
| 3 | 70.06 | 30.80 |
| 4 | 114.43 | 41.25 |
| 5 | 139.89 | 53.58 |
| 6 | 189.65 | 70.59 |
| 7 | 180.62 | 84.34 |
| 8 | 51.40 | 80.23 |
| 9 | 94.35 | 81.99 |
| 10 | 141.92 | 89.48 |

> [!note] Only one sample per RTT
> `SampleRTT` is estimated **once per RTT** — never for a retransmitted segment, whose ACK is ambiguous (is the ACK for the original or the retransmission?). This trace has no retransmissions, so every sample is clean.

---

## Part 4 — Segments, Flow Control and Throughput

### q7 — Length of the first 10 segments

**565, 1460, 1460, 1460, 1460, 1460, 1147, 1460, 1460, 1460** bytes.

The 1460 B values are one **MSS** (1500 B Ethernet MTU − 40 B TCP/IP header); the odd values (565, 1147) are where a chunk of application data ends mid-MSS.

### q8 — Minimum advertised receiver window

The minimum available buffer space the receiver (server) advertises is **`5840` bytes**, in the SYNACK. It then grows monotonically to **62780 B** and stays there. Because it always exceeds what the sender needs, **the lack of receiver buffer space never throttles the sender** — the sender is limited by its own congestion window, not by `rwnd`.

### q9 — Retransmissions?

**None.** I checked for **duplicate sequence numbers** across all client → server segments — the sequence numbers increase monotonically, no segment is re-sent, and there are no retransmission markers.

### q10 — Data acknowledged per ACK / delayed ACK

The receiver typically acknowledges **1460 B (one MSS)** at a time, but **delayed ACK is clearly present**: the most common ACK increment is **2920 B (two MSS)**, occurring 32 times (vs 20 single-MSS ACKs). With delayed ACK the receiver waits briefly (~200 ms) and piggy-backs one ACK onto two received segments rather than ACKing each one immediately.

### q11 — Throughput

$$
\text{Throughput} = \frac{164\,090\ \text{B}}{5.27\ \text{s}} \approx 31.1\ \text{KB/s} \approx 249\ \text{kb/s}
$$

*Method:* total bytes sent by the client (the POST body + headers = 164 090 B) divided by the time from the **first data segment** (14:44:20.597) to the **last data segment** (14:44:25.868).

---

## Part 5 — Congestion Control

### q12 — Slow start and congestion avoidance

In the **Time-Sequence-Graph (Stevens)** (sequence number vs time, client → server):

- **Slow start** — the initial phase, where the congestion window grows **exponentially** (roughly doubling each RTT). It appears as a **steepening, upward-curving** staircase.
- **Congestion avoidance** — after `cwnd` reaches `ssthresh`, growth turns **linear** (+1 MSS per RTT). It appears as a **constant-slope straight line**.

In this trace slow start occupies the first portion of the transfer (`cwnd` climbing ~1 → 2 → 4 → 8 … MSS), then hands off to congestion avoidance for the remainder. There is no loss event, so no fast-retransmit / fast-recovery is triggered — the whole 150 KB file completes without a timeout.

---

## Summary Table

| # | Question | Answer |
|---|---|---|
| q1 | Client IP / port | `192.168.1.102` / `1161` |
| q2 | Server IP / port | `128.119.245.12` / `80` |
| q3 | SYN sequence number | `232129012` (client ISN); SYN flag set |
| q4 | SYNACK seq / ack | seq `883061785`; ack `232129013` = client ISN + 1; SYN+ACK flags |
| q5 | POST sequence number | relative `1`; frame shows `POST … HTTP/1.1` (reassembled) |
| q6(a) | SYN RTT | ≈ 23.2 ms |
| q6(b) | 10 RTTs | 27.46 … 141.92 ms |
| q6(c) | EstimatedRTT | `(1−α)·Est + α·Sample`, α = 0.125 |
| q7 | First 10 lengths | 565, 1460×6, 1147, 1460×2 |
| q8 | Min receiver window | 5840 B → grows to 62780 B; never throttles |
| q9 | Retransmissions | none (monotonic sequence numbers) |
| q10 | Data per ACK | 1460 B; delayed ACK = 2920 B (two MSS) |
| q11 | Throughput | ≈ 31 KB/s ≈ 249 kb/s |
| q12 | Slow start / CA | exponential → linear in Stevens graph |

---

## Gotchas

- [ ] **MSS = 1460 B, not 1500 B.** The 1500 B is the *Ethernet MTU* (whole frame); the TCP payload is 1500 − 40 B of headers = 1460 B.
- [ ] **Only the last segment's time counts in an RTT.** With cumulative + delayed ACKs, an ACK acknowledges several packets — measure from the segment that *actually triggered* the ACK.
- [ ] **The SYN occupies one sequence number.** That's why the SYNACK's ack is `client_isn + 1`, not `client_isn`.
- [ ] **`rwnd` is the *receiver's* window; `cwnd` is the *sender's*.** q8 asks about `rwnd` (never throttles here); q12 is about `cwnd` growth.
- [ ] **No retransmissions → no fast retransmit / fast recovery.** The whole transfer completes under slow start → congestion avoidance, with no loss event.
- [ ] **Delayed ACK inflates ACK increments.** Don't mistake a 2920 B ACK for the receiver acknowledging "one big segment" — it's two 1460 B segments acked together.

> [!warning] Screenshots
> The lab sheet asks for a screenshot of the packet(s) used to answer each question — capture the packet summary line and only the minimum packet detail needed.

---

## Related

- [[2026-10-26 - TCP]] — the reading these mechanisms come from (handshake, flow control, congestion control)
- [[2026-10-18 - The Transport Layer & UDP]] — the previous transport-layer note

---

> [!tip] Next lecture
> Fill in the `next` field in frontmatter once the next notes arrive.
