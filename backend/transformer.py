import ast
import re
from typing import Tuple, List
from groq import Groq

class CodeTransformer:
    """Handles code optimization and transformation using AST analysis and AI"""
    
    def __init__(self):
        self.client = Groq()
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"
    
    def optimize_code(self, code: str, language: str) -> Tuple[str, List[str]]:
        """Optimize code for performance and readability"""
        suggestions = []
        
        if language.lower() == "python":
            # Apply Python-specific optimizations
            optimized_code = self._optimize_python(code, suggestions)
        else:
            # Use AI for other languages
            optimized_code = self._ai_optimize(code, language, suggestions)
        
        return optimized_code, suggestions
    
    def transform_code(self, code: str, language: str) -> Tuple[str, List[str]]:
        """Apply general code transformations (DRY, clean structure)"""
        suggestions = []
        
        if language.lower() == "python":
            transformed_code = self._transform_python(code, suggestions)
        else:
            transformed_code = self._ai_transform(code, language, suggestions)
        
        return transformed_code, suggestions
    
    def _optimize_python(self, code: str, suggestions: List[str]) -> str:
        """Apply Python-specific optimizations"""
        try:
            # Parse the code to AST
            tree = ast.parse(code)
            
            # Apply rule-based optimizations
            optimized_code = code
            
            # 1. Replace range(len()) with enumerate
            if "range(len(" in code:
                optimized_code = self._fix_range_len(optimized_code)
                suggestions.append("Replaced range(len()) with enumerate for better performance")
            
            # 2. Convert simple loops to list comprehensions
            optimized_code = self._convert_to_comprehensions(optimized_code, suggestions)
            
            # 3. Use AI for complex optimizations
            optimized_code = self._ai_optimize_python(optimized_code, suggestions)
            
            return optimized_code
            
        except SyntaxError:
            # If code can't be parsed, use AI fallback
            return self._ai_optimize(code, "python", suggestions)
    
    def _transform_python(self, code: str, suggestions: List[str]) -> str:
        """Apply Python transformations for cleaner code"""
        try:
            transformed_code = code
            
            # 1. Remove duplicate code patterns
            transformed_code = self._remove_duplicates(transformed_code, suggestions)
            
            # 2. Apply DRY principle
            transformed_code = self._apply_dry_principle(transformed_code, suggestions)
            
            # 3. Use AI for advanced transformations
            transformed_code = self._ai_transform_python(transformed_code, suggestions)
            
            return transformed_code
            
        except Exception:
            return self._ai_transform(code, "python", suggestions)
    
    def _fix_range_len(self, code: str) -> str:
        """Replace range(len()) patterns with enumerate"""
        pattern = r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):'
        replacement = r'for \1, item in enumerate(\2):'
        return re.sub(pattern, replacement, code)
    
    def _convert_to_comprehensions(self, code: str, suggestions: List[str]) -> str:
        """Convert simple loops to list comprehensions"""
        # Simple pattern matching for basic for loops that append to lists
        lines = code.split('\n')
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for pattern: for x in y: result.append(transform(x))
            if (line.startswith('for ') and i + 1 < len(lines) and 
                'append(' in lines[i + 1] and lines[i + 1].strip().count(' ') <= 8):
                
                # Extract components
                for_match = re.match(r'for\s+(\w+)\s+in\s+(.+):', line)
                if for_match and i + 1 < len(lines):
                    var_name = for_match.group(1)
                    iterable = for_match.group(2)
                    next_line = lines[i + 1].strip()
                    
                    append_match = re.match(rf'(\w+)\.append\((.+)\)', next_line)
                    if append_match:
                        list_name = append_match.group(1)
                        expression = append_match.group(2)
                        
                        # Create list comprehension
                        comprehension = f"{list_name} = [{expression} for {var_name} in {iterable}]"
                        new_lines.append(comprehension)
                        suggestions.append(f"Converted loop to list comprehension for better performance")
                        i += 2  # Skip both lines
                        continue
            
            new_lines.append(lines[i])
            i += 1
        
        return '\n'.join(new_lines)
    
    def _remove_duplicates(self, code: str, suggestions: List[str]) -> str:
        """Remove duplicate code patterns"""
        lines = code.split('\n')
        seen_patterns = {}
        
        # Look for repeated function calls or similar patterns
        for i, line in enumerate(lines):
            clean_line = line.strip()
            if len(clean_line) > 10:  # Only check substantial lines
                if clean_line in seen_patterns:
                    suggestions.append(f"Found duplicate code pattern on lines {seen_patterns[clean_line] + 1} and {i + 1}")
                else:
                    seen_patterns[clean_line] = i
        
        return code  # Return unchanged for now, could implement extraction
    
    def _apply_dry_principle(self, code: str, suggestions: List[str]) -> str:
        """Apply Don't Repeat Yourself principle"""
        # Use AI to identify and refactor repeated patterns
        return self._ai_apply_dry(code, suggestions)
    
    def _ai_optimize_python(self, code: str, suggestions: List[str]) -> str:
        """Use AI to optimize Python code"""
        prompt = f"""
        Optimize this Python code for better performance and readability:
        
        ```python
        {code}
        ```
        
        Return a JSON object with:
        - "optimized_code": the improved code
        - "improvements": list of improvements made
        
        Focus on:
        - Performance optimizations
        - Memory efficiency
        - Pythonic patterns
        - Code readability
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            suggestions.extend(result.get("improvements", []))
            return result.get("optimized_code", code)
            
        except Exception as e:
            suggestions.append(f"AI optimization failed: {str(e)}")
            return code
    
    def _ai_transform_python(self, code: str, suggestions: List[str]) -> str:
        """Use AI to transform Python code structure"""
        prompt = f"""
        Transform this Python code to be cleaner and follow best practices:
        
        ```python
        {code}
        ```
        
        Return a JSON object with:
        - "transformed_code": the cleaned code
        - "changes": list of changes made
        
        Focus on:
        - DRY principle (Don't Repeat Yourself)
        - Clean code structure
        - Removing redundancy
        - Better variable names
        - Function extraction
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            suggestions.extend(result.get("changes", []))
            return result.get("transformed_code", code)
            
        except Exception as e:
            suggestions.append(f"AI transformation failed: {str(e)}")
            return code
    
    def _ai_optimize(self, code: str, language: str, suggestions: List[str]) -> str:
        """Use AI to optimize code in any language"""
        prompt = f"""
        Optimize this {language} code for better performance:
        
        ```{language}
        {code}
        ```
        
        Return a JSON object with:
        - "optimized_code": the improved code
        - "improvements": list of improvements made
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            suggestions.extend(result.get("improvements", []))
            return result.get("optimized_code", code)
            
        except Exception as e:
            suggestions.append(f"AI optimization failed: {str(e)}")
            return code
    
    def _ai_transform(self, code: str, language: str, suggestions: List[str]) -> str:
        """Use AI to transform code structure in any language"""
        prompt = f"""
        Transform this {language} code to be cleaner and more maintainable:
        
        ```{language}
        {code}
        ```
        
        Return a JSON object with:
        - "transformed_code": the cleaned code
        - "changes": list of changes made
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            suggestions.extend(result.get("changes", []))
            return result.get("transformed_code", code)
            
        except Exception as e:
            suggestions.append(f"AI transformation failed: {str(e)}")
            return code
    
    def _ai_apply_dry(self, code: str, suggestions: List[str]) -> str:
        """Use AI to apply DRY principle"""
        prompt = f"""
        Refactor this Python code to follow the DRY (Don't Repeat Yourself) principle:
        
        ```python
        {code}
        ```
        
        Return a JSON object with:
        - "refactored_code": the DRY code
        - "extractions": list of functions/methods extracted
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            suggestions.extend(result.get("extractions", []))
            return result.get("refactored_code", code)
            
        except Exception as e:
            suggestions.append(f"DRY refactoring failed: {str(e)}")
            return code