# Judge rubric (shared by the LLM judge and human calibration labels)

Judge version `j1` (`scifact_rag/judge.py`). Human labels must follow the same
definitions, so judge–human agreement measures the judge, not a different task.

## 1. Faithfulness (answers that are not NOT_FOUND)

Read only the abstracts the answer **cites**. Label each sentence:

| Label | Meaning |
| --- | --- |
| SUPPORTED | Everything the sentence states is stated in, or directly follows from, the cited abstracts. A sentence that only says what the abstracts do not cover is SUPPORTED if that is accurate. |
| PARTIAL | Part is supported, but it adds or overstates something the abstracts do not state (e.g. "proves" for "is associated with", a wrong number, a different population). |
| NOT_SUPPORTED | The cited abstracts do not state it, or contradict it. |

The answer is **faithful** only if every sentence is SUPPORTED. Do not use
your own biomedical knowledge; a true statement that the cited abstracts do
not state is still NOT_SUPPORTED.

## 2. Abstention (NOT_FOUND answers)

Read **all** retrieved abstracts. Does at least one report a finding about the
specific entities and relationship in the claim, supporting or contradicting
it, even partly?

- **No** → the abstention is **justified**.
- **Yes** → the abstention is **not justified** (the model should have answered).

Related topics alone (same gene, different outcome; same disease, different
drug) do not count as information about the claim.

## Calibration protocol

- Items come from **validation** claims only (seeded sample), never the test set.
- The human labels each item before seeing the judge's label.
- Reported: agreement (count / items) and Cohen's kappa, separately for
  faithfulness (answer level) and abstention.
- The judge rubric is frozen before the test-set run. If agreement is poor, the
  rubric or judge may be revised once on validation; the revision and both
  agreement figures are reported.
