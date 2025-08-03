import re

def remove_think_tokens(text):
    # Remove all <think>...</think> blocks (including nested ones)
    pattern = r'<think>.*?</think>'
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up whitespace
    cleaned_text = re.sub(r'\n\s*\n+', '\n\n', cleaned_text)  # Multiple newlines to double
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

def build_execution_trace(final_state):
    trace_lines = []
    trace_lines.append("=" * 50)
    trace_lines.append("AGENT EXECUTION TRACE:")
    trace_lines.append("=" * 50)
    
    for i, message in enumerate(final_state.get("messages", [])):
        trace_lines.append(f"\nStep {i+1}: {message.__class__.__name__}")
        
        if hasattr(message, 'content') and message.content:
            trace_lines.append(f"Content: {message.content}")
        
        # This is where tool calls will be shown
        if hasattr(message, 'tool_calls') and message.tool_calls:
            trace_lines.append("🔧 Tool Calls:")
            for tool_call in message.tool_calls:
                trace_lines.append(f"  - Tool: {tool_call['name']}")
                trace_lines.append(f"  - Args: {tool_call['args']}")
        
        # This shows tool results
        if hasattr(message, 'name') and message.name:
            trace_lines.append(f"🔄 Tool Result from '{message.name}':")
            trace_lines.append(f"  Result: {message.content}")
        
        trace_lines.append("-" * 30)
    
    return "\n".join(trace_lines)