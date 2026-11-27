# Challenge workshop: summary

ti&m ran a kick-off workshop for the TrustRoom challenge on the first hackathon day. This summarises what
they said there. The raw speech-to-text transcript is in [transcript.md](transcript.md), and `L<n>` points to
its line numbers. The transcript misspells names: "TNM", "Tandem", "TUM", "TIM" and "T&M" mean ti&m, "Paltus",
"pathos", "Pythos", "Actors" and "PERTUS" mean Apertus, and "Kira" means the Keera gateway. Read the
transcript only where this summary is not enough, and trust [challenge_description.md](../../challenge_description.md)
where the two disagree (see the last section).

## Who was there

- Benedict, head of product innovation and industry lead for banking at ti&m. He gave the business part and
  answers business questions (L1-L3).
- Philipp Dietinger, ti&m's chief AI officer and the jury member for the final (L3-L5, L185).
- Two engineers from ti&m's mobile team and its machine learning team, who gave the technical part (L5-L7).
- Support: on site until 17:00 on day one, from 11:00 on day two, and in Discord outside those hours, but not
  at night (L1, L183).

## Why ti&m set this challenge

- More than 25 Swiss banks run ti&m's e-banking. The target users are retail customers, not companies or
  wealth clients (L15, L21-L23).
- OpenAI now offers personal finance management in ChatGPT with direct links to over 12,000 US banks. Google,
  Anthropic, Visa and Mastercard are building similar tools (L29-L31).
- If customers talk to their bank only through ChatGPT or Gemini, the bank loses the channel it uses to advise
  and sell mortgages and insurance, and becomes a data provider (L39-L45).
- ti&m's AI banking assistant has three stages. Reactive answers questions about e-banking and bank data.
  Proactive points out what the customer did not know, such as a missing monthly payment, idle cash before
  payday or a card payment from an unusual country. The TrustRoom is stage three and the hackathon's subject
  (L59-L71).
- The product architecture around the model is an input guardrail (bank topics only, no politics or health),
  a tool policy, a data guardrail, the model, an output guardrail (compliance), and a human who confirms every
  action such as a payment (L49-L57).

## What the TrustRoom is

- A finance AI like ChatGPT, but inside the e-banking, with no training on the customer's data (L73).
- The customer is not limited to the bank's data or to predefined use cases. They can upload outside documents,
  such as a pension statement from another provider, without sending them to a US company (L73-L75).
- The customer asks for the charts and analyses they want instead of choosing from predefined dashboards.
  Benedict's point is that existing finance tools are not personal, because every customer handles money
  differently (L77-L81).
- Example uses ti&m named: explain a confusing document, compare spending per category with last year, budget
  and scenario planning such as a move to a new city (L93-L97).

## Rules

- Apertus must be the base of the TrustRoom's AI. Coding tools such as Claude Code are fine for development
  (L99).
- Use only the provided data. Answers come from the customer's data, with no hallucinated or added figures
  (L99-L101).
- Talk to the customer in a friendly way. Never belittle them, even after the third question about the same
  document (L101).
- No closed models, and no data leaves the environment (L101-L103).
- No investment advice. Payment execution can be left out, so the focus is on analysis (L103).
- Self-hosted open models are allowed for extras such as speech-to-text, as long as Apertus stays the core
  (L133).

## How the jury judges

Benedict named four criteria (L105-L109):

- Customer value and freedom: does the customer really get value?
- Reliable output and traceability: when the TrustRoom says 200 CHF went to SBB, it must be 200 CHF.
- Software architecture.
- How realistic the integration is. ti&m treats this as real product development, so it must work beyond a
  demo.

The weights (30 %, 30 %, 20 %, 20 %) are in challenge_description.md, not in the workshop.

The deadline is 14:30 on day two (L105).

## The four customers

ti&m provides transactions, documents, a persona PDF of three to four pages and example questions for each
customer. Pick one or two and learn their situation first, because the data is built around their questions
(L85-L89, L159-L163).

- Lukas likes doing his own financial analysis and might use Claude or Gemini for it today (L87).
- Jana is a junior data analyst early in her career who wants to plan how to build wealth (L87).
- Daniela is short of money at the end of the month (L87-L89). Lina is her child, and the data contains the
  whole family's history (L91-L93).
- Marco's questions are about mortgages and loans (L89).

All data is synthetic (L91).

## What ti&m provides

- A mock e-banking: a frontend with source code, and a banking API that serves the customer profile, accounts,
  bookings, card transactions and more. Every call needs the token from the login (L123-L125, L135, L139).
- Dashboards are stored in the backend, so the TrustRoom can create and change widgets through the API
  (L141-L143). There are two widget types: declarative widgets with predefined types, as on the default
  dashboard, and free HTML widgets (L175-L177). New widgets and chart layouts are encouraged (L131).
- The banking API and the OCR service are Docker images. Don't change them (L129).
- Changing the frontend is allowed but not the point. If you change it, write down what you changed so the
  jury can take it into account (L129-L131).
- An example MCP server with a bank holidays tool, to use, extend or drop (L125-L127).
- An OCR service for document understanding (L127).
- An example TrustRoom: a small backend and one HTML page that the e-banking loads in an iframe as a side
  panel and a full page. It receives the context: current page, customer name and access token. It has a
  navigation tool that moves the e-banking to a page (L149-L157, L167-L169).
- The `starter/` folder of the repo holds the persona descriptions, the documents and the CSV files behind the
  banking API, which help check whether answers are correct (L161-L165). Every folder has a README, and
  `banking-api-contract` describes the whole API (L171-L173).
- Transactions are not categorised. Categorisation can be part of the solution (L135-L137).
- Apertus comes as four models through the Keera gateway: 70B and 8B, each with a thinking variant (L113-L115).

During the demo the example TrustRoom showed figures that the presenters could not vouch for. Making sure the
numbers are right is the core of the challenge (L153-L155).

## Q&A answers

- **Web search (Tavily, Google).** Allowed for general information, such as details about the company behind a
  booking. Not allowed if the query contains the customer's data, such as their name (L109-L113).
- **Third pillar.** The TrustRoom may set up a standing order to the third pillar provider, sum up what the
  customer paid in this year, and analyse an uploaded statement from the provider. It must not recommend a
  provider, or say how an extra 100 CHF would change the customer's taxes. Advice in general is out (L115-L121).
- **Fine-tuning Apertus or LoRA adapters.** Allowed in principle, as long as the banking API stays unchanged.
  ti&m is more interested in customer use cases than in model work, so mix both and treat it as a business
  problem first (L187-L193).
- **Scope.** A team does not have to build the whole TrustRoom. Focusing on one part, such as personalised
  charts or data analysis, is fine as long as it serves the main goal (L181-L183).

## Where the workshop and challenge_description.md disagree

- **History length.** The workshop said 24 months of data (L85) and later three years (L133).
  challenge_description.md says 36 months of booked transactions.
- **Judging.** The workshop named the four criteria without weights and called the third "software
  architecture". challenge_description.md names it "technical rigour and sovereign architecture" and weights
  the criteria 30 %, 30 %, 20 % and 20 %.
