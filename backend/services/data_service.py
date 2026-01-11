"""
Excel data processing service
"""
import pandas as pd
from config import settings
import os


class DataService:
    def __init__(self):
        self.df = None
        self.data_loaded = False
        self.load_data()
    
    def load_data(self):
        """Load Excel data"""
        try:
            excel_path = os.path.join(os.path.dirname(__file__), settings.EXCEL_FILE_PATH)
            self.df = pd.read_excel(excel_path, engine='openpyxl')
            self.data_loaded = True
            print(f"✓ Loaded {len(self.df)} employee records")
        except Exception as e:
            print(f"✗ Error loading Excel file: {e}")
            self.data_loaded = False
    
    def get_formatted_data(self) -> str:
        """Convert DataFrame to formatted string for LLM context"""
        if self.df is None or not self.data_loaded:
            return "No employee data available"
        
        # Replace NaN with empty string
        df_clean = self.df.fillna('')
        
        # Convert to structured text format
        data_text = "EMPLOYEE DATABASE:\n\n"
        
        for idx, row in df_clean.iterrows():
            data_text += f"Employee #{idx + 1}:\n"
            for col in df_clean.columns:
                value = row[col]
                # Format dates nicely
                if isinstance(value, pd.Timestamp):
                    value = value.strftime('%Y-%m-%d')
                data_text += f"  - {col}: {value}\n"
            data_text += "\n"
        
        return data_text
    
    def get_summary(self) -> dict:
        """Get dataset summary"""
        if self.df is None or not self.data_loaded:
            return {"total_employees": 0, "columns": [], "departments": 0}
        
        return {
            "total_employees": len(self.df),
            "columns": self.df.columns.tolist(),
            "departments": self.df['Department'].nunique() if 'Department' in self.df.columns else 0
        }


# Global instance
data_service = DataService()
