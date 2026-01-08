"use client"

import { Editor } from "@monaco-editor/react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Loader2, Wand2 } from "lucide-react"

interface CodeEditorProps {
  code: string
  language: string
  onCodeChange: (code: string) => void
  onLanguageChange: (language: string) => void
  onReview: () => void
  onAutoFix: () => void
  onClear: () => void
  isReviewing: boolean
  isFixing: boolean
}

const LANGUAGES = [
  { value: "python", label: "Python" },
  { value: "javascript", label: "JavaScript" },
  { value: "java", label: "Java" },
  { value: "cpp", label: "C++" },
]

const DEFAULT_CODE: Record<string, string> = {
  python: `def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price']
    return total

# Example usage
items = [{'price': 10}, {'price': 20}]
print(calculate_total(items))`,
  javascript: `function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total = total + items[i].price;
  }
  return total;
}

// Example usage
const items = [{price: 10}, {price: 20}];
console.log(calculateTotal(items));`,
  java: `public class Calculator {
    public static int calculateTotal(int[] items) {
        int total = 0;
        for (int i = 0; i < items.length; i++) {
            total = total + items[i];
        }
        return total;
    }
    
    public static void main(String[] args) {
        int[] items = {10, 20, 30};
        System.out.println(calculateTotal(items));
    }
}`,
  cpp: `#include <iostream>
#include <vector>

int calculateTotal(std::vector<int> items) {
    int total = 0;
    for (int i = 0; i < items.size(); i++) {
        total = total + items[i];
    }
    return total;
}

int main() {
    std::vector<int> items = {10, 20, 30};
    std::cout << calculateTotal(items) << std::endl;
    return 0;
}`,
}

export function CodeEditor({
  code,
  language,
  onCodeChange,
  onLanguageChange,
  onReview,
  onAutoFix,
  onClear,
  isReviewing,
  isFixing,
}: CodeEditorProps) {
  const handleLanguageChange = (newLanguage: string) => {
    onLanguageChange(newLanguage)
    if (!code) {
      onCodeChange(DEFAULT_CODE[newLanguage] || "")
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-card/50">
        <Select value={language} onValueChange={handleLanguageChange}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select language" />
          </SelectTrigger>
          <SelectContent>
            {LANGUAGES.map((lang) => (
              <SelectItem key={lang.value} value={lang.value}>
                {lang.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <div className="flex gap-2">
          <Button variant="outline" onClick={onClear} disabled={isReviewing || isFixing}>
            Clear
          </Button>
          <Button variant="secondary" onClick={onAutoFix} disabled={isReviewing || isFixing || !code.trim()}>
            {isFixing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Fixing...
              </>
            ) : (
              <>
                <Wand2 className="mr-2 h-4 w-4" />
                Auto Fix
              </>
            )}
          </Button>
          <Button onClick={onReview} disabled={isReviewing || !code.trim()}>
            {isReviewing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Reviewing...
              </>
            ) : (
              "Review Code"
            )}
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        <Editor
          height="100%"
          language={language}
          value={code || DEFAULT_CODE[language]}
          onChange={(value) => onCodeChange(value || "")}
          theme="vs-dark"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: "on",
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 2,
            wordWrap: "on",
          }}
        />
      </div>
    </div>
  )
}
