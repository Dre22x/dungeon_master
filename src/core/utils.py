import asyncio
from google.genai import types

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


async def run_agent_with_retry(runner, user_id, session_id, content, max_retries=10):
    """
    Run an agent with retry logic for model overload errors.
    
    Args:
        runner: The runner instance
        user_id: User ID for the session
        session_id: Session ID
        content: The content to send to the agent
        max_retries: Maximum number of retry attempts (default: 10)
    
    Returns:
        tuple: (success: bool, final_response: str, agent_name: str)
    """
    retry_count = 0
    final_response_text = None
    agent_name = None

    while retry_count <= max_retries:
        try:
            async for event in runner.run_async(
                user_id=user_id, session_id=session_id, new_message=content
            ):
                if event.author:
                    agent_name = event.author

                response = await process_agent_response(event)
                if response:
                    final_response_text = response
            
            return True, final_response_text, agent_name
            
        except Exception as e:
            error_message = str(e)
            print(f"{Colors.BG_RED}{Colors.WHITE}ERROR during agent run: {error_message}{Colors.RESET}")
            
            # Check if the error is due to model overload
            if "The model is overloaded" in error_message:
                retry_count += 1
                if retry_count <= max_retries:
                    print(f"{Colors.BG_YELLOW}{Colors.BLACK}{Colors.BOLD}🔄 Model overloaded. Retry attempt {retry_count}/{max_retries}. Waiting 3 seconds...{Colors.RESET}")
                    await asyncio.sleep(3)
                    continue
                else:
                    print(f"{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}❌ Maximum retries ({max_retries}) reached. Giving up.{Colors.RESET}")
                    return False, None, agent_name
            
            # Check if the error is due to quota/resource exhausted
            elif "You exceeded your current quota" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                quota_retry_count = 0
                quota_max_retries = 5
                
                while quota_retry_count < quota_max_retries:
                    quota_retry_count += 1
                    print(f"{Colors.BG_MAGENTA}{Colors.WHITE}{Colors.BOLD}💰 Resource exhausted. Retry attempt {quota_retry_count}/{quota_max_retries}. Waiting 30 seconds...{Colors.RESET}")
                    await asyncio.sleep(30)
                    
                    try:
                        async for event in runner.run_async(
                            user_id=user_id, session_id=session_id, new_message=content
                        ):
                            if event.author:
                                agent_name = event.author

                            response = await process_agent_response(event)
                            if response:
                                final_response_text = response
                        
                        return True, final_response_text, agent_name
                        
                    except Exception as quota_e:
                        quota_error_message = str(quota_e)
                        print(f"{Colors.BG_RED}{Colors.WHITE}ERROR during quota retry: {quota_error_message}{Colors.RESET}")
                        
                        if ("You exceeded your current quota" in quota_error_message or "RESOURCE_EXHAUSTED" in quota_error_message) and quota_retry_count < quota_max_retries:
                            continue
                        else:
                            print(f"{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}❌ Resource exhausted retries exhausted. Giving up.{Colors.RESET}")
                            return False, None, agent_name
                
                # If we get here, quota retries were exhausted
                return False, None, agent_name
            
            else:
                # If it's not a model overload or quota error, don't retry
                print(f"{Colors.BG_RED}{Colors.WHITE}Non-retryable error: {error_message}{Colors.RESET}")
                return False, None, agent_name


async def process_agent_response(event):
    """Process and display agent response events."""
    print(f"Event ID: {event.id}, Author: {event.author}")

    # Check for specific parts first
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"{Colors.CYAN}{Colors.BOLD}{part.text.strip()}{Colors.RESET}")
    # Check for final response after specific parts
    final_response = None
    if not has_specific_part and event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            # Use colors and formatting to make the final response stand out
            print(
                f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n"
            )
        else:
            print(
                f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Final Agent Response: [No text content in final event]{Colors.RESET}\n"
            )

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}"
    )
    
    success, final_response_text, agent_name = await run_agent_with_retry(
        runner, user_id, session_id, content
    )

    print(f"{Colors.YELLOW}{'-' * 30}{Colors.RESET}")
    return final_response_text