| Version | Correct answers | False refusals | False answers |
|---|---|---|---|
| v1, strict rule | 3 of 5 | 2 | 0 |
| v2, current | 5 of 5 | 0 | 0 |
| v3, 20 tests | 11 of 14 | 3 | 0 |
| v4, 20 tests | 13 of 14 | 1 | 0 |
| v5, k=15 | 13 of 14 | 1 | 0 |
| v6, k=15 + pizza example | 14 of 14 | 0 | 0 |

Note: results can vary 1 test between runs even at temperature 0 (flaky). Shop location was fixed at v5 (retrieval). "Only make cakes" was flaky until v6.

Changed v1 to v2 to v3 to v4 eval baseline: 
- v2: rule 3 allows logical conclusions, plus one worked example.
- v3: first 20-test baseline. 3 false refusals, all retrieval problems.
- v4: top_k raised from 3 to 5. Fixed "extra to change design." Still failing: "only make cakes" (prompt problem now) and "shop located" (retrieval problem).
- v5: top_k raised to 15, so all chunks are sent.Fixed "shop located."
- v6: added Example 2 (a list can answer "only" questions). Fixed "only make cakes."


| Part of your project	| How it works |
| search.py - finds chunks |	Meaning. Embeddings compare what the texts mean, not their words |
| rag.py - writes the answer | Prediction. The AI predicts its reply word by word, guided by your rules and the chunks |
| eval.py - grades the answer |	Keyword. A literal text match with in, which is crude and exact |