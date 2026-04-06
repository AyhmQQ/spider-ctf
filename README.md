# Spider

**Spider** is an intelligent crypto challenge analyzer built for CTF players.

Instead of forcing users to manually inspect files, guess challenge types, search for cipher patterns, and test random solvers, Spider is designed to analyze the whole challenge bundle, extract useful signals, classify likely cryptographic structures, and suggest or attempt the most relevant solving paths.

Spider is built around a simple idea:

> Give it the files of the challenge, and let it figure out where to start.

## Why Spider?

In many crypto CTF challenges, players do not receive a clean ciphertext only.  
They often get a mix of files such as:

- `challenge.py`
- `output.txt`
- `hint.txt`
- `cipher.enc`
- `pubkey.pem`

The problem is not only solving the challenge.  
The real problem is understanding:

- what type of challenge this is
- what data matters
- which file contains the useful clue
- whether the challenge is RSA, XOR, encoding-based, or multi-layered
- what attack path should be tried first

Spider is being built to solve that exact problem.

## Core Goals

Spider aims to provide:

- multi-file challenge analysis
- safe static inspection of challenge source files
- text, binary, key, and structured file classification
- cross-file correlation and context building
- guided crypto challenge triage
- smarter flag detection using expected flag formats
- future support for advanced RSA-focused analysis and attack selection

## What makes Spider different?

Spider is not meant to be just another script that brute-forces a few encodings.

It is being designed as a structured analysis framework that:

- accepts full challenge bundles
- extracts values and hints from multiple files
- avoids dangerous direct execution of challenge scripts
- explains why a challenge is likely RSA, XOR, encoding-based, or something else
- ranks possible solving directions instead of blindly guessing

## Safety First

Spider does **not** execute uploaded challenge scripts by default.

This is an important design decision to avoid:

- infinite loops
- memory abuse
- subprocess spawning
- malicious code execution
- network activity
- unsafe file system operations

The first versions of Spider focus on **safe static analysis**.

## Planned Input Support

Spider is being designed to handle common crypto CTF challenge inputs such as:

- `.txt`
- `.py`
- `.enc`
- `.pem`
- `.json`
- `.bin`

And to support:

- single file analysis
- multi-file bundle analysis
- full challenge folder inspection

## Expected Flag Format Support

Spider will support user-defined expected flag formats such as:

- `BRKCYS{}`
- `flag{}`
- `HTB{}`
- `picoCTF{}`

This helps improve:

- result scoring
- candidate ranking
- flag detection
- false positive reduction

## Version 1 Roadmap

### Phase 1
- project structure
- safe ingestion system
- file classification
- multi-file bundle loading
- file preview and summary reporting

### Phase 2
- static Python analysis
- extraction of key values and hints
- cross-file aggregation
- challenge context building

### Phase 3
- crypto family detection
- RSA-oriented context detection
- guided attack suggestions
- smarter scoring and flag pattern matching

## Project Status

Spider is currently in active development.

The initial goal is to build a strong and safe foundation for challenge ingestion, file analysis, and challenge classification before moving into deeper automated solving features.

## Vision

Spider is being built to help CTF players spend less time being lost and more time thinking clearly.

It should not only help solve challenges.  
It should help players understand them.

---

Built for CTF players who want a smarter way to inspect and break crypto challenges.
