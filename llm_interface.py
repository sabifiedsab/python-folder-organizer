import openai
from utils import list_directories

class LLMInterface:
    def __init__(self, main_dir: str):
        openai.api_key = "lm-studio"
        self.main_dir = main_dir
        self.client = openai.OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

    def get_context(self, directory_name):
        """Generates a context string about the directory."""
        
        sub_directories = list_directories(self.main_dir, directory_name)
        
        prompt = f"Describe this directory: {directory_name} with these sub directories: {sub_directories}. Include its purpose and any relevant files. Your answer should be able to stand on its own, and not be too long. Please refrain from using markdown."
        response = self.client.chat.completions.create(model="model-identifier", messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content

    def get_info_based_on_query(self, directory_name: str, query: str):
        """Gets more information about a directory based on the user's query."""
        
        sub_directories = list_directories(self.main_dir, directory_name)
        
        prompt = f"Given this directory: {directory_name} which has these sub directories: {sub_directories}, answer the question: {query}. Your answer should be able to stand on its own, and not be too long. Please refrain from using markdown."
        response = self.client.chat.completions.create(model="model-identifier", messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content
