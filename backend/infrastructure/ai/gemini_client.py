"""
Refactored AI service with configuration and proper error handling
"""
import google.generativeai as genai
import yaml
from pathlib import Path
from core.exceptions import AIServiceException, ConfigurationException
from core.logging_config import get_logger

logger = get_logger(__name__)


class GeminiAIService:
    """Google Gemini AI service"""
    
    def __init__(self, api_key: str, prompt_config_path: str):
        self.api_key = api_key
        self.prompt_config_path = prompt_config_path
        self.model = None
        self.prompt_config = None
        self.configured = False
        self._configure()
        self._load_prompt_config()
    
    def _configure(self):
        """Configure Gemini API"""
        try:
            if not self.api_key:
                raise ConfigurationException("GEMINI_API_KEY not set")
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
            self.configured = True
            logger.info("Gemini API configured successfully")
        except ConfigurationException:
            raise
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            raise ConfigurationException(f"Failed to configure Gemini API", {"error": str(e)})
    
    def _load_prompt_config(self):
        """Load prompt configuration from YAML file"""
        try:
            config_path = Path(self.prompt_config_path)
            if not config_path.exists():
                raise ConfigurationException(
                    f"Prompt config file not found",
                    {"path": str(config_path)}
                )
            
            with open(config_path, 'r') as f:
                self.prompt_config = yaml.safe_load(f)
            
            logger.info(f"Loaded prompt configuration from {config_path}")
        except ConfigurationException:
            raise
        except Exception as e:
            logger.error(f"Failed to load prompt config: {e}")
            raise ConfigurationException(
                "Failed to load prompt configuration",
                {"path": self.prompt_config_path, "error": str(e)}
            )
    
    def _build_prompt(self, user_message: str, employee_data: str) -> str:
        """Build the complete prompt from configuration"""
        try:
            # Build response style section
            response_style = "\n".join(f"- {rule}" for rule in self.prompt_config['response_style'])
            
            # Build formatting rules
            html_rules = "\n".join(f"- {rule}" for rule in self.prompt_config['formatting_rules']['html'])
            
            # Build table formatting
            table_config = self.prompt_config['formatting_rules']['tables']
            table_rules = f"""- When to use: {table_config['when_to_use']}
- Avoid: {table_config['avoid']}
- Use this table template:

{table_config['template']}

- Alternate row colors: odd={table_config['styling']['row_colors']['odd']}, even={table_config['styling']['row_colors']['even']}"""
            
            # Build content rules
            content_rules = "\n".join(f"- {rule}" for rule in self.prompt_config['content_rules'])
            
            # Build final prompt
            prompt = f"""{self.prompt_config['system_role']}

{employee_data}

RESPONSE STYLE:
{response_style}

FORMATTING RULES:
{html_rules}

TABLE FORMATTING:
{table_rules}

CONTENT RULES:
{content_rules}

User Question: {user_message}

Please provide a concise, direct, HTML-formatted response that answers ONLY what was asked."""
            
            return prompt
        except Exception as e:
            logger.error(f"Failed to build prompt: {e}")
            raise AIServiceException("Failed to build prompt", {"error": str(e)})
    
    def generate_response(self, user_message: str, employee_data: str) -> str:
        """
        Generate AI response
        
        Args:
            user_message: User's question
            employee_data: Formatted employee data
            
        Returns:
            AI generated response
            
        Raises:
            AIServiceException: If generation fails
        """
        if not self.configured or not self.model:
            raise AIServiceException("AI service is not configured")
        
        try:
            prompt = self._build_prompt(user_message, employee_data)
            
            logger.info("Generating AI response")
            response = self.model.generate_content(prompt)
            
            logger.info("AI response generated successfully")
            return response.text
        
        except AIServiceException:
            raise
        except Exception as e:
            logger.error(f"Failed to generate AI response: {e}")
            raise AIServiceException(
                "Failed to generate AI response",
                {"error": str(e)}
            )
