import aiohttp

class Oxford:
    def __init__(self, app_id: str, app_key: str, language: str ='en-gb') -> None:
        self.app_id = app_id
        self.app_key = app_key
        self.language = language
        self.url = f"https://od-api.oxforddictionaries.com:443/api/v2/entries/{self.language}/"
        self.header = {"app_id": app_id, "app_key": app_key}

    async def api_request(self, word:str) -> dict:
        """
        Normal api requests returns a huge dict
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}{word.lower()}", headers=self.header) as response:
                res = await response.json()
                return res

    async def get_word_defination(self, word:str) -> list[str]:
        """Returns list of definations of the word"""
        data = await self.api_request(word)
        empty_list = []
        backup = []
        for i in data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']:
            for e in i['definitions']:
                empty_list.append(e)
        for x in empty_list:
            backup.append(x)

        return backup

    async def get_word_examples(self, word: str) -> list[str]:
        """Get word examples """
        data = await self.api_request(word)
        empty_list = []
        backup = []
        for i in data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']:
            for e in i['examples']:
                empty_list.append(e)
        for x in empty_list:
            backup.append(x['text'])

        return backup

    async def get_audio_file(self, word) -> str:
        """Get audio file which tells you how to pronounce the word"""
        data = await self.api_request(word)
        return data['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']

    async def get_synonyms(self, word):
        """Get synonyms for the word"""
        try:
            data = await self.api_request(word)
            empty_list = []
            for i in data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']:
                empty_list.append(i['text'])

            return empty_list
        except:
            return "No Synonyms Found!"