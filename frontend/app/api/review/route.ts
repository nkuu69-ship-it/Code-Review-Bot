import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { code, language } = await request.json()

    if (!code || !language) {
      return NextResponse.json({ error: "Code and language are required" }, { status: 400 })
    }

    // Mock response for demonstration
    // In production, this would call an actual AI service
    const mockIssues = [
      {
        line: 2,
        severity: "Improvement",
        explanation: "Consider initializing the total variable inline for better readability.",
        suggested_fix: 'total = sum(item["price"] for item in items)',
      },
      {
        line: 3,
        severity: "Warning",
        explanation: "Using a for loop for summation is less efficient. Consider using built-in functions.",
        suggested_fix: "Use list comprehension with sum() function",
      },
    ]

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    return NextResponse.json({ issues: mockIssues })
  } catch (error) {
    console.error("Review API error:", error)
    return NextResponse.json({ error: "Failed to review code" }, { status: 500 })
  }
}
