---
tags: [cs320, computer-networks, transport-layer, udp, reading-notes]
module: CS320
topic: "Computer Networks — The Transport Layer & UDP"
date: 2026-10-18
next: "[[2026-10-26 - TCP]]"
prev: "[[2026-10-13 - DNS]]"
---

# The Transport Layer & UDP

> [!info] Lab 4 Reading — 2026-10-18
> CS320 Computer Networks · Kurose & Ross, *Ch. 3 — Transport Layer* (§3.1–3.4)
> Sources: `CS320_Lab4_reading_material.pdf`, `Lab 4 Summarized.pdf` (quiz notes)

**Overview**

- Transport vs network layer: logical communication
- Multiplexing & demultiplexing (ports, sockets)
- UDP: why choose it, segment structure, checksum
- Intro to reliable data transfer (rdt)

---

## 1. Transport-Layer Services

A transport-layer protocol provides **logical communication between application processes running on different hosts** — from the app's perspective the hosts look directly connected, even though they may be on opposite sides of the planet.

- Transport protocols are implemented in **end systems only**, never in routers.
- Sender: application message → (possibly fragmented) **segments** + transport header → network layer.
- Routers only act on **network-layer fields** — they never examine the transport header.
- Receiver: network layer extracts segment → transport layer → correct socket → process.

> [!example] The household analogy (Kurose & Ross)
> Two houses, each with 12 kids (cousins) writing letters to each other. One kid per house (Ann, Bill) collects/distributes household mail; the postal service moves mail house-to-house.
>
> | Household | Network |
> |---|---|
> | Letters in envelopes | Application messages |
> | The cousins | Processes |
> | The houses | Hosts / end systems |
> | Ann and Bill | **Transport-layer protocol** (end systems only) |
> | Postal service + mail carriers | **Network-layer protocol** |
>
> - When Ann/Bill are replaced by Susan/Harvey (who lose letters), the service model changes → different transport protocols offer different service models.
> - Transport services are **constrained by the network layer below**: no delay/bandwidth guarantee at the network layer → no such guarantee end-to-end from transport.
> - **But** transport can add what the network doesn't have: e.g. **reliable data transfer over an unreliable network**, or **encryption** (Ch. 8) even if IP gives no confidentiality.

### The Internet's Two Transport Protocols

