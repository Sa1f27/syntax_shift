// ===== Application State =====
const AppState = {
    currentTheme: localStorage.getItem('theme') || 'light',
    originalCode: '',
    transformedCode: '',
    currentLanguage: 'python',
    targetLanguage: 'javascript',
    isProcessing: false
};

// ===== Sample Code Data =====
const SAMPLE_CODES = {
    'inefficient-loop': {
        title: 'Inefficient Loop',
        language: 'python',
        code: `# Inefficient nested loop example
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = []

for i in range(len(numbers)):
    for j in range(len(numbers)):
        if i != j and numbers[i] + numbers[j] == 10:
            result.append((numbers[i], numbers[j]))

print(result)`
    },
    'repeated-logic': {
        title: 'Repeated Logic',
        language: 'python',
        code: `# Code with repeated logic patterns
def calculate_area_circle(radius):
    pi = 3.14159
    area = pi * radius * radius
    return area

def calculate_area_rectangle(length, width):
    area = length * width
    return area

def calculate_area_triangle(base, height):
    area = 0.5 * base * height
    return area

# Usage
circle_area = calculate_area_circle(5)
print(f"Circle area: {circle_area}")

rectangle_area = calculate_area_rectangle(10, 8)
print(f"Rectangle area: {rectangle_area}")

triangle_area = calculate_area_triangle(6, 4)
print(f"Triangle area: {triangle_area}")`
    },
    'list-operations': {
        title: 'Inefficient List Operations',
        language: 'python',
        code: `# Inefficient list operations
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Inefficient way to create squares
squares = []
for i in range(len(data)):
    squares.append(data[i] * data[i])

# Inefficient filtering
even_numbers = []
for num in data:
    if num % 2 == 0:
        even_numbers.append(num)

# Inefficient sum calculation
total = 0
for num in data:
    total = total + num

print("Squares:", squares)
print("Even numbers:", even_numbers)
print("Total:", total)`
    },
    'function-extraction': {
        title: 'Code Needing Function Extraction',
        language: 'python',
        code: `# Code that needs refactoring into functions
# Student grade processing
student1_name = "Alice"
student1_scores = [85, 92, 78, 96, 88]
student1_total = 0
for score in student1_scores:
    student1_total += score
student1_average = student1_total / len(student1_scores)
if student1_average >= 90:
    student1_grade = "A"
elif student1_average >= 80:
    student1_grade = "B"
elif student1_average >= 70:
    student1_grade = "C"
else:
    student1_grade = "F"
print(f"{student1_name}: {student1_average:.1f} ({student1_grade})")

student2_name = "Bob"
student2_scores = [76, 84, 92, 88, 79]
student2_total = 0
for score in student2_scores:
    student2_total += score
student2_average = student2_total / len(student2_scores)
if student2_average >= 90:
    student2_grade = "A"
elif student2_average >= 80:
    student2_grade = "B"
elif student2_average >= 70:
    student2_grade = "C"
else:
    student2_grade = "F"
print(f"{student2_name}: {student2_average:.1f} ({student2_grade})")`
    }
};

// ===== DOM Elements =====
const elements = {
    // Input elements
    codeInput: document.getElementById('codeInput'),
    sourceLanguage: document.getElementById('sourceLanguage'),
    targetLanguage: document.getElementById('targetLanguage'),
    
    // Action buttons
    transformBtn: document.getElementById('transformBtn'),
    optimizeBtn: document.getElementById('optimizeBtn'),
    explainBtn: document.getElementById('explainBtn'),
    convertBtn: document.getElementById('convertBtn'),
    
    // Control buttons
    loadSample: document.getElementById('loadSample'),
    clearInput: document.getElementById('clearInput'),
    copyResult: document.getElementById('copyResult'),
    downloadResult: document.getElementById('downloadResult'),
    showDiff: document.getElementById('showDiff'),
    
    // Display elements
    resultsSection: document.getElementById('resultsSection'),
    codeOutput: document.getElementById('codeOutput'),
    explanationsList: document.getElementById('explanationsList'),
    loadingIndicator: document.getElementById('loadingIndicator'),
    
    // Tabs
    tabButtons: document.querySelectorAll('.tab-btn'),
    resultTab: document.getElementById('resultTab'),
    diffTab: document.getElementById('diffTab'),
    beforeCode: document.getElementById('beforeCode'),
    afterCode: document.getElementById('afterCode'),
    
    // Modal elements
    sampleModal: document.getElementById('sampleModal'),
    closeSampleModal: document.getElementById('closeSampleModal'),
    sampleCards: document.querySelectorAll('.sample-card'),
    
    // Theme and options
    themeToggle: document.getElementById('themeToggle'),
    convertOptions: document.getElementById('convertOptions')
};

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupTheme();
    setupEventListeners();
    setupKeyboardShortcuts();
    updateLanguageHighlighting();
}

