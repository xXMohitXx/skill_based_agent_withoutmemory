---
name: math
description: Perform mathematical calculations, percentages, and unit conversions. Use when the user asks to calculate, compute, or convert numbers, temperatures, or other measurable quantities.
---

# Math Skill

## When to use this skill

Use this skill when the user:
- Asks for calculations ("what is 25 * 47", "calculate 150 / 3")
- Asks for percentages ("what's 15% of 200", "calculate tip")
- Asks for conversions ("convert 100°F to Celsius", "32°C in Fahrenheit")
- Uses math words (plus, minus, times, divided by, multiply, add, subtract)
- Asks "how much" with numbers

## Supported operations

### Basic arithmetic
- Addition: +, plus, add
- Subtraction: -, minus, subtract
- Multiplication: *, ×, times, multiply
- Division: /, ÷, divided by

### Percentages
- Calculate percentage of a number
- Calculate what percentage A is of B
- Calculate percentage increase/decrease

### Temperature conversion
- Celsius to Fahrenheit: °F = (°C × 9/5) + 32
- Fahrenheit to Celsius: °C = (°F - 32) × 5/9

### Other
- Square roots
- Powers/exponents
- Basic statistics (average, sum)

## Response format

Show:
1. The calculation being performed
2. The result
3. Human-friendly explanation if helpful

```
🔢 25 × 47 = 1,175
```

```
📊 15% of 200 = 30
(200 × 0.15 = 30)
```

```
🌡️ 100°F = 37.78°C
```

## Examples

**User**: "what's 25 times 47"
**Response**: "🔢 25 × 47 = **1,175**"

**User**: "calculate 15% of 200"
**Response**: "📊 15% of 200 = **30**
(200 × 0.15 = 30)"

**User**: "how much is 500 plus 350"
**Response**: "🔢 500 + 350 = **850**"

**User**: "convert 100 fahrenheit to celsius"
**Response**: "🌡️ 100°F = **37.78°C**
Formula: (100 - 32) × 5/9 = 37.78"

**User**: "what's the square root of 144"
**Response**: "🔢 √144 = **12**"

**User**: "if I tip 20% on a $45 bill, how much is that?"
**Response**: "💵 20% of $45 = **$9.00**
Total with tip: $54.00"

## Edge cases

- Division by zero: "Cannot divide by zero!"
- Invalid expression: "I couldn't understand that calculation. Could you rephrase it?"
- Very large numbers: Format with commas for readability
