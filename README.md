![CatagoreMail](https://github.com/user-attachments/assets/d6370ced-58fc-4b6b-a2c1-3725ecde164a)

# CatagoreMail

**An inbox triage model trained on *your* behaviour — not on a generic notion of what "important" means.**

Every email client has an importance filter, and they are all trained on somebody else's inbox. What counts as urgent is personal: the newsletter you actually read, the automated alert you have never once opened. CatagoreMail learns that boundary from the only signal that actually encodes it — which emails **you** have opened and which you have not.

It pulls your last 5,000 read and unread messages, fine-tunes DistilBERT on that split, and uses the result to predict whether a new email is worth surfacing. **88% accuracy** on the held-out test set.

📺 **[Demo](https://www.youtube.com/watch?v=rVbf_sLMUyM)**

---

## Architecture

```
Next.js  ──►  Clerk auth  ──►  Gmail API  ──►  Flask  ──►  DistilBERT
front-end     validated       last 5,000     training     read/unread
              identity        messages       + inference  classifier
```

The read/unread split is what makes this work: it is a large, already-labelled, continuously-updating dataset that every user carries around without having to annotate anything.

**Stack** — Next.js + TypeScript front-end, Flask back-end, Google Cloud project for Gmail API access, Clerk for authentication, Hugging Face `Trainer` for fine-tuning.

Clerk is load-bearing rather than decorative: identity has to be verified before any Gmail API call is made on a user's behalf, since the whole system is built around reading a real mailbox.

## Running

1. Set up Clerk authentication
2. Set up a Google Cloud project with the Gmail API enabled
3. Download the credentials JSON

```bash
git clone https://github.com/ShrishChou/CatagoreMail.git
cd CatagoreMail
npm install
npm run dev            # front-end
python3 server.py      # back-end
```