// ===== Theme Management =====
function setupTheme() {
    document.documentElement.setAttribute('data-theme', AppState.currentTheme);
    updateThemeIcon();
}

function toggleTheme() {
    AppState.currentTheme = AppState.currentTheme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', AppState.currentTheme);
    setupTheme();
}

function updateThemeIcon() {
    const icon = elements.themeToggle.querySelector('i');
    icon.className = AppState.currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Theme toggle
    elements.themeToggle.addEventListener('click', toggleTheme);
    
    // Action buttons
    elements.transformBtn.addEventListener('click', () => handleCodeOperation('transform'));
    elements.optimizeBtn.addEventListener('click', () => handleCodeOperation('optimize'));
    elements.explainBtn.addEventListener('click', () => handleCodeOperation('explain'));
    elements.convertBtn.addEventListener('click', () => handleCodeOperation('convert'));
    
    // Control buttons
    elements.loadSample.addEventListener('click', openSampleModal);
    elements.clearInput.addEventListener('click', clearCodeInput);
    elements.copyResult.addEventListener('click', copyResultToClipboard);
    elements.downloadResult.addEventListener('click', downloadResult);
    
    // Language selection
    elements.sourceLanguage.addEventListener('change', handleLanguageChange);
    elements.targetLanguage.addEventListener('change', handleTargetLanguageChange);
    
    // Convert button special behavior
    elements.convertBtn.addEventListener('click', toggleConvertOptions);
    
    // Tab switching
    elements.tabButtons.forEach(button => {
        button.addEventListener('click', () => switchTab(button.dataset.tab));
    });
    
    // Sample modal
    elements.closeSampleModal.addEventListener('click', closeSampleModal);
    elements.sampleModal.addEventListener('click', (e) => {
        if (e.target === elements.sampleModal) closeSampleModal();
    });
    
    // Sample cards
    elements.sampleCards.forEach(card => {
        card.addEventListener('click', () => loadSampleCode(card.dataset.sample));
    });
}

// ===== Keyboard Shortcuts =====
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'Enter':
                    e.preventDefault();
                    handleCodeOperation('transform');
                    break;
                case 'O':
                    if (e.shiftKey) {
                        e.preventDefault();
                        handleCodeOperation('optimize');
                    }
                    break;
                case 'E':
                    if (e.shiftKey) {
                        e.preventDefault();
                        handleCodeOperation('explain');
                    }
                    break;
                case 'L':
                    if (e.shiftKey) {
                        e.preventDefault();
                        openSampleModal();
                    }
                    break;
            }
        }
        
        if (e.key === 'Escape') {
            closeSampleModal();
        }
    });
}

// ===== Code Operations =====
async function handleCodeOperation(operation) {
    const code = elements.codeInput.value.trim();
    
    if (!code) {
        showNotification('Please enter some code first!', 'warning');
        return;
    }
    
    if (AppState.isProcessing) {
        showNotification('Please wait for the current operation to complete.', 'info');
        return;
    }
    
    AppState.originalCode = code;
    AppState.currentLanguage = elements.sourceLanguage.value;
    
    if (operation === 'convert') {
        AppState.targetLanguage = elements.targetLanguage.value;
        if (AppState.currentLanguage === AppState.targetLanguage) {
            showNotification('Source and target languages cannot be the same!', 'warning');
            return;
        }
    }
    
    try {
        AppState.isProcessing = true;
        showLoading(true);
        disableButtons(true);
        
        const result = await makeAPIRequest(operation, {
            code: code,
            source_language: AppState.currentLanguage,
            target_language: operation === 'convert' ? AppState.targetLanguage : null,
            operation: operation
        });
        
        if (result.success) {
            AppState.transformedCode = result.transformed_code;
            displayResults(result, operation);
            showNotification(`${capitalize(operation)} completed successfully!`, 'success');
        } else {
            throw new Error(result.error_message || 'Operation failed');
        }
        
    } catch (error) {
        console.error('Operation failed:', error);
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        AppState.isProcessing = false;
        showLoading(false);
        disableButtons(false);
    }
}

