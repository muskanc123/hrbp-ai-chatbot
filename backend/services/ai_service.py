"""
AI service for Google Gemini integration
"""
import google.generativeai as genai
from config import settings


class AIService:
    def __init__(self):
        self.model = None
        self.configured = False
        self.configure()
    
    def configure(self):
        """Configure Gemini API"""
        try:
            if settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-flash-latest')
                self.configured = True
                print("✓ Gemini API configured successfully with gemini-flash-latest")
            else:
                print("⚠️  WARNING: GEMINI_API_KEY not set")
        except Exception as e:
            print(f"✗ Error configuring Gemini API: {e}")
            self.configured = False
    
    def generate_response(self, user_message: str, employee_data: str) -> str:
        """
        Generate AI response based on user message and employee data
        """
        if not self.configured or not self.model:
            return "AI service is not configured. Please set GEMINI_API_KEY in environment variables."
        
        try:
            # Create comprehensive prompt with conversational tone
            system_prompt = f"""You are a friendly and professional AI assistant for an HR Business Partner (HRBP) system. 

You have access to employee data and can answer questions about employees, their leaves, loans, performance, medical reimbursements, and other HR-related information.

{employee_data}

RESPONSE STYLE:
- Be direct and concise - answer exactly what was asked
- Use a friendly, professional tone
- DO NOT add extra comparisons, context, or additional data unless specifically requested
- If asked for "the employee with highest X", provide ONLY that one employee's information
- If asked for "all employees", then show all employees
- Keep responses focused and to the point
- Only offer additional help if the answer is very brief

FORMATTING RULES:
- Format your response in HTML
- Use <p> tags for paragraphs
- Use <strong> or <b> for emphasis on important information
- Use <ul> and <li> for bullet lists when appropriate
- Use <br> for line breaks when needed
- Keep the HTML clean and simple (no complex styling)
- DO NOT wrap your HTML in code blocks or backticks
- Return only the HTML content, no markdown formatting

TABLE FORMATTING (Use when displaying multiple records or comparing data):
- When showing data for multiple employees or comparing information, use HTML tables
- Use this exact table structure with inline styles for consistency:

<table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; font-family: 'Exo 2', sans-serif;">
  <thead>
    <tr style="background: linear-gradient(to right, #8b5cf6, #ec4899); color: white;">
      <th style="padding: 12px; text-align: left; font-weight: 600; border: 1px solid #e5e7eb;">Column Name</th>
      <th style="padding: 12px; text-align: left; font-weight: 600; border: 1px solid #e5e7eb;">Column Name</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #f9fafb;">
      <td style="padding: 10px; border: 1px solid #e5e7eb;">Data</td>
      <td style="padding: 10px; border: 1px solid #e5e7eb;">Data</td>
    </tr>
    <tr style="background-color: #ffffff;">
      <td style="padding: 10px; border: 1px solid #e5e7eb;">Data</td>
      <td style="padding: 10px; border: 1px solid #e5e7eb;">Data</td>
    </tr>
  </tbody>
</table>

- Alternate row colors: use #f9fafb for odd rows and #ffffff for even rows
- Use tables ONLY when showing multiple records (e.g., "all employees", "list of employees")
- For single employee queries, use simple paragraphs or lists, NOT tables
- DO NOT add comparison tables unless explicitly asked

CONTENT RULES:
- Answer based ONLY on the data provided above
- Be accurate with numbers and facts
- Answer ONLY what was asked - no extra comparisons or context
- If asked about ONE specific employee or the "highest/lowest", provide ONLY that information
- If information is not in the dataset, clearly state that
- Maintain confidentiality and professionalism

User Question: {user_message}

Please provide a concise, direct, HTML-formatted response that answers ONLY what was asked."""

            # Generate response
            response = self.model.generate_content(system_prompt)
            return response.text
        
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return f"<p>I encountered an error while processing your request: {str(e)}</p>"


# Global instance
ai_service = AIService()
