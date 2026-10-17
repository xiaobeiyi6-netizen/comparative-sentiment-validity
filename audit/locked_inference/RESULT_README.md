# New version-pinned inference comparison

Model commit: `3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7`. Historical model revision remains unavailable.

Both source corpora and archived prediction inputs passed exact-byte and row-alignment checks. This run re-executed VADER and RoBERTa on both primary analysis corpora. No new human labels or posts were collected.

- Airline / VADER: binary label changes 0/14640; strict reversals 3/15 archived and 3/15 new; changed reversal-pair identities 0; maximum group share change 0.000000 pp.
- Airline / RoBERTa: binary label changes 0/14640; strict reversals 0/15 archived and 0/15 new; changed reversal-pair identities 0; maximum group share change 0.000000 pp.
- GOP / VADER: binary label changes 0/4483; strict reversals 7/45 archived and 7/45 new; changed reversal-pair identities 0; maximum group share change 0.000000 pp.
- GOP / RoBERTa: binary label changes 0/4483; strict reversals 7/45 archived and 7/45 new; changed reversal-pair identities 0; maximum group share change 0.000000 pp.

Budget and supplementary-corpus analyses have not been rerun by this notebook. If predictions differ, downstream analyses must be reassessed before updating the paper.

The summary folder contains aggregates and runtime/model provenance. The private_row_outputs folder contains individual prediction records and must not be placed in the public repository. No model weights, original tweet text or account fields are bundled in this result archive.