| | **UDP** | **TCP** |
|---|---|---|
| Service | Unreliable, connectionless | Reliable, connection-oriented |
| Core services | Mux/demux + error checking (that's it!) | + Reliable data transfer (flow control, seq #s, acks, timers), + congestion control |
| Regulation | Sends at any rate, forever | Regulated by congestion control (equal share of link bandwidth) |
| Header overhead | 8 bytes | 20 bytes |

- **IP** = best-effort delivery: no guarantee of delivery, ordering, or integrity.
- The **fundamental job of UDP/TCP**: extend IP's **host-to-host** delivery → **process-to-process** delivery (transport-layer multiplexing/demultiplexing).
- **Terminology**: in this book both TCP and UDP packets are called **segments**; **datagram** is reserved for network-layer packets.
- App developer picks UDP vs TCP when **creating the socket** (§2.7).

---

## 2. Multiplexing and Demultiplexing

- **Demultiplexing** (receiver): delivering an incoming segment to the correct socket, by examining segment header fields.
- **Multiplexing** (sender): gathering data chunks from different sockets, adding header info (for later demux), passing segments to the network layer.
- Needed by *any* network where one protocol at a layer serves multiple protocols above it.

**Requirements**: sockets have unique identifiers + each segment carries a field saying which socket it's for → **source port number** and **destination port number**, each **16-bit (0–65535)**.

- **Well-known ports 0–1023** are restricted/reserved: HTTP = 80, FTP = 21 (list: RFC 1700 / iana.org).
- Typical split: **client** lets transport auto-assign a port; **server** binds a specific one.

### Connectionless (UDP) Mux/Demux

- `socket(AF_INET, SOCK_DGRAM)` → auto-assigned port from **1024–65535**, or `clientSocket.bind(('', 19157))` for a specific one.
- A segment carries (data, src port 19157, dst port 46428, …); receiver demuxes on **destination port only**.
- **A UDP socket is identified by a 2-tuple: (destination IP, destination port)** — so segments from *different* sources with the same destination hit the **same socket**.
- **Source port** = part of the *return address*: the reply's destination port comes from the request's source port (complete return address = src IP + src port). The server does this with `recvfrom()`.

### Connection-Oriented (TCP) Mux/Demux

- **A TCP socket is identified by a 4-tuple: (src IP, src port, dst IP, dst port)** — the host uses all four fields to demux.
- So two segments with different source IPs/ports → **different sockets** (except the original connection-establishment request).
- Handshake flow: server's **welcoming socket** waits on port 12000 → client sends a segment with dst port 12000 + a connection-establishment bit → server does `connectionSocket, addr = serverSocket.accept()` → a **new socket** created, identified by the four values; all later matching segments demux to it.
- One host can host **many simultaneous connections**, each socket with its own 4-tuple (e.g. Fig 3.5: hosts A and C can both use source port 26145 to server B — no clash, different source IPs).

> [!warning] Focus on Security — Port scanning
> Open ports map to applications (Web, FTP, DNS, SMTP; e.g. MS SQL on UDP 1434 → Slammer worm). **Port scanners** enumerate them — most widely used: **nmap** (nmap.org, in most Linux distros).
> - TCP scan: sequentially look for ports accepting connections.
> - UDP scan: look for ports responding to segments.
> - Returns open / closed / unreachable. Revisited for TCP connection management in §3.5.6.

**Web servers & sockets:**

- High-performing servers often use **one process + a thread per connection** (thread = lightweight subprocess) — many connection sockets can attach to one process.
- **Persistent HTTP**: one socket for the whole connection. **Non-persistent HTTP**: a new TCP connection (and socket) per request/response — frequent create/close hurts performance on a busy server.

---

## 3. Connectionless Transport: UDP (RFC 768)

UDP does "just about as little as a transport protocol can do":

1. Take message from app process
2. Attach source + destination port numbers (mux/demux)
3. Add two small fields (length, checksum)
4. Pass segment to network layer

**No handshaking** before sending → **connectionless**. If the app picks UDP, it is *almost* talking directly to IP.

> [!example] DNS over UDP
> DNS builds a query → UDP adds header → IP datagram → name server. No handshake. If no reply comes (lost query/reply), try another name server or tell the app.

### Why Choose UDP over TCP?

| Reason | Explanation |
|---|---|
| **Finer app-level control** | Data passed to UDP goes out immediately. TCP throttles (congestion control) and resends until acked — bad for real-time apps that need a min rate, dislike delay, and can tolerate some loss. |
| **No connection establishment** | TCP needs a 3-way handshake first; UDP "just blasts away". **Principal reason DNS runs over UDP** — HTTP needs TCP's reliability for text. |
| **No connection state** | TCP tracks buffers, congestion params, seq/ack numbers. UDP has none → a UDP server can support **many more active clients**. |
| **Small header overhead** | TCP = **20 bytes**; UDP = **8 bytes**. |

### Which Apps Use What

| Application | App-layer protocol | Transport |
|---|---|---|
| Electronic mail | SMTP | **TCP** |
| Remote terminal | Telnet | **TCP** |
| Web | HTTP | **TCP** |
| File transfer | FTP | **TCP** |
| Remote file server | NFS | Typically **UDP** |
| Streaming multimedia | proprietary | UDP or TCP |
| Internet telephony | proprietary | UDP or TCP |
| Network management | SNMP | Typically **UDP** |
| Routing protocol | RIP | Typically **UDP** |
| Name translation | DNS | Typically **UDP** |

- **RIP**: updates every ~5 min, lost ones are replaced by newer ones anyway.
- **SNMP**: often runs when the network is *stressed* — exactly when reliable, congestion-controlled transfer is hardest.
- **Streaming**: ~75% of on-demand/live streaming used TCP (Sripanidkulchai 2004); UDP streaming is **controversial** because UDP has **no congestion control** — uncontrolled high-bitrate UDP floods routers, drives up loss, and **crowds out TCP** senders (which do back off). Proposals exist to force all sources (incl. UDP) to do adaptive congestion control.
- You *can* build reliability into the app over UDP (acks + retransmissions) — reliable without TCP's rate constraints, but a nontrivial debugging job.

### UDP Segment Structure

```
 32 bits
+---------------------------------------------+
| Source port #      |   Destination port #   |   2 bytes each
|      Length        |       Checksum         |   2 bytes each
+---------------------------------------------+
| Application data (message)                  |
+---------------------------------------------+
```

- **Length** = bytes of segment (header + data) — needed because data field size varies.
- **Checksum** = error detection at the receiver (calculated over part of the IP header too, omitted here).

### UDP Checksum — 1s Complement Sum

**Sender**: take the 1s complement of the sum of all 16-bit words (wrap overflow around) → put in checksum field.

Worked example (three 16-bit words):

```
  0110011001100000
+ 0101010101010101
= 1011101110110101
+ 1000111100001100
= 0100101011000010   (overflow wrapped around)
```

1s complement (flip all bits): `1011010100111101` → **checksum**.

**Receiver**: adds all four words *including* the checksum — result should be `1111111111111111`. Any 0 → errors introduced.

> [!tip] Why does UDP need its own checksum?
> Not all links provide error checking, and bits can flip even while a segment sits in router memory. End-to-end error detection must be done **end-to-end** → this is the celebrated **end-to-end principle** [Saltzer 1984]: *"functions placed at the lower levels may be redundant or of little value when compared to the cost of providing them at the higher level."*
>
> UDP *detects* errors but never *recovers* — some implementations discard the damaged segment, others pass it up with a warning.

---

## 4. Principles of Reliable Data Transfer (intro)

The reading ends where §3.4 begins — next up is the **rdt** protocol build-up.

- The service abstraction: a **reliable channel** — no bits corrupted or lost, all delivered in send order. Precisely TCP's service model.
- The problem: the layer below may be **unreliable** (TCP runs over best-effort IP). Viewed abstractly: an unreliable point-to-point channel.
- The framework (Fig 3.8): upper layer invokes `rdt_send()` on the sender side; sender/receiver incrementally built up over increasingly complex channel models (corruption, loss). Assumption: **packets arrive in order** (some may be lost, but never reordered).
- Applies at **transport, link, and application layers** — "a candidate to lead the top-ten list of fundamentally important problems in networking".

---

## 5. Quiz Checklist (from `Lab 4 Summarized.pdf`)

Quick self-test — everything below is examinable per the quiz notes:

- [ ] Transport layer = **logical communication between processes** on different hosts; implemented in **end systems, not routers**.
- [ ] Sender side: message → chunks + transport header → segment → IP datagram; routers ignore transport fields.
- [ ] Transport vs network: **processes vs hosts**; transport services are **constrained by the network layer** below, but can add services it doesn't offer (reliable transfer, encryption).
- [ ] UDP = unreliable, connectionless, unregulated. TCP = reliable, connection-oriented, congestion-controlled (equal share, regulates send rate) — both give **process-to-process delivery + error checking**.
- [ ] IP = best-effort: no delivery, ordering, or integrity guarantee.
- [ ] **UDP socket = 2-tuple (dst IP, dst port); TCP socket = 4-tuple (src IP, src port, dst IP, dst port).**
- [ ] Port numbers 16-bit, 0–65535; **well-known 0–1023** (HTTP 80); client auto-assigns, server binds specific.
- [ ] Return address: reply's dst port = request's src port (19157↔46428 inversion).
- [ ] Two TCP segments from different sources → **different sockets** (4-tuple), unlike UDP.
- [ ] Web server: welcoming socket per port; **thread per connection** in modern servers; persistent HTTP = one socket, non-persistent = socket churn.
- [ ] Why UDP over TCP: **finer control** · **no handshake delay** (principal DNS reason) · **no connection state** (more clients) · **8-byte vs 20-byte header**.
- [ ] RIP / SNMP / DNS run over UDP; e-mail / Telnet / Web / FTP run over TCP.
- [ ] UDP lacks congestion control → crowds out TCP → why TCP streaming is rising (some orgs block UDP).
- [ ] App-level reliability over UDP is possible (acks/retransmits in-app) but nontrivial.
- [ ] UDP segment: 4 × 2-byte fields (src port, dst port, length, checksum) — RFC 768.
- [ ] Checksum = 1s complement of 16-bit-word sum, overflow wraps; receiver sums incl. checksum → `1111111111111111` if clean. Detect-only, never recover (discard or warn). Justified by the **end-to-end principle**.
- [ ] Reliable data transfer: no corruption/loss, in-order; TCP's service model; hard because the layer below may be unreliable.

---

## 6. Lab 4 — UDP Wireshark Lab (Q&A)

> [!info] Lab questions
> Captured with `client_UDP.py` (UDP echo, server port 12000) + Wireshark `udp` filter. Answers derived from packet traces and RFC 768.

**Q1 — How many fields are in the UDP header? Name them.**

**4 fields**: Source Port · Destination Port · Length · Checksum.

**Q2 — Length (in bytes) of each header field.**

**2 bytes each** (16 bits × 4 = **8-byte header total**). In Wireshark's packet bytes pane they appear as four 2-byte pairs:

```
32 bits
+----------------+----------------+----------------+----------------+
|   Src Port (2B) |   Dst Port (2B) |   Length (2B)  |  Checksum (2B) |
+----------------+----------------+----------------+----------------+
| Application data ...                                             |
+------------------------------------------------------------------+
```

**Q3 — The value in the Length field is the length of what?**

The **entire UDP segment = header (8 bytes) + payload (application data)** — not just the payload.

*Verify on the trace*: for the echo lab, the message `"hello"` (5 bytes) → Length field = `13` (0x000D = 8 + 5). Empty payload → Length = `8`.

**Q4 — Maximum number of bytes in a UDP payload?**

The Length field is 16 bits → max value 65535.

$$\text{max payload} = 65535 - 8 = \mathbf{65527}\ \text{bytes}$$

(The real-world limit is slightly lower, 65507, because the 20-byte IP header must also fit in the 65535-byte IPv4 datagram — but the lab answer from the Length-field reasoning is 65527.)

**Q5 — Largest possible source port number?**

The source port field is 16 bits → **65535** (range 0–65535).

**Q6 — Protocol number for UDP (hex + decimal)?**

Look in the **IP header's Protocol field** of the datagram carrying the segment: **17 decimal = 0x11 hex**.

(TCP = 6 decimal / 0x06 — useful to memorise both.)

**Q7 — Request/reply pair: relationship between port numbers?**

The ports are **swapped (inverted)** between request and reply:

| | Source port | Destination port |
|---|---|---|
| Request (client → server) | client ephemeral e.g. 54321 | 12000 |
| Reply (server → client) | 12000 | 54321 |

The reply's **destination port = the request's source port** (the source port doubles as the *return address*), and the reply's **source port = the request's destination port**. Same IPs, ports inverted — exactly the Fig 3.4 behaviour from §2.

**Q8 — TCP segment fields vs UDP packet fields — how do they differ?**

TCP's header has **many more fields** than UDP's 4:

| | **UDP** | **TCP** |
|---|---|---|
| Fields | src port, dst port, length, checksum | src port, dst port, **sequence number**, **acknowledgment number**, **data offset**, **flags (SYN/ACK/FIN/RST/…)**, **window size**, checksum, **urgent pointer**, **options** |
| Header size | **8 bytes** fixed | **20 bytes** minimum (grows with options) |
| Reliability support | none — no seq/ack | sequence + acknowledgment numbers, timers |
| Flow/congestion | none | window size field; connection state |
| Setup/teardown | none | SYN / FIN flags (3-way handshake) |

Same two port fields at the top (so mux/demux works identically); everything after that is TCP's reliability machinery.

**Q9 — Smallest UDP packet in the trace & checksum verification.**

- Smallest UDP packets on a real trace are typically **DNS queries** (small fixed question section) — or an empty echo message (just the 8-byte header, Length = 8).
- **Confirm no errors via the checksum** (RFC 768 / RFC 1071):
  1. Take the segment as a sequence of **16-bit words** (big-endian), including header + data (conceptually plus the IP *pseudo-header*: src IP, dst IP, zero byte, protocol 17, UDP length).
  2. **Sum all words** (one's complement arithmetic — any overflow wrap-around by adding it back in).
  3. Take the **1s complement** (flip all bits) of the sum → this should equal the **Checksum field**.
  4. Equivalently at the receiver: add *all* words including the checksum — a clean packet gives **`1111111111111111` (0xFFFF)**; any 0 bit ⇒ error.
  - Practical method: paste the hex bytes into an online hex/1s-complement calculator, or let Wireshark display `[unchecked]`/`[wrong]` vs good status under the checksum line.
- If a captured UDP packet shows checksum `0x0000`: in **IPv4** that means the sender *didn't compute* a checksum (legal but discouraged); in **IPv6** a zero checksum is illegal — the packet must be corrupted.

---

> [!tip] Next lecture
> [[2026-10-26 - TCP]] — Lab 5 reading (TCP).