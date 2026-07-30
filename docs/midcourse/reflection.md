# Project Reflection

## AI Tools I Used
I briefly compared ChatGPT and Claude during the planning stage. I chose ChatGPT for most of the project because it followed my constraints more consistently and worked well with the small, iterative workflow used in this course. I used it to draft user stories and acceptance criteria, plan backend and frontend changes, generate focused code and pytest tests, troubleshoot errors, and improve project documentation. Claude was used only during early exploration.

## One Moment AI Helped
AI was especially useful when identifying test cases for the Due Dates and Overdue Filter and Search and Combined Filters features. It suggested edge cases I had not initially considered, including preserving a due date during an unrelated partial update, treating whitespace-only search text correctly, and ensuring completed tasks are not marked overdue. These suggestions helped the test suite grow from 23 baseline tests to 27 after Feature 1 and 36 after Feature 2.

## One Moment AI Slowed Me Down
Some early prompts caused AI to propose large backend and frontend changes at the same time. The output was harder to review and increased the chance of regressions. I corrected the workflow by rewriting prompts to cover one feature, layer, or file at a time. After each small change, I inspected the diff and ran the relevant tests or browser checks before continuing.

## How My Review Changed the Result
My review changed the implementation when AI proposed a backend `overdue` filter. I rejected it as outside the intended scope and kept overdue filtering in the browser, while the backend supports search, status, priority, assignee, and due-date filters. I also rejected displaying “No due date” on every card and confirmed that combined backend filters use AND logic. Finally, I ran the application, checked API behavior, performed browser checks, and used controlled Break Tests to verify that important tests failed when expected. This review kept the design small and ensured the final result matched the requirements rather than AI assumptions.

## Conclusion
Overall, AI made planning, coding, testing, and documentation faster, but careful review remained essential. Working in small loops helped me catch incorrect assumptions early and understand every change before accepting it. The project showed me that AI works best as a collaborative assistant: it can suggest and draft solutions, while I remain responsible for scope, correctness, verification, and the final decisions.
