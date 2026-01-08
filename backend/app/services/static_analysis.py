import ast
import re
from typing import List, Dict, Any, Literal
from app.models.schemas import ReviewIssue

class StaticAnalyzer:
    """
    Performs lightweight static analysis before sending code to LLM.
    """
    
    @staticmethod
    def analyze(code: str, language: Literal["python", "javascript", "java", "cpp"]) -> List[ReviewIssue]:
        if language == "python":
            return StaticAnalyzer._analyze_python(code)
        elif language == "javascript":
            return StaticAnalyzer._analyze_javascript(code)
        # Add other languages here if needed, or return empty list
        return []

    @staticmethod
    def _analyze_python(code: str) -> List[ReviewIssue]:
        issues = []
        try:
            tree = ast.parse(code)
            
            # Check for generic syntax correctness (implicitly done by parse)
            
            # 1. Check for unused variables (simplistic approach)
            # This is complex in pure AST without symbol table, 
            # so we'll stick to safer checks or just very obvious ones like 'bare except'
            
            for node in ast.walk(tree):
                # Detect bare except
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    issues.append(ReviewIssue(
                        line=node.lineno,
                        severity="warning",
                        explanation="Avoid using bare 'except'. It catches SystemExit and KeyboardInterrupt errors.",
                        suggested_fix="except Exception as e:"
                    ))
                
                # Detect print statements in production code (often leftover)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
                     issues.append(ReviewIssue(
                        line=node.lineno,
                        severity="improvement",
                        explanation="Found 'print' statement. Consider using a logger for production applications.",
                        suggested_fix="logger.info(...)"
                    ))
                    
        except SyntaxError as e:
            issues.append(ReviewIssue(
                line=e.lineno,
                severity="bug",
                explanation=f"Syntax Error: {e.msg}",
                suggested_fix="Fix the syntax error to allow compilation."
            ))
        except Exception as e:
            # Fallback for parser errors
            pass
            
        return issues

    @staticmethod
    def _analyze_javascript(code: str) -> List[ReviewIssue]:
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            line_num = i + 1
            
            # 1. Detect verify 'console.log'
            if 'console.log(' in line:
                 issues.append(ReviewIssue(
                    line=line_num,
                    severity="improvement",
                    explanation="Found 'console.log'. Remove or use a proper logging mechanism for production.",
                    suggested_fix="// console.log(...) or logger.debug(...)"
                ))
            
            # 2. Detect 'var' usage
            # Simple regex that tries to avoid matching inside strings, but it's not perfect.
            # Matches "var x" but not "something_var"
            if re.search(r'\bvar\s+\w+', line):
                 issues.append(ReviewIssue(
                    line=line_num,
                    severity="warning",
                    explanation="Avoid using 'var'. Use 'let' or 'const' for block scoping.",
                    suggested_fix="const variableName = ...;"
                ))
                
            # 3. Detect equality check '=='
            if re.search(r'[^!=]==[^=]', line): # matches == but not === or !==
                 issues.append(ReviewIssue(
                    line=line_num,
                    severity="bug",
                    explanation="Strict equality '===' should be preferred over loose equality '=='.",
                    suggested_fix="Use '==='"
                ))
                
        return issues
