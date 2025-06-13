# TDS Virtual Teaching Assistant (Virtual TA)

## Background

This project is a Virtual Teaching Assistant for the Tools in Data Science (TDS) course at IIT Madras’ Online Degree program. The Virtual TA automatically answers student questions based on:

- Course content for TDS Jan 2025 as of 15 Apr 2025.
- TDS Discourse posts from 1 Jan 2025 to 14 Apr 2025.

The goal is to build an API that can respond to student queries using the above knowledge base.

---

## Data Sourcing

To enable accurate answers, data is extracted from:

- Course content documents.
- Discourse posts within the specified date range.

---

## API

The application exposes a POST API endpoint that accepts student questions and optional base64-encoded file attachments as JSON.

### Example Request

```bash
curl "https://app.example.com/api/" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Should I use gpt-4o-mini which AI proxy supports, or gpt3.5 turbo?\", \"image\": \"$(base64 -w0 project-tds-virtual-ta-q1.webp)\"}"
```

### Example Response

```json
{
  "answer": "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question.",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
      "text": "Use the model that’s mentioned in the question."
    },
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3",
      "text": "My understanding is that you just have to use a tokenizer, similar to what Prof. Anand used, to get the number of tokens and multiply that by the given rate."
    }
  ]
}
```

The response must be sent within 30 seconds.

---

## Evaluation

Sample questions and evaluation parameters are provided for testing. The actual evaluation may include any realistic student question.

To run the evaluation:

- Edit `project-tds-virtual-ta-promptfoo.yaml` to replace `providers[0].config.url` with your API URL.
- Run the evaluation script:

```bash
npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml
```

---

## Deployment

Deploy your application to a public URL accessible by anyone. You may use any platform.

If using ngrok, ensure it runs continuously until you get your results.

---

## Sharing Your Code

- Create a new public GitHub repository.
- Add an MIT LICENSE file.
- Commit and push your code.

---

## Submission

Submit your GitHub repository URL and your API endpoint URL at:

[https://exam.sanand.workers.dev/tds-project-virtual-ta](https://exam.sanand.workers.dev/tds-project-virtual-ta)

---

## Pre-requisites for Evaluation

Your repository MUST meet the following criteria to be eligible for evaluation:

- Publicly accessible GitHub repository.
- LICENSE file with the MIT license in the root folder.

The evaluation uses a modified version of `project-tds-virtual-ta-promptfoo.yaml` with 10 realistic questions. Correct answers are awarded up to 2 marks each.

Your score is the sum of the marks.

---

## Bonus Points

- 1 mark if your GitHub repo includes a script that scrapes Discourse posts across a date range from a Discourse course page like TDS.
- 2 marks if your solution is deployed (with minimal modifications) as an official solution for students to use.

---

## Contact

For any questions or issues, please contact the course instructors or teaching assistants.
