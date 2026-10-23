# Prompting Styles for Language Models

This README introduces three common prompting styles used with large language models (LLMs):

1. **ChatML prompting**
2. **Alpaca prompting**
3. **INS (Instruction-style) prompting**

It explains each format, shows examples, and compares when to use them.

> **Note on terminology:** ChatML and Alpaca refer to recognizable prompt formats. “INS” is not one universally standardized format; in this README, it means a simple instruction-based format with clearly labeled instruction, optional input, and response sections.

---

## 1. ChatML Prompting

ChatML represents a conversation using explicit message-boundary and control tokens. It is useful for structuring messages by speaker and separating system instructions, user input, and assistant responses.

### General structure

```text
<|im_start|>system
You are a helpful assistant.
<|im_end|>
<|im_start|>user
Explain machine learning in simple terms.
<|im_end|>
<|im_start|>assistant
Machine learning is a way for computers to learn patterns from examples...
<|im_end|>
```

### Common tokens

- ` <|im_start|> ` — begins a message.
- ` <|im_sep|> ` — separates a header from its body.
- ` <|im_end|> ` — ends a message.
- ` <|im_start|>assistant` — identifies an assistant message.
- ` <|im_start|>assistant` with a tool or channel header may be used in more advanced conversation formats.

Exact token handling depends on the model and tokenizer. The visible spellings above represent special tokens in systems that support ChatML; they are not necessarily interpreted as special tokens by every model.

### Example: role-based conversation

```text
<|im_start|>system
You are a concise Python tutor. Explain concepts clearly and include a short example.
<|im_end|>
<|im_start|>user
What is a Python list?
<|im_end|>
<|im_start|>assistant
A Python list is an ordered collection that can hold multiple items.

Example:
numbers = [1, 2, 3]
print(numbers[0])  # 1
<|im_end|>
```

### When to use ChatML

- Multi-turn conversations
- Separating system, user, assistant, and tool messages
- Chat-model training or inference pipelines that expect ChatML
- Applications that need explicit message boundaries

---

## 2. Alpaca Prompting

Alpaca-style prompting is associated with an instruction-following dataset format. It commonly uses the labels `Instruction`, `Input`, and `Response`.

### General structure

```text
Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
Summarize the benefits of exercise.

### Input:
Write for a general audience in three bullet points.

### Response:
- Exercise supports cardiovascular and muscular health.
- It can improve mood and help manage stress.
- Regular activity can support sleep and overall well-being.
```

The `Input` section is optional when the instruction contains all necessary information.

### Example without an input section

```text
Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
Translate "Good morning" into Spanish.

### Response:
Buenos días.
```

### Example with an input section

```text
Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
Rewrite the text to sound more professional.

### Input:
hey, i can't come to the meeting today. can we do it tomorrow?

### Response:
Hello, I’m unable to attend today’s meeting. Would it be possible to reschedule for tomorrow?
```

### When to use Alpaca prompting

- Instruction-following datasets
- Fine-tuning or evaluating models trained on Alpaca-style examples
- Simple task-and-input templates
- Tasks such as summarization, rewriting, classification, and translation

---

## 3. INS / Instruction-Style Prompting

In this README, **INS** means a straightforward instruction-style prompt. Unlike a strict token format, it is a general template: state the task clearly, provide any context or input, and specify the desired output.

### General structure

```text
Instruction: [What the model should do]

Context (optional): [Relevant background information]

Input: [Text or data to work on]

Output requirements: [Format, tone, length, or constraints]

Response:
```

### Example: summarization

```text
Instruction:
Summarize the text.

Input:
Large language models generate text by learning patterns from large collections
of training data. They can assist with writing, coding, analysis, and other tasks.

Output requirements:
- Use plain English.
- Keep the summary to two sentences.
- Do not add claims that are absent from the input.

Response:
Large language models learn patterns from training data to generate text.
They can help with writing, coding, analysis, and many other tasks.
```

### Example: structured output

```text
Instruction:
Extract the key details from the supplied text.

Input:
The workshop will take place in Room 204 on 12 November at 10:30 AM.

Output requirements:
Return the result using these fields:
- Event
- Date
- Time
- Location

Response:
Event: Workshop
Date: 12 November
Time: 10:30 AM
Location: Room 204
```

### When to use instruction-style prompting

- General-purpose prompts
- Tasks that need clear constraints or output formats
- Prototyping prompts before adopting a model-specific template
- Applications where readability and ease of editing matter

---

## Comparison

| Feature | ChatML | Alpaca | INS / Instruction-style |
|---|---|---|---|
| Main purpose | Structure conversational messages | Structure instruction-following examples | State a task and its requirements clearly |
| Typical labels/tokens | Message boundary and role tokens | `Instruction`, optional `Input`, `Response` | Flexible labels such as `Instruction`, `Context`, `Input`, `Output requirements` |
| Best suited for | Chat and multi-turn interactions | Instruction datasets and compatible fine-tuning setups | General prompting and task templates |
| Strict format? | Yes, when required by the target model | A recognizable template, but model-dependent | No single universal standard |
| Model compatibility | Requires a model/system that supports the format | Depends on the model's training and prompt template | Broad, but results still depend on model behavior |

---

## Best Practices

1. **Be specific.** Say what the model should do instead of giving a vague request.
2. **Provide context.** Include only information relevant to the task.
3. **Define the output.** Specify format, length, tone, or required fields when these matter.
4. **Use examples when helpful.** One or two examples can demonstrate the expected pattern.
5. **Separate instructions from input.** This makes prompts easier to read and maintain.
6. **Match the model's expected format.** A model may require a particular chat template or special tokens; using a different format can reduce performance.
7. **Test prompts.** Compare outputs on representative examples and revise based on observed results.

## Quick Templates

### ChatML

```text
<|im_start|>system
[Role and behavior instructions]
<|im_end|>
<|im_start|>user
[User request]
<|im_end|>
<|im_start|>assistant
```

### Alpaca

```text
### Instruction:
[Task]

### Input:
[Optional context or data]

### Response:
```

### INS / Instruction-style

```text
Instruction: [Task]
Context: [Optional context]
Input: [Data to process]
Output requirements: [Desired format and constraints]
Response:
```

## Final Notes

Prompt formatting is not a guarantee of better results on its own. The best format is the one expected by the target model and application. In particular, use ChatML special tokens only where supported, and treat Alpaca and INS-style labels as plain text unless the model's prompt template specifies otherwise.