// ===== API Communication =====
async function makeAPIRequest(operation, data) {
    const response = await fetch('/api/transform', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// ===== Results Display =====
function displayResults(result, operation) {
    // Show results section
    elements.resultsSection.classList.remove('hidden');
    
    // Update code output
    elements.codeOutput.textContent = result.transformed_code;
    elements.beforeCode.textContent = AppState.originalCode;
    elements.afterCode.textContent = result.transformed_code;
    
    // Update syntax highlighting
    updateResultHighlighting(operation);
    
    // Display explanations and suggestions
    displayExplanations(result.explanations, result.suggestions);
    
    // Switch to result tab
    switchTab('result');
    
    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function updateResultHighlighting(operation) {
    const targetLang = operation === 'convert' ? AppState.targetLanguage : AppState.currentLanguage;
    const langClass = `language-${targetLang}`;
    
    // Update code output language
    elements.codeOutput.className = langClass;
    elements.beforeCode.className = `language-${AppState.currentLanguage}`;
    elements.afterCode.className = langClass;
    
    // Re-highlight
    Prism.highlightElement(elements.codeOutput);
    Prism.highlightElement(elements.beforeCode);
    Prism.highlightElement(elements.afterCode);
}

function displayExplanations(explanations, suggestions) {
    elements.explanationsList.innerHTML = '';
    
    // Add explanations
    explanations.forEach(explanation => {
        addExplanationItem(explanation, 'explanation');
    });
    
    // Add suggestions
    suggestions.forEach(suggestion => {
        addExplanationItem(suggestion, 'suggestion');
    });
    
    if (explanations.length === 0 && suggestions.length === 0) {
        addExplanationItem('No specific explanations or suggestions generated.', 'info');
    }
}

function addExplanationItem(text, type) {
    const item = document.createElement('div');
    item.className = `explanation-item ${type}`;
    item.textContent = text;
    elements.explanationsList.appendChild(item);
}

// ===== UI Controls =====
function switchTab(tabName) {
    // Update tab buttons
    elements.tabButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}Tab`);
    });
}

function toggleConvertOptions() {
    const isHidden = elements.convertOptions.classList.contains('hidden');
    elements.convertOptions.classList.toggle('hidden', !isHidden);
    
    if (!isHidden) {
        // If showing options, trigger convert operation
        handleCodeOperation('convert');
    }
}

function showLoading(show) {
    elements.loadingIndicator.classList.toggle('hidden', !show);
}

function disableButtons(disable) {
    const buttons = [
        elements.transformBtn,
        elements.optimizeBtn,
        elements.explainBtn,
        elements.convertBtn
    ];
    
    buttons.forEach(btn => {
        btn.disabled = disable;
    });
}

// ===== Sample Code Management =====
function openSampleModal() {
    elements.sampleModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeSampleModal() {
    elements.sampleModal.classList.add('hidden');
    document.body.style.overflow = '';
}

function loadSampleCode(sampleKey) {
    const sample = SAMPLE_CODES[sampleKey];
    if (sample) {
        elements.codeInput.value = sample.code;
        elements.sourceLanguage.value = sample.language;
        updateLanguageHighlighting();
        showNotification(`Loaded sample: ${sample.title}`, 'success');
        closeSampleModal();
    }
}

// ===== Utility Functions =====
function clearCodeInput() {
    elements.codeInput.value = '';
    elements.resultsSection.classList.add('hidden');
    showNotification('Code input cleared', 'info');
}

function handleLanguageChange() {
    AppState.currentLanguage = elements.sourceLanguage.value;
    updateLanguageHighlighting();
}

function handleTargetLanguageChange() {
    AppState.targetLanguage = elements.targetLanguage.value;
}

function updateLanguageHighlighting() {
    // Update placeholder text based on language
    const placeholders = {
        python: 'def hello_world():\n    print("Hello, World!")\n\nhello_world()',
        javascript: 'function helloWorld() {\n    console.log("Hello, World!");\n}\n\nhelloWorld();',
        cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',
        java: 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}'
    };
    
    const placeholder = placeholders[AppState.currentLanguage] || 'Enter your code here...';
    elements.codeInput.placeholder = `Paste your ${AppState.currentLanguage} code here or try:\n\n${placeholder}`;
}

async function copyResultToClipboard() {
    try {
        await navigator.clipboard.writeText(AppState.transformedCode);
        showNotification('Code copied to clipboard!', 'success');
    } catch (error) {
        console.error('Failed to copy:', error);
        showNotification('Failed to copy code', 'error');
    }
}

function downloadResult() {
    if (!AppState.transformedCode) {
        showNotification('No code to download', 'warning');
        return;
    }
    
    const extensions = {
        python: 'py',
        javascript: 'js',
        cpp: 'cpp',
        java: 'java'
    };
    
    const extension = extensions[AppState.targetLanguage || AppState.currentLanguage] || 'txt';
    const blob = new Blob([AppState.transformedCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `transformed_code.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Code downloaded successfully!', 'success');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--bg-primary);
        color: var(--text-primary);
        padding: 1rem 1.5rem;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-heavy);
        border-left: 4px solid var(--accent-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : type === 'success' ? 'success' : 'primary'});
        z-index: 1001;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// ===== Error Handling =====
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showNotification('An unexpected error occurred', 'error');
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('Network or server error occurred', 'error');
});

