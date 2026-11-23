---
tags: [cs320, lab, computer-networks, network-layer, ip, wireshark, lecture-notes]
module: CS320
topic: "Lab 6 — IP Protocol: Wireshark Lab"
date: 2026-11-23
next: "[[]]"
prev: "[[2026-11-05 - Lab 5 TCP - Wireshark Lab]]"
---

# Lab 6 — IP Protocol: Wireshark Lab

> [!info] CS320 Lab 6 (Wireshark IP) — 2026-11-23
> CS320 Computer Networks · based on Kurose & Ross *A Top-Down Approach*, 6th ed. §4.4
> Source: `CS320_Lab6_WINDOWS.pdf` (Wireshark IP lab, Windows version) · `CS320_Lab6_reading_material.pdf` (§4.4) · `Lab 6 7.pdf` (quiz slides)

**Overview**

- The network layer has **3 components**: the **IP protocol**, the **routing** component (path selection / forwarding tables), and **ICMP** (error reporting).
- The **IP datagram** is a 20-byte (no-options) header plus payload; its fields drive addressing, fragmentation, and demultiplexing.
- **Fragmentation** happens when an outgoing link's **MTU** is smaller than the datagram; IPv4 reassembles **only at the end system**.
- **IPv4 addressing** uses **CIDR** (`a.b.c.d/x`); **DHCP** assigns addresses automatically, **NAT** hides a private network behind one public IP.
- **IPv6** uses a fixed 40-byte header, 128-bit addresses, and **no router fragmentation**.
- The Wireshark lab analyses **traceroute** datagrams to inspect the IP header and fragmentation.

---

## 1. The Network Layer & the IP Datagram

The Internet network layer has three major pieces:

| Component | Role |
|---|---|
| IP protocol | addressing conventions, datagram format, packet-handling rules |
| Routing component | picks the path a datagram follows (RIP/OSPF/BGP build forwarding tables) |
| ICMP | reports errors + responds to network-layer info requests |

### IPv4 datagram format (header fields)

| Field | Bits | Purpose |
|---|---|---|
| Version | 4 | IP version (4); tells how to interpret the datagram |
| Header length | 4 | length in 32-bit words; where the data begins (typ. 5 → 20 B) |
| Type of service (TOS) | 8 | requested QoS (low delay, high throughput) |
| Datagram length | 16 | header + data in bytes; max 65535 B; typ. 1500 B |
| Identifier, flags, frag offset | 32 | used for fragmentation (removed in IPv6) |
| Time-to-live (TTL) | 8 | decremented by 1 per router; dropped at 0 |
| Protocol | 8 | which transport protocol the payload belongs to (6 = TCP, 17 = UDP, 1 = ICMP) |
| Header checksum | 16 | 1s-complement sum of 2-byte words; recomputed per router |
| Source / dest IP | 32 each | set by source (dest found via DNS) |
| Options | var | rarely used; dropped in IPv6 |

> [!note] The "glue" analogy
> The **protocol number** in IP binds network↔transport (like the **port number** binds transport↔application).

> [!tip] Payload & totals
> No options → 20-byte IP header. Carrying TCP → each datagram = 40 B of headers (20 TCP + 20 IP) + application data. The payload can also carry ICMP, UDP, etc.

---

## 2. IP Datagram Fragmentation

- Link-layer protocols carry different max sizes: **Ethernet = 1500 B**, wide-area links often **576 B** → the **MTU** places a hard limit.
- If the outgoing link's MTU < datagram length, the datagram is split into **fragments**; reassembled **before** reaching the transport layer.
- **IPv4 reassembles only in end systems**, not routers. Three header fields make this possible:

| Field | Role |
|---|---|
| Identification | stamped by host, incremented per datagram; all fragments share the original's ID |
| Flag bit | **1 = "more fragments follow"**; 0 = this is the last fragment |
| Fragmentation offset | where this fragment fits, in **units of 8 bytes** |

> [!example] Offset arithmetic
> A 2nd fragment carrying 1480 B has offset = 1480 / 8 = **185**.

> [!warning] Fragmentation risks
> Fragments may be lost (IP is unreliable), and hostile "bizarre fragments" enable **DoS attacks**. **IPv6 removes router fragmentation** to streamline processing and harden IP.

---

## 3. IPv4 Addressing

- An **interface** is the boundary between a host/router and a link; a router has many. **Each interface has its own IP address.**
- An IPv4 address is **32 bits**, written in **dotted-decimal** (`223.1.1.9`).
- A **subnet** = the network interconnecting host interfaces + one router interface (e.g. `223.1.1.0/24` — the `/24` mask says the leftmost 24 bits are the subnet address).
- **CIDR** (Classless Interdomain Routing) = `a.b.c.d/x`; the **x** most-significant bits are the **network prefix**.
  - **Route aggregation / summarisation**: one prefix advertises many networks → smaller forwarding tables (routers outside only look at the leading x bits).
- **Classful addressing** (pre-CIDR) fixed prefixes to 8/16/24 bits — Class A (8-bit), B (16-bit, 65534 hosts), C (24-bit, 254 hosts) — awkward for mid-size orgs.
- **Broadcast** `255.255.255.255` → delivered to all hosts on the subnet.
- Address space is managed globally by **ICANN**.

### DHCP (Dynamic Host Configuration Protocol)

Four-step process for a newly-arriving host:

1. **DHCP discovery** — client broadcasts (UDP port 67 → dst `255.255.255.255`, src `0.0.0.0`).
2. **DHCP offer** — server(s) respond with a proposed IP, network mask, and **lease time**.
3. **DHCP request** — client picks one offer and echoes the params.
4. **DHCP ACK** — server confirms.

