import ast
import re
from typing import List, Dict
from groq import Groq

class CodeExplainer:
    """Generates clear, friendly explanations for code and transformations"""
    
    def __init__(self):
        self.client = Groq()
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"
    
    def explain_code(self, code: str, language: str) -> List[str]:
        """Generate explanations for what the code does"""
        explanations = []
        
        if language.lower() == "python":
            explanations.extend(self._explain_python_code(code))
        
        # Add AI-powered explanation
        ai_explanations = self._ai_explain_code(code, language)
        explanations.extend(ai_explanations)
        
        return explanations
    
    def explain_changes(self, original_code: str, modified_code: str, language: str) -> List[str]:
        """Explain what changes were made and why"""
        if original_code.strip() == modified_code.strip():
            return ["No changes were made to the code."]
        
        return self._ai_explain_changes(original_code, modified_code, language)
    
    def _explain_python_code(self, code: str) -> List[str]:
        """Analyze Python code and provide explanations"""
        explanations = []
        
        try:
            tree = ast.parse(code)
            
            # Analyze the AST for different constructs
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    explanations.append(f"🔧 Function '{node.name}' defined with {len(node.args.args)} parameter(s)")
                
                elif isinstance(node, ast.For):
                    if isinstance(node.target, ast.Name):
                        explanations.append(f"🔄 For loop iterates over data using variable '{node.target.id}'")
                
                elif isinstance(node, ast.While):
                    explanations.append("🔄 While loop continues until condition becomes false")
                
                elif isinstance(node, ast.If):
                    explanations.append("🔀 Conditional statement checks a condition and executes code accordingly")
                
                elif isinstance(node, ast.ListComp):
                    explanations.append("⚡ List comprehension creates a new list efficiently in one line")
                
                elif isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                    explanations.append(f"📦 Imports modules: {', '.join(modules)}")
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        explanations.append(f"📦 Imports specific items from {node.module}")
        
        except SyntaxError:
            explanations.append("⚠️ Code has syntax errors that prevent detailed analysis")
        
        # Check for common patterns
        if "range(len(" in code:
            explanations.append("🐌 Found range(len()) pattern - consider using enumerate() for better performance")
        
        if code.count("for ") > 1 and "append(" in code:
            explanations.append("💡 Multiple loops with append() - might benefit from list comprehensions")
        
        if "import" not in code and any(func in code for func in ["print", "len", "range"]):
            explanations.append("✅ Uses built-in Python functions without imports")
        
        return explanations
    
    def _ai_explain_code(self, code: str, language: str) -> List[str]:
        """Use AI to explain what the code does"""
        prompt = f"""
        Explain this {language} code in simple, friendly terms:
        
        ```{language}
        {code}
        ```
        
        Return a JSON object with:
        - "explanations": list of clear explanations about what the code does
        - "purpose": overall purpose of the code
        - "key_concepts": important programming concepts used
        
        Make explanations:
        1. Simple and easy to understand
        2. Friendly and encouraging
        3. Focus on WHAT the code does, not just HOW
        4. Include emojis to make it more engaging
        5. Explain any complex logic step by step
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            explanations = result.get("explanations", [])
            
            if result.get("purpose"):
                explanations.insert(0, f"🎯 Purpose: {result['purpose']}")
            
            if result.get("key_concepts"):
                explanations.append(f"📚 Key concepts: {', '.join(result['key_concepts'])}")
            
            return explanations
            
        except Exception as e:
            return [f"⚠️ Could not generate AI explanation: {str(e)}"]
    
    def _ai_explain_changes(self, original: str, modified: str, language: str) -> List[str]:
        """Use AI to explain what changes were made"""
        prompt = f"""
        Compare these two {language} code versions and explain the changes:
        
        Original:
        ```{language}
        {original}
        ```
        
        Modified:
        ```{language}
        {modified}
        ```
        
        Return a JSON object with:
        - "changes": list of specific changes made
        - "benefits": why these changes improve the code
        - "impact": how these changes affect performance or readability
        
        Make explanations:
        1. Clear and specific about what changed
        2. Explain the benefits in simple terms
        3. Use friendly, encouraging language
        4. Include emojis for engagement
        5. Focus on improvements and learning
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
            explanations = []
            
            # Add changes
            changes = result.get("changes", [])
            for change in changes:
                explanations.append(f"🔄 {change}")
            
            # Add benefits
            benefits = result.get("benefits", [])
            for benefit in benefits:
                explanations.append(f"✅ {benefit}")
            
            # Add impact
            impact = result.get("impact", [])
            for imp in impact:
                explanations.append(f"📈 {imp}")
            
            return explanations
            
        except Exception as e:
            return [f"⚠️ Could not explain changes: {str(e)}"]
    
    def get_code_complexity(self, code: str, language: str) -> Dict[str, any]:
        """Analyze code complexity"""
        if language.lower() == "python":
            return self._analyze_python_complexity(code)
        else:
            return self._ai_analyze_complexity(code, language)
    
    def _analyze_python_complexity(self, code: str) -> Dict[str, any]:
        """Analyze Python code complexity"""
        try:
            tree = ast.parse(code)
            
            complexity = {
                "lines": len(code.split('\n')),
                "functions": 0,
                "loops": 0,
                "conditions": 0,
                "imports": 0,
                "complexity_level": "Simple"
            }
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity["functions"] += 1
                elif isinstance(node, (ast.For, ast.While)):
                    complexity["loops"] += 1
                elif isinstance(node, ast.If):
                    complexity["conditions"] += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    complexity["imports"] += 1
            
            # Determine complexity level
            total_constructs = complexity["functions"] + complexity["loops"] + complexity["conditions"]
            if total_constructs > 10:
                complexity["complexity_level"] = "Complex"
            elif total_constructs > 5:
                complexity["complexity_level"] = "Moderate"
            
            return complexity
            
        except SyntaxError:
            return {
                "lines": len(code.split('\n')),
                "error": "Syntax errors prevent analysis",
                "complexity_level": "Unknown"
            }
    
    def _ai_analyze_complexity(self, code: str, language: str) -> Dict[str, any]:
        """Use AI to analyze code complexity"""
        prompt = f"""
        Analyze the complexity of this {language} code:
        
        ```{language}
        {code}
        ```
        
        Return a JSON object with:
        - "complexity_level": "Simple", "Moderate", or "Complex"
        - "analysis": detailed complexity analysis
        - "suggestions": ways to reduce complexity if needed
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_completion_tokens=512,
                response_format={"type": "json_object"}
            )
            
            return eval(completion.choices[0].message.content)
            
        except Exception:
            return {
                "complexity_level": "Unknown",
                "analysis": "Could not analyze complexity",
                "suggestions": []
            }
    
    def generate_learning_tips(self, code: str, language: str) -> List[str]:
        """Generate learning tips based on the code"""
        tips = []
        
        if language.lower() == "python":
            # Python-specific tips
            if "def " in code:
                tips.append("💡 Functions help organize code and make it reusable!")
            
            if "for " in code:
                tips.append("🔄 Loops are powerful for repeating actions - Python makes them very readable!")
            
            if "[" in code and "]" in code and "for" in code:
                tips.append("⚡ List comprehensions are a Pythonic way to create lists efficiently!")
            
            if "import" in code:
                tips.append("📚 Libraries extend Python's capabilities - there's a library for almost everything!")
        
        # Add AI-generated tips
        ai_tips = self._ai_generate_tips(code, language)
        tips.extend(ai_tips)
        
        return tips
    
    def _ai_generate_tips(self, code: str, language: str) -> List[str]:
        """Use AI to generate learning tips"""
        prompt = f"""
        Generate helpful learning tips based on this {language} code:
        
        ```{language}
        {code}
        ```
        
        Return a JSON object with:
        - "tips": list of educational tips and insights
        
        Make tips:
        1. Educational and encouraging
        2. Relevant to concepts in the code
        3. Include best practices
        4. Use emojis for engagement
        5. Suitable for learners
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_completion_tokens=512,
                response_format={"type": "json_object"}
            )
            
            result = eval(completion.choices[0].message.content)
            return result.get("tips", [])
            
        except Exception:
            return ["Keep practicing and experimenting with code! 🚀"]