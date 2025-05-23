from typing import Tuple, List
from groq import Groq

class LanguageConverter:
    """Handles cross-language code conversion"""
    
    def __init__(self):
        self.client = Groq()
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"
        
        # Language mappings and syntax patterns
        self.language_mappings = {
            "python": {
                "extension": ".py",
                "comment": "#",
                "features": ["dynamic_typing", "indentation", "list_comprehension"]
            },
            "javascript": {
                "extension": ".js", 
                "comment": "//",
                "features": ["dynamic_typing", "prototypes", "async_await"]
            },
            "cpp": {
                "extension": ".cpp",
                "comment": "//",
                "features": ["static_typing", "pointers", "templates"]
            },
            "java": {
                "extension": ".java",
                "comment": "//", 
                "features": ["static_typing", "oop", "garbage_collection"]
            }
        }
    
    def convert_language(self, code: str, source_lang: str, target_lang: str) -> Tuple[str, List[str]]:
        """Convert code from source language to target language"""
        notes = []
        
        # Validate languages
        if source_lang.lower() not in self.language_mappings:
            raise ValueError(f"Unsupported source language: {source_lang}")
        if target_lang.lower() not in self.language_mappings:
            raise ValueError(f"Unsupported target language: {target_lang}")
        
        # Apply specific conversion rules
        if source_lang.lower() == "python" and target_lang.lower() == "javascript":
            return self._python_to_javascript(code, notes)
        elif source_lang.lower() == "python" and target_lang.lower() == "cpp":
            return self._python_to_cpp(code, notes)
        elif source_lang.lower() == "python" and target_lang.lower() == "java":
            return self._python_to_java(code, notes)
        elif source_lang.lower() == "javascript" and target_lang.lower() == "python":
            return self._javascript_to_python(code, notes)
        else:
            # Use AI for other conversions
            return self._ai_convert(code, source_lang, target_lang, notes)
    
    def _python_to_javascript(self, code: str, notes: List[str]) -> Tuple[str, List[str]]:
        """Convert Python code to JavaScript"""
        # Basic rule-based conversion
        js_code = code
        
        # Replace Python print with JavaScript console.log
        js_code = js_code.replace("print(", "console.log(")
        
        # Replace Python def with JavaScript function
        js_code = js_code.replace("def ", "function ")
        
        # Add semicolons and braces (simplified)
        lines = js_code.split('\n')
        converted_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.endswith(':'):
                # Convert Python : to JavaScript {
                converted_lines.append(line.replace(':', ' {'))
            elif stripped and not stripped.startswith('#') and not stripped.startswith('//'):
                # Add semicolon if not present
                if not stripped.endswith(('{', '}', ';')) and stripped:
                    converted_lines.append(line + ';')
                else:
                    converted_lines.append(line)
            else:
                converted_lines.append(line)
        
        js_code = '\n'.join(converted_lines)
        
        # Use AI for more complex conversion
        return self._ai_convert_with_base(js_code, "python", "javascript", notes)
    
    def _python_to_cpp(self, code: str, notes: List[str]) -> Tuple[str, List[str]]:
        """Convert Python code to C++"""
        notes.append("C++ requires explicit type declarations")
        notes.append("Memory management may need to be handled manually")
        notes.append("Added necessary #include statements")
        
        return self._ai_convert(code, "python", "cpp", notes)
    
    def _python_to_java(self, code: str, notes: List[str]) -> Tuple[str, List[str]]:
        """Convert Python code to Java"""
        notes.append("Java requires class structure and public static void main")
        notes.append("Variable types need to be explicitly declared")
        notes.append("Python's dynamic features may not translate directly")
        
        return self._ai_convert(code, "python", "java", notes)
    
    def _javascript_to_python(self, code: str, notes: List[str]) -> Tuple[str, List[str]]:
        """Convert JavaScript code to Python"""
        # Basic rule-based conversion
        py_code = code
        
        # Replace JavaScript console.log with Python print
        py_code = py_code.replace("console.log(", "print(")
        
        # Replace function with def
        py_code = py_code.replace("function ", "def ")
        
        # Remove semicolons and convert braces to colons
        lines = py_code.split('\n')
        converted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Handle closing braces
            if stripped == '}':
                indent_level = max(0, indent_level - 1)
                continue
            
            # Handle opening braces
            if stripped.endswith(' {'):
                line = line.replace(' {', ':')
                converted_lines.append(line)
                indent_level += 1
                continue
            
            # Remove semicolons
            if stripped.endswith(';'):
                line = line[:-1]
            
            # Apply Python indentation
            if stripped and not stripped.startswith('#') and not stripped.startswith('//'):
                indented_line = '    ' * indent_level + stripped
                converted_lines.append(indented_line)
            else:
                converted_lines.append(line)
        
        py_code = '\n'.join(converted_lines)
        
        # Use AI for more complex conversion
        return self._ai_convert_with_base(py_code, "javascript", "python", notes)
    
    def _ai_convert(self, code: str, source_lang: str, target_lang: str, notes: List[str]) -> Tuple[str, List[str]]:
        """Use AI to convert code between languages"""
        prompt = f"""
        Convert this {source_lang} code to {target_lang}:
        
        ```{source_lang}
        {code}
        ```
        
        Return a JSON object with:
        - "converted_code": the equivalent code in {target_lang}
        - "conversion_notes": list of important notes about the conversion
        - "language_differences": key differences to be aware of
        
        Make sure the converted code:
        1. Maintains the same functionality
        2. Follows {target_lang} best practices and conventions
        3. Includes proper syntax and structure
        4. Has appropriate type declarations if needed
        5. Includes necessary imports/includes
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Lower temperature for more consistent conversions
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            notes.extend(result.get("conversion_notes", []))
            notes.extend(result.get("language_differences", []))
            
            return result.get("converted_code", code), notes
            
        except Exception as e:
            notes.append(f"AI conversion failed: {str(e)}")
            return code, notes
    
    def _ai_convert_with_base(self, base_code: str, source_lang: str, target_lang: str, notes: List[str]) -> Tuple[str, List[str]]:
        """Use AI to improve an already partially converted code"""
        prompt = f"""
        Improve this partially converted {source_lang} to {target_lang} code:
        
        ```{target_lang}
        {base_code}
        ```
        
        Return a JSON object with:
        - "improved_code": the properly converted and improved code
        - "improvements": list of improvements made
        - "syntax_fixes": syntax corrections applied
        
        Focus on:
        1. Fixing any syntax errors
        2. Following {target_lang} conventions
        3. Proper variable declarations and types
        4. Correct function definitions
        5. Appropriate built-in function usage
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            notes.extend(result.get("improvements", []))
            notes.extend(result.get("syntax_fixes", []))
            
            return result.get("improved_code", base_code), notes
            
        except Exception as e:
            notes.append(f"AI improvement failed: {str(e)}")
            return base_code, notes
    
    def get_conversion_template(self, target_lang: str) -> str:
        """Get a basic template for the target language"""
        templates = {
            "python": """# Python code template
def main():
    # Your code here
    pass

if __name__ == "__main__":
    main()
""",
            "javascript": """// JavaScript code template
function main() {
    // Your code here
}

main();
""",
            "cpp": """#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {
    // Your code here
    return 0;
}
""",
            "java": """public class Main {
    public static void main(String[] args) {
        // Your code here
    }
}
"""
        }
        
        return templates.get(target_lang.lower(), "// Template not available")
    
    def get_language_info(self, language: str) -> dict:
        """Get information about a programming language"""
        return self.language_mappings.get(language.lower(), {
            "extension": ".txt",
            "comment": "//",
            "features": ["unknown"]
        })