// ===== CSS Animations (added dynamically) =====
const animationStyles = document.createElement('style');
animationStyles.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
    
    .notification {
        font-family: inherit;
        font-size: 0.875rem;
        font-weight: 500;
    }
`;
document.head.appendChild(animationStyles);

// ===== Advanced Features =====

// Auto-save functionality
let autoSaveTimeout;
elements.codeInput.addEventListener('input', function() {
    clearTimeout(autoSaveTimeout);
    autoSaveTimeout = setTimeout(() => {
        localStorage.setItem('syntaxshift_code', elements.codeInput.value);
        localStorage.setItem('syntaxshift_language', elements.sourceLanguage.value);
    }, 1000);
});

// Load saved code on page load
window.addEventListener('load', function() {
    const savedCode = localStorage.getItem('syntaxshift_code');
    const savedLanguage = localStorage.getItem('syntaxshift_language');
    
    if (savedCode) {
        elements.codeInput.value = savedCode;
    }
    
    if (savedLanguage) {
        elements.sourceLanguage.value = savedLanguage;
        updateLanguageHighlighting();
    }
});

// Code validation
function validateCode(code, language) {
    if (!code.trim()) {
        return { valid: false, message: 'Code cannot be empty' };
    }
    
    if (code.length > 50000) {
        return { valid: false, message: 'Code is too long (max 50,000 characters)' };
    }
    
    // Basic syntax checks for Python
    if (language === 'python') {
        const lines = code.split('\n');
        let indentStack = [0];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            if (line.trim() === '') continue;
            
            const indent = line.length - line.trimStart().length;
            
            // Check for consistent indentation (simplified)
            if (line.trim().endsWith(':')) {
                indentStack.push(indent);
            }
        }
    }
    
    return { valid: true };
}

// Enhanced error handling for API calls
async function makeAPIRequestWithRetry(operation, data, maxRetries = 3) {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            return await makeAPIRequest(operation, data);
        } catch (error) {
            if (attempt === maxRetries - 1) {
                throw error;
            }
            
            // Wait before retry (exponential backoff)
            await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
            showNotification(`Retrying... (${attempt + 1}/${maxRetries})`, 'info');
        }
    }
}

// Code complexity analysis
function analyzeCodeComplexity(code) {
    const metrics = {
        lines: code.split('\n').filter(line => line.trim()).length,
        functions: (code.match(/def\s+\w+/g) || []).length,
        loops: (code.match(/for\s+.*:|while\s+.*:/g) || []).length,
        conditions: (code.match(/if\s+.*:|elif\s+.*:/g) || []).length,
        classes: (code.match(/class\s+\w+/g) || []).length
    };
    
    const complexity = metrics.functions + metrics.loops + metrics.conditions + metrics.classes;
    
    let level;
    if (complexity <= 3) level = 'Simple';
    else if (complexity <= 8) level = 'Moderate';
    else level = 'Complex';
    
    return { ...metrics, complexity, level };
}

// Performance monitoring
const performanceMetrics = {
    startTime: null,
    endTime: null,
    operations: []
};

function startPerformanceTracking(operation) {
    performanceMetrics.startTime = performance.now();
    performanceMetrics.currentOperation = operation;
}

function endPerformanceTracking() {
    if (performanceMetrics.startTime) {
        const duration = performance.now() - performanceMetrics.startTime;
        performanceMetrics.operations.push({
            operation: performanceMetrics.currentOperation,
            duration: duration,
            timestamp: new Date()
        });
        
        console.log(`Operation ${performanceMetrics.currentOperation} took ${duration.toFixed(2)}ms`);
    }
}

// Enhanced code operation with performance tracking
const originalHandleCodeOperation = handleCodeOperation;
async function handleCodeOperation(operation) {
    const code = elements.codeInput.value.trim();
    
    // Validate code first
    const validation = validateCode(code, AppState.currentLanguage);
    if (!validation.valid) {
        showNotification(validation.message, 'warning');
        return;
    }
    
    // Analyze complexity
    const complexity = analyzeCodeComplexity(code);
    if (complexity.level === 'Complex') {
        showNotification(`Detected ${complexity.level.toLowerCase()} code (${complexity.complexity} constructs). Processing may take longer.`, 'info');
    }
    
    // Start performance tracking
    startPerformanceTracking(operation);
    
    try {
        await originalHandleCodeOperation(operation);
        endPerformanceTracking();
    } catch (error) {
        endPerformanceTracking();
        throw error;
    }
}

// Code formatting utilities
function formatCode(code, language) {
    if (language === 'python') {
        // Basic Python formatting
        const lines = code.split('\n');
        let formatted = [];
        let indentLevel = 0;
        
        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed) {
                formatted.push('');
                continue;
            }
            
            // Decrease indent for certain keywords
            if (trimmed.startsWith('except') || trimmed.startsWith('finally') || 
                trimmed.startsWith('elif') || trimmed.startsWith('else')) {
                indentLevel = Math.max(0, indentLevel - 1);
            }
            
            // Add the line with proper indentation
            formatted.push('    '.repeat(indentLevel) + trimmed);
            
            // Increase indent after certain patterns
            if (trimmed.endsWith(':')) {
                indentLevel++;
            }
        }
        
        return formatted.join('\n');
    }
    
    return code; // Return unchanged for other languages
}

// Export functionality
function exportResults() {
    if (!AppState.transformedCode) {
        showNotification('No results to export', 'warning');
        return;
    }
    
    const exportData = {
        originalCode: AppState.originalCode,
        transformedCode: AppState.transformedCode,
        sourceLanguage: AppState.currentLanguage,
        targetLanguage: AppState.targetLanguage,
        timestamp: new Date().toISOString(),
        complexity: analyzeCodeComplexity(AppState.originalCode)
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `syntax_shift_export_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Results exported successfully!', 'success');
}

// Add export button functionality if it exists
const exportBtn = document.getElementById('exportResults');
if (exportBtn) {
    exportBtn.addEventListener('click', exportResults);
}

// Enhanced keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
            case 's':
                e.preventDefault();
                if (AppState.transformedCode) {
                    downloadResult();
                }
                break;
            case 'k':
                if (e.shiftKey) {
                    e.preventDefault();
                    clearCodeInput();
                }
                break;
            case 'd':
                if (e.shiftKey) {
                    e.preventDefault();
                    toggleTheme();
                }
                break;
        }
    }
});

// Update footer with additional shortcuts
const footerShortcuts = document.querySelector('.footer-shortcuts');
if (footerShortcuts) {
    footerShortcuts.innerHTML += `
        <span><kbd>Ctrl</kbd> + <kbd>S</kbd> to Download</span>
        <span><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>K</kbd> to Clear</span>
        <span><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>D</kbd> to Toggle Theme</span>
    `;
}

// Initialize enhanced features
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add loading states to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if (!this.disabled) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            }
        });
    });
    
    // Initialize tooltips for buttons
    document.querySelectorAll('[title]').forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.position = 'relative';
        });
    });
});

console.log('🚀 Syntax Shift frontend loaded successfully!');