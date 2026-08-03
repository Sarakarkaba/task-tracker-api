# My Personal AI Coding Playbook

AI is my drafting and thinking partner, not the person responsible for the result. I use it to expose edge cases and turn a clear requirement into a small first draft. I keep ownership of the scope, evidence, and final decision.

## My decision card

| When I am... | I reach for... | My rule |
|---|---|---|
| Planning a new feature | **ChatGPT first** | I ask for user stories and acceptance criteria before code. In Module 1, that helped me make due dates optional, exclude completed tasks from overdue results, and choose AND logic for combined filters. |
| Implementing a feature | **ChatGPT in small loops** | I limit each prompt to one feature, layer, or file. In Modules 2 and 3, separating backend and frontend work made the Due Dates and Search changes easier to understand and test. |
| Reviewing code or repository-wide work | **Codex app in read-only mode first** | I give it structured repository context and ask for evidence by file. The architecture comparison showed me that broad context gave better coverage, while targeted context was more precise for a single request flow. |
| Debugging | **The failing test or browser behavior first, then AI** | I reproduce the problem before asking for a diagnosis. My break tests proved that the suite caught dropped due dates and weakened date validation. |
| Working on CI, Docker, or infrastructure | **Codex app for repository context** | Module 4 taught me to inspect generated configuration: CI needed an import-path fix, and I reviewed the Docker stages, non-root user, health check, and command. |
| Doing a security or governance review | **Codex app for a read-only first pass** | I treat every finding as a claim to grade, not an automatic fix. In Module 5, I kept only evidence-backed findings, separated course-scope decisions from defects, and did not turn the review into application changes. |

I briefly tried Claude during planning, but ChatGPT followed my constraints more consistently, so it became my main drafting tool. I choose a tool because its working style fits the risk and size of the task, not because the experience feels smooth.

## When I do not reach for AI

I do not start with AI when I have not reproduced a bug, cannot describe the expected behavior, or may be handling secrets or real personal data. I first inspect the code, run the smallest relevant check, and remove anything the model does not need. I also avoid broad requests when a focused edit will do. The proposed backend `overdue` filter, database migrations, extra endpoints, frameworks, and date libraries all sounded reasonable but did not fit this project.

## My non-negotiables

- I never paste credentials, environment values, private URLs, personal data, or unidentified external data. Module 5 showed me that even stack traces can expose local paths, so I sanitize them and use made-up data when possible.
- I inspect the diff and understand the important lines before accepting them. Early mixed backend/frontend prompts taught me that a large plausible change is harder to review safely.
- I protect the requested scope. I rejected AI suggestions for migrations, extra endpoints, frameworks, and libraries because the existing in-memory, vanilla-JavaScript architecture already fit the assignment.
- I record meaningful AI contributions and how I verified them. My governance worksheet now separates generated work, my understanding, and my evidence.

## My review rules

The verification must match the change. For backend work, I run focused tests and then the full suite. For frontend work, I check real browser interactions and states that could regress, including drag-and-drop, empty columns, filters, and editing. For CI and Docker, I inspect triggers, permissions, commands, runtime user, and health behavior. For documentation or security claims, I trace them to files I inspected and label anything unverified.

My review is allowed to change the answer. I rejected "No due date" text on every card, kept overdue filtering in the browser, removed searches over task IDs, required exact assignee matching, and added a Clear action. Review is not a final polish step; it is where I make the work mine.

## What I am still figuring out

I am still learning when a small editor assistant would be faster than a longer ChatGPT or Codex thread, and how much context is enough without making the task too broad. In 30 days, I will check which tool I actually used, whether I kept changes reviewable, and whether my verification caught real mistakes. I will revise this playbook from that evidence.

## Decision Card

AI can generate, explain, and review; I inspect, verify, reject, revise, and own the final result.