Also delivers subnet mask, first-hop router, and local DNS server address. Plug-and-play; renews lease on expiry.

### NAT (Network Address Translation)

- Private address spaces (e.g. `10.0.0.0/8`) are meaningful only inside the home network.
- A **NAT-enabled router** presents the whole home network as **one device with one IP**.
- The **NAT translation table** maps (internal IP : port) → (public IP : new port) so replies route back correctly.
- **Limitation**: breaks P2P (a NATed peer can't accept inbound connections). Workarounds: **connection reversal**, **UPnP** (host asks NAT to create a public↔private port mapping).

---

## 4. ICMP

- Hosts & routers use ICMP to pass **network-layer info** and **report errors** (e.g. "type 3 = destination unreachable" when no path to host).
- ICMP sits **above IP**, carried in the IP payload; has a **type + code** field plus the first 8 bytes of the offending datagram.
- ICMP powers **traceroute**: the source sends datagrams (each carrying a UDP segment) with TTL = 1, 2, 3, … Each router drops the expired one and returns an **ICMP TTL-exceeded** message, revealing its name + IP + RTT. The final datagram reaches the destination with an unlikely UDP port → **port-unreachable** ICMP → source knows to stop.

---

## 5. IPv6

| Change | IPv4 | IPv6 |
|---|---|---|
| Address size | 32 bits | **128 bits** |
| Header | variable (options) | **fixed 40 bytes** (faster) |
| Fragmentation | routers + hosts | **source/destination only** (router sends "Packet Too Big") |
| Header checksum | yes | **removed** (transport/link already checksum) |
| Options | in header | moved to a "next header" |

IPv6 fields: Version (4b) · Traffic class (8b, ≈ TOS) · **Flow label** (20b) · Payload length (16b) · Next header (TCP/UDP) · Hop limit (≈ TTL) · 128-bit src/dst. ICMPv6 adds "Packet Too Big" + subsumes IGMP.

**Transition**: dual-stack (IPv6 nodes keep a full IPv4 stack) and **tunneling** (wrap a whole IPv6 datagram inside an IPv4 payload across IPv4 routers).

> [!note] IPsec (brief)
> VPN/security — encrypts + authenticates IP payloads; provides confidentiality, integrity, origin authentication.

---

## 6. The Wireshark Lab — traceroute datagrams

The lab captures an execution of **traceroute** and inspects the IP headers. (Standard Kurose trace `ip-ethereal-trace-1`: client `192.168.1.102`.)

| # | Question | Key answer / method |
|---|---|---|
| q1 | Your computer's IP address | read the **source** address of the first ICMP echo request |
| q2 | Upper-layer protocol field | **1** (ICMP) |
| q3 | IP header bytes / payload bytes | header length field ×4 (typ. **20 B**); payload = total length − header |
| q4 | Fragmented? | check fragment offset = 0 and "more fragments" flag = 0 → **not fragmented** |
| q5 | Fields that always change | **Identification** (+1 each), **header checksum**, **TTL** |
| q6 | Fields that stay constant | version, header length, TOS, protocol, src IP, dst IP |
| q7 | Identification pattern | increments **by 1** per datagram |
| q8 | TTL-exceeded reply: Identification + TTL | TTL = **64** (or 255); each reply has its own Identification |
| q9 | Do they stay unchanged? | TTL stays constant; Identification changes per reply |
| q10 | Fragmented at 2000 B? | **yes** → 2 fragments (Ethernet MTU 1500 → max 1480 B data/fragment) |
| q11 | First fragment | "more fragments" flag = **1**, offset = **0**, length = 1500 |
| q12 | Second fragment | flag = **0**, offset = **185** (=1480/8) → it is the last |
| q13 | Fields changed between fragments | total length, flags, fragment offset, checksum |
| q14 | Fragments at 3500 B? | **3 fragments** (1500 + 1500 + remainder) |
| q15 | Fields changed among fragments | same as q13 (offset/flag/checksum/length) |
| q16 | UDP inside IP | protocol field = **17** instead of 1 |
| q17 | TCP inside IP | protocol field = **6** instead of 1 |

> [!warning] Ethernet 1500-byte limit
> On Ethernet, IP packets >1500 B should fragment. If Wireshark reports one oversized datagram, it's the Ethernet-driver/Wireshark interaction — use the provided trace instead.

---

## 7. Summary Table

| Concept | Key fact |
|---|---|
| Network layer components | IP + routing + ICMP |
| IPv4 header | 20 B (no options); header length field ×4 |
| Protocol field | 6=TCP, 17=UDP, 1=ICMP |
| Fragmentation | ID + "more fragments" flag + offset (8-byte units) |
| MTU | Ethernet 1500 B; wide-area 576 B |
| CIDR | `a.b.c.d/x` prefix addressing |
| DHCP | discover → offer → request → ACK |
| NAT | private net behind one public IP via translation table |
| IPv6 | 128-bit, 40-byte fixed header, no router fragmentation |

## 8. Gotchas

- [ ] Fragmentation offset is in **8-byte units** (offset 185 → 1480 bytes).
- [ ] IPv4 reassembly happens at the **end host**, never in routers.
- [ ] TTL decremented by 1 per router; datagram dropped at 0.
- [ ] Protocol number (IP) vs port number (transport) vs application (socket).
- [ ] IPv6 has **no** header checksum and **no** router fragmentation.

## 9. Related

- [[2026-11-05 - Lab 5 TCP - Wireshark Lab]] — previous lab (TCP, transport layer).
- [[2026-10-26 - TCP]] — transport-layer lecture.

> [!tip] Next lecture
> The next Wireshark lab covers **ICMP** in detail (the traceroute mechanics seen here).
